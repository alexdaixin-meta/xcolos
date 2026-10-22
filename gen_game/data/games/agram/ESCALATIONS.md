
2026-10-13 10:16 ## Iteration 2: infra findings, the loop stopped

- I2.1 [minor, infra] hand 1, trick 1, seat 3's first question (the prompt shown to the player): After the private hand message the player is shown an extra line: 'Living seats: [1, 2, 3, 4].' This line is not in the transcript's [to] messages, so the harness added it when building the prompt. (expected: The DESIGN says to 'drop living-seats lines', and SPEC R19 says the start-of-hand private message has 'no other lines' besides 'Your hand ...; dealer seat D; hand k of 6; points so far ...'.)
  fix proposed: Stop the platform's prompt builder from adding the living-seats line, at least for games that have no elimination, or let the game file turn it off.

Nothing was changed. Review these, then decide what to change in the platform or the tools before the loop continues.

