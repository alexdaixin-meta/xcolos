"""Linking a real model to the judge seam.

Nothing here calls a provider. The Anthropic adapter is exercised against a
fake client, which is enough to pin the request shape and the failure paths;
the network call itself is not testable on this machine and is not pretended to
be.
"""

from __future__ import annotations

import json
import sys

from xcolos.flow import ModelJudge, Output
from xcolos.flow.backends import (
    DEFAULT_MODEL,
    AnthropicCompletion,
    gateway_completion,
    CommandCompletion,
    MUSE_MODEL,
    CompletionError,
    EchoCompletion,
    FallbackCompletion,
    MuseCompletion,
    from_spec,
    read_key,
    split_alternatives,
)
from xcolos.flow.judge import Call


#: Shaped like a real Model API key so the shape check passes. Not a key.
FAKE_KEY = "LLM|1234567890|not-a-real-token"


class FakeStream:
    def __init__(self, message):
        self.message = message

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def get_final_message(self):
        return self.message


class Block:
    def __init__(self, type, text=""):
        self.type, self.text = type, text


class FakeClient:
    """Records the request and returns a canned message."""

    def __init__(self, blocks=None, error=None, stop_reason="end_turn"):
        self.blocks = blocks or [Block("text", '{"answer": true, "reason": "ok"}')]
        self.error = error
        self.stop_reason = stop_reason
        self.requests = []
        self.messages = self

    def stream(self, **request):
        self.requests.append(request)
        if self.error:
            raise self.error
        return FakeStream(type("M", (), {"content": self.blocks, "stop_reason": self.stop_reason, "stop_details": None})())


# ----------------------------------------------------------------------
# The Anthropic adapter
# ----------------------------------------------------------------------


def test_the_request_names_the_current_model_and_asks_for_adaptive_thinking():
    client = FakeClient()
    text = AnthropicCompletion(client=client).complete("Has the town won?")
    assert text == '{"answer": true, "reason": "ok"}'

    request = client.requests[0]
    assert request["model"] == DEFAULT_MODEL == "claude-opus-5"
    assert request["thinking"] == {"type": "adaptive"}
    assert "budget_tokens" not in request.get("thinking", {}), (
        "budget_tokens is rejected on this model family"
    )
    assert request["messages"] == [{"role": "user", "content": "Has the town won?"}]
    assert request["max_tokens"] > 0


class FakeBetaClient(FakeClient):
    """Also answers `client.beta.messages.stream`, the path the refusal-fallback beta takes."""

    def __init__(self, **kw):
        super().__init__(**kw)
        self.beta = self


def test_the_gateway_spec_points_the_claude_client_at_the_ai_gateway():
    c = from_spec("gateway")
    assert isinstance(c, AnthropicCompletion) and c.model == "claude-opus-5-5"
    kw = c.client_kwargs()
    assert kw["base_url"] == "http://anthropic.ai-gateway.x2p.facebook.net" and kw["api_key"] == "meta-ai-gateway-placeholder"
    assert kw["default_headers"]["x-meta-ai-gateway-calling-product"] == "xcolos"
    assert kw["default_headers"]["x-meta-ai-gateway-sensitive"] == "false"
    assert c.proxy == "http://localhost:10054" and c.max_tokens == 64000 and c.effort == "high" and c.fallbacks
    assert from_spec("gateway:claude-sonnet-5-5").model == "claude-sonnet-5-5"
    assert gateway_completion(effort="low").effort == "low"


def test_a_gateway_request_sets_effort_caches_the_system_and_asks_for_fallbacks():
    client = FakeBetaClient()
    AnthropicCompletion(client=client, model="claude-opus-5-5", effort="high", fallbacks=True).complete("go", system="rules")
    r = client.requests[0]
    assert r["output_config"] == {"effort": "high"} and r["system"][0]["cache_control"] == {"type": "ephemeral"}
    assert r["betas"] == ["server-side-fallback-2026-07-01"] and r["fallbacks"] == "default"


