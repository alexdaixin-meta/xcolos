"""Linking a real model to the judge seam.

`ModelJudge` takes any object with one method:

    complete(prompt: str, system: str = "") -> str

That is the whole contract. The split is what makes caching possible: `system`
holds the standing instructions and the game's rules and is byte-identical on
every call in a match, while `prompt` holds the table as it stands now. A
backend that can cache marks the system half and stops paying to re-read the
rules; one that cannot simply concatenates the two.

Nothing below is required to use XColos. The engine runs a definition written
entirely in arithmetic with no model at all, and the test suite does exactly
that. These are here so that wiring one up at runtime is a line of code rather
than a project.

Four of them, in the order most people will want them:

    MuseCompletion       Meta's internal Model API (Muse Spark), over HTTP.
    AnthropicCompletion  the Claude API. One stateless request per call.
    CommandCompletion    run a program: prompt on stdin, reply on stdout.
                         Works with any CLI, any harness, no dependency.
    EchoCompletion       returns a fixed string. For tests.

**This is not how players are connected.** A player is somebody's own live
assistant session, pulling from `/api/play` and keeping its own history; XColos
never calls a provider on a player's behalf and could not, because the context
that makes the player good at the game lives in their session, not here.

The judge is the opposite case and that is why an API call suits it. It is
stateless by design, sees the whole table, and returns a typed value rather
than conversation. There is no history to lose.
"""

from __future__ import annotations

import json
import os
import re
import shlex
import subprocess
from pathlib import Path
import urllib.error
import urllib.request
from typing import Any, Protocol

#: The model to reach for unless told otherwise.
DEFAULT_MODEL = "claude-opus-5"

#: A referee's reply is a small JSON object. The ceiling is for the reasoning
#: that precedes it, not the answer.
DEFAULT_MAX_TOKENS = 4096


class CompletionError(Exception):
    """The model could not be reached. Never a judgement about the answer."""


def read_key(
    explicit: str | None = None,
    *,
    file_variable: str = "MODEL_API_KEY_FILE",
    value_variable: str = "MODEL_API_KEY",
    path: str | None = None,
) -> str:
    """Find an API key, preferring a file over an environment variable.

    A file is the better place for a secret than a variable, for a reason that
    is easy to underrate: a variable has to be *typed* somewhere to be set, and
    everything that transcribes what you type then holds the key. A shell
    history, a process listing, a crash dump, a terminal scrollback, or an
    agent transcript. A path can be written into a command safely; a key
    cannot. The file itself is written once, by you, somewhere nothing is
    reading over your shoulder.

    Resolution order: an explicit argument, then the file named by
    `api_key_file` or `$MODEL_API_KEY_FILE`, then `$MODEL_API_KEY`. Returns an
    empty string when there is nothing to find; the caller decides whether that
    is fatal, because listing models and making a call fail differently.
    """
    if explicit:
        return explicit.strip()

    where = path or os.environ.get(file_variable)
    if where:
        keyfile = Path(where).expanduser()
        try:
            raw = keyfile.read_text(encoding="utf-8")
        except OSError as error:
            raise CompletionError(f"cannot read the key file {keyfile}: {error}") from None
        key = raw.strip()
        if not key:
            raise CompletionError(f"the key file {keyfile} is empty")
        if "\n" in key:
            # A pasted key that picked up a line break would otherwise be sent
            # as a bearer token and rejected with an unhelpful 401.
            raise CompletionError(
                f"the key file {keyfile} holds more than one line; it should "
                f"contain the key and nothing else"
            )
        return key

    return (os.environ.get(value_variable) or "").strip()


class Completion(Protocol):
    """One prompt in, one string out. No state, no history, no session.

    `system` is the part that repeats across calls. Keeping it a separate
    argument rather than a prefix is the whole reason a backend can cache it.
    """

    def complete(self, prompt: str, system: str = "") -> str: ...


