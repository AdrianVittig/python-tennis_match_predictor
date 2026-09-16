def validate_required_columns(data_frame):
    required_columns = [
        "tourney_id",
        "tourney_date",
        "surface",
        "match_num",
        "winner_id",
        "winner_name",
        "loser_id",
        "loser_name",
        "winner_rank",
        "loser_rank"
    ]
    for column in required_columns:
        if column not in data_frame.columns:
            raise ValueError(f"Missing required column: {column}")