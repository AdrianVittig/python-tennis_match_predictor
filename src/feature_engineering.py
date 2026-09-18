from json.decoder import NaN

import pandas as pd

from src.elo import update_player_elo, update_surface_elo
from src.player_state import (
    get_or_create_player_state,
    calculate_win_rate,
    calculate_recent_form,
    calculate_surface_recent_form,
    update_basic_player_stats,
    update_player_form, calculate_average_service_metrics, update_service_metrics_history,
)
from src.h2h import (
    calculate_h2h_win_rate,
    update_h2h,
)

def add_historical_features(data_frame: pd.DataFrame) -> pd.DataFrame:
    player_stats = {}
    h2h_stats = {}
    for index, row in data_frame.iterrows():
        winner_id = row['winner_id']
        loser_id = row["loser_id"]
        surface = None if pd.isna(row['surface']) else  str(row["surface"])

        winner_state = get_or_create_player_state(
            player_stats,
            winner_id
        )
        loser_state = get_or_create_player_state(
            player_stats,
            loser_id
        )

        winner_service_metrics_before_match = calculate_average_service_metrics(
            winner_state["service_metrics_history"]
        )

        loser_service_metrics_before_match = calculate_average_service_metrics(
            loser_state["service_metrics_history"]
        )

        winner_elo_before_match = winner_state["elo"]
        loser_elo_before_match = loser_state["elo"]
        winner_matches_before_match = winner_state["matches"]
        loser_matches_before_match = loser_state["matches"]

        winner_win_rate = calculate_win_rate(
            winner_state["wins"],
            winner_matches_before_match
        )
        loser_win_rate = calculate_win_rate(
            loser_state["wins"],
            loser_matches_before_match
        )
        winner_recent_form = calculate_recent_form(
            winner_state["recent_results"],
        )
        loser_recent_form = calculate_recent_form(
            loser_state["recent_results"],
        )

        if surface is None:
            winner_surface_specific_form = 0.5
            loser_surface_specific_form = 0.5
            winner_surface_elo_before_match = 1500.0
            loser_surface_elo_before_match = 1500.0
        else:
            winner_surface_specific_form = calculate_surface_recent_form(
                winner_state["surface_recent_results"],
                surface
            )
            loser_surface_specific_form = calculate_surface_recent_form(
                loser_state["surface_recent_results"],
                surface
            )
            winner_surface_elo_before_match = winner_state["surface_elo"][surface]
            loser_surface_elo_before_match = loser_state["surface_elo"][surface]

        winner_h2h_win_rate = calculate_h2h_win_rate(
            h2h_stats,
            winner_id,
            loser_id
        )

        loser_h2h_win_rate = calculate_h2h_win_rate(
            h2h_stats,
            loser_id,
            winner_id
        )

        data_frame.at[index, "winner_elo_before_match"] = winner_elo_before_match
        data_frame.at[index, "loser_elo_before_match"] = loser_elo_before_match

        data_frame.at[index, "winner_matches_before_match"] = winner_matches_before_match
        data_frame.at[index, "loser_matches_before_match"] = loser_matches_before_match

        data_frame.at[index, "winner_win_rate_before_match"] = winner_win_rate
        data_frame.at[index, "loser_win_rate_before_match"] = loser_win_rate

        data_frame.at[index, "winner_recent_form_before_match"] = winner_recent_form
        data_frame.at[index, "loser_recent_form_before_match"] = loser_recent_form

        data_frame.at[index, "winner_surface_form_before_match"] = winner_surface_specific_form
        data_frame.at[index, "loser_surface_form_before_match"] = loser_surface_specific_form

        data_frame.at[index, "winner_surface_elo_before_match"] = winner_surface_elo_before_match
        data_frame.at[index, "loser_surface_elo_before_match"] = loser_surface_elo_before_match

        data_frame.at[index, "winner_h2h_win_rate_before_match"] = winner_h2h_win_rate
        data_frame.at[index, "loser_h2h_win_rate_before_match"] = loser_h2h_win_rate

        data_frame.at[index, "winner_ace_rate_before_match"] = (
            winner_service_metrics_before_match)["ace_rate"]
        data_frame.at[index, "loser_ace_rate_before_match"] = (
            loser_service_metrics_before_match)["ace_rate"]

        data_frame.at[index, "winner_double_fault_rate_before_match"] = (
            winner_service_metrics_before_match)["double_fault_rate"]
        data_frame.at[index, "loser_double_fault_rate_before_match"] = (
            loser_service_metrics_before_match)["double_fault_rate"]

        data_frame.at[index, "winner_first_serve_percentage_before_match"] = (
            winner_service_metrics_before_match)["first_serve_percentage"]
        data_frame.at[index, "loser_first_serve_percentage_before_match"] = (
            loser_service_metrics_before_match)["first_serve_percentage"]

        data_frame.at[index, "winner_first_serve_points_won_percentage_before_match"] = (
            winner_service_metrics_before_match)["first_serve_points_won_percentage"]
        data_frame.at[index, "loser_first_serve_points_won_percentage_before_match"] = (
            loser_service_metrics_before_match)["first_serve_points_won_percentage"]

        data_frame.at[index, "winner_second_serve_points_won_percentage_before_match"] = (
            winner_service_metrics_before_match)["second_serve_points_won_percentage"]
        data_frame.at[index, "loser_second_serve_points_won_percentage_before_match"] = (
            loser_service_metrics_before_match)["second_serve_points_won_percentage"]

        data_frame.at[index, "winner_break_points_saved_percentage_before_match"] = (
            winner_service_metrics_before_match)["break_points_saved_percentage"]
        data_frame.at[index, "loser_break_points_saved_percentage_before_match"] = (
            loser_service_metrics_before_match)["break_points_saved_percentage"]

        new_winner_elo, new_loser_elo = update_player_elo(
            winner_state["elo"],
            loser_state["elo"]
        )

        winner_state["elo"] = new_winner_elo
        loser_state["elo"] = new_loser_elo

        if surface is not None:
            new_winner_surface_elo, new_loser_surface_elo = update_surface_elo(
                winner_state["surface_elo"][surface],
                loser_state["surface_elo"][surface]
            )
            winner_state["surface_elo"][surface] = new_winner_surface_elo
            loser_state["surface_elo"][surface] = new_loser_surface_elo

        update_basic_player_stats(winner_state, True)
        update_basic_player_stats(loser_state, False)

        update_player_form(
            winner_state,
            surface,
            True
        )

        update_player_form(
            loser_state,
            surface,
            False
        )

        update_h2h(h2h_stats, winner_id, loser_id)

        winner_current_service_metrics = calculate_service_metrics(
            row,
            "w"
        )

        loser_current_service_metrics = calculate_service_metrics(
            row,
            "l"
        )

        if winner_current_service_metrics is not None:
            update_service_metrics_history(
                winner_state["service_metrics_history"],
                winner_current_service_metrics
            )

        if loser_current_service_metrics is not None:
            update_service_metrics_history(
                loser_state["service_metrics_history"],
                loser_current_service_metrics
            )

    return data_frame