class EchoCompletion:
    """Returns whatever it was given. For tests and for wiring checks."""

    def __init__(self, reply: str = '{"answer": false, "reason": "stub"}') -> None:
        self.reply = reply
        self.prompts: list[str] = []
        self.systems: list[str] = []

    def complete(self, prompt: str, system: str = "") -> str:
        self.prompts.append(prompt)
        self.systems.append(system)
        return self.reply


class CommandCompletion:
    """Run a program. Prompt on stdin, reply on stdout.

    The general adapter, and worth reaching for first. It needs no library, no
    network and no agreement about request shape: if you can print an answer,
    you can referee. Wraps a local model, a shell script, or your own harness
    equally well.
    """

    def __init__(self, command: str | list[str], timeout_s: int = 120) -> None:
        self.command = shlex.split(command) if isinstance(command, str) else list(command)
        self.timeout_s = timeout_s

    def complete(self, prompt: str, system: str = "") -> str:
        # A CLI has nowhere to put a system prompt, so the two halves are
        # concatenated. Nothing is cached, which is the honest outcome rather
        # than a flag that claims otherwise.
        whole = f"{system}\n\n{prompt}" if system else prompt
        try:
            done = subprocess.run(
                self.command,
                input=whole,
                capture_output=True,
                text=True,
                timeout=self.timeout_s,
            )
        except FileNotFoundError:
            raise CompletionError(f"no such command: {self.command[0]}") from None
        except subprocess.TimeoutExpired:
            raise CompletionError(
                f"{self.command[0]} did not answer in {self.timeout_s}s"
            ) from None
        if done.returncode != 0:
            raise CompletionError(
                f"{self.command[0]} exited {done.returncode}: "
                f"{done.stderr.strip()[:200]}"
            )
        return done.stdout


class AnthropicCompletion:
    """The Claude API, one stateless request per call.

    The SDK is imported when the first call is made, not when this module is,
    so the package is only needed by someone who actually wires a model in. The
    engine, the tests and the offline path never touch it.

    Adaptive thinking is on because a referee reading a rule written in English
    is doing the kind of work it helps with, and the reply is a few dozen
    tokens either way. Streaming is used so a long thinking block cannot hit a
    request timeout; the answer is collected before it is returned, because the
    judge has nothing to do with a partial one.

    The system prompt is sent as a cacheable block. Within one match every call
    repeats the same instructions and the same rules, so the rules are read
    once and the rest of the match pays only for the table. Caching has a
    minimum block size; a game with a short rules text simply will not hit it,
    which costs nothing and changes no behaviour.
    """

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        *,
        api_key: str | None = None,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        thinking: bool = True,
        client: Any = None,
    ) -> None:
        self.model = model
        self.max_tokens = max_tokens
        self.thinking = thinking
        self._api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self._client = client

    def _get_client(self) -> Any:
        if self._client is not None:
            return self._client
        try:
            import anthropic
        except ImportError:
            raise CompletionError(
                "the `anthropic` package is not installed; `pip install anthropic`, "
                "or use CommandCompletion to run a model over a CLI instead"
            ) from None
        if not self._api_key:
            raise CompletionError(
                "no API key: set ANTHROPIC_API_KEY or pass api_key="
            )
        self._client = anthropic.Anthropic(api_key=self._api_key)
        return self._client

    def complete(self, prompt: str, system: str = "") -> str:
        request: dict[str, Any] = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system:
            request["system"] = [
                {
                    "type": "text",
                    "text": system,
                    "cache_control": {"type": "ephemeral"},
                }
            ]
        if self.thinking:
            request["thinking"] = {"type": "adaptive"}

        try:
            with self._get_client().messages.stream(**request) as stream:
                message = stream.get_final_message()
        except CompletionError:
            raise
        except Exception as error:
            raise CompletionError(f"the model call failed: {error}") from None

        return "".join(
            block.text
            for block in message.content
            if getattr(block, "type", None) == "text"
        )


