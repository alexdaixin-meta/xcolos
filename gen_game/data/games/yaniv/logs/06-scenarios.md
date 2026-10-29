# 06 scenarios

- time: 2026-10-28T04:02:01+00:00 (163.5s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 87470a4d7b1d9f65, reply sha256 24cb1bba58d1e2e2

## Sent

````
SPEC:
{
  "name": "Simultaneous Yaniv: Claims",
  "summary": "Low-hand card game played in simultaneous turns: each round players secretly call or discard, then secretly claim another player's discarded card or take a shared blind draw. A caller who is not strictly lowest is caught (Asaf) for +30, and the lowest total when someone reaches 150 or after 40 rounds wins.",
  "players": {
    "min": 3,
    "max": 5,
    "suggested": 4
  },
  "parameters": {
    "hand_size_start": 5,
    "call_limit": 7,
    "asaf_penalty": 30,
    "end_total": 150,
    "max_rounds": 40,
    "min_set_size": 2,
    "min_run_length": 3,
    "max_tens_in_run": 1,
    "min_cards_kept": 1,
    "shoe_size": 54,
    "copies_per_value_1_to_9": 4,
    "copies_value_10": 16,
    "copies_value_0": 2,
    "run_offer_cards": 2,
    "set_or_single_offer_cards": 1,
    "contest_threshold": 2,
    "blind_draws_per_round": 1
  },
  "attributes": {
    "player": [
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "Card values the player holds (0 to 10). Revealed to all at a showdown.",
        "observable": false
      },
      {
        "key": "hand_sum",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "Sum of the values in hand.",
        "observable": false
      },
      {
        "key": "hand_size",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of cards in hand.",
        "observable": true
      },
      {
        "key": "total",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Running score. Lower is better.",
        "observable": true
      },
      {
        "key": "round_score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Points scored at the latest showdown.",
        "observable": true
      },
      {
        "key": "first_choice",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "This round's secret first choice: CALL, a list of discarded values, or NONE.",
        "observable": false
      },
      {
        "key": "called",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "Whether the player called this round. Revealed at the showdown.",
        "observable": false
      },
      {
        "key": "discard",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Values discarded this round. Announced at the offers step.",
        "observable": false
      },
      {
        "key": "claim",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "This round's second choice: BLIND or an offer id. Made secretly and announced in the public result.",
        "observable": false
      },
      {
        "key": "claim_failed",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "Whether this round's claim was lost to a contest.",
        "observable": false
      },
      {
        "key": "took_blind",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "Whether the player received the blind card this round.",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "shoe",
        "type": "list",
        "visible": "none",
        "initial": "[0,0, 1x4, 2x4, 3x4, 4x4, 5x4, 6x4, 7x4, 8x4, 9x4, 10x16] (54 values)",
        "meaning": "Card source. Every draw picks a value at random and does not remove it (reshuffled before every draw).",
        "observable": false
      },
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Current round number.",
        "observable": true
      },
      {
        "key": "called_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of players who called this round.",
        "observable": false
      },
      {
        "key": "lowest_sum",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "L, the lowest hand sum at a showdown.",
        "observable": false
      },
      {
        "key": "offers",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Offered cards this round, each 'seat S: value V'.",
        "observable": false
      },
      {
        "key": "blind_card",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "Value of this round's blind card. Each BLIND player gets a copy and is told the value privately.",
        "observable": false
      },
      {
        "key": "last_results",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Previous round's public results: discards, claims, failed claims, BLIND takers, or the showdown outcome.",
        "observable": false
      }
    ]
  },
  "setup": [
    "Every player's total is set to 0 and round is set to 1.",
    "The shoe holds 54 values: two 0s, four each of 1 to 9, and sixteen 10s.",
    "Each player is dealt 5 cards. Each card is a value drawn at random from the shoe without removing it, appended to that player's hand.",
    "Each player's hand_sum and hand_size are computed. hand_size is public and the hand is private."
  ],
  "round": [
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce round, every player's hand_size and total, and last_results."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player privately sees their own hand and hand_sum."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "CALL, or the list of card values from own hand to discard (one card, two or more equal values, or a run of 3 or more consecutive values). A 1-card player with hand_sum <= 7 is offered only CALL. A 1-card player with hand_sum > 7 is offered only NONE.",
      "effect": "first_choice := the answer."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Any illegal first_choice is replaced: a player with hand_size >= 2 discards their single highest card; a player with hand_size 1 discards nothing (NONE). Then called := (first_choice == CALL), and called_count := the number of players with called true.",
      "judged": "This player's first choice is legal: CALL with hand_sum at most 7; or values all held in their hand that form a single card, two or more cards of equal value, or a run of three or more consecutive values with no 0 and at most one 10; and at least one card is left in hand."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When called_count >= 1 (showdown): all discards are cancelled and lowest_sum := the minimum hand_sum. For each player: if called and hand_sum == lowest_sum and the count of players with hand_sum == lowest_sum is 1, round_score := 0; else if called, round_score := hand_sum + 30; else if hand_sum == lowest_sum, round_score := 0; else round_score := hand_sum. total += round_score. last_results records the revealed hands, the callers and the scores."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "When called_count >= 1: reveal every hand, hand_sum, called, round_score and total."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "When called_count >= 1: end the game if any total >= 150 or round == 40."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When called_count >= 1 and round < 40: each hand is cleared and gets 5 random draws from the shoe (without removal). hand_sum and hand_size are recomputed."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When called_count == 0: discard := the discarded values, which are removed from hand; hand_sum and hand_size are recomputed. offers := for each player who discarded one card or an equal-value set, one entry 'seat S: value V'; for each player who discarded a run, two entries, its lowest and its highest value. A player who discarded nothing makes no offer."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "When called_count == 0: announce every player's discard and the offers list."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "BLIND, or one entry of offers that belongs to another seat.",
      "effect": "When called_count == 0: claim := the answer. An illegal answer becomes BLIND."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When called_count == 0 (contests): for each offer entry claimed by 2 or more players, each of those players gets claim_failed := true and claim := BLIND. took_blind := (claim == BLIND)."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When called_count == 0: blind_card := one value drawn at random from the shoe (without removal). Each player whose claim is an offer appends that offer's value to hand. Each player with took_blind appends blind_card to hand. hand_sum and hand_size are recomputed."
    },
    {
      "action": "tell",
      "who": "each player with took_blind true",
      "answer": null,
      "effect": "When called_count == 0: privately tell the player the value of blind_card."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When called_count == 0: last_results := who claimed which card, which claims failed through contest, and who took BLIND. The blind_card value is not included."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "When called_count == 0: announce last_results."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When round == 40 and called_count == 0 (final showdown): lowest_sum := the minimum hand_sum. Each player gets round_score := 0 if hand_sum == lowest_sum, else round_score := hand_sum. total += round_score."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "When round == 40 and called_count == 0: reveal every hand, hand_sum, round_score and total."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Reset called, discard, claim, claim_failed, took_blind and offers. round += 1."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if any total >= 150 or round > 40."
    }
  ],
  "ending": {
    "condition": "any player's total >= 150 after a showdown, or round > 40 (after round 40 is played)",
    "rank_by": "-you.total",
    "decided_by": "The player with the lowest total wins. Players level at the lowest total share the result (the source calls this a draw)."
  },
  "rules": [
    {
      "id": "R1",
      "text": "Card values: Ace = 1, 2 to 10 = face value, J/Q/K = 10, Joker = 0. Every draw is a random value from a 54-card shoe (two 0s, four each of 1 to 9, sixteen 10s), reshuffled before each draw."
    },
    {
      "id": "R2",
      "text": "Before round 1, each player is dealt 5 cards and every total is 0."
    },
    {
      "id": "R3",
      "text": "When a player's hand_sum is 7 or less, then CALL is a legal first choice; when it is 8 or more, CALL is illegal."
    },
    {
      "id": "R4",
      "text": "When a player discards, then the discard is exactly one card, two or more cards of equal value, or a run of 3 or more consecutive values."
    },
    {
      "id": "R5",
      "text": "When a run contains a 0 or more than one 10, then it is illegal; 8-9-10 is legal and 9-10-10 is not."
    },
    {
      "id": "R6",
      "text": "When a discard would leave 0 cards in hand, then it is illegal."
    },
    {
      "id": "R7",
      "text": "When a player holds 1 card and hand_sum <= 7, then that player must CALL; when they hold 1 card and hand_sum > 7, then they discard nothing and still make the second choice."
    },
    {
      "id": "R8",
      "text": "When a first choice is illegal, then it is replaced by discarding the single highest card, or by discarding nothing for a player with 1 card."
    },
    {
      "id": "R9",
      "text": "When at least one player calls, then all discards are cancelled and a showdown is held on the hands as they stood."
    },
    {
      "id": "R10",
      "text": "At a showdown, when a caller's hand_sum is strictly lower than every other player's, then that caller scores 0."
    },
    {
      "id": "R11",
      "text": "At a showdown, when a caller is not strictly lowest, then the caller is caught (Asaf) and scores hand_sum + 30 (a caller with sum 6 tied at 6 scores 36)."
    },
    {
      "id": "R12",
      "text": "At a showdown, when a non-caller's hand_sum equals the lowest sum L, then they score 0; otherwise they score their hand_sum."
    },
    {
      "id": "R13",
      "text": "After a showdown, when no total is 150 or more and the round is not 40, then every player is dealt a fresh hand of 5 cards, and steps 5 to 10 are skipped."
    },
    {
      "id": "R14",
      "text": "When no one calls, then every discard is announced publicly and leaves play."
    },
    {
      "id": "R15",
      "text": "When a single card or an equal-value set is discarded, then it makes one offer of that value; when a run is discarded, then it makes two offers, its lowest and its highest value."
    },
    {
      "id": "R16",
      "text": "When no one calls, then each player chooses BLIND or a claim on one offered card of another player; claiming one's own offer is illegal and becomes BLIND."
    },
    {
      "id": "R17",
      "text": "When two or more players claim the same offered card, then none of them receives it and each is treated as BLIND."
    },
    {
      "id": "R18",
      "text": "When exactly one player claims an offered card, then that card is added to that player's hand."
    },
    {
      "id": "R19",
      "text": "When no one calls, then one blind card is drawn, and each BLIND player adds a copy of it to their hand and is privately told its value."
    },
    {
      "id": "R20",
      "text": "When the public result is announced, then it names who claimed which card, which claims failed through contest, and who took BLIND, but not the blind card's value."
    },
    {
      "id": "R21",
      "text": "When round 40 ends with no showdown that round, then all hands are revealed, each player at the lowest sum scores 0 and every other player scores their hand_sum."
    },
    {
      "id": "R22",
      "text": "When any total is 150 or more after a showdown, or round 40 is over, then the game ends."
    },
    {
      "id": "R23",
      "text": "When the game ends, then the player with the strictly lowest total wins; when two or more tie for lowest, then the game is a draw (shared result)."
    }
  ],
  "offers": [
    {
      "question": "First choice (step 3)",
      "who": "all players",
      "options": "A player with 2 or more cards and hand_sum <= 7: CALL, or any legal discard from their hand (one card, an equal-value set of 2 or more, or a run of 3 or more consecutive values with no 0 and at most one 10), keeping at least 1 card. A player with 2 or more cards and hand_sum > 7: any such legal discard only. A player with 1 card and hand_sum <= 7: CALL only. A player with 1 card and hand_sum > 7: NONE only."
    },
    {
      "question": "Second choice (step 6)",
      "who": "all players, including those who discarded nothing",
      "options": "BLIND, or any entry of offers that belongs to a seat other than their own."
    }
  ],
  "choices": [
    {
      "what": "3 to 5 players, suggested 4",
      "why": "4 is the designer's size and is kept. Three is the minimum for contests over offered cards and for a caller to face more than one rival. More than five makes contests near-certain and the showdown arithmetic too long to follow."
    },
    {
      "what": "No talk step",
      "why": "The source has no talk. Strategy lies in reading discards and claims (claiming a card reveals what you hold), timing the call, and avoiding contested claims."
    },
    {
      "what": "A 1-card player is offered only the forced option",
      "why": "The rules force CALL (if allowed) or discarding nothing, so no other option is offered."
    },
    {
      "what": "Draws are with replacement from a 54-value list",
      "why": "The source reshuffles the shoe before every draw, so the shoe's frequencies never change."
    },
    {
      "what": "Each card of a run's two offers is claimable separately",
      "why": "The rules call each one an offered card that a player may claim."
    }
  ],
  "simplifications": [
    {
      "what": "The legality of a discard (set or run) is judged by a referee sentence",
      "why": "Checking that values are held and form a set or a valid run is list logic, beyond simple arithmetic. Scoring stays arithmetic."
    },
    {
      "what": "A tie for the lowest total is a shared win rather than a declared draw",
      "why": "The engine shares the win among players level at the top. This is the same outcome as the source's draw."
    },
    {
      "what": "The lowest total wins via rank_by = -total",
      "why": "The engine ranks the highest value first."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: hand_size, total, round_score; table: round.
````

## Reply

````
```json
[
  {"name": "R1: setup deals 5 cards to each seat (values random, only the counts are asserted)", "rule": "R1", "players": 4, "seed": 1, "rounds": 0,
   "rules": [],
   "expect": {"lens": {"players": {"1": {"hand": 5}, "2": {"hand": 5}, "3": {"hand": 5}, "4": {"hand": 5}}},
              "players": {"1": {"hand_size": 5}, "2": {"hand_size": 5}, "3": {"hand_size": 5}, "4": {"hand_size": 5}},
              "game": {"round": 1}}},

  {"name": "R2: before round 1 every total is 0 and each seat holds 5 cards", "rule": "R2", "players": 3, "seed": 2, "rounds": 0,
   "rules": [],
   "expect": {"players": {"1": {"total": 0, "hand_size": 5}, "2": {"total": 0, "hand_size": 5}, "3": {"total": 0, "hand_size": 5}},
              "game": {"round": 1}}},

  {"name": "R3: CALL is offered at sum 7 and not at sum 8", "rule": "R3", "players": 3, "seed": 3, "rounds": 1, "default": "first",
   "given": {"players": {"1": {"hand": [3, 4], "hand_sum": 7, "hand_size": 2},
                         "2": {"hand": [4, 4], "hand_sum": 8, "hand_size": 2},
                         "3": {"hand": [10, 10], "hand_sum": 20, "hand_size": 2}}},
   "judge": {"This player's first choice is legal": true},
   "rules": [{"seat": 1, "options_include": "CALL"}],
   "expect": {"offered": [{"seat": 1, "option": "CALL"}],
              "not_offered": [{"seat": 2, "option": "CALL"}, {"seat": 3, "option": "CALL"}],
              "players": {"1": {"round_score": 0, "total": 0}, "2": {"round_score": 8, "total": 8}, "3": {"round_score": 20, "total": 20}}}},

  {"name": "R4: a pair whose full discard would empty the hand discards exactly one card", "rule": "R4", "players": 3, "seed": 4, "default": "first",
   "given": {"players": {"1": {"hand": [7, 7], "hand_sum": 14, "hand_size": 2},
                         "2": {"hand": [10, 10], "hand_sum": 20, "hand_size": 2},
                         "3": {"hand": [6, 6], "hand_sum": 12, "hand_size": 2}},
             "game": {"round": 40}},
   "rules": [{"seat": 1, "options_include": "seat 3: value 6"},
             {"seat": 2, "options_include": "seat 1: value 7"},
             {"seat": 3, "options_include": "seat 2: value 10"}],
   "expect": {"winner": 1,
              "standings": {"1": 0, "2": -17, "3": -16},
              "players": {"1": {"total": 0, "hand_size": 2}, "2": {"total": 17, "hand_size": 2}, "3": {"total": 16, "hand_size": 2}}}},

  {"name": "R5: a 9-10-10 hand never discards an illegal run; the fallback discards one 10", "rule": "R5", "players": 3, "seed": 5, "default": "first",
   "given": {"players": {"1": {"hand": [9, 10, 10], "hand_sum": 29, "hand_size": 3},
                         "2": {"hand": [8, 1], "hand_sum": 9, "hand_size": 2},
                         "3": {"hand": [7, 2], "hand_sum": 9, "hand_size": 2}},
             "game": {"round": 40}},
   "rules": [{"seat": 1, "options_include": "seat 3: value 7"},
             {"seat": 2, "options_include": "seat 1: value 10"},
             {"seat": 3, "options_include": "seat 2: value 8"}],
   "expect": {"winner": 3,
              "standings": {"1": -26, "2": -11, "3": 0},
              "players": {"1": {"total": 26, "hand_size": 3}, "2": {"total": 11, "hand_size": 2}, "3": {"total": 0, "hand_size": 2}}}},

  {"name": "R6: a discard may not empty the hand; pairs keep one card", "rule": "R6", "players": 3, "seed": 6, "default": "first",
   "given": {"players": {"1": {"hand": [9, 9], "hand_sum": 18, "hand_size": 2},
                         "2": {"hand": [8, 8], "hand_sum": 16, "hand_size": 2},
                         "3": {"hand": [10, 10], "hand_sum": 20, "hand_size": 2}},
             "game": {"round": 40}},
   "rules": [{"seat": 1, "options_include": "seat 2: value 8"},
             {"seat": 2, "options_include": "seat 3: value 10"},
             {"seat": 3, "options_include": "seat 1: value 9"}],
   "expect": {"winner": 1,
              "standings": {"1": 0, "2": -18, "3": -19},
              "players": {"1": {"total": 0, "hand_size": 2}, "2": {"total": 18, "hand_size": 2}, "3": {"total": 19, "hand_size": 2}}}},

  {"name": "R7: a 1-card player with sum 3 must CALL and wins the showdown", "rule": "R7", "players": 3, "seed": 7, "rounds": 1, "default": "first",
   "given": {"players": {"1": {"hand": [3], "hand_sum": 3, "hand_size": 1},
                         "2": {"hand": [10, 10], "hand_sum": 20, "hand_size": 2},
                         "3": {"hand": [9, 9], "hand_sum": 18, "hand_size": 2}}},
   "judge": {"This player's first choice is legal": true},
   "rules": [{"seat": 1, "options_include": "CALL"}],
   "expect": {"offered": [{"seat": 1, "option": "CALL"}],
              "players": {"1": {"round_score": 0, "total": 0, "hand_size": 5}, "2": {"round_score": 20, "total": 20, "hand_size": 5}, "3": {"round_score": 18, "total": 18, "hand_size": 5}}}},

  {"name": "R7: a 1-card player with sum 9 discards nothing and still takes a card (hand sizes only, blind value is random)", "rule": "R7", "players": 3, "seed": 8, "rounds": 1, "default": "first",
   "given": {"players": {"1": {"hand": [9], "hand_sum": 9, "hand_size": 1},
                         "2": {"hand": [10, 5], "hand_sum": 15, "hand_size": 2},
                         "3": {"hand": [10, 6], "hand_sum": 16, "hand_size": 2}}},
   "rules": [{"seat": 1, "options_include": "NONE"},
             {"seat": 1, "options_include": "BLIND"},
             {"seat": 2, "options_include": "BLIND"},
             {"seat": 3, "options_include": "BLIND"}],
   "expect": {"offered": [{"seat": 1, "option": "NONE"}],
              "not_offered": [{"seat": 1, "option": "CALL"}],
              "players": {"1": {"hand_size": 2, "total": 0}, "2": {"hand_size": 2, "total": 0}, "3": {"hand_size": 2, "total": 0}}}},

  {"name": "R8: an illegal first choice becomes discarding the single highest card", "rule": "R8", "players": 3, "seed": 9, "default": "first",
   "given": {"players": {"1": {"hand": [10, 3, 2], "hand_sum": 15, "hand_size": 3},
                         "2": {"hand": [6, 5], "hand_sum": 11, "hand_size": 2},
                         "3": {"hand": [9, 4], "hand_sum": 13, "hand_size": 2}},
             "game": {"round": 40}},
   "rules": [{"seat": 1, "options_include": "seat 2: value 6"},
             {"seat": 2, "options_include": "seat 3: value 9"},
             {"seat": 3, "options_include": "seat 1: value 10"}],
   "expect": {"winner": 1,
              "standings": {"1": 0, "2": -14, "3": -14},
              "players": {"1": {"total": 0, "hand_size": 3}, "2": {"total": 14, "hand_size": 2}, "3": {"total": 14, "hand_size": 2}}}},

  {"name": "R9: a call cancels discards and the showdown scores the hands as they stood", "rule": "R9", "players": 3, "seed": 10, "rounds": 1, "default": "first",
   "given": {"players": {"1": {"hand": [2, 3], "hand_sum": 5, "hand_size": 2},
                         "2": {"hand": [9, 10], "hand_sum": 19, "hand_size": 2},
                         "3": {"hand": [10, 10, 8], "hand_sum": 28, "hand_size": 3}}},
   "judge": {"This player's first choice is legal": true},
   "rules": [{"seat": 1, "options_include": "CALL"}],
   "expect": {"players": {"1": {"round_score": 0, "total": 0}, "2": {"round_score": 19, "total": 19}, "3": {"round_score": 28, "total": 28}}}},

  {"name": "R10: a caller strictly lowest scores 0", "rule": "R10", "players": 3, "seed": 11, "rounds": 1, "default": "first",
   "given": {"players": {"1": {"hand": [1, 2], "hand_sum": 3, "hand_size": 2},
                         "2": {"hand": [5, 5], "hand_sum": 10, "hand_size": 2},
                         "3": {"hand": [10, 10], "hand_sum": 20, "hand_size": 2}}},
   "judge": {"This player's first choice is legal": true},
   "rules": [{"seat": 1, "options_include": "CALL"}],
   "expect": {"players": {"1": {"round_score": 0, "total": 0}, "2": {"round_score": 10, "total": 10}, "3": {"round_score": 20, "total": 20}},
              "game": {"round": 2}}},

  {"name": "R11: two callers tied at 6 are both caught and score 36", "rule": "R11", "players": 3, "seed": 12, "rounds": 1, "default": "first",
   "given": {"players": {"1": {"hand": [3, 3], "hand_sum": 6, "hand_size": 2},
                         "2": {"hand": [6], "hand_sum": 6, "hand_size": 1},
                         "3": {"hand": [10, 10], "hand_sum": 20, "hand_size": 2}}},
   "judge": {"This player's first choice is legal": true},
   "rules": [{"seat": 1, "options_include": "CALL"}, {"seat": 2, "options_include": "CALL"}],
   "expect": {"players": {"1": {"round_score": 36, "total": 36}, "2": {"round_score": 36, "total": 36}, "3": {"round_score": 20, "total": 20}}}},

  {"name": "R12: non-callers above the lowest sum score their hand_sum", "rule": "R12", "players": 3, "seed": 13, "rounds": 1, "default": "first",
   "given": {"players": {"1": {"hand": [1, 1], "hand_sum": 2, "hand_size": 2, "total": 10},
                         "2": {"hand": [10, 6], "hand_sum": 16, "hand_size": 2, "total": 10},
                         "3": {"hand": [8, 8], "hand_sum": 16, "hand_size": 2, "total": 10}}},
   "judge": {"This player's first choice is legal": true},
   "rules": [{"seat": 1, "options_include": "CALL"}],
   "expect": {"players": {"1": {"round_score": 0, "total": 10}, "2": {"round_score": 16, "total": 26}, "3": {"round_score": 16, "total": 26}}}},

  {"name": "R13: after a showdown below 150 everyone gets a fresh 5-card hand", "rule": "R13", "players": 3, "seed": 14, "rounds": 1, "default": "first",
   "given": {"players": {"1": {"hand": [1, 2], "hand_sum": 3, "hand_size": 2},
                         "2": {"hand": [10, 10, 10], "hand_sum": 30, "hand_size": 3},
                         "3": {"hand": [9], "hand_sum": 9, "hand_size": 1}}},
   "judge": {"This player's first choice is legal": true},
   "rules": [{"seat": 1, "options_include": "CALL"}],
   "expect": {"players": {"1": {"round_score": 0, "total": 0, "hand_size": 5}, "2": {"round_score": 30, "total": 30, "hand_size": 5}, "3": {"round_score": 9, "total": 9, "hand_size": 5}},
              "game": {"round": 2}}},

  {"name": "R14: discarded cards leave play and do not count at the final showdown", "rule": "R14", "players": 3, "seed": 15, "default": "first",
   "given": {"players": {"1": {"hand": [10, 2], "hand_sum": 12, "hand_size": 2},
                         "2": {"hand": [10, 3], "hand_sum": 13, "hand_size": 2},
                         "3": {"hand": [10, 4], "hand_sum": 14, "hand_size": 2}},
             "game": {"round": 40}},
   "rules": [{"seat": 1, "options_include": "seat 2: value 10"},
             {"seat": 2, "options_include": "seat 3: value 10"},
             {"seat": 3, "options_include": "seat 1: value 10"}],
   "expect": {"winner": 1,
              "standings": {"1": 0, "2": -13, "3": -14},
              "players": {"1": {"total": 0, "hand_size": 2}, "2": {"total": 13, "hand_size": 2}, "3": {"total": 14, "hand_size": 2}}}},

  {"name": "R15: a single-card discard makes one offer that another seat can claim", "rule": "R15", "players": 3, "seed": 16, "rounds": 1, "default": "first",
   "given": {"players": {"1": {"hand": [10, 4], "hand_sum": 14, "hand_size": 2},
                         "2": {"hand": [9, 3], "hand_sum": 12, "hand_size": 2},
                         "3": {"hand": [8, 2], "hand_sum": 10, "hand_size": 2}}},
   "rules": [{"seat": 1, "options_include": "seat 2: value 9"},
             {"seat": 2, "options_include": "seat 1: value 10"},
             {"seat": 3, "options_include": "BLIND"}],
   "expect": {"offered": [{"seat": 2, "option": "seat 1: value 10"}, {"seat": 3, "option": "seat 2: value 9"}],
              "players": {"1": {"hand_size": 2}, "2": {"hand_size": 2}, "3": {"hand_size": 2}}}},

  {"name": "R16: a seat is not offered its own discard (hand sizes only, blind value is random)", "rule": "R16", "players": 3, "seed": 17, "rounds": 1, "default": "first",
   "given": {"players": {"1": {"hand": [10, 10, 5], "hand_sum": 25, "hand_size": 3},
                         "2": {"hand": [9, 2], "hand_sum": 11, "hand_size": 2},
                         "3": {"hand": [8, 1], "hand_sum": 9, "hand_size": 2}}},
   "rules": [{"seat": 1, "options_include": "BLIND"},
             {"seat": 2, "options_include": "BLIND"},
             {"seat": 3, "options_include": "BLIND"}],
   "expect": {"offered": [{"seat": 1, "option": "BLIND"}, {"seat": 2, "option": "seat 1: value 10"}],
              "not_offered": [{"seat": 1, "option": "seat 1: value 10"}, {"seat": 2, "option": "seat 2: value 9"}, {"seat": 3, "option": "seat 3: value 8"}],
              "players": {"1": {"hand_size": 3}, "2": {"hand_size": 2}, "3": {"hand_size": 2}}}},

  {"name": "R17: two seats claiming the same card both go BLIND (only chance-proof values asserted)", "rule": "R17", "players": 3, "seed": 18, "default": "first",
   "given": {"players": {"1": {"hand": [10, 1], "hand_sum": 11, "hand_size": 2},
                         "2": {"hand": [9, 9, 9], "hand_sum": 27, "hand_size": 3},
                         "3": {"hand": [8, 8, 8], "hand_sum": 24, "hand_size": 3}},
             "game": {"round": 40}},
   "rules": [{"seat": 1, "options_include": "seat 2: value 9"},
             {"seat": 2, "options_include": "seat 1: value 10"},
             {"seat": 3, "options_include": "seat 1: value 10"}],
   "expect": {"winner": 1,
              "players": {"1": {"total": 0, "round_score": 0, "hand_size": 2}, "2": {"hand_size": 3}, "3": {"hand_size": 3}}}},

  {"name": "R18: a sole claimant adds the offered card to their hand", "rule": "R18", "players": 3, "seed": 19, "default": "first",
   "given": {"players": {"1": {"hand": [10, 0], "hand_sum": 10, "hand_size": 2},
                         "2": {"hand": [5, 5], "hand_sum": 10, "hand_size": 2},
                         "3": {"hand": [9, 3], "hand_sum": 12, "hand_size": 2}},
             "game": {"round": 40}},
   "rules": [{"seat": 1, "options_include": "seat 2: value 5"},
             {"seat": 2, "options_include": "seat 3: value 9"},
             {"seat": 3, "options_include": "seat 1: value 10"}],
   "expect": {"winner": 1,
              "standings": {"1": 0, "2": -14, "3": -13},
              "players": {"1": {"total": 0, "hand_size": 2}, "2": {"total": 14, "hand_size": 2}, "3": {"total": 13, "hand_size": 2}}}},

  {"name": "R19: each BLIND seat adds one card (blind value is random, sizes only)", "rule": "R19", "players": 3, "seed": 20, "rounds": 1, "default": "first",
   "given": {"players": {"1": {"hand": [10, 4], "hand_sum": 14, "hand_size": 2},
                         "2": {"hand": [9], "hand_sum": 9, "hand_size": 1},
                         "3": {"hand": [10, 10, 10], "hand_sum": 30, "hand_size": 3}}},
   "rules": [{"seat": 1, "options_include": "BLIND"},
             {"seat": 2, "options_include": "BLIND"},
             {"seat": 3, "options_include": "BLIND"}],
   "expect": {"offered": [{"seat": 1, "option": "BLIND"}, {"seat": 2, "option": "BLIND"}, {"seat": 3, "option": "BLIND"}],
              "players": {"1": {"hand_size": 2, "total": 0}, "2": {"hand_size": 2, "total": 0}, "3": {"hand_size": 3, "total": 0}}}},

  {"name": "R20: a claim round completes with the round advanced and no score change", "rule": "R20", "players": 3, "seed": 21, "rounds": 1, "default": "first",
   "given": {"players": {"1": {"hand": [10, 4], "hand_sum": 14, "hand_size": 2},
                         "2": {"hand": [9, 3], "hand_sum": 12, "hand_size": 2},
                         "3": {"hand": [8, 2], "hand_sum": 10, "hand_size": 2}},
             "game": {"round": 5}},
   "rules": [{"seat": 1, "options_include": "seat 3: value 8"},
             {"seat": 2, "options_include": "seat 1: value 10"},
             {"seat": 3, "options_include": "seat 2: value 9"}],
   "expect": {"players": {"1": {"hand_size": 2, "total": 0}, "2": {"hand_size": 2, "total": 0}, "3": {"hand_size": 2, "total": 0}},
              "game": {"round": 6}}},

  {"name": "R21: round 40 without a call ends with a final showdown, lowest scores 0", "rule": "R21", "players": 3, "seed": 22, "default": "first",
   "given": {"players": {"1": {"hand": [10, 1, 1], "hand_sum": 12, "hand_size": 3},
                         "2": {"hand": [9, 2], "hand_sum": 11, "hand_size": 2},
                         "3": {"hand": [8, 8, 8], "hand_sum": 24, "hand_size": 3}},
             "game": {"round": 40}},
   "rules": [{"seat": 1, "options_include": "seat 3: value 8"},
             {"seat": 2, "options_include": "seat 1: value 10"},
             {"seat": 3, "options_include": "seat 2: value 9"}],
   "expect": {"winner": 1,
              "standings": {"1": 0, "2": -12, "3": -25},
              "players": {"1": {"round_score": 0, "total": 0, "hand_size": 3}, "2": {"round_score": 12, "total": 12, "hand_size": 2}, "3": {"round_score": 25, "total": 25, "hand_size": 3}}}},

  {"name": "R22: a showdown pushing a total to 150 or more ends the game", "rule": "R22", "players": 3, "seed": 23, "default": "first",
   "given": {"players": {"1": {"hand": [1, 1], "hand_sum": 2, "hand_size": 2, "total": 0},
                         "2": {"hand": [10, 10], "hand_sum": 20, "hand_size": 2, "total": 140},
                         "3": {"hand": [9, 9], "hand_sum": 18, "hand_size": 2, "total": 50}}},
   "judge": {"This player's first choice is legal": true},
   "rules": [{"seat": 1, "options_include": "CALL"}],
   "expect": {"winner": 1,
              "standings": {"1": 0, "2": -160, "3": -68},
              "players": {"1": {"total": 0}, "2": {"total": 160}, "3": {"total": 68}}}},

  {"name": "R23: seats tied at the lowest total share the win", "rule": "R23", "players": 3, "seed": 24, "default": "first",
   "given": {"players": {"1": {"hand": [1, 1], "hand_sum": 2, "hand_size": 2, "total": 10},
                         "2": {"hand": [10, 10], "hand_sum": 20, "hand_size": 2, "total": 145},
                         "3": {"hand": [5, 5], "hand_sum": 10, "hand_size": 2, "total": 0}}},
   "judge": {"This player's first choice is legal": true},
   "rules": [{"seat": 1, "options_include": "CALL"}],
   "expect": {"winner": [1, 3],
              "standings": {"1": -10, "2": -165, "3": -10},
              "players": {"1": {"total": 10}, "2": {"total": 165}, "3": {"total": 10}}}}
]
```
````