def determine_player_order(
        winner_id: int,
        loser_id: int
) -> tuple[int, int, int]:
    if winner_id < loser_id:
        player_a_id = winner_id
        player_b_id = loser_id
        target = 1
    else:
        player_a_id = loser_id
        player_b_id = winner_id
        target = 0
    return player_a_id, player_b_id, target

def transform_match_identity(
        row: pd.Series
) -> tuple[int, int, int]:
    winner_id = row["winner_id"]
    loser_id = row["loser_id"]
    return determine_player_order(
        winner_id,
        loser_id
    )

def transform_match_features(
        row: pd.Series
) -> dict:
    player_a_id, player_b_id, target = transform_match_identity(row)

    winner_elo = row["winner_elo_before_match"]
    loser_elo = row["loser_elo_before_match"]

    winner_surface_elo = row["winner_surface_elo_before_match"]
    loser_surface_elo = row["loser_surface_elo_before_match"]

    winner_win_rate = row["winner_win_rate_before_match"]
    loser_win_rate = row["loser_win_rate_before_match"]

    winner_recent_form = row["winner_recent_form_before_match"]
    loser_recent_form = row["loser_recent_form_before_match"]

    winner_surface_form = row["winner_surface_form_before_match"]
    loser_surface_form = row["loser_surface_form_before_match"]

    winner_h2h_win_rate = row["winner_h2h_win_rate_before_match"]
    loser_h2h_win_rate = row["loser_h2h_win_rate_before_match"]

    winner_matches = row["winner_matches_before_match"]
    loser_matches = row["loser_matches_before_match"]

    winner_rank = row["winner_rank"]
    loser_rank = row["loser_rank"]

    winner_ace_rate = row["winner_ace_rate_before_match"]
    loser_ace_rate = row["loser_ace_rate_before_match"]

    winner_double_fault_rate = row["winner_double_fault_rate_before_match"]
    loser_double_fault_rate = row["loser_double_fault_rate_before_match"]

    winner_first_serve_percentage = row["winner_first_serve_percentage_before_match"]
    loser_first_serve_percentage = row["loser_first_serve_percentage_before_match"]

    winner_first_serve_points_won_percentage = row["winner_first_serve_points_won_percentage_before_match"]
    loser_first_serve_points_won_percentage = row["loser_first_serve_points_won_percentage_before_match"]

    winner_second_serve_points_won_percentage = row["winner_second_serve_points_won_percentage_before_match"]
    loser_second_serve_points_won_percentage = row["loser_second_serve_points_won_percentage_before_match"]

    winner_break_points_saved_percentage = row["winner_break_points_saved_percentage_before_match"]
    loser_break_points_saved_percentage = row["loser_break_points_saved_percentage_before_match"]

    winner_features = {
        "elo": winner_elo,
        "surface_elo": winner_surface_elo,
        "win_rate": winner_win_rate,
        "recent_form": winner_recent_form,
        "surface_form": winner_surface_form,
        "h2h_win_rate": winner_h2h_win_rate,
        "matches": winner_matches,
        "rank": winner_rank,
        "ace_rate": winner_ace_rate,
        "double_fault_rate": winner_double_fault_rate,
        "first_serve_percentage": winner_first_serve_percentage,
        "first_serve_points_won_percentage": winner_first_serve_points_won_percentage,
        "second_serve_points_won_percentage": winner_second_serve_points_won_percentage,
        "break_points_saved_percentage": winner_break_points_saved_percentage,
    }

    loser_features = {
        "elo": loser_elo,
        "surface_elo": loser_surface_elo,
        "win_rate": loser_win_rate,
        "recent_form": loser_recent_form,
        "surface_form": loser_surface_form,
        "h2h_win_rate": loser_h2h_win_rate,
        "matches": loser_matches,
        "rank": loser_rank,
        "ace_rate": loser_ace_rate,
        "double_fault_rate": loser_double_fault_rate,
        "first_serve_percentage": loser_first_serve_percentage,
        "first_serve_points_won_percentage": loser_first_serve_points_won_percentage,
        "second_serve_points_won_percentage": loser_second_serve_points_won_percentage,
        "break_points_saved_percentage": loser_break_points_saved_percentage,
    }

    if player_a_id == row["winner_id"]:
        player_a_features = winner_features
        player_b_features = loser_features
    else:
        player_a_features = loser_features
        player_b_features = winner_features

    return {
        "player_a_id": player_a_id,
        "player_b_id": player_b_id,
        "target": target,
        "player_a": player_a_features,
        "player_b": player_b_features,
    }