#: Meta's internal Model API. Muse Spark speaks the OpenAI Responses shape and
#: only that: there is no chat-completions path for it.
MUSE_ENDPOINT = "https://api.meta.ai/v1/responses"
MUSE_MODELS_ENDPOINT = "https://api.meta.ai/v1/models"

#: Model ids are granted per team, and the id a team actually holds is often
#: not the one the onboarding docs name: a key granted through the playground
#: carries `rl-muse-spark-*-playground` rather than `muse-spark-*-eval`. Asking
#: the server beats guessing, so `models()` lists them and a 404 reports them.
#: Measured on this key, on the same trivial referee prompt:
#:
#:     rl-muse-spark-1-1-playground          2-3s
#:     rl-muse-spark-1-3-sglang-playground   40-60s, and drops the connection
#:
#: Twenty times the latency for a yes-or-no question about a table that is
#: already fully described. A judge is called several times a round, so the
#: newest model is the wrong default here; name it explicitly if a game needs
#: it. Run `MuseCompletion().models()` to see what a key actually holds.
MUSE_MODEL = "rl-muse-spark-1-1-playground"

#: The server rejects anything else with a 400, including "none".
MUSE_EFFORTS = ("minimal", "low", "medium", "high")

#: The backend sheds load with a 503 and asks to be retried. A referee that
#: gave up on one would decline an ending for a reason that has nothing to do
#: with the game, so these are retried rather than surfaced.
MUSE_RETRY_STATUSES = (429, 500, 502, 503, 504)
MUSE_RETRIES = 3

#: A Model API key is `LLM|<app id>|<token>`. Checking the shape before the
#: call turns the most common setup mistake into a sentence instead of a bare
#: 401. The mistake is not exotic: the usual way to get a key into a file is to
#: copy it and paste it, and anything else copied in between silently wins.
MUSE_KEY_SHAPE = re.compile(r"^LLM\|\d+\|[A-Za-z0-9_-]+$")

#: Muse Spark is a reasoning model and its hidden reasoning tokens are charged
#: against the same budget as the answer. A ceiling sized for the answer alone
#: is exhausted mid-reasoning and the call comes back empty rather than short,
#: which reads like a broken prompt. The internal runbook's advice is to be
#: generous; this is a ceiling, not a target, so it is free on a normal call.
#:
#: The opposite mistake is worse: setting it to the context window 500s the
#: server. It bounds the output, not the input.
MUSE_MAX_OUTPUT_TOKENS = 8192


