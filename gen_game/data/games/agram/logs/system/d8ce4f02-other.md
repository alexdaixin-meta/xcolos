You check that the RULES TEXT a player reads says what a game's numbered rules say. A player has only the rules text (plus their own state and the question
they are asked); if a numbered rule has an outcome the text never states, or states differently, the player decides without knowing a rule that applies to them.

For each numbered rule, ask: could a player who read only the rules text know what this rule says will happen, in each case it covers (true and false, success and failure,
who is affected, whether the action still goes ahead)? Report a rule only when the text OMITS an outcome a player needs for a decision, or says something DIFFERENT (a different
order of steps, a different cost, a different winner). Do not report wording, style or detail a player would not decide on, and do not report rules about hidden bookkeeping.
Report at most eight, the most important first. If the text covers everything, report none.

Reply with ONE JSON object and nothing else:
  {"gaps": [{"rule": "R21", "problem": "what the text leaves out or gets wrong", "add": "the sentence to add or the wording to use"}]}