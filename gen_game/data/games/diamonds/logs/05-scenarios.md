# 05 scenarios

- time: 2026-10-27T18:05:09+00:00 (78.5s)  model: claude-opus-5-5
- system prompt: [system/8e9a17ed-scenarios.md](system/8e9a17ed-scenarios.md) (sha256 8e9a17ed7c2a08b3)
- sent sha256 976cc7da9f4725ad, reply sha256 02f849e9a863d4be

## Sent

````
SPEC:
{
  "name": "Diamonds: Three-Hand Vault",
  "summary": "A three-player trick-taking game over 3 hands of 10 tricks. Each suit's action moves crystals into your showroom (1 point each) or your vault (2 points each), or steals from an opponent's showroom.",
  "players": {
    "min": 3,
    "max": 3,
    "suggested": 3
  },
  "parameters": {
    "deck_size": 36,
    "suits": 4,
    "ranks_per_suit": 9,
    "lowest_rank": 1,
    "highest_rank": 9,
    "cards_dealt_per_player": 10,
    "cards_set_aside": 6,
    "cards_passed": 2,
    "hands": 3,
    "tricks_per_hand": 10,
    "total_rounds": 30,
    "cards_per_trick": 3,
    "crystals_per_action": 1,
    "vault_crystal_points": 2,
    "showroom_crystal_points": 1,
    "zero_trick_diamond_actions": 2,
    "dealer_hand_1_seat": 3,
    "dealer_hand_2_seat": 1,
    "dealer_hand_3_seat": 2,
    "rank_tiebreak_multiplier": 100
  },
  "attributes": {
    "player": [
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "Cards held, coded suit letter + rank, e.g. D7, H3, S9, C1",
        "observable": false
      },
      {
        "key": "pass_cards",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "The 2 cards secretly chosen to pass left this hand",
        "observable": false
      },
      {
        "key": "showroom",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Crystals in the showroom, worth 1 point each",
        "observable": true
      },
      {
        "key": "vault",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Crystals in the vault, worth 2 points each",
        "observable": true
      },
      {
        "key": "score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "2 x vault + 1 x showroom, recomputed after every change",
        "observable": true
      },
      {
        "key": "won_diamonds",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Diamond cards won in tricks this hand",
        "observable": false
      },
      {
        "key": "won_hearts",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Heart cards won in tricks this hand",
        "observable": false
      },
      {
        "key": "won_spades",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Spade cards won in tricks this hand",
        "observable": false
      },
      {
        "key": "won_clubs",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Club cards won in tricks this hand",
        "observable": false
      },
      {
        "key": "tricks_won",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Tricks won this hand",
        "observable": false
      },
      {
        "key": "played_card",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Card this player played to the current trick",
        "observable": false
      },
      {
        "key": "played_suit",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Suit letter of played_card",
        "observable": false
      },
      {
        "key": "played_rank",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Rank of played_card",
        "observable": false
      },
      {
        "key": "clubs_target",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat this player named as Clubs target for the current trick",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "Undealt cards; filled with all 36 cards at the start of each hand",
        "observable": false
      },
      {
        "key": "set_aside",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "The 6 cards set aside face down this hand",
        "observable": false
      },
      {
        "key": "round_number",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Current round, 1 to 30, one trick per round",
        "observable": true
      },
      {
        "key": "hand_number",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Current hand, 1 to 3",
        "observable": false
      },
      {
        "key": "dealer",
        "type": "number",
        "visible": "public",
        "initial": 3,
        "meaning": "Dealer seat this hand (1=A, 2=B, 3=C)",
        "observable": false
      },
      {
        "key": "leader",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Seat that leads the current trick",
        "observable": false
      },
      {
        "key": "led_suit",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Suit letter of the first card of the current trick",
        "observable": false
      },
      {
        "key": "trick_winner",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat that won the last trick",
        "observable": false
      }
    ]
  },
  "setup": [
    "Seats are A=1, B=2, C=3. The left of seat s is seat (s mod 3) + 1.",
    "Every player's showroom, vault and score start at 0.",
    "round_number is set to 1 and hand_number to 1.",
    "The 36 cards are D1-D9, H1-H9, S1-S9 and C1-C9. The crystal supply is unlimited, so it is not tracked."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "when": "(round_number - 1) mod 10 == 0",
      "effect": "Start of a hand. Set hand_number = (round_number - 1) / 10 + 1. Set dealer = 3, 1 or 2 for hand 1, 2 or 3. Set leader = (dealer mod 3) + 1. Gather all 36 cards into deck and clear every hand, pass_cards and set_aside. Deal 10 cards at random from deck into each player's hand, then move the remaining 6 into set_aside. Reset won_diamonds, won_hearts, won_spades, won_clubs and tricks_won to 0 for every player."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "when": "(round_number - 1) mod 10 == 0",
      "effect": "Each player privately sees their own hand."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "one card from own hand",
      "when": "(round_number - 1) mod 10 == 0",
      "effect": "Append the chosen card to pass_cards (first pass card)."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "one card from own hand not already in pass_cards",
      "when": "(round_number - 1) mod 10 == 0",
      "effect": "Append the chosen card to pass_cards (second pass card)."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "when": "(round_number - 1) mod 10 == 0",
      "effect": "Remove each player's pass_cards from their hand and append them to the hand of the player on their left. Clear pass_cards. Nothing is announced about which cards moved."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "when": "(round_number - 1) mod 10 == 0",
      "effect": "Each player privately sees their new hand."
    },
    {
      "action": "ask",
      "who": "seat game.leader",
      "answer": "any card from own hand",
      "effect": "Remove the card from the leader's hand. Set the leader's played_card, played_suit and played_rank. Set led_suit = played_suit."
    },
    {
      "action": "ask",
      "who": "seat game.leader",
      "answer": "one of the two other seats",
      "effect": "Set the leader's clubs_target to the named seat. Announce the leader's card and target."
    },
    {
      "action": "ask",
      "who": "seat (game.leader mod 3) + 1",
      "answer": "a card from own hand of led_suit if any is held, otherwise any card from own hand",
      "effect": "Remove the card from hand. Set played_card, played_suit and played_rank."
    },
    {
      "action": "ask",
      "who": "seat (game.leader mod 3) + 1",
      "answer": "one of the two other seats",
      "effect": "Set clubs_target. Announce the card and the target."
    },
    {
      "action": "update",
      "who": "seat (game.leader mod 3) + 1",
      "answer": null,
      "when": "played_suit != led_suit",
      "effect": "Off-suit action for this player, by played_suit. D: vault +1. H: showroom +1. S: if showroom > 0 then showroom -1 and vault +1. C: if the clubs_target's showroom > 0 then the target's showroom -1 and own showroom +1. Recompute score for affected players and announce the action."
    },
    {
      "action": "ask",
      "who": "seat ((game.leader + 1) mod 3) + 1",
      "answer": "a card from own hand of led_suit if any is held, otherwise any card from own hand",
      "effect": "Remove the card from hand. Set played_card, played_suit and played_rank."
    },
    {
      "action": "ask",
      "who": "seat ((game.leader + 1) mod 3) + 1",
      "answer": "one of the two other seats",
      "effect": "Set clubs_target. Announce the card and the target."
    },
    {
      "action": "update",
      "who": "seat ((game.leader + 1) mod 3) + 1",
      "answer": null,
      "when": "played_suit != led_suit",
      "effect": "Off-suit action, the same as for the second player: D vault +1; H showroom +1; S if showroom > 0 move 1 from showroom to vault; C if the clubs_target's showroom > 0 move 1 from it to own showroom. Recompute score and announce."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "trick_winner = the seat with the highest played_rank among players whose played_suit == led_suit. The winner adds the 3 played cards to won_diamonds, won_hearts, won_spades and won_clubs by each card's suit, and tricks_won +1. The winner then takes the led_suit action using the winner's own clubs_target: D vault +1; H showroom +1; S if showroom > 0 move 1 from showroom to vault; C if the clubs_target's showroom > 0 move 1 from it to the winner's showroom. Set leader = trick_winner. Recompute every score."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce the three cards, the Clubs targets, the trick winner, every action taken, and every player's showroom, vault and won counts."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "when": "round_number mod 10 == 0",
      "effect": "End of hand, applied in order. (1) Diamonds: if one player has strictly the most won_diamonds, that player's vault +1. (2) Hearts: if one player has strictly the most won_hearts, that player's showroom +1. (3) Spades: if one player has strictly the most won_spades and their showroom > 0, that player moves 1 from showroom to vault. (4) Clubs: if one player has strictly the most won_clubs, they take 1 from the showroom of the opponent with the largest showroom; if those two opponents are tied, the opponent on the receiver's left is robbed; nothing moves if that showroom is 0. (5) Each player with tricks_won == 0 gets vault +2. Recompute every score."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "when": "round_number mod 10 == 0",
      "effect": "Announce the end-of-hand actions, the 6 cards in set_aside (revealed), and every score."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "If round_number == 30, end the game. Otherwise round_number +1 and clear every played_card, played_suit, played_rank, clubs_target and led_suit."
    }
  ],
  "ending": {
    "condition": "round_number == 30 after the end-of-hand step of hand 3",
    "rank_by": "you.score * 100 + you.vault",
    "decided_by": "Highest score (2 x vault + showroom) wins. On a score tie, more vault crystals wins. Players still level share the win, which is the source's draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game starts, the deck has 36 cards (4 suits x ranks 1-9) and every showroom, vault and score is 0."
    },
    {
      "id": "R2",
      "text": "When a hand starts (rounds 1, 11, 21), each player is dealt 10 cards into hand and the other 6 go to set_aside, unseen."
    },
    {
      "id": "R3",
      "text": "When a hand starts, the dealer is C (seat 3) for hand 1, A (seat 1) for hand 2 and B (seat 2) for hand 3, and the dealer's left leads the first trick."
    },
    {
      "id": "R4",
      "text": "When a hand starts, all players simultaneously choose exactly 2 different cards from their hand, and those cards move to the hand of the player on their left without being announced."
    },
    {
      "id": "R5",
      "text": "When a hand starts, every player's won_diamonds, won_hearts, won_spades, won_clubs and tricks_won are reset to 0."
    },
    {
      "id": "R6",
      "text": "When the leader plays, any card from hand may be played and its suit becomes led_suit."
    },
    {
      "id": "R7",
      "text": "When a player holds a card of led_suit, they must play a card of led_suit; when they hold none, they may play any card."
    },
    {
      "id": "R8",
      "text": "When a player plays a card, they name one of the two other seats as clubs_target."
    },
    {
      "id": "R9",
      "text": "When a non-leader plays a card not of led_suit, they immediately take that card's suit action before the next player plays."
    },
    {
      "id": "R10",
      "text": "When a Diamonds action is taken, the taker's vault increases by 1."
    },
    {
      "id": "R11",
      "text": "When a Hearts action is taken, the taker's showroom increases by 1."
    },
    {
      "id": "R12",
      "text": "When a Spades action is taken with showroom > 0, the taker's showroom decreases by 1 and vault increases by 1; with showroom 0, nothing happens."
    },
    {
      "id": "R13",
      "text": "When a Clubs action is taken from a trick or an off-suit play, 1 crystal moves from the named clubs_target's showroom to the taker's showroom, or nothing happens if that showroom is 0."
    },
    {
      "id": "R14",
      "text": "When all three cards are played, the highest rank of led_suit wins the trick, and the winner adds each card to its suit's won count and adds 1 to tricks_won."
    },
    {
      "id": "R15",
      "text": "When a trick is won, the winner takes the led_suit action and leads the next trick."
    },
    {
      "id": "R16",
      "text": "When a hand ends, for Diamonds, Hearts, Spades and Clubs in that order, the player with strictly the most won cards of that suit takes that suit's action once; on a tie for the most, no one does."
    },
    {
      "id": "R17",
      "text": "When an end-of-hand Clubs action is taken, it robs the opponent with the larger showroom, or the opponent on the receiver's left if the two are tied."
    },
    {
      "id": "R18",
      "text": "When a hand ends, each player with tricks_won == 0 takes two Diamond actions (vault +2)."
    },
    {
      "id": "R19",
      "text": "When a hand ends, the 6 set_aside cards are revealed to all players."
    },
    {
      "id": "R20",
      "text": "A player's score is always 2 x vault + 1 x showroom."
    },
    {
      "id": "R21",
      "text": "When round 30 and the third end-of-hand step finish, the game ends."
    },
    {
      "id": "R22",
      "text": "When the game ends, the highest score wins, ties are broken by more vault crystals, and players still tied share the win (a draw)."
    }
  ],
  "offers": [
    {
      "question": "First pass card (poll at the start of a hand)",
      "who": "all players",
      "options": "every card in the player's own hand"
    },
    {
      "question": "Second pass card",
      "who": "all players",
      "options": "every card in the player's own hand except the one already chosen"
    },
    {
      "question": "Leader's card",
      "who": "seat game.leader",
      "options": "every card in own hand"
    },
    {
      "question": "Following player's card",
      "who": "the second and third players of the trick",
      "options": "if the player holds any card of led_suit: only those cards; otherwise: every card in own hand"
    },
    {
      "question": "Clubs target",
      "who": "each player after playing a card",
      "options": "the two seats other than the player's own"
    }
  ],
  "choices": [
    {
      "what": "3 players exactly (suggested 3)",
      "why": "The designer fixed 3 seats. The dealer rotation, 'left', the 36-card deal (3 x 10 + 6) and the end-of-hand Clubs tie rule all assume 3 players."
    },
    {
      "what": "No talk step",
      "why": "The source has no table talk, and adding it would add a mechanic. Strategy lives in passing, suit play, off-suit timing and Clubs targeting: hold Hearts to build a showroom, use Spades to bank it, and point Clubs at the leader."
    },
    {
      "what": "Card codes such as D7 and seat numbers A=1, B=2, C=3",
      "why": "Gives arithmetic a concrete suit letter and rank to compare."
    },
    {
      "what": "The pass is two simultaneous polls of one card each",
      "why": "A question returns one choice; two polls keep the pass secret and simultaneous."
    },
    {
      "what": "Every player names a Clubs target with every card, even when Clubs cannot apply",
      "why": "The source says every player names one; it is used only if a Clubs action fires."
    },
    {
      "what": "Ranking expression score*100 + vault",
      "why": "Vault stays well below 100, so this ranks by score first and vault second, and remaining ties share the win (the draw)."
    },
    {
      "what": "End-of-hand suit actions are applied one after another, each seeing the previous result",
      "why": "The source says 'for each suit in turn', so a Hearts crystal can be banked by a following Spades action."
    }
  ],
  "simplifications": [
    {
      "what": "The crystal supply is not tracked",
      "why": "The source says it is unlimited."
    },
    {
      "what": "Each player's turn is split into two asks: card, then Clubs target",
      "why": "A question returns a single choice."
    },
    {
      "what": "Follow-suit is enforced by restricting the offered cards",
      "why": "Options are filtered from the hand list by led_suit instead of checking after the play."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: showroom, vault, score; table: round_number.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
```json
[
  {
    "name": "Game starts with every showroom, vault and score at 0 and round 1",
    "rule": "R1",
    "players": 3,
    "rounds": 0,
    "expect": {
      "players": {
        "1": {"showroom": 0, "vault": 0, "score": 0},
        "2": {"showroom": 0, "vault": 0, "score": 0},
        "3": {"showroom": 0, "vault": 0, "score": 0}
      },
      "game": {"round_number": 1}
    }
  },
  {
    "name": "Hand start deals 10 each and sets 6 aside (after pass and one trick each hand holds 9; random cards, only counts asserted)",
    "rule": "R2",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "expect": {
      "lens": {
        "game": {"set_aside": 6, "deck": 0},
        "players": {"1": {"hand": 9}, "2": {"hand": 9}, "3": {"hand": 9}}
      },
      "game": {"round_number": 2}
    }
  },
  {
    "name": "Hand 2 starts with a fresh deal and one trick played (random cards, only counts asserted)",
    "rule": "R3",
    "players": 3,
    "seed": 2,
    "rounds": 1,
    "default": "first",
    "given": {"game": {"round_number": 11}},
    "expect": {
      "lens": {
        "game": {"set_aside": 6},
        "players": {"1": {"hand": 9}, "2": {"hand": 9}, "3": {"hand": 9}}
      },
      "game": {"round_number": 12}
    }
  },
  {
    "name": "Passing two cards left keeps every hand at 10 before the trick and clears pass_cards (random cards, counts only)",
    "rule": "R4",
    "players": 3,
    "seed": 3,
    "rounds": 1,
    "default": "first",
    "expect": {
      "lens": {
        "players": {
          "1": {"hand": 9, "pass_cards": 0},
          "2": {"hand": 9, "pass_cards": 0},
          "3": {"hand": 9, "pass_cards": 0}
        }
      },
      "game": {"round_number": 2}
    }
  },
  {
    "name": "Hand 3 start resets the hand and deals again (random cards, only counts asserted)",
    "rule": "R5",
    "players": 3,
    "seed": 4,
    "rounds": 1,
    "default": "first",
    "given": {
      "game": {"round_number": 21},
      "players": {
        "1": {"tricks_won": 5, "won_diamonds": 4},
        "2": {"tricks_won": 5, "won_hearts": 4},
        "3": {"tricks_won": 0}
      }
    },
    "expect": {
      "lens": {
        "game": {"set_aside": 6},
        "players": {"1": {"hand": 9}, "2": {"hand": 9}, "3": {"hand": 9}}
      },
      "game": {"round_number": 22}
    }
  },
  {
    "name": "Leader may play any card in hand; a Diamond lead won by the leader gives vault +1",
    "rule": "R6",
    "players": 3,
    "rounds": 1,
    "given": {
      "game": {"round_number": 5, "leader": 1},
      "players": {
        "1": {"hand": ["S2", "H5", "D9"]},
        "2": {"hand": ["D4"]},
        "3": {"hand": ["D3"]}
      }
    },
    "rules": [{"seat": 1, "options_include": "D9"}],
    "expect": {
      "offered": [
        {"seat": 1, "option": "S2"},
        {"seat": 1, "option": "H5"},
        {"seat": 1, "option": "D9"}
      ],
      "players": {
        "1": {"showroom": 0, "vault": 1, "score": 2},
        "2": {"showroom": 0, "vault": 0, "score": 0},
        "3": {"showroom": 0, "vault": 0, "score": 0}
      },
      "game": {"round_number": 6}
    }
  },
  {
    "name": "Followers holding the led suit are only offered that suit",
    "rule": "R7",
    "players": 3,
    "rounds": 1,
    "given": {
      "game": {"round_number": 5, "leader": 1},
      "players": {
        "1": {"hand": ["H5", "S2"]},
        "2": {"hand": ["H3", "D4"]},
        "3": {"hand": ["H9", "C1"]}
      }
    },
    "rules": [{"seat": 1, "options_include": "H5"}],
    "expect": {
      "offered": [
        {"seat": 2, "option": "H3"},
        {"seat": 3, "option": "H9"}
      ],
      "not_offered": [
        {"seat": 2, "option": "D4"},
        {"seat": 3, "option": "C1"}
      ],
      "players": {
        "1": {"showroom": 0, "vault": 0, "score": 0},
        "2": {"showroom": 0, "vault": 0, "score": 0},
        "3": {"showroom": 1, "vault": 0, "score": 1}
      }
    }
  },
  {
    "name": "Each player names one of the two other seats as Clubs target, never itself",
    "rule": "R8",
    "players": 3,
    "rounds": 1,
    "given": {
      "game": {"round_number": 5, "leader": 1},
      "players": {
        "1": {"hand": ["H5"]},
        "2": {"hand": ["H3"]},
        "3": {"hand": ["H2"]}
      }
    },
    "expect": {
      "offered": [
        {"seat": 1, "option": 2},
        {"seat": 1, "option": 3},
        {"seat": 2, "option": 1},
        {"seat": 2, "option": 3},
        {"seat": 3, "option": 1},
        {"seat": 3, "option": 2}
      ],
      "not_offered": [
        {"seat": 1, "option": 1},
        {"seat": 2, "option": 2},
        {"seat": 3, "option": 3}
      ],
      "players": {"1": {"showroom": 1, "score": 1}}
    }
  },
  {
    "name": "An off-suit Diamond gives the follower vault +1; the led Heart winner gets showroom +1",
    "rule": "R9",
    "players": 3,
    "rounds": 1,
    "given": {
      "game": {"round_number": 5, "leader": 1},
      "players": {
        "1": {"hand": ["H5"]},
        "2": {"hand": ["D4"]},
        "3": {"hand": ["H2"]}
      }
    },
    "expect": {
      "players": {
        "1": {"showroom": 1, "vault": 0, "score": 1},
        "2": {"showroom": 0, "vault": 1, "score": 2},
        "3": {"showroom": 0, "vault": 0, "score": 0}
      }
    }
  },
  {
    "name": "Diamond trick win gives vault +1",
    "rule": "R10",
    "players": 3,
    "rounds": 1,
    "given": {
      "game": {"round_number": 5, "leader": 1},
      "players": {
        "1": {"hand": ["D9"]},
        "2": {"hand": ["D2"]},
        "3": {"hand": ["D3"]}
      }
    },
    "expect": {
      "players": {
        "1": {"showroom": 0, "vault": 1, "score": 2},
        "2": {"vault": 0, "score": 0},
        "3": {"vault": 0, "score": 0}
      }
    }
  },
  {
    "name": "Heart trick win gives showroom +1 to the highest Heart",
    "rule": "R11",
    "players": 3,
    "rounds": 1,
    "given": {
      "game": {"round_number": 5, "leader": 1},
      "players": {
        "1": {"hand": ["H5"]},
        "2": {"hand": ["H3"]},
        "3": {"hand": ["H9"]}
      }
    },
    "expect": {
      "players": {
        "1": {"showroom": 0, "score": 0},
        "2": {"showroom": 0, "score": 0},
        "3": {"showroom": 1, "vault": 0, "score": 1}
      }
    }
  },
  {
    "name": "Spade trick win with a showroom moves 1 crystal from showroom to vault",
    "rule": "R12",
    "players": 3,
    "rounds": 1,
    "given": {
      "game": {"round_number": 5, "leader": 1},
      "players": {
        "1": {"hand": ["S9"], "showroom": 2, "vault": 0, "score": 2},
        "2": {"hand": ["S1"]},
        "3": {"hand": ["S2"]}
      }
    },
    "expect": {
      "players": {"1": {"showroom": 1, "vault": 1, "score": 3}}
    }
  },
  {
    "name": "Spade trick win with an empty showroom does nothing",
    "rule": "R12",
    "players": 3,
    "rounds": 1,
    "given": {
      "game": {"round_number": 5, "leader": 1},
      "players": {
        "1": {"hand": ["S9"], "showroom": 0, "vault": 1, "score": 2},
        "2": {"hand": ["S1"]},
        "3": {"hand": ["S2"]}
      }
    },
    "expect": {
      "players": {"1": {"showroom": 0, "vault": 1, "score": 2}}
    }
  },
  {
    "name": "Club trick win steals 1 showroom crystal from the named target",
    "rule": "R13",
    "players": 3,
    "rounds": 1,
    "given": {
      "game": {"round_number": 5, "leader": 1},
      "players": {
        "1": {"hand": ["C9"]},
        "2": {"hand": ["C1"], "showroom": 2, "score": 2},
        "3": {"hand": ["C2"], "showroom": 2, "score": 2}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "C9"},
      {"seat": 1, "options_include": 3}
    ],
    "expect": {
      "players": {
        "1": {"showroom": 1, "score": 1},
        "2": {"showroom": 2, "score": 2},
        "3": {"showroom": 1, "score": 1}
      }
    }
  },
  {
    "name": "Off-suit Club steals from the follower's named target",
    "rule": "R13",
    "players": 3,
    "rounds": 1,
    "given": {
      "game": {"round_number": 5, "leader": 1},
      "players": {
        "1": {"hand": ["D5"], "showroom": 0},
        "2": {"hand": ["C4"], "showroom": 0},
        "3": {"hand": ["D2"], "showroom": 2, "score": 2}
      }
    },
    "rules": [{"seat": 2, "options_include": 3}],
    "expect": {
      "players": {
        "1": {"showroom": 0, "vault": 1, "score": 2},
        "2": {"showroom": 1, "vault": 0, "score": 1},
        "3": {"showroom": 1, "score": 1}
      }
    }
  },
  {
    "name": "Highest rank of the led suit wins even when an off-suit card is higher",
    "rule": "R14",
    "players": 3,
    "rounds": 1,
    "given": {
      "game": {"round_number": 5, "leader": 1},
      "players": {
        "1": {"hand": ["H2"]},
        "2": {"hand": ["H4"]},
        "3": {"hand": ["S9"]}
      }
    },
    "expect": {
      "players": {
        "1": {"showroom": 0, "score": 0},
        "2": {"showroom": 1, "vault": 0, "score": 1},
        "3": {"showroom": 0, "vault": 0, "score": 0}
      }
    }
  },
  {
    "name": "Trick winner leads the next trick and may lead any card",
    "rule": "R15",
    "players": 3,
    "rounds": 2,
    "given": {
      "game": {"round_number": 5, "leader": 1},
      "players": {
        "1": {"hand": ["H5", "D1"]},
        "2": {"hand": ["H3", "D2"]},
        "3": {"hand": ["H9", "S8", "D3"]}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "H5"},
      {"seat": 3, "options_include": "D3"}
    ],
    "expect": {
      "offered": [{"seat": 3, "option": "S8"}],
      "players": {
        "1": {"showroom": 0, "vault": 0, "score": 0},
        "2": {"showroom": 0, "vault": 0, "score": 0},
        "3": {"showroom": 1, "vault": 1, "score": 3}
      },
      "game": {"round_number": 7}
    }
  },
  {
    "name": "End of hand: strict-most suit actions in order, Clubs tie gives nothing, zero-trick player gets vault +2",
    "rule": "R16",
    "players": 3,
    "rounds": 1,
    "given": {
      "game": {"round_number": 10, "leader": 1},
      "players": {
        "1": {"hand": ["S9"], "showroom": 2, "vault": 0, "score": 2, "won_diamonds": 5, "won_hearts": 2, "won_spades": 4, "won_clubs": 4, "tricks_won": 5},
        "2": {"hand": ["S1"], "showroom": 1, "vault": 0, "score": 1, "won_diamonds": 2, "won_hearts": 5, "won_spades": 1, "won_clubs": 4, "tricks_won": 4},
        "3": {"hand": ["S2"], "showroom": 0, "vault": 0, "score": 0, "won_diamonds": 0, "won_hearts": 0, "won_spades": 0, "won_clubs": 0, "tricks_won": 0}
      }
    },
    "expect": {
      "players": {
        "1": {"showroom": 0, "vault": 3, "score": 6},
        "2": {"showroom": 2, "vault": 0, "score": 2},
        "3": {"showroom": 0, "vault": 2, "score": 4}
      },
      "game": {"round_number": 11}
    }
  },
  {
    "name": "End-of-hand Clubs robs the opponent with the larger showroom",
    "rule": "R17",
    "players": 3,
    "rounds": 1,
    "given": {
      "game": {"round_number": 10, "leader": 1},
      "players": {
        "1": {"hand": ["C9"], "showroom": 0, "vault": 0, "score": 0, "won_diamonds": 3, "won_hearts": 3, "won_spades": 3, "won_clubs": 0, "tricks_won": 3},
        "2": {"hand": ["C1"], "showroom": 1, "vault": 0, "score": 1, "won_diamonds": 3, "won_hearts": 3, "won_spades": 3, "won_clubs": 0, "tricks_won": 3},
        "3": {"hand": ["C2"], "showroom": 3, "vault": 0, "score": 3, "won_diamonds": 3, "won_hearts": 3, "won_spades": 3, "won_clubs": 0, "tricks_won": 3}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "C9"},
      {"seat": 1, "options_include": 2}
    ],
    "expect": {
      "players": {
        "1": {"showroom": 2, "vault": 0, "score": 2},
        "2": {"showroom": 0, "vault": 0, "score": 0},
        "3": {"showroom": 2, "vault": 0, "score": 2}
      }
    }
  },
  {
    "name": "End-of-hand Clubs with tied opponents robs the receiver's left",
    "rule": "R17",
    "players": 3,
    "rounds": 1,
    "given": {
      "game": {"round_number": 10, "leader": 1},
      "players": {
        "1": {"hand": ["C9"], "showroom": 0, "vault": 0, "score": 0, "won_diamonds": 3, "won_hearts": 3, "won_spades": 3, "won_clubs": 0, "tricks_won": 3},
        "2": {"hand": ["C1"], "showroom": 2, "vault": 0, "score": 2, "won_diamonds": 3, "won_hearts": 3, "won_spades": 3, "won_clubs": 0, "tricks_won": 3},
        "3": {"hand": ["C2"], "showroom": 3, "vault": 0, "score": 3, "won_diamonds": 3, "won_hearts": 3, "won_spades": 3, "won_clubs": 0, "tricks_won": 3}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "C9"},
      {"seat": 1, "options_include": 3}
    ],
    "expect": {
      "players": {
        "1": {"showroom": 2, "vault": 0, "score": 2},
        "2": {"showroom": 1, "vault": 0, "score": 1},
        "3": {"showroom": 2, "vault": 0, "score": 2}
      }
    }
  },
  {
    "name": "Players with zero tricks this hand get vault +2 at the end of the hand",
    "rule": "R18",
    "players": 3,
    "rounds": 1,
    "given": {
      "game": {"round_number": 10, "leader": 1},
      "players": {
        "1": {"hand": ["D9"], "won_diamonds": 0, "won_hearts": 0, "won_spades": 0, "won_clubs": 0, "tricks_won": 9},
        "2": {"hand": ["D1"], "won_diamonds": 0, "won_hearts": 0, "won_spades": 0, "won_clubs": 0, "tricks_won": 0},
        "3": {"hand": ["D2"], "won_diamonds": 0, "won_hearts": 0, "won_spades": 0, "won_clubs": 0, "tricks_won": 0}
      }
    },
    "expect": {
      "players": {
        "1": {"showroom": 0, "vault": 2, "score": 4},
        "2": {"showroom": 0, "vault": 2, "score": 4},
        "3": {"showroom": 0, "vault": 2, "score": 4}
      }
    }
  },
  {
    "name": "End of hand reveals the set-aside cards without removing them (only the count is asserted)",
    "rule": "R19",
    "players": 3,
    "rounds": 1,
    "given": {
      "game": {"round_number": 10, "leader": 1, "set_aside": ["D8", "H8", "S8", "C8", "D7", "H7"]},
      "players": {
        "1": {"hand": ["H9"], "tricks_won": 3},
        "2": {"hand": ["H1"], "tricks_won": 3},
        "3": {"hand": ["H2"], "tricks_won": 3}
      }
    },
    "expect": {
      "lens": {"game": {"set_aside": 6}},
      "game": {"round_number": 11}
    }
  },
  {
    "name": "Score is 2 x vault + showroom after a Heart gain",
    "rule": "R20",
    "players": 3,
    "rounds": 1,
    "given": {
      "game": {"round_number": 5, "leader": 1},
      "players": {
        "1": {"hand": ["H9"], "showroom": 1, "vault": 2, "score": 5},
        "2": {"hand": ["H1"]},
        "3": {"hand": ["H2"]}
      }
    },
    "expect": {
      "players": {"1": {"showroom": 2, "vault": 2, "score": 6}}
    }
  },
  {
    "name": "Game ends after round 30; a score tie is broken by vault",
    "rule": "R21",
    "players": 3,
    "given": {
      "game": {"round_number": 30, "leader": 1},
      "players": {
        "1": {"hand": ["H9"], "showroom": 0, "vault": 1, "score": 2, "won_diamonds": 3, "won_hearts": 3, "won_spades": 3, "won_clubs": 0, "tricks_won": 3},
        "2": {"hand": ["H1"], "showroom": 0, "vault": 2, "score": 4, "won_diamonds": 3, "won_hearts": 3, "won_spades": 3, "won_clubs": 0, "tricks_won": 3},
        "3": {"hand": ["H2"], "showroom": 3, "vault": 0, "score": 3, "won_diamonds": 3, "won_hearts": 3, "won_spades": 3, "won_clubs": 0, "tricks_won": 3}
      }
    },
    "expect": {
      "winner": 2,
      "standings": {"1": 401, "2": 402, "3": 300},
      "players": {
        "1": {"showroom": 2, "vault": 1, "score": 4},
        "2": {"showroom": 0, "vault": 2, "score": 4},
        "3": {"showroom": 3, "vault": 0, "score": 3}
      },
      "game": {"round_number": 30}
    }
  },
  {
    "name": "Players level on score and vault share the win",
    "rule": "R22",
    "players": 3,
    "given": {
      "game": {"round_number": 30, "leader": 1},
      "players": {
        "1": {"hand": ["H9"], "showroom": 0, "vault": 1, "score": 2, "won_diamonds": 3, "won_hearts": 3, "won_spades": 3, "won_clubs": 0, "tricks_won": 3},
        "2": {"hand": ["H1"], "showroom": 2, "vault": 1, "score": 4, "won_diamonds": 3, "won_hearts": 3, "won_spades": 3, "won_clubs": 0, "tricks_won": 3},
        "3": {"hand": ["H2"], "showroom": 2, "vault": 1, "score": 4, "won_diamonds": 3, "won_hearts": 3, "won_spades": 3, "won_clubs": 0, "tricks_won": 3}
      }
    },
    "expect": {
      "winner": [1, 2, 3],
      "standings": {"1": 401, "2": 401, "3": 401},
      "players": {
        "1": {"showroom": 2, "vault": 1, "score": 4},
        "2": {"showroom": 2, "vault": 1, "score": 4},
        "3": {"showroom": 2, "vault": 1, "score": 4}
      }
    }
  }
]
```

Why it was refused: scenario 1: needs `rules` (what each seat answers, by option name); scenario 2: needs `rules` (what each seat answers, by option name); scenario 3: needs `rules` (what each seat answers, by option name); scenario 4: needs `rules` (what each seat answers, by option name); scenario 5: needs `rules` (what each seat answers, by option name); scenario 8: needs `rules` (what each seat answers, by option name); scenario 9: needs `rules` (what each seat answers, by option name); scenario 10: needs `rules` (what each seat answers, by option name); scenario 11: needs `rules` (what each seat answers, by option name); scenario 12: needs `rules` (what each seat answers, by option name); scenario 13: needs `rules` (what each seat answers, by option name); scenario 16: needs `rules` (what each seat answers, by option name); scenario 18: needs `rules` (what each seat answers, by option name); scenario 21: needs `rules` (what each seat answers, by option name); scenario 22: needs `rules` (what each seat answers, by option name); scenario 23: needs `rules` (what each seat answers, by option name); scenario 24: needs `rules` (what each seat answers, by option name); scenario 25: needs `rules` (what each seat answers, by option name)
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
[
  {
    "name": "Game starts with every showroom, vault and score at 0 and round 1",
    "rule": "R1",
    "players": 3,
    "rounds": 0,
    "rules": [
      {"seat": 1, "options_include": 2, "times": "all"}
    ],
    "expect": {
      "players": {
        "1": {"showroom": 0, "vault": 0, "score": 0},
        "2": {"showroom": 0, "vault": 0, "score": 0},
        "3": {"showroom": 0, "vault": 0, "score": 0}
      },
      "game": {"round_number": 1}
    }
  },
  {
    "name": "Hand start deals 10 each and sets 6 aside (after pass and one trick each hand holds 9; random cards, only counts asserted)",
    "rule": "R2",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "rules": [
      {"seat": 1, "options_include": 2, "times": "all"},
      {"seat": 2, "options_include": 3, "times": "all"},
      {"seat": 3, "options_include": 1, "times": "all"}
    ],
    "expect": {
      "lens": {
        "game": {"set_aside": 6, "deck": 0},
        "players": {"1": {"hand": 9}, "2": {"hand": 9}, "3": {"hand": 9}}
      },
      "game": {"round_number": 2}
    }
  },
  {
    "name": "Hand 2 starts with a fresh deal and one trick played (random cards, only counts asserted)",
    "rule": "R3",
    "players": 3,
    "seed": 2,
    "rounds": 1,
    "default": "first",
    "given": {"game": {"round_number": 11}},
    "rules": [
      {"seat": 1, "options_include": 2, "times": "all"},
      {"seat": 2, "options_include": 3, "times": "all"},
      {"seat": 3, "options_include": 1, "times": "all"}
    ],
    "expect": {
      "lens": {
        "game": {"set_aside": 6},
        "players": {"1": {"hand": 9}, "2": {"hand": 9}, "3": {"hand": 9}}
      },
      "game": {"round_number": 12}
    }
  },
  {
    "name": "Passing two cards left keeps every hand at 10 before the trick and clears pass_cards (random cards, counts only)",
    "rule": "R4",
    "players": 3,
    "seed": 3,
    "rounds": 1,
    "default": "first",
    "rules": [
      {"seat": 1, "options_include": 3, "times": "all"},
      {"seat": 2, "options_include": 1, "times": "all"},
      {"seat": 3, "options_include": 2, "times": "all"}
    ],
    "expect": {
      "lens": {
        "players": {
          "1": {"hand": 9, "pass_cards": 0},
          "2": {"hand": 9, "pass_cards": 0},
          "3": {"hand": 9, "pass_cards": 0}
        }
      },
      "game": {"round_number": 2}
    }
  },
  {
    "name": "Hand 3 start resets the hand and deals again (random cards, only counts asserted)",
    "rule": "R5",
    "players": 3,
    "seed": 4,
    "rounds": 1,
    "default": "first",
    "given": {
      "game": {"round_number": 21},
      "players": {
        "1": {"tricks_won": 5, "won_diamonds": 4},
        "2": {"tricks_won": 5, "won_hearts": 4},
        "3": {"tricks_won": 0}
      }
    },
    "rules": [
      {"seat": 1, "options_include": 2, "times": "all"},
      {"seat": 2, "options_include": 3, "times": "all"},
      {"seat": 3, "options_include": 1, "times": "all"}
    ],
    "expect": {
      "lens": {
        "game": {"set_aside": 6},
        "players": {"1": {"hand": 9}, "2": {"hand": 9}, "3": {"hand": 9}}
      },
      "game": {"round_number": 22}
    }
  },
  {
    "name": "Leader may play any card in hand; a Diamond lead won by the leader gives vault +1",
    "rule": "R6",
    "players": 3,
    "rounds": 1,
    "given": {
      "game": {"round_number": 5, "leader": 1},
      "players": {
        "1": {"hand": ["S2", "H5", "D9"]},
        "2": {"hand": ["D4"]},
        "3": {"hand": ["D3"]}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "D9"},
      {"seat": 2, "options_include": "D4"},
      {"seat": 3, "options_include": "D3"}
    ],
    "expect": {
      "offered": [
        {"seat": 1, "option": "S2"},
        {"seat": 1, "option": "H5"},
        {"seat": 1, "option": "D9"}
      ],
      "players": {
        "1": {"showroom": 0, "vault": 1, "score": 2},
        "2": {"showroom": 0, "vault": 0, "score": 0},
        "3": {"showroom": 0, "vault": 0, "score": 0}
      },
      "game": {"round_number": 6}
    }
  },
  {
    "name": "Followers holding the led suit are only offered that suit",
    "rule": "R7",
    "players": 3,
    "rounds": 1,
    "given": {
      "game": {"round_number": 5, "leader": 1},
      "players": {
        "1": {"hand": ["H5", "S2"]},
        "2": {"hand": ["H3", "D4"]},
        "3": {"hand": ["H9", "C1"]}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "H5"},
      {"seat": 2, "options_include": "H3"},
      {"seat": 3, "options_include": "H9"}
    ],
    "expect": {
      "offered": [
        {"seat": 2, "option": "H3"},
        {"seat": 3, "option": "H9"}
      ],
      "not_offered": [
        {"seat": 2, "option": "D4"},
        {"seat": 3, "option": "C1"}
      ],
      "players": {
        "1": {"showroom": 0, "vault": 0, "score": 0},
        "2": {"showroom": 0, "vault": 0, "score": 0},
        "3": {"showroom": 1, "vault": 0, "score": 1}
      }
    }
  },
  {
    "name": "Each player names one of the two other seats as Clubs target, never itself",
    "rule": "R8",
    "players": 3,
    "rounds": 1,
    "given": {
      "game": {"round_number": 5, "leader": 1},
      "players": {
        "1": {"hand": ["H5"]},
        "2": {"hand": ["H3"]},
        "3": {"hand": ["H2"]}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "H5"},
      {"seat": 1, "options_include": 3},
      {"seat": 2, "options_include": "H3"},
      {"seat": 2, "options_include": 1},
      {"seat": 3, "options_include": "H2"},
      {"seat": 3, "options_include": 2}
    ],
    "expect": {
      "offered": [
        {"seat": 1, "option": 2},
        {"seat": 1, "option": 3},
        {"seat": 2, "option": 1},
        {"seat": 2, "option": 3},
        {"seat": 3, "option": 1},
        {"seat": 3, "option": 2}
      ],
      "not_offered": [
        {"seat": 1, "option": 1},
        {"seat": 2, "option": 2},
        {"seat": 3, "option": 3}
      ],
      "players": {"1": {"showroom": 1, "score": 1}}
    }
  },
  {
    "name": "An off-suit Diamond gives the follower vault +1; the led Heart winner gets showroom +1",
    "rule": "R9",
    "players": 3,
    "rounds": 1,
    "given": {
      "game": {"round_number": 5, "leader": 1},
      "players": {
        "1": {"hand": ["H5"]},
        "2": {"hand": ["D4"]},
        "3": {"hand": ["H2"]}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "H5"},
      {"seat": 2, "options_include": "D4"},
      {"seat": 3, "options_include": "H2"}
    ],
    "expect": {
      "players": {
        "1": {"showroom": 1, "vault": 0, "score": 1},
        "2": {"showroom": 0, "vault": 1, "score": 2},
        "3": {"showroom": 0, "vault": 0, "score": 0}
      }
    }
  },
  {
    "name": "Diamond trick win gives vault +1",
    "rule": "R10",
    "players": 3,
    "rounds": 1,
    "given": {
      "game": {"round_number": 5, "leader": 1},
      "players": {
        "1": {"hand": ["D9"]},
        "2": {"hand": ["D2"]},
        "3": {"hand": ["D3"]}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "D9"},
      {"seat": 2, "options_include": "D2"},
      {"seat": 3, "options_include": "D3"}
    ],
    "expect": {
      "players": {
        "1": {"showroom": 0, "vault": 1, "score": 2},
        "2": {"vault": 0, "score": 0},
        "3": {"vault": 0, "score": 0}
      }
    }
  },
  {
    "name": "Heart trick win gives showroom +1 to the highest Heart",
    "rule": "R11",
    "players": 3,
    "rounds": 1,
    "given": {
      "game": {"round_number": 5, "leader": 1},
      "players": {
        "1": {"hand": ["H5"]},
        "2": {"hand": ["H3"]},
        "3": {"hand": ["H9"]}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "H5"},
      {"seat": 2, "options_include": "H3"},
      {"seat": 3, "options_include": "H9"}
    ],
    "expect": {
      "players": {
        "1": {"showroom": 0, "score": 0},
        "2": {"showroom": 0, "score": 0},
        "3": {"showroom": 1, "vault": 0, "score": 1}
      }
    }
  },
  {
    "name": "Spade trick win with a showroom moves 1 crystal from showroom to vault",
    "rule": "R12",
    "players": 3,
    "rounds": 1,
    "given": {
      "game": {"round_number": 5, "leader": 1},
      "players": {
        "1": {"hand": ["S9"], "showroom": 2, "vault": 0, "score": 2},
        "2": {"hand": ["S1"]},
        "3": {"hand": ["S2"]}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "S9"},
      {"seat": 2, "options_include": "S1"},
      {"seat": 3, "options_include": "S2"}
    ],
    "expect": {
      "players": {"1": {"showroom": 1, "vault": 1, "score": 3}}
    }
  },
  {
    "name": "Spade trick win with an empty showroom does nothing",
    "rule": "R12",
    "players": 3,
    "rounds": 1,
    "given": {
      "game": {"round_number": 5, "leader": 1},
      "players": {
        "1": {"hand": ["S9"], "showroom": 0, "vault": 1, "score": 2},
        "2": {"hand": ["S1"]},
        "3": {"hand": ["S2"]}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "S9"},
      {"seat": 2, "options_include": "S1"},
      {"seat": 3, "options_include": "S2"}
    ],
    "expect": {
      "players": {"1": {"showroom": 0, "vault": 1, "score": 2}}
    }
  },
  {
    "name": "Club trick win steals 1 showroom crystal from the named target",
    "rule": "R13",
    "players": 3,
    "rounds": 1,
    "given": {
      "game": {"round_number": 5, "leader": 1},
      "players": {
        "1": {"hand": ["C9"]},
        "2": {"hand": ["C1"], "showroom": 2, "score": 2},
        "3": {"hand": ["C2"], "showroom": 2, "score": 2}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "C9"},
      {"seat": 1, "options_include": 3},
      {"seat": 2, "options_include": "C1"},
      {"seat": 3, "options_include": "C2"}
    ],
    "expect": {
      "players": {
        "1": {"showroom": 1, "score": 1},
        "2": {"showroom": 2, "score": 2},
        "3": {"showroom": 1, "score": 1}
      }
    }
  },
  {
    "name": "Off-suit Club steals from the follower's named target",
    "rule": "R13",
    "players": 3,
    "rounds": 1,
    "given": {
      "game": {"round_number": 5, "leader": 1},
      "players": {
        "1": {"hand": ["D5"], "showroom": 0},
        "2": {"hand": ["C4"], "showroom": 0},
        "3": {"hand": ["D2"], "showroom": 2, "score": 2}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "D5"},
      {"seat": 2, "options_include": "C4"},
      {"seat": 2, "options_include": 3},
      {"seat": 3, "options_include": "D2"}
    ],
    "expect": {
      "players": {
        "1": {"showroom": 0, "vault": 1, "score": 2},
        "2": {"showroom": 1, "vault": 0, "score": 1},
        "3": {"showroom": 1, "score": 1}
      }
    }
  },
  {
    "name": "Highest rank of the led suit wins even when an off-suit card is higher",
    "rule": "R14",
    "players": 3,
    "rounds": 1,
    "given": {
      "game": {"round_number": 5, "leader": 1},
      "players": {
        "1": {"hand": ["H2"]},
        "2": {"hand": ["H4"]},
        "3": {"hand": ["S9"]}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "H2"},
      {"seat": 2, "options_include": "H4"},
      {"seat": 3, "options_include": "S9"}
    ],
    "expect": {
      "players": {
        "1": {"showroom": 0, "score": 0},
        "2": {"showroom": 1, "vault": 0, "score": 1},
        "3": {"showroom": 0, "vault": 0, "score": 0}
      }
    }
  },
  {
    "name": "Trick winner leads the next trick and may lead any card",
    "rule": "R15",
    "players": 3,
    "rounds": 2,
    "given": {
      "game": {"round_number": 5, "leader": 1},
      "players": {
        "1": {"hand": ["H5", "D1"]},
        "2": {"hand": ["H3", "D2"]},
        "3": {"hand": ["H9", "S8", "D3"]}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "H5"},
      {"seat": 3, "options_include": "D3"}
    ],
    "expect": {
      "offered": [{"seat": 3, "option": "S8"}],
      "players": {
        "1": {"showroom": 0, "vault": 0, "score": 0},
        "2": {"showroom": 0, "vault": 0, "score": 0},
        "3": {"showroom": 1, "vault": 1, "score": 3}
      },
      "game": {"round_number": 7}
    }
  },
  {
    "name": "End of hand: strict-most suit actions in order, Clubs tie gives nothing, zero-trick player gets vault +2",
    "rule": "R16",
    "players": 3,
    "rounds": 1,
    "given": {
      "game": {"round_number": 10, "leader": 1},
      "players": {
        "1": {"hand": ["S9"], "showroom": 2, "vault": 0, "score": 2, "won_diamonds": 5, "won_hearts": 2, "won_spades": 4, "won_clubs": 4, "tricks_won": 5},
        "2": {"hand": ["S1"], "showroom": 1, "vault": 0, "score": 1, "won_diamonds": 2, "won_hearts": 5, "won_spades": 1, "won_clubs": 4, "tricks_won": 4},
        "3": {"hand": ["S2"], "showroom": 0, "vault": 0, "score": 0, "won_diamonds": 0, "won_hearts": 0, "won_spades": 0, "won_clubs": 0, "tricks_won": 0}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "S9"},
      {"seat": 2, "options_include": "S1"},
      {"seat": 3, "options_include": "S2"}
    ],
    "expect": {
      "players": {
        "1": {"showroom": 0, "vault": 3, "score": 6},
        "2": {"showroom": 2, "vault": 0, "score": 2},
        "3": {"showroom": 0, "vault": 2, "score": 4}
      },
      "game": {"round_number": 11}
    }
  },
  {
    "name": "End-of-hand Clubs robs the opponent with the larger showroom",
    "rule": "R17",
    "players": 3,
    "rounds": 1,
    "given": {
      "game": {"round_number": 10, "leader": 1},
      "players": {
        "1": {"hand": ["C9"], "showroom": 0, "vault": 0, "score": 0, "won_diamonds": 3, "won_hearts": 3, "won_spades": 3, "won_clubs": 0, "tricks_won": 3},
        "2": {"hand": ["C1"], "showroom": 1, "vault": 0, "score": 1, "won_diamonds": 3, "won_hearts": 3, "won_spades": 3, "won_clubs": 0, "tricks_won": 3},
        "3": {"hand": ["C2"], "showroom": 3, "vault": 0, "score": 3, "won_diamonds": 3, "won_hearts": 3, "won_spades": 3, "won_clubs": 0, "tricks_won": 3}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "C9"},
      {"seat": 1, "options_include": 2},
      {"seat": 2, "options_include": "C1"},
      {"seat": 3, "options_include": "C2"}
    ],
    "expect": {
      "players": {
        "1": {"showroom": 2, "vault": 0, "score": 2},
        "2": {"showroom": 0, "vault": 0, "score": 0},
        "3": {"showroom": 2, "vault": 0, "score": 2}
      }
    }
  },
  {
    "name": "End-of-hand Clubs with tied opponents robs the receiver's left",
    "rule": "R17",
    "players": 3,
    "rounds": 1,
    "given": {
      "game": {"round_number": 10, "leader": 1},
      "players": {
        "1": {"hand": ["C9"], "showroom": 0, "vault": 0, "score": 0, "won_diamonds": 3, "won_hearts": 3, "won_spades": 3, "won_clubs": 0, "tricks_won": 3},
        "2": {"hand": ["C1"], "showroom": 2, "vault": 0, "score": 2, "won_diamonds": 3, "won_hearts": 3, "won_spades": 3, "won_clubs": 0, "tricks_won": 3},
        "3": {"hand": ["C2"], "showroom": 3, "vault": 0, "score": 3, "won_diamonds": 3, "won_hearts": 3, "won_spades": 3, "won_clubs": 0, "tricks_won": 3}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "C9"},
      {"seat": 1, "options_include": 3},
      {"seat": 2, "options_include": "C1"},
      {"seat": 3, "options_include": "C2"}
    ],
    "expect": {
      "players": {
        "1": {"showroom": 2, "vault": 0, "score": 2},
        "2": {"showroom": 1, "vault": 0, "score": 1},
        "3": {"showroom": 2, "vault": 0, "score": 2}
      }
    }
  },
  {
    "name": "Players with zero tricks this hand get vault +2 at the end of the hand",
    "rule": "R18",
    "players": 3,
    "rounds": 1,
    "given": {
      "game": {"round_number": 10, "leader": 1},
      "players": {
        "1": {"hand": ["D9"], "won_diamonds": 0, "won_hearts": 0, "won_spades": 0, "won_clubs": 0, "tricks_won": 9},
        "2": {"hand": ["D1"], "won_diamonds": 0, "won_hearts": 0, "won_spades": 0, "won_clubs": 0, "tricks_won": 0},
        "3": {"hand": ["D2"], "won_diamonds": 0, "won_hearts": 0, "won_spades": 0, "won_clubs": 0, "tricks_won": 0}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "D9"},
      {"seat": 2, "options_include": "D1"},
      {"seat": 3, "options_include": "D2"}
    ],
    "expect": {
      "players": {
        "1": {"showroom": 0, "vault": 2, "score": 4},
        "2": {"showroom": 0, "vault": 2, "score": 4},
        "3": {"showroom": 0, "vault": 2, "score": 4}
      }
    }
  },
  {
    "name": "End of hand reveals the set-aside cards without removing them (only the count is asserted)",
    "rule": "R19",
    "players": 3,
    "rounds": 1,
    "given": {
      "game": {"round_number": 10, "leader": 1, "set_aside": ["D8", "H8", "S8", "C8", "D7", "H7"]},
      "players": {
        "1": {"hand": ["H9"], "tricks_won": 3},
        "2": {"hand": ["H1"], "tricks_won": 3},
        "3": {"hand": ["H2"], "tricks_won": 3}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "H9"},
      {"seat": 2, "options_include": "H1"},
      {"seat": 3, "options_include": "H2"}
    ],
    "expect": {
      "lens": {"game": {"set_aside": 6}},
      "game": {"round_number": 11}
    }
  },
  {
    "name": "Score is 2 x vault + showroom after a Heart gain",
    "rule": "R20",
    "players": 3,
    "rounds": 1,
    "given": {
      "game": {"round_number": 5, "leader": 1},
      "players": {
        "1": {"hand": ["H9"], "showroom": 1, "vault": 2, "score": 5},
        "2": {"hand": ["H1"]},
        "3": {"hand": ["H2"]}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "H9"},
      {"seat": 2, "options_include": "H1"},
      {"seat": 3, "options_include": "H2"}
    ],
    "expect": {
      "players": {"1": {"showroom": 2, "vault": 2, "score": 6}}
    }
  },
  {
    "name": "Game ends after round 30; a score tie is broken by vault",
    "rule": "R21",
    "players": 3,
    "given": {
      "game": {"round_number": 30, "leader": 1},
      "players": {
        "1": {"hand": ["H9"], "showroom": 0, "vault": 1, "score": 2, "won_diamonds": 3, "won_hearts": 3, "won_spades": 3, "won_clubs": 0, "tricks_won": 3},
        "2": {"hand": ["H1"], "showroom": 0, "vault": 2, "score": 4, "won_diamonds": 3, "won_hearts": 3, "won_spades": 3, "won_clubs": 0, "tricks_won": 3},
        "3": {"hand": ["H2"], "showroom": 3, "vault": 0, "score": 3, "won_diamonds": 3, "won_hearts": 3, "won_spades": 3, "won_clubs": 0, "tricks_won": 3}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "H9"},
      {"seat": 2, "options_include": "H1"},
      {"seat": 3, "options_include": "H2"}
    ],
    "expect": {
      "winner": 2,
      "standings": {"1": 401, "2": 402, "3": 300},
      "players": {
        "1": {"showroom": 2, "vault": 1, "score": 4},
        "2": {"showroom": 0, "vault": 2, "score": 4},
        "3": {"showroom": 3, "vault": 0, "score": 3}
      },
      "game": {"round_number": 30}
    }
  },
  {
    "name": "Players level on score and vault share the win",
    "rule": "R22",
    "players": 3,
    "given": {
      "game": {"round_number": 30, "leader": 1},
      "players": {
        "1": {"hand": ["H9"], "showroom": 0, "vault": 1, "score": 2, "won_diamonds": 3, "won_hearts": 3, "won_spades": 3, "won_clubs": 0, "tricks_won": 3},
        "2": {"hand": ["H1"], "showroom": 2, "vault": 1, "score": 4, "won_diamonds": 3, "won_hearts": 3, "won_spades": 3, "won_clubs": 0, "tricks_won": 3},
        "3": {"hand": ["H2"], "showroom": 2, "vault": 1, "score": 4, "won_diamonds": 3, "won_hearts": 3, "won_spades": 3, "won_clubs": 0, "tricks_won": 3}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "H9"},
      {"seat": 2, "options_include": "H1"},
      {"seat": 3, "options_include": "H2"}
    ],
    "expect": {
      "winner": [1, 2, 3],
      "standings": {"1": 401, "2": 401, "3": 401},
      "players": {
        "1": {"showroom": 2, "vault": 1, "score": 4},
        "2": {"showroom": 2, "vault": 1, "score": 4},
        "3": {"showroom": 2, "vault": 1, "score": 4}
      }
    }
  }
]
```
````