class MuseCompletion:
    """Meta's internal Model API, over plain HTTP. Standard library only.

    Getting a key is a one-time setup at modelapi.internalmeta.com: landing
    there creates an account, "Create Team" creates a project and a default
    key, and Muse Spark then needs the Evaluation or BYOC tier granted to that
    team. See the module docstring of the tests for the rest.

    Several Muse-specific constraints are encoded here rather than left to the
    caller, because each of them fails in a way that looks like something else:

    - **Responses API only.** There is no chat-completions path for Muse Spark.
    - **`temperature` and `top_p` at 1**, per the model card.
    - **No vLLM sampling extensions.** `repetition_penalty` and
      `guided_decode_json_schema` are not supported and return zero candidates
      rather than an error. The judge already asks for its JSON in the prompt
      and parses it out of the reply, so structured output needs neither.
    - **A generous timeout.** The default is ten minutes; a low one surfaces
      mid-stream as a server-side timeout rather than a client one.

    On `prompt_cache_key`: it is sent on every call and it is not optional
    here. It is what gives this caller its own slice of the prefix cache, and
    the system prompt (the rules, identical all match) is exactly the prefix
    worth caching. Omitting it is a known cross-tenant issue, so the default is
    derived from the system prompt rather than left unset.
    """

    def __init__(
        self,
        model: str = MUSE_MODEL,
        *,
        api_key: str | None = None,
        endpoint: str = MUSE_ENDPOINT,
        max_output_tokens: int = MUSE_MAX_OUTPUT_TOKENS,
        reasoning_effort: str = "minimal",
        timeout_s: int = 600,
        cache_key: str | None = None,
        retries: int = MUSE_RETRIES,
        api_key_file: str | None = None,
        opener: Any = None,
    ) -> None:
        self.model = model
        self.endpoint = endpoint
        self.max_output_tokens = max_output_tokens
        if reasoning_effort and reasoning_effort not in MUSE_EFFORTS:
            # Caught here rather than as a 400 three layers down, mid-match.
            raise CompletionError(
                f"reasoning_effort must be one of {list(MUSE_EFFORTS)}, "
                f"got {reasoning_effort!r}"
            )
        self.reasoning_effort = reasoning_effort
        self.timeout_s = timeout_s
        self.cache_key = cache_key
        self.retries = retries
        self._api_key = read_key(api_key, path=api_key_file)
        #: Injected in tests. Anything with `.open(request, timeout=)`.
        self._opener = opener or urllib.request

    def _key(self) -> str:
        if not self._api_key:
            raise CompletionError(
                "no Model API key. Write it to a file and point "
                "MODEL_API_KEY_FILE at that file, or set MODEL_API_KEY. "
                "Create a key at https://modelapi.internalmeta.com/dashboard/api-keys."
            )
        if not MUSE_KEY_SHAPE.match(self._api_key):
            raise CompletionError(
                f"that is not a Model API key. A key looks like "
                f"`LLM|<app id>|<token>`; {_describe(self._api_key)}. "
                f"Check {os.environ.get('MODEL_API_KEY_FILE') or 'MODEL_API_KEY'}."
            )
        return self._api_key

    def body(self, prompt: str, system: str = "") -> dict[str, Any]:
        """The request, separated out so a test can read it without a call."""
        request: dict[str, Any] = {
            "model": self.model,
            "input": prompt,
            "max_output_tokens": self.max_output_tokens,
            "temperature": 1.0,
            "top_p": 1.0,
            # The stable half of the prompt. Held apart from `input` so the
            # server sees the same prefix on every call in a match.
            "prompt_cache_key": self.cache_key or _cache_key(system),
        }
        if system:
            request["instructions"] = system
        if self.reasoning_effort:
            request["reasoning"] = {"effort": self.reasoning_effort}
        return request

    def models(self) -> list[str]:
        """Every model id this key may call. Empty if the list cannot be read."""
        request = urllib.request.Request(
            MUSE_MODELS_ENDPOINT,
            headers={"Authorization": f"Bearer {self._key()}"},
        )
        try:
            with self._opener.urlopen(request, timeout=30) as response:
                data = json.loads(response.read().decode("utf-8"))
        except Exception:
            return []
        rows = data.get("data") if isinstance(data, dict) else data
        return sorted(
            str(row["id"])
            for row in (rows or ())
            if isinstance(row, dict) and row.get("id")
        )

    def complete(self, prompt: str, system: str = "") -> str:
        data = self._post(json.dumps(self.body(prompt, system)).encode("utf-8"))
        text = extract_output_text(data)
        if not text.strip():
            # The failure mode the runbook warns about: a budget sized for the
            # answer is spent on reasoning and the reply is empty rather than
            # truncated. Saying so beats returning "" to a JSON parser.
            raise CompletionError(
                f"Model API returned no text (response id "
                f"{data.get('id', 'unknown')}). If this repeats, "
                f"max_output_tokens={self.max_output_tokens} is probably being "
                f"consumed by reasoning; raise it."
            )
        return text

    def _post(self, payload: bytes) -> dict[str, Any]:
        """One request, retried while the backend is shedding load."""
        request = urllib.request.Request(
            self.endpoint,
            data=payload,
            headers={
                "Authorization": f"Bearer {self._key()}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        last = ""
        for attempt in range(self.retries + 1):
            try:
                with self._opener.urlopen(request, timeout=self.timeout_s) as reply:
                    return json.loads(reply.read().decode("utf-8"))
            except urllib.error.HTTPError as error:
                detail = error.read().decode("utf-8", "replace")[:300]
                if error.code == 404:
                    # Almost always the model id, not the key. Say which ids
                    # this key does hold rather than leaving it to a wiki.
                    raise CompletionError(
                        f"Model API has no model {self.model!r} for this key. "
                        f"Available: {self.models() or 'could not be listed'}"
                    ) from None
                last = f"Model API returned {error.code}: {detail}"
                if error.code not in MUSE_RETRY_STATUSES or attempt == self.retries:
                    raise CompletionError(last) from None
            except Exception as error:
                # A reset or a dropped connection is the same kind of event as
                # a 503 and arrives as neither an HTTPError nor a status code.
                # Treating it as fatal was the whole reason the first live call
                # failed, so it retries on the same ladder.
                last = f"the model call failed: {error}"
                if attempt == self.retries:
                    raise CompletionError(last) from None
            _sleep(2.0 ** attempt)
        raise CompletionError(last)


def _describe(value: str) -> str:
    """Say what a bad key looks like without repeating it.

    Never echoes the value. A key that turns out to be real would otherwise be
    printed into whatever is reading the error, which is the same class of
    mistake this message exists to report.
    """
    if " " in value:
        return "this one contains spaces, so it looks like a line of shell"
    if value.startswith("mg-api-"):
        return "this one is a MetaGen key, which is a different credential"
    if value.isdigit():
        return "this one is all digits, so it looks like an app id"
    return f"this one is {len(value)} characters with {value.count('|')} pipes"


def _sleep(seconds: float) -> None:
    import time

    time.sleep(seconds)


def extract_output_text(data: dict[str, Any]) -> str:
    """Pull the assistant's text out of a Responses payload.

    Tolerant on purpose: the payload nests text inside output items inside
    content parts, and a reasoning model adds items this does not want. Only
    `output_text` parts of `message` items are read.
    """
    parts: list[str] = []
    for item in data.get("output") or ():
        if not isinstance(item, dict) or item.get("type") != "message":
            continue
        for content in item.get("content") or ():
            if isinstance(content, dict) and content.get("type") == "output_text":
                parts.append(str(content.get("text", "")))
    if parts:
        return "".join(parts)
    # Some deployments also surface the flattened convenience field.
    return str(data.get("output_text") or "")


def _cache_key(system: str) -> str:
    """A stable, non-secret handle for this caller's slice of the cache."""
    import hashlib

    digest = hashlib.sha256(system.encode("utf-8")).hexdigest()[:16]
    return f"xcolos-judge-{digest}"


def from_spec(spec: str) -> Completion:
    """Build a backend from one string, for a command line or a config file.

    Three forms, so a match can be pointed at a judge without code:

        anthropic                     the default model
        anthropic:claude-opus-5       a named model
        muse                          Muse Spark on the internal Model API
        muse:muse-spark-1.1-byoc      a named Muse model
        command:ollama run llama3     any program
        echo:{"answer": true}         a fixed reply, for a wiring check
    """
    kind, _, rest = spec.partition(":")
    kind = kind.strip().lower()
    if kind == "anthropic":
        return AnthropicCompletion(model=rest.strip() or DEFAULT_MODEL)
    if kind == "muse":
        return MuseCompletion(model=rest.strip() or MUSE_MODEL)
    if kind == "command":
        if not rest.strip():
            raise CompletionError("command: needs a program to run")
        return CommandCompletion(rest.strip())
    if kind == "echo":
        return EchoCompletion(rest or json.dumps({"answer": False, "reason": "echo"}))
    raise CompletionError(
        f"unknown backend {spec!r}; expected anthropic:, command: or echo:"
    )
