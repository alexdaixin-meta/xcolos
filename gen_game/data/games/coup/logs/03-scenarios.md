# 03 scenarios

- time: 2026-10-09T20:57:29+00:00 (166.5s)  model: 
- system prompt: [system/94d67838-scenarios.md](system/94d67838-scenarios.md) (sha256 94d67838c22d97b9)
- sent sha256 e195c4f076f871bd, reply sha256 2615f87df695d0db

## Sent

````
SPEC:
{
  "name": "Coup (XColos)",
  "summary": "Each player holds two hidden role cards. On your turn you take an action, and some actions require claiming a role you may not hold. Other players can challenge or block. Lose both cards and you are out; the last player holding a hidden card wins.",
  "players": {
    "min": 3,
    "max": 5
  },
  "parameters": {
    "deck_size": 15,
    "copies_per_role": 3,
    "hand_size": 2,
    "first_player_start_coins": 1,
    "other_player_start_coins": 2,
    "forced_coup_threshold": 10,
    "income_gain": 1,
    "foreign_aid_gain": 2,
    "coup_cost": 7,
    "tax_gain": 3,
    "assassinate_cost": 3,
    "steal_amount": 2,
    "exchange_draw": 1,
    "exchange_return": 1,
    "loss_per_hit": 1,
    "turn_cap": 40
  },
  "attributes": {
    "player": [
      {
        "key": "coins",
        "type": "number",
        "visible": "public",
        "initial": 2,
        "meaning": "Coins held. Seat 1 starts with 1 and every other seat with 2. Set to 0 when the player is eliminated.",
        "observable": true
      },
      {
        "key": "hidden_cards",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "The player's face-down role cards. Only the owner sees them. A challenge is checked against this list.",
        "observable": false
      },
      {
        "key": "revealed_cards",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Face-up role cards the player has lost. They are public and stay revealed.",
        "observable": true
      },
      {
        "key": "hidden_count",
        "type": "number",
        "visible": "public",
        "initial": 2,
        "meaning": "How many hidden cards the player holds. Always equals the length of hidden_cards outside an Exchange. 0 means eliminated.",
        "observable": true
      },
      {
        "key": "alive",
        "type": "bool",
        "visible": "public",
        "initial": true,
        "meaning": "False once the player has no hidden cards left.",
        "observable": true
      },
      {
        "key": "pending_loss",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Influence the player must lose in this turn's resolve step. Reset to 0 at the end of every turn.",
        "observable": false
      },
      {
        "key": "must_return",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "1 when the player owes the deck one hidden card from an Exchange this turn, otherwise 0.",
        "observable": false
      },
      {
        "key": "reaction",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "This turn's answer to the action: pass, challenge, block_duke, block_contessa, block_captain or block_ambassador. All reactions are announced.",
        "observable": false
      },
      {
        "key": "block_response",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "This turn's answer to a block: accept or challenge. Announced.",
        "observable": false
      },
      {
        "key": "reveal_choice",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "The hidden card the player chose to reveal when losing one of two cards.",
        "observable": false
      },
      {
        "key": "return_choice",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "The hidden card the player chose to put back in the deck after an Exchange. Never announced.",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": [
          "Duke",
          "Duke",
          "Duke",
          "Assassin",
          "Assassin",
          "Assassin",
          "Captain",
          "Captain",
          "Captain",
          "Ambassador",
          "Ambassador",
          "Ambassador",
          "Contessa",
          "Contessa",
          "Contessa"
        ],
        "meaning": "The face-down deck. Drawing takes a random card from it, so it is always shuffled.",
        "observable": false
      },
      {
        "key": "deck_count",
        "type": "number",
        "visible": "public",
        "initial": 15,
        "meaning": "Number of cards in the deck. Announced every turn.",
        "observable": false
      },
      {
        "key": "turn_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Turns played so far.",
        "observable": true
      },
      {
        "key": "active_seat",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Seat of the player taking the current turn.",
        "observable": false
      },
      {
        "key": "action",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "This turn's action: income, foreign_aid, coup, tax, assassinate, steal or exchange.",
        "observable": false
      },
      {
        "key": "claimed_role",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The role the action claims (Duke for tax, Assassin for assassinate, Captain for steal, Ambassador for exchange), or empty if it claims none.",
        "observable": false
      },
      {
        "key": "target",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat targeted by coup, assassinate or steal. 0 if the action has no target.",
        "observable": false
      },
      {
        "key": "action_status",
        "type": "text",
        "visible": "public",
        "initial": "going",
        "meaning": "going, failed (the action challenge succeeded) or blocked.",
        "observable": false
      },
      {
        "key": "challenger",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The first seat after the active player that challenged the action. 0 if nobody did.",
        "observable": false
      },
      {
        "key": "blocker",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The first seat after the active player that blocked. 0 if nobody did.",
        "observable": false
      },
      {
        "key": "block_role",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The role the counting blocker claims.",
        "observable": false
      },
      {
        "key": "block_challenger",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The first seat after the blocker that challenged the block. 0 if nobody did.",
        "observable": false
      },
      {
        "key": "stolen",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "Coins moved by this turn's Steal: the smaller of 2 and the target's coins.",
        "observable": false
      },
      {
        "key": "living_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of players with at least one hidden card.",
        "observable": false
      },
      {
        "key": "winner",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The result once the game ends: 'seat N' or 'draw'.",
        "observable": true
      }
    ]
  },
  "setup": [
    "The deck holds 15 cards: 3 each of Duke, Assassin, Captain, Ambassador and Contessa.",
    "Each player draws 2 cards at random from deck into hidden_cards, so deck_count becomes 15 - 2 x player count and every hidden_count becomes 2.",
    "Seat 1 gets coins = 1 and every other seat gets coins = 2.",
    "living_count is set to the player count, turn_count to 0 and active_seat to 1.",
    "Each player is sent their own hidden_cards."
  ],
  "round": [
    {
      "action": "update",
      "who": "engine",
      "answer": null,
      "effect": "Start of turn: action_status = going; challenger = blocker = block_challenger = target = stolen = 0; action, claimed_role, block_role and every player's reaction, block_response, reveal_choice and return_choice are cleared; turn_count += 1."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce each player's coins, revealed_cards and hidden_count, plus deck_count and active_seat."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Send each player their own hidden_cards."
    },
    {
      "action": "ask",
      "who": "the player at active_seat",
      "answer": "One choice of action: income, foreign_aid, coup (only if coins >= 7), tax, assassinate (only if coins >= 3), steal or exchange. If coins >= 10 at the start of the turn, the only option is coup.",
      "effect": "action = the answer; claimed_role = Duke for tax, Assassin for assassinate, Captain for steal, Ambassador for exchange, empty otherwise."
    },
    {
      "action": "ask",
      "who": "the player at active_seat, when action is coup, assassinate or steal",
      "answer": "The seat of any other player with alive = true.",
      "effect": "target = the chosen seat."
    },
    {
      "action": "update",
      "who": "engine",
      "answer": null,
      "effect": "Pay costs now, with no refund later: if action = coup, active coins -= 7; if action = assassinate, active coins -= 3."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce the active seat's action, claimed_role and target."
    },
    {
      "action": "poll",
      "who": "every living player except the active player, when action is foreign_aid, tax, assassinate, steal or exchange",
      "answer": "pass; challenge (only if claimed_role is set); block_duke (anyone, only against foreign_aid); block_contessa (only the target, only against assassinate); block_captain or block_ambassador (only the target, only against steal).",
      "effect": "Each answering player's reaction = the answer."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce every player's reaction."
    },
    {
      "action": "update",
      "who": "engine",
      "answer": null,
      "effect": "challenger = the first seat in seat order after active_seat with reaction = challenge, 0 if none. blocker = the first seat after active_seat whose reaction starts with block_, 0 if none. block_role = that block's role."
    },
    {
      "action": "update",
      "who": "engine, when challenger > 0",
      "answer": null,
      "effect": "Action challenge. If claimed_role is in the active player's hidden_cards: remove one claimed_role card from the active player's hidden_cards and append it to deck, then draw one card at random from deck into the active player's hidden_cards; challenger's pending_loss += 1. Otherwise: active player's pending_loss += 1, action_status = failed, blocker = 0."
    },
    {
      "action": "tell",
      "who": "all players, when challenger > 0",
      "answer": null,
      "effect": "Announce whether the challenged claim was true and who takes the pending loss. The card the active player draws is not named."
    },
    {
      "action": "poll",
      "who": "every living player except the blocker, when action_status = going and blocker > 0",
      "answer": "accept or challenge",
      "effect": "Each answering player's block_response = the answer."
    },
    {
      "action": "tell",
      "who": "all players, when action_status = going and blocker > 0",
      "answer": null,
      "effect": "Announce every player's block_response."
    },
    {
      "action": "update",
      "who": "engine, when action_status = going and blocker > 0",
      "answer": null,
      "effect": "block_challenger = the first seat in seat order after blocker with block_response = challenge, 0 if none. If block_challenger = 0: action_status = blocked. Otherwise, if block_role is in the blocker's hidden_cards: move that card from the blocker's hidden_cards to deck, draw one card at random from deck into the blocker's hidden_cards, block_challenger's pending_loss += 1, action_status = blocked. Otherwise: blocker's pending_loss += 1 and the action goes ahead (action_status stays going)."
    },
    {
      "action": "update",
      "who": "engine, when action_status = going",
      "answer": null,
      "effect": "Effect. income: active coins += 1. foreign_aid: active coins += 2. tax: active coins += 3. steal: stolen = the smaller of 2 and the target's coins, target coins -= stolen, active coins += stolen. coup or assassinate: target pending_loss += 1. exchange: draw one card at random from deck into the active player's hidden_cards and set the active player's must_return = 1."
    },
    {
      "action": "poll",
      "who": "every player with (pending_loss = 1 and hidden_count = 2) or must_return = 1",
      "answer": "One card from the player's own hidden_cards. A player who both loses a card and owes an Exchange return answers twice: the card to reveal and the card to return.",
      "effect": "reveal_choice = the card to reveal; return_choice = the card to return to the deck."
    },
    {
      "action": "update",
      "who": "engine",
      "answer": null,
      "effect": "Resolve. A player with pending_loss = 1 and hidden_count = 2 moves reveal_choice from hidden_cards to revealed_cards. A player with must_return = 1 moves return_choice from hidden_cards to deck. Any player with pending_loss >= hidden_count and pending_loss > 0 moves all of hidden_cards to revealed_cards, alive = false, coins = 0. Then hidden_count = length of hidden_cards for every player, deck_count = length of deck, living_count = number of players with alive = true. Every pending_loss and must_return goes back to 0."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce every card revealed this turn and every player eliminated. Returned cards are never named."
    },
    {
      "action": "check",
      "who": "engine",
      "answer": null,
      "effect": "End the game if living_count = 1 or turn_count >= 40, otherwise continue."
    },
    {
      "action": "update",
      "who": "engine",
      "answer": null,
      "effect": "active_seat = the next seat after active_seat in seat order, wrapping around and skipping players with alive = false."
    }
  ],
  "ending": {
    "condition": "living_count = 1 or turn_count >= 40",
    "results": [
      "seat 1",
      "seat 2",
      "seat 3",
      "seat 4",
      "seat 5",
      "draw"
    ],
    "decided_by": "If living_count = 1, the result is the seat with hidden_count >= 1. Otherwise, after 40 turns, the result is the seat with the highest hidden_count; if several tie, the tied seat with the most coins; if they are still tied, draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game is set up, the deck has 15 cards (3 each of Duke, Assassin, Captain, Ambassador, Contessa), each player has hidden_count = 2, and deck_count = 15 - 2 x player count."
    },
    {
      "id": "R2",
      "text": "When the game is set up, seat 1 has coins = 1 and every other seat has coins = 2."
    },
    {
      "id": "R3",
      "text": "When a player takes Income unchallenged and unblocked, then their coins rise by exactly 1, and no player is offered a challenge or block."
    },
    {
      "id": "R4",
      "text": "When a player takes Foreign Aid and nobody blocks, then their coins rise by 2."
    },
    {
      "id": "R5",
      "text": "When a player takes Foreign Aid and another player blocks as Duke and nobody challenges the block, then the active player's coins do not change."
    },
    {
      "id": "R6",
      "text": "When a player takes Foreign Aid, then challenge is not offered against the action."
    },
    {
      "id": "R7",
      "text": "When a player with 7 or more coins takes Coup on a target, then their coins fall by 7 and the target loses 1 hidden card; nobody may challenge or block."
    },
    {
      "id": "R8",
      "text": "When a player has fewer than 7 coins, then Coup is not among their options."
    },
    {
      "id": "R9",
      "text": "When a player starts their turn with 10 or more coins, then Coup is their only option."
    },
    {
      "id": "R10",
      "text": "When a player takes Tax and nobody challenges, then their coins rise by 3."
    },
    {
      "id": "R11",
      "text": "When a player with 3 or more coins takes Assassinate, then their coins fall by 3 at once, even if the action is later blocked or fails a challenge."
    },
    {
      "id": "R12",
      "text": "When a player has fewer than 3 coins, then Assassinate is not among their options."
    },
    {
      "id": "R13",
      "text": "When Assassinate goes ahead unblocked, then the target loses 1 hidden card."
    },
    {
      "id": "R14",
      "text": "When the target of Assassinate blocks as Contessa and nobody challenges the block, then the target loses no card and the assassin's 3 coins are not refunded."
    },
    {
      "id": "R15",
      "text": "When a player Steals from a target with 2 or more coins and the action goes ahead, then the target's coins fall by 2 and the active player's coins rise by 2."
    },
    {
      "id": "R16",
      "text": "When a player Steals from a target with 1 coin and the action goes ahead, then the target ends with 0 coins and the active player gains 1; with 0 coins, nobody's coins change."
    },
    {
      "id": "R17",
      "text": "When the target of a Steal blocks as Captain or as Ambassador and nobody challenges the block, then no coins move."
    },
    {
      "id": "R18",
      "text": "When a player other than the target answers a Steal or Assassinate, then they are not offered block_contessa, block_captain or block_ambassador."
    },
    {
      "id": "R19",
      "text": "When a player takes Exchange and the action goes ahead, then they draw 1 card from the deck and return 1 hidden card of their choice, ending with the same hidden_count and the same deck_count."
    },
    {
      "id": "R20",
      "text": "When an Exchange returns a card, then the returned card is never announced."
    },
    {
      "id": "R21",
      "text": "When a challenged active player holds the claimed role, then that card goes into the deck, they draw a replacement (keeping hidden_count), the first challenger in seat order after them loses 1 hidden card, and the action continues."
    },
    {
      "id": "R22",
      "text": "When a challenged active player does not hold the claimed role, then they lose 1 hidden card, the action has no effect, and any block is ignored."
    },
    {
      "id": "R23",
      "text": "When several players challenge the action, then only the first challenger in seat order after the active player can lose a card from it."
    },
    {
      "id": "R24",
      "text": "When several players block, then only the first blocker in seat order after the active player counts."
    },
    {
      "id": "R25",
      "text": "When a challenged blocker holds the blocking role, then that card goes into the deck, they draw a replacement, the first block challenger in seat order after the blocker loses 1 hidden card, and the action is blocked."
    },
    {
      "id": "R26",
      "text": "When a challenged blocker does not hold the blocking role, then the blocker loses 1 hidden card and the action goes ahead."
    },
    {
      "id": "R27",
      "text": "When the Assassinate target's Contessa block is challenged and they do not hold Contessa, then the target gets 2 pending losses and, holding 2 hidden cards, is eliminated."
    },
    {
      "id": "R28",
      "text": "When a player with 2 hidden cards gets exactly 1 pending loss, then they reveal the one card they choose and keep the other hidden."
    },
    {
      "id": "R29",
      "text": "When a player's pending losses are equal to or more than their hidden cards, then all their hidden cards are revealed, alive becomes false, and their coins become 0."
    },
    {
      "id": "R30",
      "text": "When a card is revealed, then it moves to revealed_cards, stays public, and never returns to the hand."
    },
    {
      "id": "R31",
      "text": "When a turn ends, then every pending_loss is 0."
    },
    {
      "id": "R32",
      "text": "When a turn ends and the game goes on, then the next turn belongs to the next seat with alive = true, skipping eliminated seats."
    },
    {
      "id": "R33",
      "text": "When a target is chosen, then it must be another player with alive = true."
    },
    {
      "id": "R34",
      "text": "When only one player has hidden_count >= 1, then the game ends and that seat wins."
    },
    {
      "id": "R35",
      "text": "When 40 turns have been played and more than one player is alive, then the seat with the most hidden cards wins; a tie goes to the most coins; a remaining tie is a draw."
    },
    {
      "id": "R36",
      "text": "When players react to an action or a block, then they answer in a poll, and no one sees another's answer until all are in."
    }
  ],
  "choices": [
    {
      "what": "3 to 5 players",
      "why": "Bluffing needs at least 3 players: a claim faces more than one possible challenger, and Foreign Aid can be blocked by a third party. With 2, every claim is a one-on-one guess. 5 is the maximum because a 15-card deck dealt 2 each leaves 5 cards for draws and exchanges; with more players the deck thins out and the counting gets too long to follow. This matches the source."
    },
    {
      "what": "The strategy is what makes it a game",
      "why": "A thoughtful player tracks the revealed cards and past claims to judge whether a claim is likely true (3 copies per role), bluffs roles that are still plausible, saves the forced Coup for the strongest rival, and challenges only when being wrong costs less than letting the action through."
    },
    {
      "what": "No talk step",
      "why": "The source says there is no free discussion. Claims, challenges and blocks are the only communication."
    },
    {
      "what": "Action choice by ask, reactions and block responses by poll",
      "why": "The active player acts alone. The source says reactions and block responses are made at the same moment without seeing each other, so they use poll."
    },
    {
      "what": "Card choice by poll",
      "why": "The source says reveal and return choices are made at the same moment."
    },
    {
      "what": "Each player is offered only the reactions they may legally make",
      "why": "The source limits Challenge to claimed roles, Duke blocks to Foreign Aid, and Contessa, Captain and Ambassador blocks to the target. Offering only legal options enforces this."
    },
    {
      "what": "A turn is one round",
      "why": "Seat order with skipping is kept by active_seat, so the turn cap of 40 counts directly as turn_count."
    },
    {
      "what": "A player who both loses a card and owes an Exchange return answers both in the card-choice poll",
      "why": "The source does not say how the two choices combine. In practice this is rare, because the active player in an Exchange only takes a pending loss when the Exchange failed."
    }
  ],
  "simplifications": [
    {
      "what": "'Top card of the deck' is a random draw from the deck list, and 'shuffle the deck' is dropped",
      "why": "The deck is hidden and drawing is random, so every draw is the same as taking the top of a freshly shuffled deck. The source's reshuffle is already implied."
    },
    {
      "what": "The many branches of a turn (challenge, block, block challenge, effect) are written as flat steps, each with an arithmetic `when` condition on action_status, challenger and blocker",
      "why": "The engine has no block-of-steps branching, but each branch here is a single update or poll, so per-step conditions express the rules exactly."
    },
    {
      "what": "The 40-turn tiebreak (most hidden cards, then most coins, then draw) is computed from hidden_count and coins with arithmetic",
      "why": "The engine's arithmetic ranking is a workaround that needs calc. The outcome stays decided by counting, as the source requires."
    },
    {
      "what": "Card-choice options come from the player's own hidden_cards list",
      "why": "Taking options from a list is the engine's workaround for choosing from a hand."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: coins, revealed_cards, hidden_count, alive; table: turn_count, winner.
````

## Reply

````
```json
[
  {"name": "Setup: every seat holds 2 hidden cards, nothing revealed, all alive (3 players)", "rule": "R1", "players": 3, "seed": 1, "default": "decline", "rounds": 1,
   "rules": [{"seat": 1, "options_include": "income"}],
   "expect": {"players": {"1": {"hidden_count": 2, "revealed_cards": [], "alive": true},
                          "2": {"hidden_count": 2, "revealed_cards": [], "alive": true},
                          "3": {"hidden_count": 2, "revealed_cards": [], "alive": true}}}},
  {"name": "Setup: every seat holds 2 hidden cards, nothing revealed, all alive (5 players)", "rule": "R1", "players": 5, "seed": 2, "default": "decline", "rounds": 1,
   "rules": [{"seat": 1, "options_include": "income"}],
   "expect": {"players": {"1": {"hidden_count": 2, "revealed_cards": []}, "2": {"hidden_count": 2, "revealed_cards": []},
                          "3": {"hidden_count": 2, "revealed_cards": []}, "4": {"hidden_count": 2, "revealed_cards": []},
                          "5": {"hidden_count": 2, "revealed_cards": []}}}},
  {"name": "Setup: seat 1 starts with 1 coin, the others with 2 (seat 1 then takes Income)", "rule": "R2", "players": 4, "seed": 1, "default": "decline", "rounds": 1,
   "rules": [{"seat": 1, "options_include": "income"}],
   "expect": {"players": {"1": {"coins": 2}, "2": {"coins": 2}, "3": {"coins": 2}, "4": {"coins": 2}}}},
  {"name": "Income gives exactly 1 coin and nobody loses a card", "rule": "R3", "players": 3, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"players": {"1": {"coins": 3}, "2": {"coins": 2}, "3": {"coins": 2}}, "game": {"active_seat": 1}},
   "rules": [{"seat": 1, "options_include": "income"},
             {"seat": 2, "options_include": "challenge"}, {"seat": 3, "options_include": "block_duke"}],
   "expect": {"players": {"1": {"coins": 4, "hidden_count": 2}, "2": {"coins": 2, "hidden_count": 2}, "3": {"coins": 2, "hidden_count": 2}}}},
  {"name": "Foreign Aid with nobody blocking gives 2 coins", "rule": "R4", "players": 3, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"players": {"1": {"coins": 2}}, "game": {"active_seat": 1}},
   "rules": [{"seat": 1, "options_include": "foreign_aid"}],
   "expect": {"players": {"1": {"coins": 4, "hidden_count": 2}}}},
  {"name": "Foreign Aid blocked as Duke, block accepted: no coins gained", "rule": "R5", "players": 3, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"players": {"1": {"coins": 2}, "2": {"hidden_cards": ["Captain", "Contessa"], "hidden_count": 2}}, "game": {"active_seat": 1}},
   "rules": [{"seat": 1, "options_include": "foreign_aid"}, {"seat": 2, "options_include": "block_duke"}],
   "expect": {"players": {"1": {"coins": 2, "hidden_count": 2}, "2": {"hidden_count": 2}, "3": {"hidden_count": 2}}}},
  {"name": "Foreign Aid cannot be challenged: would-be challengers pass and the aid goes through", "rule": "R6", "players": 3, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"players": {"1": {"coins": 2}}, "game": {"active_seat": 1}},
   "rules": [{"seat": 1, "options_include": "foreign_aid"},
             {"seat": 2, "options_include": "challenge"}, {"seat": 3, "options_include": "challenge"}],
   "expect": {"players": {"1": {"coins": 4, "hidden_count": 2, "revealed_cards": []}, "2": {"hidden_count": 2}, "3": {"hidden_count": 2}}}},
  {"name": "Coup costs 7 and the target loses one card", "rule": "R7", "players": 3, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"players": {"1": {"coins": 7}, "2": {"coins": 2, "hidden_cards": ["Duke", "Captain"], "hidden_count": 2}}, "game": {"active_seat": 1}},
   "rules": [{"seat": 1, "options_include": "coup"}, {"seat": 1, "options_include": 2},
             {"seat": 2, "options_include": "Duke"}, {"seat": 3, "options_include": "challenge"}],
   "expect": {"players": {"1": {"coins": 0, "hidden_count": 2}, "2": {"coins": 2, "hidden_count": 1, "revealed_cards": ["Duke"], "alive": true}, "3": {"hidden_count": 2}}}},
  {"name": "With 6 coins Coup is not offered, so the seat falls back to Tax", "rule": "R8", "players": 3, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"players": {"1": {"coins": 6}}, "game": {"active_seat": 1}},
   "rules": [{"seat": 1, "options_include": "coup"}, {"seat": 1, "options_include": "tax"}],
   "expect": {"players": {"1": {"coins": 9}, "2": {"hidden_count": 2}, "3": {"hidden_count": 2}}}},
  {"name": "With 10 coins Coup is forced even when the seat asks for Income", "rule": "R9", "players": 3, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"players": {"1": {"coins": 10}, "2": {"hidden_cards": ["Duke", "Captain"], "hidden_count": 2}}, "game": {"active_seat": 1}},
   "rules": [{"seat": 1, "options_include": "income"}, {"seat": 1, "options_include": "coup"}, {"seat": 1, "options_include": 2},
             {"seat": 2, "options_include": "Duke"}],
   "expect": {"players": {"1": {"coins": 3}, "2": {"hidden_count": 1, "revealed_cards": ["Duke"]}}}},
  {"name": "Tax with nobody challenging gives 3 coins", "rule": "R10", "players": 3, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"players": {"1": {"coins": 2}}, "game": {"active_seat": 1}},
   "rules": [{"seat": 1, "options_include": "tax"}],
   "expect": {"players": {"1": {"coins": 5, "hidden_count": 2}}}},
  {"name": "Assassinate's 3 coins are paid even when a challenge makes it fail", "rule": "R11", "players": 3, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"players": {"1": {"coins": 4, "hidden_cards": ["Duke", "Captain"], "hidden_count": 2},
                         "2": {"hidden_cards": ["Contessa", "Ambassador"], "hidden_count": 2}}, "game": {"active_seat": 1}},
   "rules": [{"seat": 1, "options_include": "assassinate"}, {"seat": 1, "options_include": 2}, {"seat": 1, "options_include": "Duke"},
             {"seat": 2, "options_include": "challenge"}],
   "expect": {"players": {"1": {"coins": 1, "hidden_count": 1, "revealed_cards": ["Duke"]}, "2": {"hidden_count": 2, "revealed_cards": []}}}},
  {"name": "With 2 coins Assassinate is not offered, so the seat falls back to Tax", "rule": "R12", "players": 3, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"players": {"1": {"coins": 2}}, "game": {"active_seat": 1}},
   "rules": [{"seat": 1, "options_include": "assassinate"}, {"seat": 1, "options_include": "tax"}],
   "expect": {"players": {"1": {"coins": 5}, "2": {"hidden_count": 2}, "3": {"hidden_count": 2}}}},
  {"name": "Unblocked Assassinate costs 3 and the target loses one card", "rule": "R13", "players": 3, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"players": {"1": {"coins": 3, "hidden_cards": ["Assassin", "Duke"], "hidden_count": 2},
                         "2": {"hidden_cards": ["Captain", "Duke"], "hidden_count": 2}}, "game": {"active_seat": 1}},
   "rules": [{"seat": 1, "options_include": "assassinate"}, {"seat": 1, "options_include": 2}, {"seat": 2, "options_include": "Captain"}],
   "expect": {"players": {"1": {"coins": 0, "hidden_count": 2}, "2": {"hidden_count": 1, "revealed_cards": ["Captain"], "alive": true}}}},
  {"name": "Contessa block accepted: target keeps both cards, assassin gets no refund", "rule": "R14", "players": 3, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"players": {"1": {"coins": 3, "hidden_cards": ["Assassin", "Duke"], "hidden_count": 2},
                         "2": {"hidden_cards": ["Contessa", "Duke"], "hidden_count": 2}}, "game": {"active_seat": 1}},
   "rules": [{"seat": 1, "options_include": "assassinate"}, {"seat": 1, "options_include": 2}, {"seat": 2, "options_include": "block_contessa"}],
   "expect": {"players": {"1": {"coins": 0, "hidden_count": 2}, "2": {"hidden_count": 2, "revealed_cards": []}, "3": {"hidden_count": 2}}}},
  {"name": "Steal from a target with 4 coins moves 2", "rule": "R15", "players": 3, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"players": {"1": {"coins": 1}, "2": {"coins": 4}}, "game": {"active_seat": 1}},
   "rules": [{"seat": 1, "options_include": "steal"}, {"seat": 1, "options_include": 2}],
   "expect": {"players": {"1": {"coins": 3}, "2": {"coins": 2}}}},
  {"name": "Steal from a target with 1 coin moves only 1", "rule": "R16", "players": 3, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"players": {"1": {"coins": 1}, "2": {"coins": 1}}, "game": {"active_seat": 1}},
   "rules": [{"seat": 1, "options_include": "steal"}, {"seat": 1, "options_include": 2}],
   "expect": {"players": {"1": {"coins": 2}, "2": {"coins": 0}}}},
  {"name": "Steal from a target with 0 coins moves nothing", "rule": "R16", "players": 3, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"players": {"1": {"coins": 1}, "2": {"coins": 0}}, "game": {"active_seat": 1}},
   "rules": [{"seat": 1, "options_include": "steal"}, {"seat": 1, "options_include": 2}],
   "expect": {"players": {"1": {"coins": 1}, "2": {"coins": 0, "alive": true}}}},
  {"name": "Steal blocked as Captain, block accepted: no coins move", "rule": "R17", "players": 3, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"players": {"1": {"coins": 1}, "2": {"coins": 4}}, "game": {"active_seat": 1}},
   "rules": [{"seat": 1, "options_include": "steal"}, {"seat": 1, "options_include": 2}, {"seat": 2, "options_include": "block_captain"}],
   "expect": {"players": {"1": {"coins": 1, "hidden_count": 2}, "2": {"coins": 4, "hidden_count": 2}}}},
  {"name": "Steal blocked as Ambassador, block accepted: no coins move", "rule": "R17", "players": 3, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"players": {"1": {"coins": 1}, "2": {"coins": 4}}, "game": {"active_seat": 1}},
   "rules": [{"seat": 1, "options_include": "steal"}, {"seat": 1, "options_include": 2}, {"seat": 2, "options_include": "block_ambassador"}],
   "expect": {"players": {"1": {"coins": 1, "hidden_count": 2}, "2": {"coins": 4, "hidden_count": 2}}}},
  {"name": "A non-target cannot block a Steal: seat 3's block is not offered and the steal goes through", "rule": "R18", "players": 3, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"players": {"1": {"coins": 1}, "2": {"coins": 4}}, "game": {"active_seat": 1}},
   "rules": [{"seat": 1, "options_include": "steal"}, {"seat": 1, "options_include": 2},
             {"seat": 3, "options_include": "block_captain"}, {"seat": 3, "options_include": "block_ambassador"}, {"seat": 3, "options_include": "block_contessa"}],
   "expect": {"players": {"1": {"coins": 3}, "2": {"coins": 2}, "3": {"hidden_count": 2}}}},
  {"name": "A non-target cannot block Assassinate as Contessa: the target still loses a card", "rule": "R18", "players": 3, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"players": {"1": {"coins": 3, "hidden_cards": ["Assassin", "Duke"], "hidden_count": 2},
                         "2": {"hidden_cards": ["Captain", "Duke"], "hidden_count": 2}}, "game": {"active_seat": 1}},
   "rules": [{"seat": 1, "options_include": "assassinate"}, {"seat": 1, "options_include": 2}, {"seat": 2, "options_include": "Captain"},
             {"seat": 3, "options_include": "block_contessa"}],
   "expect": {"players": {"1": {"coins": 0}, "2": {"hidden_count": 1, "revealed_cards": ["Captain"]}, "3": {"hidden_count": 2}}}},
  {"name": "Exchange draws 1 and returns 1: still 2 hidden cards, nothing revealed (which card comes back depends on chance)", "rule": "R19", "players": 3, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"players": {"1": {"coins": 1, "hidden_cards": ["Duke", "Captain"], "hidden_count": 2}}, "game": {"active_seat": 1}},
   "rules": [{"seat": 1, "options_include": "exchange"}],
   "expect": {"players": {"1": {"coins": 1, "hidden_count": 2, "revealed_cards": [], "alive": true}}}},
  {"name": "The card an Exchange returns is not revealed", "rule": "R20", "players": 3, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"players": {"1": {"hidden_cards": ["Duke", "Captain"], "hidden_count": 2}}, "game": {"active_seat": 1}},
   "rules": [{"seat": 1, "options_include": "exchange"}, {"seat": 1, "options_include": "Duke"}],
   "expect": {"players": {"1": {"hidden_count": 2, "revealed_cards": []}, "2": {"revealed_cards": []}, "3": {"revealed_cards": []}}}},
  {"name": "Tax challenged, Duke is held: challenger loses a card, tax still pays 3", "rule": "R21", "players": 3, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"players": {"1": {"coins": 2, "hidden_cards": ["Duke", "Captain"], "hidden_count": 2},
                         "2": {"hidden_cards": ["Captain", "Contessa"], "hidden_count": 2}}, "game": {"active_seat": 1}},
   "rules": [{"seat": 1, "options_include": "tax"}, {"seat": 2, "options_include": "challenge"}, {"seat": 2, "options_include": "Captain"}],
   "expect": {"players": {"1": {"coins": 5, "hidden_count": 2, "revealed_cards": []}, "2": {"hidden_count": 1, "revealed_cards": ["Captain"]}, "3": {"hidden_count": 2}}}},
  {"name": "Tax challenged, bluff (no Duke): bluffer loses a card and gains nothing", "rule": "R22", "players": 3, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"players": {"1": {"coins": 2, "hidden_cards": ["Captain", "Contessa"], "hidden_count": 2},
                         "2": {"hidden_cards": ["Duke", "Assassin"], "hidden_count": 2}}, "game": {"active_seat": 1}},
   "rules": [{"seat": 1, "options_include": "tax"}, {"seat": 1, "options_include": "Captain"}, {"seat": 2, "options_include": "challenge"}],
   "expect": {"players": {"1": {"coins": 2, "hidden_count": 1, "revealed_cards": ["Captain"]}, "2": {"hidden_count": 2, "revealed_cards": []}}}},
  {"name": "Bluffed Steal is challenged: the target's block is ignored, no coins move, only the bluffer loses a card", "rule": "R22", "players": 3, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"players": {"1": {"coins": 1, "hidden_cards": ["Duke", "Contessa"], "hidden_count": 2},
                         "2": {"coins": 4, "hidden_cards": ["Assassin", "Contessa"], "hidden_count": 2},
                         "3": {"hidden_cards": ["Duke", "Assassin"], "hidden_count": 2}}, "game": {"active_seat": 1}},
   "rules": [{"seat": 1, "options_include": "steal"}, {"seat": 1, "options_include": 2}, {"seat": 1, "options_include": "Duke"},
             {"seat": 2, "options_include": "block_captain"}, {"seat": 3, "options_include": "challenge"}],
   "expect": {"players": {"1": {"coins": 1, "hidden_count": 1, "revealed_cards": ["Duke"]}, "2": {"coins": 4, "hidden_count": 2}, "3": {"hidden_count": 2}}}},
  {"name": "Several challenge a true Tax claim: only the first seat after the active seat (wrapping) loses a card", "rule": "R23", "players": 4, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"players": {"3": {"coins": 2, "hidden_cards": ["Duke", "Captain"], "hidden_count": 2},
                         "4": {"hidden_cards": ["Captain", "Contessa"], "hidden_count": 2},
                         "1": {"hidden_cards": ["Assassin", "Contessa"], "hidden_count": 2}}, "game": {"active_seat": 3}},
   "rules": [{"seat": 3, "options_include": "tax"},
             {"seat": 4, "options_include": "challenge"}, {"seat": 4, "options_include": "Captain"},
             {"seat": 1, "options_include": "challenge"}],
   "expect": {"players": {"3": {"coins": 5, "hidden_count": 2}, "4": {"hidden_count": 1, "revealed_cards": ["Captain"]}, "1": {"hidden_count": 2, "revealed_cards": []}, "2": {"hidden_count": 2}}}},
  {"name": "Two Duke blocks: only seat 2's counts; it is a bluff, so seat 2 loses a card and the aid goes through", "rule": "R24", "players": 3, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"players": {"1": {"coins": 1, "hidden_cards": ["Captain", "Assassin"], "hidden_count": 2},
                         "2": {"hidden_cards": ["Captain", "Contessa"], "hidden_count": 2},
                         "3": {"hidden_cards": ["Duke", "Assassin"], "hidden_count": 2}}, "game": {"active_seat": 1}},
   "rules": [{"seat": 1, "options_include": "foreign_aid"}, {"seat": 1, "options_include": "accept", "answer": "challenge"},
             {"seat": 2, "options_include": "block_duke"}, {"seat": 2, "options_include": "Captain"},
             {"seat": 3, "options_include": "block_duke"}],
   "expect": {"players": {"1": {"coins": 3, "hidden_count": 2}, "2": {"hidden_count": 1, "revealed_cards": ["Captain"]}, "3": {"hidden_count": 2, "revealed_cards": []}}}},
  {"name": "Captain block challenged and the blocker holds Captain: challenger loses a card, steal blocked", "rule": "R25", "players": 3, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"players": {"1": {"coins": 1, "hidden_cards": ["Captain", "Duke"], "hidden_count": 2},
                         "2": {"coins": 4, "hidden_cards": ["Captain", "Assassin"], "hidden_count": 2},
                         "3": {"hidden_cards": ["Duke", "Contessa"], "hidden_count": 2}}, "game": {"active_seat": 1}},
   "rules": [{"seat": 1, "options_include": "steal"}, {"seat": 1, "options_include": 2},
             {"seat": 2, "options_include": "block_captain"},
             {"seat": 3, "options_include": "accept", "answer": "challenge"}, {"seat": 3, "options_include": "Duke"}],
   "expect": {"players": {"1": {"coins": 1, "hidden_count": 2}, "2": {"coins": 4, "hidden_count": 2, "revealed_cards": []}, "3": {"hidden_count": 1, "revealed_cards": ["Duke"]}}}},
  {"name": "Captain block challenged and it is a bluff: blocker loses a card and the steal moves 2", "rule": "R26", "players": 3, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"players": {"1": {"coins": 1, "hidden_cards": ["Captain", "Duke"], "hidden_count": 2},
                         "2": {"coins": 4, "hidden_cards": ["Duke", "Contessa"], "hidden_count": 2},
                         "3": {"hidden_cards": ["Assassin", "Contessa"], "hidden_count": 2}}, "game": {"active_seat": 1}},
   "rules": [{"seat": 1, "options_include": "steal"}, {"seat": 1, "options_include": 2},
             {"seat": 2, "options_include": "block_captain"}, {"seat": 2, "options_include": "Duke"},
             {"seat": 3, "options_include": "accept", "answer": "challenge"}],
   "expect": {"players": {"1": {"coins": 3, "hidden_count": 2}, "2": {"coins": 2, "hidden_count": 1, "revealed_cards": ["Duke"]}, "3": {"hidden_count": 2, "revealed_cards": []}}}},
  {"name": "A bluffed Contessa block is challenged: the target loses 2 and is out", "rule": "R27", "players": 3, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"players": {"1": {"coins": 3, "hidden_cards": ["Assassin", "Duke"], "hidden_count": 2},
                         "2": {"coins": 2, "hidden_cards": ["Duke", "Captain"], "hidden_count": 2},
                         "3": {"hidden_cards": ["Ambassador", "Contessa"], "hidden_count": 2}}, "game": {"active_seat": 1}},
   "rules": [{"seat": 1, "options_include": "assassinate"}, {"seat": 1, "options_include": 2},
             {"seat": 2, "options_include": "block_contessa"},
             {"seat": 3, "options_include": "accept", "answer": "challenge"}],
   "expect": {"players": {"1": {"coins": 0, "hidden_count": 2}, "2": {"hidden_count": 0, "alive": false, "coins": 0}, "3": {"hidden_count": 2}}}},
  {"name": "Losing one of two cards: the player reveals the card they choose (the second one)", "rule": "R28", "players": 3, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"players": {"1": {"coins": 7}, "2": {"hidden_cards": ["Duke", "Captain"], "hidden_count": 2}}, "game": {"active_seat": 1}},
   "rules": [{"seat": 1, "options_include": "coup"}, {"seat": 1, "options_include": 2}, {"seat": 2, "options_include": "Captain"}],
   "expect": {"players": {"2": {"hidden_count": 1, "revealed_cards": ["Captain"], "alive": true}}}},
  {"name": "Coup on a player with one card left: they are out with 0 coins", "rule": "R29", "players": 3, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"players": {"1": {"coins": 7}, "2": {"coins": 5, "hidden_cards": ["Duke"], "revealed_cards": ["Captain"], "hidden_count": 1}}, "game": {"active_seat": 1}},
   "rules": [{"seat": 1, "options_include": "coup"}, {"seat": 1, "options_include": 2}],
   "expect": {"players": {"1": {"coins": 0}, "2": {"hidden_count": 0, "alive": false, "coins": 0}, "3": {"alive": true}}}},
  {"name": "A revealed card stays revealed and does not come back through an Exchange", "rule": "R30", "players": 3, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"players": {"2": {"hidden_cards": ["Duke"], "revealed_cards": ["Captain"], "hidden_count": 1}}, "game": {"active_seat": 2}},
   "rules": [{"seat": 2, "options_include": "exchange"}],
   "expect": {"players": {"2": {"hidden_count": 1, "revealed_cards": ["Captain"], "alive": true}}}},
  {"name": "A loss does not carry into the next turn: the target loses 1 to Coup, then takes Income and keeps 1 card", "rule": "R31", "players": 3, "seed": 1, "default": "decline", "rounds": 2,
   "given": {"players": {"1": {"coins": 7}, "2": {"coins": 2, "hidden_cards": ["Duke", "Captain"], "hidden_count": 2}}, "game": {"active_seat": 1}},
   "rules": [{"seat": 1, "options_include": "coup"}, {"seat": 1, "options_include": 2},
             {"seat": 2, "options_include": "Duke"}, {"seat": 2, "options_include": "income"}],
   "expect": {"players": {"1": {"coins": 0}, "2": {"coins": 3, "hidden_count": 1, "revealed_cards": ["Duke"], "alive": true}}}},
  {"name": "The next turn skips an eliminated seat: after seat 1, seat 3 plays (seat 2 is out)", "rule": "R32", "players": 3, "seed": 1, "default": "decline", "rounds": 2,
   "given": {"players": {"1": {"coins": 1},
                         "2": {"coins": 0, "hidden_cards": [], "revealed_cards": ["Duke", "Captain"], "hidden_count": 0, "alive": false},
                         "3": {"coins": 2}},
             "game": {"active_seat": 1, "living_count": 2}},
   "rules": [{"seat": 1, "options_include": "income", "times": "all"}, {"seat": 3, "options_include": "tax"}],
   "expect": {"players": {"1": {"coins": 2}, "2": {"coins": 0, "alive": false}, "3": {"coins": 5}}}},
  {"name": "A Coup target must be another living player: self and the eliminated seat are not offered, so seat 3 is hit", "rule": "R33", "players": 3, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"players": {"1": {"coins": 7},
                         "2": {"coins": 0, "hidden_cards": [], "revealed_cards": ["Duke", "Captain"], "hidden_count": 0, "alive": false},
                         "3": {"hidden_cards": ["Duke", "Contessa"], "hidden_count": 2}},
             "game": {"active_seat": 1, "living_count": 2}},
   "rules": [{"seat": 1, "options_include": "coup"}, {"seat": 1, "options_include": 1}, {"seat": 1, "options_include": 2}, {"seat": 1, "options_include": 3},
             {"seat": 3, "options_include": "Duke"}],
   "expect": {"players": {"1": {"coins": 0, "hidden_count": 2}, "2": {"hidden_count": 0, "alive": false}, "3": {"hidden_count": 1, "revealed_cards": ["Duke"]}}}},
  {"name": "Last player with hidden cards wins: seat 1 Coups the last rival", "rule": "R34", "players": 3, "seed": 1, "default": "decline",
   "given": {"players": {"1": {"coins": 7},
                         "2": {"coins": 2, "hidden_cards": ["Duke"], "revealed_cards": ["Captain"], "hidden_count": 1},
                         "3": {"coins": 0, "hidden_cards": [], "revealed_cards": ["Assassin", "Contessa"], "hidden_count": 0, "alive": false}},
             "game": {"active_seat": 1, "living_count": 2}},
   "rules": [{"seat": 1, "options_include": "coup"}, {"seat": 1, "options_include": 2}],
   "expect": {"result": "seat 1", "players": {"1": {"alive": true}, "2": {"alive": false, "hidden_count": 0, "coins": 0}}, "game": {"winner": "seat 1"}}},
  {"name": "Turn cap: after turn 40 the seat with the most hidden cards wins", "rule": "R35", "players": 3, "seed": 1, "default": "decline",
   "given": {"players": {"1": {"coins": 1, "hidden_cards": ["Duke", "Captain"], "hidden_count": 2},
                         "2": {"coins": 6, "hidden_cards": ["Duke"], "revealed_cards": ["Contessa"], "hidden_count": 1},
                         "3": {"coins": 6, "hidden_cards": ["Assassin"], "revealed_cards": ["Contessa"], "hidden_count": 1}},
             "game": {"active_seat": 1, "turn_count": 39}},
   "rules": [{"seat": 1, "options_include": "income"}],
   "expect": {"result": "seat 1", "game": {"winner": "seat 1", "turn_count": 40}}},
  {"name": "Turn cap: tied on hidden cards, the tied seat with more coins wins", "rule": "R35", "players": 3, "seed": 1, "default": "decline",
   "given": {"players": {"1": {"coins": 1, "hidden_cards": ["Duke"], "revealed_cards": ["Captain"], "hidden_count": 1},
                         "2": {"coins": 5, "hidden_cards": ["Duke", "Assassin"], "hidden_count": 2},
                         "3": {"coins": 3, "hidden_cards": ["Contessa", "Ambassador"], "hidden_count": 2}},
             "game": {"active_seat": 1, "turn_count": 39}},
   "rules": [{"seat": 1, "options_include": "income"}],
   "expect": {"result": "seat 2", "game": {"winner": "seat 2"}}},
  {"name": "Turn cap: tied on hidden cards and coins is a draw", "rule": "R35", "players": 3, "seed": 1, "default": "decline",
   "given": {"players": {"1": {"coins": 1, "hidden_cards": ["Duke"], "revealed_cards": ["Captain"], "hidden_count": 1},
                         "2": {"coins": 4, "hidden_cards": ["Duke", "Assassin"], "hidden_count": 2},
                         "3": {"coins": 4, "hidden_cards": ["Contessa", "Ambassador"], "hidden_count": 2}},
             "game": {"active_seat": 1, "turn_count": 39}},
   "rules": [{"seat": 1, "options_include": "income"}],
   "expect": {"result": "draw", "game": {"winner": "draw"}}},
  {"name": "Reactions are a poll: both seats challenge a bluffed Tax, only the bluffer loses a card", "rule": "R36", "players": 3, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"players": {"1": {"coins": 2, "hidden_cards": ["Captain", "Contessa"], "hidden_count": 2},
                         "2": {"hidden_cards": ["Duke", "Assassin"], "hidden_count": 2},
                         "3": {"hidden_cards": ["Ambassador", "Assassin"], "hidden_count": 2}}, "game": {"active_seat": 1}},
   "rules": [{"seat": 1, "options_include": "tax"}, {"seat": 1, "options_include": "Contessa"},
             {"seat": 2, "options_include": "challenge"}, {"seat": 3, "options_include": "challenge"}],
   "expect": {"players": {"1": {"coins": 2, "hidden_count": 1, "revealed_cards": ["Contessa"]}, "2": {"hidden_count": 2}, "3": {"hidden_count": 2}}}}
]
```

````
