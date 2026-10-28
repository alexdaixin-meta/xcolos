# 01 design

- time: 2026-10-28T03:31:19+00:00 (92.7s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 e6fac0256be5a18a, reply sha256 124e8517d7d514e3

## Sent

````
Original game: Smear
Players in the original: 3 to 8

Original rules:
Deal 10 cards each from 54 cards including two jokers and left bower Jick. Players in order bid the points they will win or pass; highest bidder becomes pitcher and declares trump. Pitcher takes 14-card stock and discards to six, others discard to six, keeping trumps if possible. Pitcher leads trump. Must follow suit led if able, but may play trump instead. Highest of led suit wins unless trumped. Play 6 tricks. Score up to 10 points per deal: High trump, Low trump, Jack, Jick, each Joker, Game by most card points with A=4 K=3 Q=2 J=1 10=10, and 3 for winning trump Three. Pitcher failing bid goes set back and scores zero. First team to 21 over multiple deals wins.
````

## Reply

````
```json
{
  "original_summary": "Smear is a trick-taking card game for 3 to 8 players using a 54-card deck with two jokers and a 'Jick' (the off-colour jack, which counts as trump). Players bid how many of up to 10 point categories they will win; the high bidder picks trump, refills from a stock and leads trump. Six tricks are played, and a pitcher who misses the bid is set back. Play repeats until a team reaches 21.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "Always passing gives up the pitcher's large scores. Always bidding the maximum gets set back often. Choices in bidding, trump choice, ducking and trumping all change who captures the point cards. The open-ended race to 21 gives no fixed seat edge, though bid order matters."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Hand strength from the deal and the stock refill drives a single deal heavily. Skill shows over many deals in bid sizing and card play, but one lucky stock draw can swing a short game."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Judging a bid from a partial hand, card counting, choosing when to duck or trump, and helping the other defenders set the pitcher all leave room to improve. A weak player still collects defender points."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands are hidden and many cards are never dealt. Players must infer who holds the high trump and the trump Three from bids and plays, and plan over the six tricks."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Each point category and the set-back rule follow by arithmetic from the cards captured."
    },
    {
      "criterion": "fits_platform",
      "verdict": "bad",
      "evidence": "Several features break the limits:\n- A 54-card deck with a stock refill and discards for every player.\n- Joker and Jick ranking quirks and seven scoring categories.\n- Six tricks for up to 8 players, giving far more than 4 choices per round.\n- Teams that are never defined.\n- An open-ended race to 21.\nTogether these break the step, choice and attribute limits and leave the length unbounded."
    }
  ],
  "problems": [
    "P1: Too large to build. The 54-card deck, stock refill, discard phase, jokers and Jick, and seven scoring categories exceed the step and attribute limits.",
    "P2: Too many choices per round. Up to 8 players playing 6 tricks, plus sequential bidding, needs far more than 4 choice steps.",
    "P3: Unbounded length. Racing to 21 over an unspecified number of deals, with teams never defined, has no fixed round count.",
    "P4: Seat edge. Sequential bidding order and dealer position are uneven unless every player deals equally often.",
    "P5: Luck. The stock refill and a large swing per deal let the draw dominate a short game.",
    "P6: The all-pass case is undefined. Nothing says what happens if nobody bids."
  ],
  "changes": [
    {
      "what": "Use a 24-card deck: three suits (Red, Blue, Green), ranks 1 to 8. Deal 4 cards to each of 3 players; 12 cards stay undealt and unseen. Drop the stock, discards, jokers and Jick.",
      "why": "Cuts the state to something buildable. The undealt cards keep real uncertainty about which trumps are in play.",
      "fixes": "P1"
    },
    {
      "what": "Fix the game at 3 players with 4 tricks per deal. Bids are sealed and simultaneous (pass, or 2 to 6) and carry a trump suit in the same answer. One round is one trick, and the bid happens in the first trick's round.",
      "why": "Keeps the choice steps to at most 4 per round: one bid poll plus three card plays.",
      "fixes": "P2"
    },
    {
      "what": "Play exactly 9 deals (36 rounds), with the dealer rotating so each player deals 3 times. The highest total wins.",
      "why": "Gives a fixed length and equal dealer exposure. Three-player cutthroat play means one rival's loss is not automatically your gain.",
      "fixes": "P3"
    },
    {
      "what": "Break bid ties by rotating priority: the player after the dealer first, the dealer last.",
      "why": "No seat keeps the tiebreak advantage across the game.",
      "fixes": "P4"
    },
    {
      "what": "Score only High (1), Low (1), Game (1) and the trump Three (3). All are computed from captured piles at the end of the deal, and a deal is worth at most 6 points.",
      "why": "Keeps Smear's signature categories, including the Three bonus, with smaller swings. Nine deals then let bid judgement and card play outweigh any single hand.",
      "fixes": "P5"
    },
    {
      "what": "If all three pass, the dealer is stuck as pitcher at a bid of 2, using the suit the dealer named in the sealed answer.",
      "why": "Defines the all-pass case. It also borrows the 'stick the dealer' tradition so that passing everything is not free.",
      "fixes": "P6"
    },
    {
      "what": "Set-back: a pitcher who scores less than the bid loses points equal to the bid. Defenders always score what they capture.",
      "why": "Keeps the original's set-back so the bid is a real risk. It also gives the two defenders a temporary shared goal.",
      "fixes": "P5"
    }
  ],
  "keeps": [
    "Bidding the number of points you will win, with the high bidder (pitcher) naming trump",
    "The pitcher must lead trump to the first trick",
    "Follow suit if able, but you may trump instead",
    "Scoring categories High, Low, Game (by card points with high cards worth 4/3/2/1) and the 3-point trump Three",
    "A set-back for a pitcher who misses the bid",
    "A cutthroat score race over several deals"
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "A pared-down bid-and-trick core fits within 4 choices and about 14 steps per round. It keeps Smear's hidden hands, bidding risk and point-card fights."
  },
  "variation": {
    "name": "Pocket Smear",
    "summary": "A three-player, nine-deal Smear. Players make sealed bids on a 4-card hand drawn from a 24-card deck, then play four tricks to capture High, Low, Game and the 3-point trump Three. A pitcher who misses the bid is set back.",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "rules": "DECK. 24 cards: three suits (Red, Blue, Green), each with ranks 1 to 8. Card points (used only for Game): 8 = 4, 7 = 3, 6 = 2, 5 = 1, all other ranks 0.\n\nSTRUCTURE. The game is 9 deals. Each deal is 4 rounds, one trick per round, so 36 rounds in total. Player 1 deals deal 1, Player 2 deals deal 2, Player 3 deals deal 3, and so on in rotation, so each player deals 3 times. 'Priority order' for a deal is: the player after the dealer, then the next player, then the dealer.\n\nDEAL (first round of each deal). Shuffle all 24 cards and deal 4 to each player privately. The remaining 12 cards are set aside unseen for the whole deal. Each player sees only their own hand.\n\nBID (first round of each deal, at the same moment). Each player secretly submits:\n(a) a bid, either PASS or a whole number from 2 to 6;\n(b) a suit that is among the suits in their own hand.\nAll bids are revealed together. The highest bid wins, and ties go to the tied player earliest in priority order. That player becomes the PITCHER, the bid becomes the CONTRACT, and the pitcher's named suit becomes TRUMP. If all three pass, the dealer becomes pitcher with a contract of 2, and trump is the suit the dealer named. The pitcher, contract and trump are announced to all.\n\nTRICKS. In each round, three cards are played one at a time, starting with the LEADER and continuing in seat order (1, 2, 3, wrapping around).\n- Leader: in the first trick of a deal, the leader is the pitcher, who must lead a trump card. In later tricks, the leader is whoever won the previous trick, and may lead any card.\n- Following: each later player must play a card of the led suit if they have one, but may instead play a trump even if they hold the led suit. A player with no card of the led suit may play any card.\n- Winning: the trick goes to the highest trump played. If no trump was played, it goes to the highest card of the led suit.\n- Every played card is visible to all. The three cards go face up into the winner's captured pile.\n\nDEAL SCORING (after the 4th trick of each deal). Only cards played this deal count.\n- HIGH (1 point): to the player who captured the highest-ranked trump played.\n- LOW (1 point): to the player who captured the lowest-ranked trump played. This can be the same card as High.\n- GAME (1 point): to the player whose captured pile has the most card points. If players tie for most, nobody scores Game.\n- THREE (3 points): to the player who captured the trump of rank 3, if it was played. If it was undealt, nobody scores it.\nEach player's deal points are the sum of the categories they won, from 0 to 6.\n- Defenders add their deal points to their score.\n- If the pitcher's deal points are at least the contract, the pitcher adds their deal points.\n- Otherwise the pitcher is SET: the pitcher subtracts the contract from their score, and their deal points are not added.\nScores may go negative. Captured piles are cleared and the next deal begins.\n\nNo table talk: players communicate only through bids and cards.\n\nEND. After the 9th deal is scored, the game ends.",
    "objective": "After 9 deals, the player with the highest total score wins. If two or more players tie for the highest total, the game is a draw.",
    "expected_effect": "Bidding becomes a risk judgement under hidden information. With 12 cards undealt, a player holding the trump 6 cannot know whether the 7 and 8 are out. The sealed bid also reveals strength, which defenders then exploit.\n\nThe set-back makes the two defenders temporary allies against the pitcher: trumping the pitcher's lead or feeding a point card to each other. Yet they still compete with each other for the win, so each must judge when helping the other defender hands them the lead.\n\nSimple policies lose:\n- Always passing lets the other players take the large pitcher scores, and still risks being the dealer stuck at 2 points with a weak hand.\n- Always bidding 6 is set back on most hands.\n- Always bidding 2 wins few auctions against opponents who bid what their hands are worth.\n\nNine deals with at most 6 points each, and equal dealing, let careful bidding, counting played trumps, and ducking or trumping at the right moment outweigh single good hands.\n\nTalk is left out on purpose. The two defenders would use it mainly to reveal their hands to each other, which removes the inference from card play that is the heart of the game. Bids and played cards already carry signals that players must read and can bluff with."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 14,
    "choice_steps_per_round": 4,
    "attributes": 16,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 36
  }
}
```
````