def build_training_row(
        row: pd.Series
) -> dict:
    match_features = transform_match_features(row)
    player_a = match_features["player_a"]
    player_b = match_features["player_b"]
    elo_difference = player_a["elo"] - player_b["elo"]

    surface_elo_difference = player_a["surface_elo"] - player_b["surface_elo"]

    win_rate_difference = player_a["win_rate"] - player_b["win_rate"]

    recent_form_difference = player_a["recent_form"] - player_b["recent_form"]

    surface_form_difference = player_a["surface_form"] - player_b["surface_form"]

    h2h_difference = player_a["h2h_win_rate"] - player_b["h2h_win_rate"]

    matches_difference = player_a["matches"] - player_b["matches"]

    rank_difference = player_a["rank"] - player_b["rank"]

    ace_rate_difference = player_a["ace_rate"] - player_b["ace_rate"]

    double_fault_rate_difference = (
            player_a["double_fault_rate"] - player_b["double_fault_rate"]
    )

    first_serve_percentage_difference = (
        player_a["first_serve_percentage"] - player_b["first_serve_percentage"]
    )

    first_serve_points_won_percentage_difference = (
        player_a["first_serve_points_won_percentage"]
        - player_b["first_serve_points_won_percentage"]
    )

    second_serve_points_won_percentage_difference = (
        player_a["second_serve_points_won_percentage"]
        - player_b["second_serve_points_won_percentage"]
    )

    break_points_saved_percentage_difference = (
        player_a["break_points_saved_percentage"]
        - player_b["break_points_saved_percentage"]
    )

    return {
        "player_a_id": match_features["player_a_id"],
        "player_b_id": match_features["player_b_id"],
        "target": match_features["target"],
        "tourney_date": row["tourney_date"],
        "elo_difference": elo_difference,
        "surface_elo_difference": surface_elo_difference,
        "win_rate_difference": win_rate_difference,
        "recent_form_difference": recent_form_difference,
        "surface_form_difference": surface_form_difference,
        "h2h_win_rate_difference": h2h_difference,
        "matches_difference": matches_difference,
        "rank_difference": rank_difference,
        "ace_rate_difference": ace_rate_difference,
        "double_fault_rate_difference": double_fault_rate_difference,
        "first_serve_percentage_difference": first_serve_percentage_difference,
        "first_serve_points_won_percentage_difference": first_serve_points_won_percentage_difference,
        "second_serve_points_won_percentage_difference": second_serve_points_won_percentage_difference,
        "break_points_saved_percentage_difference": break_points_saved_percentage_difference
    }

