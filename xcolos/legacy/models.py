"""Linking a seat to a real model, on the client.

Everything here runs in the player's own process. The server is never told what
sits behind a seat and has no way to find out.

Three ways to link one, all satisfying the same `Completion` signature:

    command   Run a program. The conversation goes in on stdin, the answer
              comes back on stdout. Works with anything that has a CLI:
              `ollama run llama3`, a script wrapping any SDK, your own harness.

    http      POST to a chat-completions endpoint you are already running,
              such as Ollama, LM Studio or vLLM on localhost.

    offline   A stand-in that needs nothing. Used for tests and demos.

The command adapter is the general one and is worth reaching for first. It needs
no network, no library, and no agreement about request shape. If you can produce
an answer on stdout, you can play.
"""

from __future__ import annotations

import json
import os
import shlex
import subprocess
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from typing import Any

from xcolos.protocol import Envelope


class ModelUnavailable(Exception):
    """The model could not be reached, or gave nothing back.

    Raised rather than returned, so a broken link is visible. The agent turns it
    into a missing answer, and the server's failure ladder takes it from there.
    """


@dataclass
class ModelSpec:
    """How to reach one model. Lives on the client and stays there."""

    kind: str  # "command" | "http" | "offline"
    target: str = ""
    model: str = ""
    temperature: float = 0.8
    max_tokens: int = 512
    timeout_s: float = 60.0
    #: Name of an environment variable holding a bearer token, if the endpoint
    #: needs one. The value is read here and never recorded or transmitted
    #: anywhere but the request itself.
    auth_env: str = ""
    extra: dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def parse(spec: str) -> "ModelSpec":
        """Read a one-line spec.

            cmd:ollama run llama3
            http://127.0.0.1:11434/v1
            http://127.0.0.1:1234/v1#my-model
            offline
        """
        spec = (spec or "").strip()
        if not spec or spec == "offline":
            return ModelSpec(kind="offline")
        if spec.startswith(("cmd:", "command:")):
            return ModelSpec(kind="command", target=spec.split(":", 1)[1].strip())
        if spec.startswith(("http://", "https://")):
            url, _, model = spec.partition("#")
            return ModelSpec(kind="http", target=url, model=model)
        raise ValueError(
            f"cannot read model spec {spec!r}. "
            "Use 'cmd:<program>', a chat-completions URL, or 'offline'."
        )

    def describe(self) -> dict[str, Any]:
        """Safe to print. Never includes a token."""
        return {"kind": self.kind, "target": self.target, "model": self.model}


# ----------------------------------------------------------------------
# The question put to a model
# ----------------------------------------------------------------------


def build_request(messages: list[dict[str, str]], env: Envelope) -> dict[str, Any]:
    """What the client hands a model: the seat's conversation and the ask.

    Sent as one JSON object so a command-line model has everything it needs
    without parsing prose. The conversation is this seat's session and nothing
    else, so a model cannot condition on another seat's view.
    """
    schema = env.schema
    return {
        "seat": env.seat,
        "match_id": env.match_id,
        "turn_seq": env.turn_seq,
        "messages": messages,
        "question": env.body,
        "action": schema.id if schema else None,
        "answer_with": schema.target if schema else None,
        "choices": list(schema.choices) if schema and schema.choices else [],
        "legal_targets": list(env.legal_targets),
        "deadline_ms": env.deadline_ms,
    }


def as_prompt(request: dict[str, Any]) -> str:
    """The same request as plain text, for a model that wants a single string."""
    lines = []
    for m in request["messages"]:
        lines.append(f"[{m['role']}] {m['content']}")
    if request["legal_targets"]:
        lines.append(f"Answer with one of: {request['legal_targets']}")
    elif request["answer_with"] == "text":
        lines.append("Answer with what you want to say.")
    return "\n".join(lines)


# ----------------------------------------------------------------------
# Adapters
# ----------------------------------------------------------------------


def command_model(spec: ModelSpec):
    """Run a program. Conversation in on stdin, answer out on stdout.

    The most general link there is. Anything with a command line can hold a
    seat, and nothing needs to be installed for it to work.
    """
    argv = shlex.split(spec.target)
    if not argv:
        raise ValueError("a command model needs a program to run")

    def complete(messages: list[dict[str, str]], env: Envelope) -> str:
        request = build_request(messages, env)
        payload = json.dumps(request)
        try:
            done = subprocess.run(
                argv,
                input=payload,
                capture_output=True,
                text=True,
                timeout=spec.timeout_s,
                env={**os.environ, "XCOLOS_PROMPT": as_prompt(request)[:32000]},
            )
        except subprocess.TimeoutExpired:
            raise ModelUnavailable(
                f"{argv[0]} did not answer within {spec.timeout_s:.0f}s"
            ) from None
        except OSError as exc:
            raise ModelUnavailable(f"could not run {argv[0]}: {exc}") from None

        if done.returncode != 0:
            detail = (done.stderr or "").strip()[:200]
            raise ModelUnavailable(f"{argv[0]} exited {done.returncode}: {detail}")
        return done.stdout

    return complete


def http_model(spec: ModelSpec):
    """POST to a chat-completions endpoint you are running.

    Covers Ollama, LM Studio and vLLM on localhost, which all speak the same
    shape. The endpoint is the player's own; nothing about it reaches the
    server.
    """
    url = spec.target.rstrip("/")
    if not url.endswith("/chat/completions"):
        url = url + "/chat/completions"

    def complete(messages: list[dict[str, str]], env: Envelope) -> str:
        body = {
            "model": spec.model or "local",
            "messages": messages,
            "temperature": spec.temperature,
            "max_tokens": spec.max_tokens,
            "stream": False,
            **spec.extra,
        }
        headers = {"Content-Type": "application/json"}
        if spec.auth_env:
            token = os.environ.get(spec.auth_env, "")
            if token:
                headers["Authorization"] = f"Bearer {token}"

        req = urllib.request.Request(
            url, data=json.dumps(body).encode(), headers=headers, method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=spec.timeout_s) as r:
                data = json.loads(r.read())
        except urllib.error.HTTPError as exc:
            raise ModelUnavailable(
                f"{url} returned {exc.code}: {exc.read().decode()[:200]}"
            ) from None
        except (urllib.error.URLError, TimeoutError, ValueError) as exc:
            raise ModelUnavailable(f"could not reach {url}: {exc}") from None

        try:
            return data["choices"][0]["message"]["content"] or ""
        except (KeyError, IndexError, TypeError):
            raise ModelUnavailable(
                f"{url} answered in an unexpected shape: {str(data)[:200]}"
            ) from None

    return complete


def completion_for(spec: ModelSpec | str):
    """Turn a spec into something an LLM agent can call."""
    if isinstance(spec, str):
        spec = ModelSpec.parse(spec)
    if spec.kind == "command":
        return command_model(spec)
    if spec.kind == "http":
        return http_model(spec)

    from xcolos.agents import offline_model

    return offline_model(0)
