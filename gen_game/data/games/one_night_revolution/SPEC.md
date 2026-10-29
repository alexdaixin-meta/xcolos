# One Night Revolution: Ten Nights

Five players play ten rounds of hidden roles. Each round a secretly scheduled pair are Informants and the other three are Rebels; players investigate or frame at night, talk twice, then vote, and score points individually.

Players: 5 to 5, best with 5

## Parameters

- `player_count` = 5
- `rounds` = 10
- `possible_pairs` = 10
- `informants_per_round` = 2
- `rebels_per_round` = 3
- `informant_rounds_per_player` = 4
- `rebel_rounds_per_player` = 6
- `starting_points` = 0
- `termination_vote_threshold` = 2
- `rebel_correct_vote_points` = 2
- `rebel_informant_terminated_bonus` = 1
- `informant_points_per_rebel_misvote` = 1
- `informant_max_misvote_points` = 3
- `informant_survival_bonus` = 2
- `messages_per_round` = 2

## Round

1. **update** (all players): round += 1. For every player, reset target, result, claim, response and vote to '', terminated to false, revealed_role to '' and votes_received to 0. Set framed_seats to [] and reset max_votes, informant_terminated and rebel_misvotes.
2. **update** (all players): Let the pair be pair_order[round]. Each seat in the pair gets role = 'Informant' and partner = the other seat of the pair. Every other seat gets role = 'Rebel' and partner = ''.
3. **sync** (all players): Each player privately sees their own role and, if an Informant, their partner.
4. **poll** (all players): Set target. Then, for each Informant, append that Informant's target to framed_seats if it is not already there. Framing the partner has no extra effect.
5. **update** (each Rebel): result = 'Informant' if target.role == 'Informant' or target is in framed_seats; otherwise result = 'Rebel'.
6. **sync** (each Rebel): Each Rebel privately sees their result. Informants receive no result.
7. **poll** (all players): Set claim; broadcast {"to": "all", "text": "Seat {seat} says: {value}"}.
8. **poll** (all players): Set response; broadcast {"to": "all", "text": "Seat {seat} responds: {value}"}.
9. **poll** (all players): Set vote; publicly announce every voter and whom they voted for.
10. **update** (all players): votes_received = number of players whose vote names this seat; max_votes = the highest votes_received.
11. **update** (all players): If max_votes >= 2, then terminated = true for each player with votes_received == max_votes. For each terminated player, revealed_role = role. informant_terminated = true if any terminated player has role 'Informant'. Announce the revealed roles of terminated players only.
12. **update** (all players): rebel_misvotes = number of Rebels whose vote names a Rebel. Each Rebel gains g = (2 if their vote names an Informant else 0) + (1 if informant_terminated else 0); score += g and rebel_points += g. Each Informant gains g = rebel_misvotes + (2 if not informant_terminated else 0); score += g and informant_points += g.
13. **tell** (all players): Announce every player's score, rebel_points and informant_points.
14. **check** (all players): If round >= 10, end the game; otherwise run the next round. No one is ever removed from play.

## Ending

- ends when: round >= 10
- ranked by: `you.score * 10000 + you.rebel_points * 100 + you.informant_points` (the highest wins; players level at the top share the win)
- decided by: Highest total points wins. Ties are broken by most Rebel points, then by most Informant points. Players still level share the result, which counts as the draw.

## Choices the source did not make

- Exactly 5 players (min = max = suggested = 5): The designer fixed 5. The schedule of 10 pairs over 10 rounds, with each player an Informant 4 times and partnered with everyone once, only works with 5 seats. Five also leaves 3 Rebels, enough for a 2-Informant minority to hide in.
- Keep both talk phases as simultaneous polls broadcast to all: The rules make both message phases simultaneous. Talk matters because Informants want Rebels to misvote while Rebels want to find the Informants, so following a claim can cost a player.
- rebel_points and informant_points are public: The rules announce everyone's totals and use these sub-totals as tie-breaks; making them public is the plainest reading.
- Rank expression score*10000 + rebel_points*100 + informant_points: Each sub-total stays well below 100 over 10 rounds, so the weights keep the order: score first, then Rebel points, then Informant points. Players still level share the win, which is the draw.
- Player strategy: Rebels compare results and claims, knowing a 'Rebel' result is always true while an 'Informant' result may be a frame. Informants frame Rebels and coordinate a story with their partner. Everyone tracks past pairings, since each pair is Informants only once.

## Simplifications

- The secret schedule is stored as a hidden table list pair_order, and roles are recomputed from it each round: The engine needs the schedule as stated state; this is the rule's own mechanism.
- Which players were framed is kept in a hidden table list framed_seats rather than on each player: A player attribute cannot be hidden from its owner, and a framed player must not learn of the frame; a table list with visibility none keeps it secret.
- Per-round scratch values (votes_received, max_votes, informant_terminated, rebel_misvotes) are held as attributes: The engine computes termination and scoring by arithmetic on stated attributes.

## Unsupported (needs engine work)

- none
