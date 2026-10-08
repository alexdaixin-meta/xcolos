"""A Muse that can hold a conversation, and that works in the background.

The platform's `MuseCompletion` sends one prompt, waits for the whole reply in one HTTP response, and keeps
nothing. Two things about Muse's endpoint matter for writing a whole game file:

  * It takes a list of messages as well as a prompt, so a repair can be a real next turn (what it said, then
    what was wrong with it). Checked: given `user, assistant, user` it used the assistant turn.
  * A request that is still open after about a minute is cut ("Remote end closed connection without
    response"), and streaming does not help: the stream is cut at the same point. A game file at medium
    reasoning effort takes longer than a minute, so every attempt was cut and retried the same way. The
    Responses API can run a request in the background: the POST returns at once with an id and a status of
    `queued`, and the reply is fetched by polling `GET .../responses/<id>` until it is `completed`. No single
    HTTP request is then open for long, so the cap does not apply. Checked live, on a short request.
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request

from xcolos.flow.backends import CompletionError, MuseCompletion, extract_output_text

DONE = ("completed", "failed", "incomplete", "cancelled")


def _sleep(seconds: float) -> None:
    time.sleep(seconds)


class MuseChat(MuseCompletion):
    #: Called with {response_id, status, polls, seconds} when a request is accepted and after every poll, so something
    #: outside can show that the model is still working on it. Set by `calls.Recorded`.
    on_status = None
    #: How long to wait for one reply in all, and how often to ask. A game file at medium effort has taken a few minutes.
    max_wait_s = 900
    poll_s = 3.0

    def converse(self, messages: list[dict], system: str = "") -> str:
        """The next assistant turn, given the whole conversation so far: [{role, content}, ...]."""
        body = self.body("", system)
        body["input"] = messages
        return self._background(body)

    def complete(self, prompt: str, system: str = "") -> str:
        return self._background(self.body(prompt, system))

    def _call(self, method: str, url: str, payload: dict | None = None) -> dict:
        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8") if payload is not None else None,
            headers={"Authorization": f"Bearer {self._key()}", "Content-Type": "application/json"},
            method=method,
        )
        try:
            with self._opener.urlopen(request, timeout=min(self.timeout_s, 60)) as reply:
                return json.loads(reply.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            raise CompletionError(f"Model API returned {exc.code}: {exc.read().decode('utf-8', 'replace')[:300]}") from None

    def _report(self, rid, status, polls, started) -> None:
        if self.on_status is not None:
            try:
                self.on_status({"response_id": rid, "muse_status": status, "polls": polls, "seconds": round(time.time() - started, 1)})
            except Exception:  # noqa: BLE001 - a status line must never break a model call
                pass

    def _background(self, body: dict) -> str:
        job = self._call("POST", self.endpoint, {**body, "background": True, "store": True})
        rid = job.get("id")
        if not rid:
            raise CompletionError(f"Model API did not accept a background request: {str(job)[:200]}")
        started = time.time()
        deadline = started + self.max_wait_s
        errors = 0
        polls = 0
        data = job
        self._report(rid, data.get("status"), polls, started)
        while data.get("status") not in DONE:
            if time.time() > deadline:
                raise CompletionError(f"the model call failed: no reply within {self.max_wait_s}s (response {rid})")
            _sleep(self.poll_s)
            try:
                data = self._call("GET", f"{self.endpoint}/{rid}")
                errors = 0
                polls += 1
                self._report(rid, data.get("status"), polls, started)
            except Exception as exc:  # a dropped poll is not a dropped job: ask again a few times
                errors += 1
                if errors > 5:
                    raise CompletionError(f"the model call failed: polling response {rid} kept failing: {exc}") from None
        status = data.get("status")
        if status != "completed" and status != "incomplete":
            raise CompletionError(f"Model API response {rid} {status}: {str(data.get('error'))[:300]}")
        text = extract_output_text(data)
        if status == "incomplete" or not text.strip():
            reason = (data.get("incomplete_details") or {}).get("reason", "no text")
            raise CompletionError(f"Model API returned {'a reply cut short' if text.strip() else 'no text'} ({reason}); "
                                  f"max_output_tokens={self.max_output_tokens} may be spent on reasoning")
        return text