def test_without_gateway_options_the_anthropic_request_is_unchanged():
    client = FakeClient()
    AnthropicCompletion(client=client).complete("x")
    assert not {"output_config", "betas", "fallbacks"} & set(client.requests[0])
    assert "base_url" not in AnthropicCompletion(api_key="k").client_kwargs()


def test_a_refusal_or_a_reply_with_no_text_raises_a_completion_error():
    cases = (([Block("text", "no")], "refusal", "refus"), ([Block("thinking", "hm")], "end_turn", "no text"))
    for blocks, stop, words in cases:
        try:
            AnthropicCompletion(client=FakeClient(blocks=blocks, stop_reason=stop)).complete("x")
        except CompletionError as error:
            assert words in str(error), str(error)
        else:
            raise AssertionError(f"{stop} should raise")


def test_the_gateway_request_is_labelled_xcolos_even_inside_claude_code():
    """A Claude Code shell exports its own calling product; the gateway request must still say xcolos."""
    import os

    import pytest

    try:
        import anthropic
    except ImportError:
        pytest.skip("the anthropic SDK is not installed")
    try:
        import httpx2 as http  # anthropic 1.x
    except ImportError:
        import httpx as http  # anthropic 0.x
    seen = []

    def handler(request):
        seen.append(request)
        raise http.ConnectError("stop here")

    old = os.environ.get("ANTHROPIC_CUSTOM_HEADERS")
    os.environ["ANTHROPIC_CUSTOM_HEADERS"] = (
        "X-Meta-AI-Gateway-Calling-Product: claude_code:cli\nx-meta-ai-gateway-harness: claude_code\n"
        "X-Meta-AI-Gateway-Trace-Id: claude_code_invocation_1"
    )
    try:
        c = gateway_completion()
        c.http_client = anthropic.DefaultHttpxClient(transport=http.MockTransport(handler))
        try:
            c.complete("x")
        except CompletionError:
            pass
    finally:
        if old is None:
            os.environ.pop("ANTHROPIC_CUSTOM_HEADERS", None)
        else:
            os.environ["ANTHROPIC_CUSTOM_HEADERS"] = old
    assert seen and all(r.headers["x-meta-ai-gateway-calling-product"] == "xcolos" for r in seen)
    assert seen[0].url.host == "anthropic.ai-gateway.x2p.facebook.net"
    # anthropic 2.x sends the key as a bearer token, 0.x/1.x as x-api-key; the gateway replaces either placeholder
    sent = seen[0].headers.get("x-api-key") or seen[0].headers.get("authorization", "").removeprefix("Bearer ")
    assert sent == "meta-ai-gateway-placeholder"
    # nothing else of Claude Code's own labelling rides along
    assert "x-meta-ai-gateway-harness" not in seen[0].headers
    assert "claude_code" not in seen[0].headers.get("x-meta-ai-gateway-trace-id", "")


def test_thinking_can_be_turned_off():
    client = FakeClient()
    AnthropicCompletion(client=client, thinking=False).complete("x")
    assert "thinking" not in client.requests[0]


def test_only_text_blocks_are_returned():
    client = FakeClient(blocks=[
        Block("thinking", "let me count the living players"),
        Block("text", '{"answer": '),
        Block("text", 'false}'),
    ])
    assert AnthropicCompletion(client=client).complete("x") == '{"answer": false}'


def test_a_failing_call_raises_a_completion_error_rather_than_the_sdk_error():
    client = FakeClient(error=RuntimeError("429 overloaded"))
    try:
        AnthropicCompletion(client=client).complete("x")
    except CompletionError as error:
        assert "429 overloaded" in str(error)
    else:
        raise AssertionError("the caller must see one error type")


def test_a_missing_key_is_reported_before_any_call_is_attempted():
    if "anthropic" in sys.modules:
        return  # the real package is installed; this path is about its absence
    try:
        AnthropicCompletion(api_key=None).complete("x")
    except CompletionError as error:
        assert "anthropic" in str(error) or "API key" in str(error)
    else:
        raise AssertionError("it must say what is missing")


