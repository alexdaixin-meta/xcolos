# A Claude backend through Meta's AI Gateway

2026-10-26. A short design: a small change to `xcolos/flow/backends.py` and `gen_game/cli.py`.

## Intent

Let game generation (and model seats) use Claude through **Meta's AI Gateway**, Meta's sanctioned route for calling
third-party models from internal tools, with the model spec `gateway[:model]`, e.g. `gateway:claude-opus-5-5`. There
is no personal key: your Meta identity is the authentication, through the local proxy. A probe on 2026-10-26 got
HTTP 200 from `claude-opus-5-5` through both the `anthropic` and the `vertex` gateways, from inside a Claude Code
session, tagged `x-meta-ai-gateway-calling-product: xcolos`.

## Goals

- `--model gateway[:model]` works wherever a model spec is taken: `gen_game convert` (design, critic, spec,
  scenarios, triage, the completion coder), `review`, `revise`, `brief`, `loop`, and model seats (`--players`).
- Long outputs (a whole game file, about 15k tokens) don't time out.
- Traffic is labelled as xcolos, not as Claude Code.

## Non-goals and anti-goals

- No personal Anthropic key and no Claude Code credentials: only the gateway's identity-based access.
- No devserver (TLS client cert) route, only the corp-Mac proxy. Add it when someone runs there.
- No new required dependency for the platform: `anthropic` is imported only when a gateway or anthropic model is used.
- Anti-goal: traffic attributed to `claude_code:cli`, or marked sensitive (DSS4) when the game data is not.

## Approaches considered

1. **Reuse the SDK-based `AnthropicCompletion` (chosen).** The project already has it (`backends.py:171`):
   streaming, adaptive thinking, a cached system prompt, and a lazy SDK import. `gateway` is the same class, pointed at
   the gateway. Cost: `pip install anthropic` into `.venv`, and running the pipeline with `.venv/bin/python`.
2. Plain HTTP (urllib), like the Muse backend: no dependency, but it hand-writes streaming, retries and errors that
   the SDK provides, against Anthropic's guidance for languages with an SDK.

## The design

**`AnthropicCompletion`** gains optional `base_url`, `proxy`, `headers` and `effort` (all defaulting to today's
behaviour). With a `proxy`, the client is built with the SDK's `DefaultHttpxClient(proxy=...)`. `effort` goes in
`output_config.effort`. Claude Opus 5.5 defaults to `medium`, so the gateway sets it explicitly. The class also:

- turns on server-side refusal fallbacks by default (`fallbacks: "default"`, beta `server-side-fallback-2026-07-01`).
  If the gateway refuses the beta, it is dropped and the ruling recorded;
- raises `CompletionError` on `stop_reason == "refusal"` (with its category) and on a reply with no text, and joins
  the text blocks of anything else, skipping thinking blocks.

**`from_spec("gateway[:model]")`** builds it with:
- base URL `http://anthropic.ai-gateway.x2p.facebook.net`, through the proxy `http://localhost:10054`;
- the placeholder key `meta-ai-gateway-placeholder`, which the gateway replaces;
- headers `x-meta-ai-gateway-calling-product: xcolos` and `x-meta-ai-gateway-sensitive: false`;
- model default `claude-opus-5-5`, `max_tokens` 64000 (streaming), effort `high`.

A Claude Code session exports `ANTHROPIC_CUSTOM_HEADERS` (its own calling product). If the SDK merges that variable,
the gateway client must not carry it. A test pins that the outgoing calling product is `xcolos`.

**`gen_game` `completion_for("gateway[:model]", effort)`** maps the pipeline's effort (`minimal|low|medium|high`) to
the API's (`low|low|medium|high`) and wraps the backend in `Patient`, as for Muse.

**Defaults (Alex, 2026-10-26: "muse is still an option; if Claude works, set Claude by default").** Only after the live
gateway check passes, the generator's defaults become `gateway`:
- `convert --model` (today required) defaults to `gateway`;
- `review`, `revise` and `brief` `--model` change from `muse` to `gateway`;
- `loop --model` and `--review-model` change from `claude` (the CLI, which cannot start inside a Claude Code session)
  to `gateway`;
- `loop --encoder` changes from `claude` (the Claude Code agent) to `completion`, i.e. the `--model`, which is now
  Claude through the gateway. The agent stays available as `--encoder claude`.

Muse stays available everywhere as `--model muse`. Model seats (`--players`) keep their defaults (`muse`): the players
are the models a game measures, a separate choice from the generator. If the live check fails, no default changes.

**Running it.** `.venv/bin/python -m gen_game convert <id> --judge` (now Claude through the gateway). The README's model section gets
one paragraph: what `gateway` is, the `.venv` requirement, and that a team workload should register its own gateway
(onboarding: https://www.internalfb.com/intern/staticdocs/ai-gateway/docs/owning/onboarding).

## Tests

- `from_spec("gateway")` and `from_spec("gateway:claude-sonnet-5-5")` build an `AnthropicCompletion` with the gateway
  URL, proxy, placeholder key, xcolos headers, `max_tokens` 64000 and effort `high`; `anthropic:` is unchanged.
- With an injected fake client: the request carries `output_config.effort`, the cached system block, and the
  fallbacks beta; a refusal and an empty reply raise `CompletionError`; thinking blocks are not in the text.
- With the SDK installed: the outgoing request (an `httpx2` mock transport) has calling product `xcolos`, even with
  `ANTHROPIC_CUSTOM_HEADERS` naming `claude_code:cli`.
- One live check (not in the suite): a short gateway call through `completion_for("gateway", "low")`.
- `python3 run_tests.py` and `python3 gen_game/run_tests.py` stay green with and without the SDK installed.

## Left to the builder

Exact parameter names; where the effort map lives; whether the fallback beta needs `client.beta.messages.stream`.
