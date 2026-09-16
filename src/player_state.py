def create_player_state() -> dict:
    return {
        "matches": 0,
        "wins": 0,
        "elo": 1500.0,
        "surface_elo": {
            "Hard": 1500.0,
            "Clay": 1500.0,
            "Grass": 1500.0,
        },
        "recent_results": [],
        "surface_recent_results": {
            "Hard": [],
            "Clay": [],
            "Grass": [],
        },
        "service_metrics_history": [],
    }

def get_or_create_player_state(
        player_stats: dict,
        player_id: int
) -> dict:
    if player_id not in player_stats:
        player_stats[player_id] = create_player_state()

    return player_stats[player_id]

def calculate_win_rate(
        wins: int,
        matches: int
) -> float:
    if matches == 0:
        return .5
    return wins / matches

def calculate_recent_form(
    recent_results: list[int],
    window: int = 10
) -> float:
    recent = recent_results[-window:]
    if not recent:
        return 0.5
    return sum(recent) / len(recent)

def calculate_surface_win_rate(
        surface_wins: int,
        surface_matches: int
) -> float:
    if surface_matches == 0:
        return .5
    return surface_wins / surface_matches


def update_basic_player_stats(
        player_state: dict,
        won: bool
) -> None:
    player_state["matches"] += 1
    if won:
        player_state["wins"] += 1


def update_recent_results(
        recent_results: list[int],
        result: int,
        max_size: int = 20
) -> None:
    recent_results.append(result)
    if len(recent_results) > max_size:
        recent_results.pop(0)

def update_surface_recent_results(
        surface_results: dict[str, list[int]],
        surface: str,
        result: int,
        max_size: int = 20
) -> None:
    surface_recent = surface_results[surface]
    surface_recent.append(result)
    if len(surface_recent) > max_size:
        surface_recent.pop(0)

def calculate_surface_recent_form(
        surface_results: dict[str, list[int]],
        surface: str,
        window: int = 10
) -> float:
    surface_recent = surface_results[surface]
    return calculate_recent_form(surface_recent, window)

def update_player_form(
        player_state: dict,
        surface: str | None,
        won: bool
) -> None:
    result = 1 if won else 0

    update_recent_results(
        player_state["recent_results"],
        result
    )

    if surface is not None:
        update_surface_recent_results(
            player_state["surface_recent_results"],
            surface,
            result
        )


def calculate_average_service_metrics(
        service_metrics_history: list[dict[str, float]],
        window: int = 10
) -> dict[str, float]:
    recent_metrics = service_metrics_history[-window:]
    if len(recent_metrics) == 0:
        return {
            "ace_rate": 0.0,
            "double_fault_rate": 0.0,
            "first_serve_percentage": 0.0,
            "first_serve_points_won_percentage": 0.0,
            "second_serve_points_won_percentage": 0.0,
            "break_points_saved_percentage": 0.0,
        }

    total_aces = sum(
        match["aces"]
        for match in recent_metrics
    )

    total_service_points = sum(
        match["service_points"]
        for match in recent_metrics
    )

    if total_service_points == 0:
        average_ace_rate = 0.0
    else:
        average_ace_rate = total_aces / total_service_points

    total_double_faults = sum(
        match["double_faults"]
        for match in recent_metrics
    )

    if total_service_points == 0:
        average_double_fault_rate = 0.0
    else:
        average_double_fault_rate = (
                total_double_faults / total_service_points
        )

    total_first_serves_in = sum(
        match["first_serves_in"]
        for match in recent_metrics
    )

    if total_service_points == 0:
        average_first_serve_percentage = 0.0
    else:
        average_first_serve_percentage = (
                total_first_serves_in / total_service_points
        )

    total_first_serve_points_won = sum(
        match["first_serve_points_won"]
        for match in recent_metrics
    )

    if total_first_serves_in == 0:
        average_first_serve_points_won_percentage = 0.0
    else:
        average_first_serve_points_won_percentage = (
                total_first_serve_points_won
                / total_first_serves_in
        )

    total_second_serve_points = (
            total_service_points - total_first_serves_in
    )

    total_second_serve_points_won = sum(
        match["second_serve_points_won"]
        for match in recent_metrics
    )

    if total_second_serve_points == 0:
        average_second_serve_points_won_percentage = 0.0
    else:
        average_second_serve_points_won_percentage = (
                total_second_serve_points_won
                / total_second_serve_points
        )

    total_break_points_saved = sum(
        match["break_points_saved"]
        for match in recent_metrics
    )

    total_break_points_faced = sum(
        match["break_points_faced"]
        for match in recent_metrics
    )

    if total_break_points_faced == 0:
        average_break_points_saved_percentage = 0.0
    else:
        average_break_points_saved_percentage = (
                total_break_points_saved
                / total_break_points_faced
        )

    return {
        "ace_rate": average_ace_rate,
        "double_fault_rate": average_double_fault_rate,
        "first_serve_percentage": average_first_serve_percentage,
        "first_serve_points_won_percentage": average_first_serve_points_won_percentage,
        "second_serve_points_won_percentage": average_second_serve_points_won_percentage,
        "break_points_saved_percentage": average_break_points_saved_percentage,
    }

def update_service_metrics_history(
        service_metrics_history: list[dict[str, float]],
        service_metrics: dict[str, float],
        max_size: int = 20
) -> None:
    service_metrics_history.append(service_metrics)

    if len(service_metrics_history) > max_size:
        service_metrics_history.pop(0)