def test_the_rules_go_out_as_a_cacheable_system_block():
    client = FakeClient()
    AnthropicCompletion(client=client).complete("the table now", system="the rules")
    system = client.requests[0]["system"]
    assert system == [
        {"type": "text", "text": "the rules",
         "cache_control": {"type": "ephemeral"}}
    ]
    assert client.requests[0]["messages"][0]["content"] == "the table now", (
        "the varying half must stay out of the cached block"
    )


def test_no_system_block_is_sent_when_there_is_nothing_to_cache():
    client = FakeClient()
    AnthropicCompletion(client=client).complete("just this")
    assert "system" not in client.requests[0]


def test_a_command_backend_gets_both_halves_because_it_cannot_cache():
    backend = CommandCompletion([sys.executable, "-c", "import sys; print(sys.stdin.read())"])
    out = backend.complete("the table", system="the rules")
    assert "the rules" in out and "the table" in out


def test_a_judge_over_a_failing_backend_still_declines_rather_than_crashing():
    """The whole point of the error type: a bad referee must not end a match."""
    client = FakeClient(error=RuntimeError("no route to host"))
    judge = ModelJudge(AnthropicCompletion(client=client))
    reply = judge.decide(Call(task="Is it over?", output=Output(kind="boolean")))
    assert reply.ok is False
    assert reply.yes is False
    assert reply.source == "error"


# ----------------------------------------------------------------------
# The command adapter
# ----------------------------------------------------------------------


def test_a_command_gets_the_prompt_on_stdin_and_answers_on_stdout():
    backend = CommandCompletion([sys.executable, "-c", "import sys; print(sys.stdin.read().upper())"])
    assert backend.complete("hello").strip() == "HELLO"


def test_a_missing_command_is_a_completion_error():
    try:
        CommandCompletion("definitely-not-a-real-program-xyz").complete("x")
    except CompletionError as error:
        assert "no such command" in str(error)
    else:
        raise AssertionError("a missing program must be reported clearly")


def test_a_command_that_fails_reports_its_exit_code_and_stderr():
    backend = CommandCompletion(
        [sys.executable, "-c", "import sys; sys.stderr.write('bad prompt'); sys.exit(3)"]
    )
    try:
        backend.complete("x")
    except CompletionError as error:
        assert "3" in str(error) and "bad prompt" in str(error)
    else:
        raise AssertionError("a non-zero exit is a failure")


# ----------------------------------------------------------------------
# Choosing one from a string
# ----------------------------------------------------------------------


def test_a_spec_string_builds_each_backend():
    assert isinstance(from_spec("anthropic"), AnthropicCompletion)
    assert from_spec("anthropic").model == DEFAULT_MODEL
    assert from_spec("anthropic:claude-sonnet-5").model == "claude-sonnet-5"
    assert isinstance(from_spec("command:echo hi"), CommandCompletion)
    assert from_spec("command:echo hi").command == ["echo", "hi"]
    assert isinstance(from_spec('echo:{"answer": true}'), EchoCompletion)
    assert from_spec('echo:{"answer": true}').complete("x") == '{"answer": true}'


def test_an_unknown_or_incomplete_spec_says_what_is_accepted():
    for bad in ("gpt4", "", "command:", "command:   "):
        try:
            from_spec(bad)
        except CompletionError:
            pass
        else:
            raise AssertionError(f"{bad!r} should not build a backend")


class Down:
    """A model that cannot be reached, counting how often it is asked."""

    model = "down"

    def __init__(self) -> None:
        self.calls = 0

    def complete(self, prompt: str, system: str = "") -> str:
        self.calls += 1
        raise CompletionError("Model API returned 403: requires the Meta corporate network")


