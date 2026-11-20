# One Night Revolution: Ten Nights, Hidden Ledger

5 players play 10 rounds as rotating Rebels and Informants with framing, claims, and termination votes for hidden points.

Players: 5 to 5, best with 5

## Parameters

- `num_players` = 5
- `num_rounds` = 10
- `num_pairs` = 10
- `initial_points` = 0
- `informant_rounds_per_player` = 4
- `rebel_rounds_per_player` = 6
- `rebel_correct_vote_gain` = 2
- `rebel_team_bonus` = 1
- `informant_per_misdirected_gain` = 1
- `informant_survival_gain` = 2
- `termination_min_votes` = 2

## Round

1. **update** (all players): sets each player current_role and partner from pair_order for game.round_number; clears is_terminated, revealed_role, target, vote, investigation_result
2. **sync** (all players): privately sends each player current_role; Informants also receive partner
3. **poll** (all players): sets player.target; Rebel target is investigated and Informant target is framed
4. **update** (all players): sets player.investigation_result to Informant if target current_role is Informant or target was framed by any Informant, else Rebel; Informants keep empty
5. **sync** (all players): privately sends each Rebel investigation_result; Informants receive no result
6. **poll** (all players): sets player.claim_msg and broadcasts to all as Seat {seat} says: {value}
7. **poll** (all players): sets player.response_msg and broadcasts to all as Seat {seat} says: {value}
8. **poll** (all players): sets player.vote
9. **tell** (all players): announces all player.vote showing who voted for whom using vote
10. **update** (all players): sets player.is_terminated: if no seat has 2 or more votes then false for all, else true for seats tied for most votes; sets player.revealed_role to current_role if is_terminated else empty; sets game.terminated_informant_count
11. **tell** (all players): announces player.is_terminated and player.revealed_role for terminated players only
12. **update** (all players): adds hidden points: Rebels who voted for an Informant gain 2 to total_points and rebel_points; if terminated_informant_count >=1 each Rebel gains 1 more to total_points and rebel_points; each Informant gains 1 per Rebel who voted for a Rebel to total_points and informant_points; each Informant with is_terminated false gains 2 to total_points and informant_points; increments game.round_number; nothing about points is announced
13. **check** (all players): continues if game.round_number <= 10, otherwise ends and announces total_points, rebel_points and informant_points

## Ending

- ends when: game.round_number > 10
- ranked by: `you.total_points * 1000000 + you.rebel_points * 1000 + you.informant_points` (the highest wins; players level at the top share the win)
- decided by: standing is total_points, tie-break most rebel_points then most informant_points; highest wins and tied top share the win

## Choices the source did not make

- 5 to 5 players, suggested 5: designer set 5; minimum 5 because 2 Informants versus 3 Rebels plus framing and 2-vote termination needs a minority that can hide; maximum not larger because 10-pair schedule and vote math are built for 5
- simultaneous poll for night, claims, responses and votes: source says simultaneous, so poll with nobody seeing answers until all are in; ask not used because order must not leak
- rank_by you.total_points * 1000000 + you.rebel_points * 1000 + you.informant_points: encodes total first then Rebel points then Informant points as tie-breaks within one arithmetic expression; scaling exceeds max attainable points
- talk kept as two simultaneous polls with broadcast to all: claims and responses give material to reason about and players disagree because Informants want misdirected votes and Rebels want true votes, so following a proposal could cost them

## Simplifications

- pair schedule stored as secret game list pair_order drawn by position each round: to fit shared_deck_draw workaround with remove/append operations and no extra randomness

## Unsupported (needs engine work)

- none
