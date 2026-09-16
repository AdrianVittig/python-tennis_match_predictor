def create_h2h_key(
        player_a_id: int,
        player_b_id: int
) -> tuple[int, int]:
    return (min(player_a_id, player_b_id),
            max(player_a_id, player_b_id))


def get_h2h_record(
        h2h_stats: dict,
        player_a_id: int,
        player_b_id: int
) -> dict:
    key =\
        create_h2h_key(player_a_id, player_b_id)
    if key not in h2h_stats:
        h2h_stats[key] = {
            "matches": 0,
            "wins": {}
        }
    return h2h_stats[key]

def update_h2h(
        h2h_stats: dict,
        winner_id: int,
        loser_id: int
) -> None:
    record = get_h2h_record(
        h2h_stats,
        winner_id,
        loser_id
    )

    record["matches"] += 1

    if winner_id not in record["wins"]:
        record["wins"][winner_id] = 0

    record["wins"][winner_id] += 1

def calculate_h2h_win_rate(
        h2h_stats: dict,
        player_id: int,
        opponent_id: int
) -> float:
    record = get_h2h_record(
        h2h_stats,
        player_id,
        opponent_id
    )
    if record["matches"] == 0:
        return .5
    player_wins = (record["wins"]
                   .get(player_id, 0))
    return player_wins / record["matches"]