def test_alternatives_ask_the_next_model_when_one_fails_and_keep_the_one_that_answered():
    import contextlib
    import io

    down, said = Down(), io.StringIO()
    both = FallbackCompletion([down, EchoCompletion("ok")])
    with contextlib.redirect_stderr(said):
        assert both.complete("x") == "ok" and both.complete("y") == "ok"
    assert down.calls == 1  # a model that is down costs one failed call, not one per call
    assert said.getvalue().count("down: Model API returned 403") == 1  # the switch is said once, so a run shows which model answered


def test_alternatives_report_every_failure_when_none_answers():
    try:
        FallbackCompletion([Down(), Down()]).complete("x")
    except CompletionError as exc:
        assert str(exc).count("403") == 2
    else:
        raise AssertionError("no model answered, so the call must fail")


def test_a_spec_names_alternatives_with_a_bar():
    both = from_spec("echo:a|echo:b")
    assert isinstance(both, FallbackCompletion) and both.complete("x") == "a"
    assert from_spec("echo:a|b").complete("x") == "a|b"  # a bar inside one spec's text is not a choice
    assert split_alternatives(" gateway | muse ") == ["gateway", "muse"]
    assert split_alternatives("command:sort | uniq") == ["command:sort | uniq"]


def test_a_seat_falls_back_to_the_next_model_when_the_first_cannot_be_reached():
    from xcolos.seat_models import seat_completion

    complete = seat_completion("command:false|echo:Pass", pause=lambda s: None)
    assert complete([{"role": "user", "content": "your move"}], None) == "Pass"


# ----------------------------------------------------------------------
# The internal Model API (Muse Spark)
#
# Getting a key, for reference:
#   1. https://modelapi.internalmeta.com/ — landing there creates an account.
#   2. "Create Team" — makes a default project and a default API key.
#   3. Have Muse Spark granted to that team, on the Evaluation tier (no
#      capacity needed) or the BYOC tier (your team transfers GPU capacity).
#   4. export MODEL_API_KEY=<the key from the API Keys page>
# Support: the "Muse Spark Internal Access" Workplace group.
#
# No test here reaches the network. They pin the request shape and the failure
# paths against a fake opener, which is all that can be checked offline.
# ----------------------------------------------------------------------


class FakeResponse:
    def __init__(self, payload):
        self._body = json.dumps(payload).encode()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def read(self):
        return self._body


class FakeOpener:
    def __init__(self, payload=None, error=None):
        self.payload = payload
        self.error = error
        self.requests = []

    def urlopen(self, request, timeout=None):
        self.requests.append((request, timeout))
        if self.error:
            raise self.error
        return FakeResponse(self.payload)


def message(text):
    return {
        "id": "resp_abc",
        "output": [
            {"type": "reasoning", "summary": []},
            {"type": "message",
             "content": [{"type": "output_text", "text": text}]},
        ],
    }


def test_the_request_uses_the_responses_shape_the_model_card_asks_for():
    body = MuseCompletion(api_key=FAKE_KEY).body("the table now", system="the rules")
    assert body["model"] == MUSE_MODEL
    assert body["input"] == "the table now"
    assert body["instructions"] == "the rules", "the system half is held apart"
    assert body["temperature"] == 1.0 and body["top_p"] == 1.0
    assert body["reasoning"] == {"effort": "minimal"}


def test_no_vllm_sampling_extension_is_ever_sent():
    """Muse Spark answers these with zero candidates rather than an error."""
    body = MuseCompletion(api_key=FAKE_KEY).body("x", system="y")
    for unsupported in ("repetition_penalty", "guided_decode_json_schema",
                        "response_format", "max_tokens"):
        assert unsupported not in body, f"{unsupported} returns an empty reply"


def test_the_output_budget_leaves_room_for_reasoning():
    body = MuseCompletion(api_key=FAKE_KEY).body("x")
    assert body["max_output_tokens"] >= 4096, (
        "a budget sized for the answer alone is spent on hidden reasoning"
    )