def build_training_dataset(
        data_frame: pd.DataFrame
) -> pd.DataFrame:
    training_rows = []
    for _, row in data_frame.iterrows():
        training_rows.append(build_training_row(row))
    return pd.DataFrame(training_rows)

def calculate_service_metrics(
        row: pd.Series,
        prefix: str
) -> dict[str, float] | None:
    aces = row[f"{prefix}_ace"]
    service_points = row[f"{prefix}_svpt"]

    if pd.isna(service_points) or service_points == 0:
        return None

    double_faults = row[f"{prefix}_df"]
    first_serves_in = row[f"{prefix}_1stIn"]
    first_serve_points_won = row[f"{prefix}_1stWon"]
    second_serve_points_won = row[f"{prefix}_2ndWon"]
    break_points_saved = row[f"{prefix}_bpSaved"]
    break_points_faced = row[f"{prefix}_bpFaced"]

    if pd.isna(aces):
        aces = 0

    if pd.isna(double_faults):
        double_faults = 0

    if pd.isna(first_serves_in):
        first_serves_in = 0

    if pd.isna(first_serve_points_won):
        first_serve_points_won = 0

    if pd.isna(second_serve_points_won):
        second_serve_points_won = 0

    if pd.isna(break_points_saved):
        break_points_saved = 0

    if pd.isna(break_points_faced):
        break_points_faced = 0

    else:
        ace_rate = aces / service_points
        double_fault_rate = double_faults / service_points
        first_serve_percentage = first_serves_in / service_points
        second_serve_points = max(service_points - first_serves_in, 0)

    if first_serves_in == 0:
        first_serve_points_won_percentage = 0
    else:
        first_serve_points_won_percentage = (
                first_serve_points_won / first_serves_in
        )

    if second_serve_points == 0:
        second_serve_points_won_percentage = 0
    else:
        second_serve_points_won_percentage = (
                second_serve_points_won / second_serve_points
        )

    if break_points_faced == 0:
        break_points_saved_percentage = 0
    else:
        break_points_saved_percentage = (
                break_points_saved / break_points_faced
        )

    return {
        "aces": aces,
        "service_points": service_points,
        "double_faults": double_faults,
        "first_serves_in": first_serves_in,
        "first_serve_points_won": first_serve_points_won,
        "second_serve_points_won": second_serve_points_won,
        "break_points_saved": break_points_saved,
        "break_points_faced": break_points_faced,
        "ace_rate": ace_rate,
        "double_fault_rate": double_fault_rate,
        "first_serve_percentage": first_serve_percentage,
        "first_serve_points_won_percentage": first_serve_points_won_percentage,
        "second_serve_points_won_percentage": second_serve_points_won_percentage,
        "break_points_saved_percentage": break_points_saved_percentage,
    }

def calculate_return_metrics(
        row: pd.Series,
        opponent_prefix: str
) -> dict[str, float] | None:
    opponent_service_points = row[f"{opponent_prefix}_svpt"]
    opponent_first_serve_points_won = row[f"{opponent_prefix}_1stWon"]
    opponent_second_serve_points_won = row[f"{opponent_prefix}_2ndWon"]

    if pd.isna(opponent_service_points) or opponent_service_points == 0:
        return None

    if pd.isna(opponent_first_serve_points_won):
        return None

    if pd.isna(opponent_second_serve_points_won):
        return None

    return_points_won = (
        opponent_service_points - opponent_first_serve_points_won
        - opponent_second_serve_points_won
    )

    return_points_won_rate = (
        return_points_won / opponent_service_points
    )

    return {
        "return_points_won": return_points_won,
        "return_points_total": opponent_service_points,
        "return_points_won_rate": return_points_won_rate
    }