def test_a_cache_key_is_always_sent_and_follows_the_stable_half():
    a = MuseCompletion(api_key=FAKE_KEY).body("round 1", system="the rules")
    b = MuseCompletion(api_key=FAKE_KEY).body("round 9", system="the rules")
    c = MuseCompletion(api_key=FAKE_KEY).body("round 1", system="other rules")

    assert a["prompt_cache_key"], "omitting it shares a cache slice with everyone"
    assert a["prompt_cache_key"] == b["prompt_cache_key"], (
        "the cached prefix does not change within a match, so neither may the key"
    )
    assert a["prompt_cache_key"] != c["prompt_cache_key"]
    assert "the rules" not in a["prompt_cache_key"], "the key is not the content"
    assert MuseCompletion(api_key=FAKE_KEY, cache_key="mine").body("x")[
        "prompt_cache_key"] == "mine"


def test_a_call_carries_the_bearer_token_and_a_generous_timeout():
    fake = FakeOpener(payload=message("hello"))
    backend = MuseCompletion(api_key=FAKE_KEY, opener=fake)
    assert backend.complete("x", system="y") == "hello"

    request, timeout = fake.requests[0]
    assert request.get_header("Authorization") == f"Bearer {FAKE_KEY}"
    assert request.get_header("Content-type") == "application/json"
    assert request.full_url.endswith("/v1/responses")
    assert timeout >= 600, "a short timeout surfaces as a server-side error"


def test_only_message_text_is_read_out_of_the_payload():
    fake = FakeOpener(payload={
        "output": [
            {"type": "reasoning", "content": [
                {"type": "output_text", "text": "SHOULD NOT APPEAR"}]},
            {"type": "message", "content": [
                {"type": "output_text", "text": '{"answer": '},
                {"type": "refusal", "refusal": "SHOULD NOT APPEAR"},
                {"type": "output_text", "text": "true}"},
            ]},
        ],
    })
    assert MuseCompletion(api_key=FAKE_KEY, opener=fake).complete("x") == '{"answer": true}'


def test_an_empty_reply_names_the_budget_as_the_likely_cause():
    fake = FakeOpener(payload={"id": "resp_xyz", "output": []})
    try:
        MuseCompletion(api_key=FAKE_KEY, opener=fake).complete("x")
    except CompletionError as error:
        assert "resp_xyz" in str(error), "the response id is what the trace viewer takes"
        assert "max_output_tokens" in str(error)
    else:
        raise AssertionError("an empty reply is not an answer")


def test_an_http_error_reports_the_status_and_the_body():
    import io
    import urllib.error

    fake = FakeOpener(error=urllib.error.HTTPError(
        "u", 401, "Unauthorized", {}, io.BytesIO(b'{"error":"bad key"}')))
    try:
        MuseCompletion(api_key=FAKE_KEY, opener=fake).complete("x")
    except CompletionError as error:
        assert "401" in str(error) and "bad key" in str(error)
    else:
        raise AssertionError("a rejected key must say so")


def test_a_missing_key_says_where_to_get_one():
    backend = MuseCompletion(api_key=FAKE_KEY)
    backend._api_key = None
    try:
        backend.complete("x")
    except CompletionError as error:
        assert "MODEL_API_KEY" in str(error)
        assert "modelapi.internalmeta.com" in str(error)
    else:
        raise AssertionError("it must say what is missing and where to fix it")


def test_a_judge_over_muse_declines_rather_than_crashing_when_it_fails():
    fake = FakeOpener(error=RuntimeError("no route to host"))
    judge = ModelJudge(MuseCompletion(api_key=FAKE_KEY, opener=fake))
    reply = judge.decide(Call(task="Is it over?", output=Output(kind="boolean")))
    assert reply.ok is False and reply.source == "error"


def test_a_404_reports_the_models_this_key_actually_has():
    """The id in the docs is often not the id a team was granted."""
    import io
    import urllib.error

    class Opener:
        def urlopen(self, request, timeout=None):
            if request.full_url.endswith("/v1/models"):
                return FakeResponse({"data": [{"id": "rl-muse-spark-1-3-x"},
                                              {"id": "rl-muse-spark-1-1-x"}]})
            raise urllib.error.HTTPError(
                "u", 404, "Not Found", {},
                io.BytesIO(b'{"error":{"code":"model_not_found"}}'))

    try:
        MuseCompletion(model="muse-spark-1.1-eval", api_key=FAKE_KEY,
                       opener=Opener()).complete("x")
    except CompletionError as error:
        assert "muse-spark-1.1-eval" in str(error)
        assert "rl-muse-spark-1-3-x" in str(error), "say what is available"
    else:
        raise AssertionError("a wrong model id must be diagnosed, not retried")


def test_models_lists_what_the_key_holds_and_survives_a_failure():
    ok = FakeOpener(payload={"data": [{"id": "b"}, {"id": "a"}]})
    assert MuseCompletion(api_key=FAKE_KEY, opener=ok).models() == ["a", "b"]
    broken = FakeOpener(error=RuntimeError("down"))
    assert MuseCompletion(api_key=FAKE_KEY, opener=broken).models() == []


class FlakyOpener:
    """Fails the first `fails` attempts, then succeeds."""

    def __init__(self, fails, error):
        self.left, self.error, self.calls = fails, error, 0

    def urlopen(self, request, timeout=None):
        self.calls += 1
        if self.left > 0:
            self.left -= 1
            raise self.error
        return FakeResponse(message("recovered"))


def test_an_overloaded_backend_is_retried_rather_than_surfaced():
    import io
    import urllib.error

    overloaded = urllib.error.HTTPError(
        "u", 503, "Service Unavailable", {},
        io.BytesIO(b'{"error":{"code":"service_overloaded"}}'))
    flaky = FlakyOpener(2, overloaded)
    backend = MuseCompletion(api_key=FAKE_KEY, opener=flaky)
    backend_sleep_free(backend)
    assert backend.complete("x") == "recovered"
    assert flaky.calls == 3


def test_a_dropped_connection_is_retried_too():
    """Not an HTTPError and carries no status, but the same kind of event."""
    flaky = FlakyOpener(1, ConnectionResetError("Remote end closed connection"))
    backend = MuseCompletion(api_key=FAKE_KEY, opener=flaky)
    backend_sleep_free(backend)
    assert backend.complete("x") == "recovered"
    assert flaky.calls == 2


def test_retries_are_bounded_and_the_last_failure_is_reported():
    flaky = FlakyOpener(99, ConnectionResetError("still down"))
    backend = MuseCompletion(api_key=FAKE_KEY, opener=flaky, retries=2)
    backend_sleep_free(backend)
    try:
        backend.complete("x")
    except CompletionError as error:
        assert "still down" in str(error)
    else:
        raise AssertionError("it must give up eventually")
    assert flaky.calls == 3, "the original attempt plus two retries"


def test_a_rejected_key_is_not_retried():
    import io
    import urllib.error

    flaky = FlakyOpener(99, urllib.error.HTTPError(
        "u", 401, "Unauthorized", {}, io.BytesIO(b'{"error":"bad key"}')))
    backend = MuseCompletion(api_key=FAKE_KEY, opener=flaky)
    backend_sleep_free(backend)
    try:
        backend.complete("x")
    except CompletionError as error:
        assert "401" in str(error)
    else:
        raise AssertionError("a bad key is not transient")
    assert flaky.calls == 1, "retrying a rejected key only wastes time"


def backend_sleep_free(backend):
    """Run the retry ladder without the backoff. Tests should not wait."""
    import xcolos.flow.backends as module

    module._sleep = lambda seconds: None


def test_an_unsupported_reasoning_effort_fails_at_construction():
    """The server answers "none" with a 400; better to find out before a match."""
    for bad in ("none", "off", "High"):
        try:
            MuseCompletion(api_key=FAKE_KEY, reasoning_effort=bad)
        except CompletionError as error:
            assert "minimal" in str(error)
        else:
            raise AssertionError(f"{bad!r} is rejected by the server")
    for good in ("minimal", "low", "medium", "high"):
        assert MuseCompletion(api_key=FAKE_KEY, reasoning_effort=good).reasoning_effort


def test_muse_is_reachable_from_a_spec_string():
    assert isinstance(from_spec("muse"), MuseCompletion)
    assert from_spec("muse").model == MUSE_MODEL
    assert from_spec("muse:muse-spark-1.1-byoc").model == "muse-spark-1.1-byoc"


# ----------------------------------------------------------------------
# Where the key comes from
#
# A file, not a variable. The reason is not that files are magically safer:
# it is that a variable has to be typed somewhere to be set, and everything
# that transcribes what you type then holds the key — shell history, a process
# listing, a crash dump, an agent transcript. A path is safe to type. A key
# is not.
# ----------------------------------------------------------------------


def write_key(tmp, text):
    import pathlib
    path = pathlib.Path(tmp) / "key"
    path.write_text(text)
    return str(path)


class environment:
    """Set env vars for a block and put the old ones back.

    Both key variables are always controlled, never just the one a test is
    about. These tests read the real environment, and a developer who has a key
    file configured would otherwise see a different result from CI.
    """

    def __init__(self, **values):
        import os
        self.values = {"MODEL_API_KEY": None, "MODEL_API_KEY_FILE": None, **values}
        self.before = {k: os.environ.get(k) for k in self.values}

    def __enter__(self):
        import os
        for key, value in self.values.items():
            os.environ.pop(key, None)
            if value is not None:
                os.environ[key] = value
        return self

    def __exit__(self, *exc):
        import os
        for key, value in self.before.items():
            os.environ.pop(key, None)
            if value is not None:
                os.environ[key] = value
        return False


def test_a_key_file_beats_the_environment_variable():
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        path = write_key(tmp, "LLM|1|from-file\n")
        with environment(MODEL_API_KEY="LLM|1|from-env"):
            assert read_key(path=path) == "LLM|1|from-file"
            assert read_key() == "LLM|1|from-env", "the variable is the fallback"
            assert read_key("LLM|1|explicit") == "LLM|1|explicit"


def test_the_file_variable_is_honoured():
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        path = write_key(tmp, "LLM|1|via-variable\n")
        with environment(MODEL_API_KEY_FILE=path):
            assert read_key() == "LLM|1|via-variable"
            assert MuseCompletion()._api_key == "LLM|1|via-variable"


def test_nothing_configured_finds_nothing_rather_than_the_developers_own_key():
    with environment():
        assert read_key() == ""


def test_trailing_whitespace_is_stripped_rather_than_sent():
    """A pasted key picks up a newline, and a newline in a bearer token 401s."""
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        assert read_key(path=write_key(tmp, "  LLM|1|k  \n")) == "LLM|1|k"


def test_a_file_with_more_than_a_key_in_it_is_refused():
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        for bad, expected in (
            ("", "empty"),
            ("   \n", "empty"),
            ("export K=1\nLLM|1|k\n", "more than one line"),
        ):
            try:
                read_key(path=write_key(tmp, bad))
            except CompletionError as error:
                assert expected in str(error), f"{bad!r} -> {error}"
            else:
                raise AssertionError(f"{bad!r} is not a key file")


def test_a_missing_key_file_says_which_one():
    try:
        read_key(path="/no/such/key/file")
    except CompletionError as error:
        assert "/no/such/key/file" in str(error)
    else:
        raise AssertionError("a missing file must name itself")


def test_the_missing_key_message_leads_with_the_file():
    backend = MuseCompletion(api_key=FAKE_KEY)
    backend._api_key = ""
    try:
        backend.complete("x")
    except CompletionError as error:
        assert "MODEL_API_KEY_FILE" in str(error)
        assert "dashboard/api-keys" in str(error)
    else:
        raise AssertionError("it must say what is missing and where to fix it")


def test_a_key_that_is_not_a_key_is_named_before_the_call():
    """The 401 you get from a wrong key file tells you nothing. This does."""
    cases = {
        "umask 077 && pbpaste > ~/.config/k": "shell",
        "mg-api-8c276b149adf": "MetaGen",
        "1234567890123456": "app id",
        "LLM|abc|token": "pipes",
    }
    for bad, expected in cases.items():
        try:
            MuseCompletion(api_key=bad)._key()
        except CompletionError as error:
            assert expected in str(error), f"{bad!r} -> {error}"
            assert bad not in str(error), "the message must not echo the value"
        else:
            raise AssertionError(f"{bad!r} is not a Model API key")


def test_a_real_looking_key_passes_the_shape_check():
    for good in ("LLM|1234567890|aBcDeFgHiJkLmNoPqRsTuVwXyZ0", "LLM|1|a-b_c"):
        assert MuseCompletion(api_key=good)._key() == good


class ModelByModelOpener:
    """Overloaded for the models named in `down`; answers for any other, and remembers which model each request asked for."""

    def __init__(self, down):
        self.down, self.asked = set(down), []

    def urlopen(self, request, timeout=None):
        import io
        import urllib.error

        model = json.loads(request.data)["model"]
        self.asked.append(model)
        if model in self.down:
            raise urllib.error.HTTPError("u", 503, "Service Unavailable", {}, io.BytesIO(b'{"error":{"code":"service_overloaded"}}'))
        return FakeResponse(message(f"answered by {model}"))


def test_an_overloaded_model_falls_back_to_the_next_one_and_a_healthy_one_is_not_left():
    opener = ModelByModelOpener(down={"newest"})
    backend = MuseCompletion(model="newest", api_key=FAKE_KEY, opener=opener, retries=1, fallbacks=("older", "oldest"))
    backend_sleep_free(backend)
    assert backend.complete("x") == "answered by older"
    assert opener.asked == ["newest", "newest", "older"]  # its own retry first, then the next model, and no further
    healthy = ModelByModelOpener(down=set())
    assert MuseCompletion(model="newest", api_key=FAKE_KEY, opener=healthy, fallbacks=("older",)).complete("x") == "answered by newest"
    assert healthy.asked == ["newest"]


def test_when_every_model_is_overloaded_the_last_error_is_reported_and_without_fallbacks_nothing_changes():
    all_down = ModelByModelOpener(down={"a", "b"})
    backend = MuseCompletion(model="a", api_key=FAKE_KEY, opener=all_down, retries=0, fallbacks=("b",))
    backend_sleep_free(backend)
    try:
        backend.complete("x")
    except CompletionError as error:
        assert "503" in str(error)
    else:
        raise AssertionError("it must report the failure")
    assert all_down.asked == ["a", "b"]
    plain = ModelByModelOpener(down={"a"})
    solo = MuseCompletion(model="a", api_key=FAKE_KEY, opener=plain, retries=0)
    backend_sleep_free(solo)
    try:
        solo.complete("x")
    except CompletionError:
        pass
    assert plain.asked == ["a"]


def test_the_servers_first_choice_is_the_newest_model_unless_the_environment_names_another():
    import os
    from xcolos.flow.backends import MUSE_FALLBACKS, MUSE_LATEST, muse_first_choice

    saved = os.environ.pop("XCOLOS_MUSE_MODEL", None)
    try:
        assert muse_first_choice() == MUSE_LATEST and MUSE_LATEST not in MUSE_FALLBACKS
        os.environ["XCOLOS_MUSE_MODEL"] = "something-else"
        assert muse_first_choice() == "something-else"
    finally:
        os.environ.pop("XCOLOS_MUSE_MODEL", None)
        if saved is not None:
            os.environ["XCOLOS_MUSE_MODEL"] = saved


def test_a_model_seat_is_asked_for_its_reasons_before_its_answer():
    from xcolos.seat_models import SEAT_SYSTEM

    assert SEAT_SYSTEM.startswith("You are one player in a game")
    assert "one to three short sentences" in SEAT_SYSTEM and "last line" in SEAT_SYSTEM  # so a play can be read for how the player thought
