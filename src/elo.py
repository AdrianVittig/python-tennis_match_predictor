K_FACTOR = 48

def calculate_expected_score(
        player_elo: float,
        opponent_elo: float
                             ) -> float:
    return 1 / (1 + 10 ** ((opponent_elo - player_elo) / 400))

def calculate_new_elo(old_elo: float,
                      opponent_elo: float,
                      actual_score: float
                      ) -> float:
    expected_score = calculate_expected_score(old_elo, opponent_elo)
    new_elo = old_elo + K_FACTOR * (actual_score - expected_score)
    return new_elo

def update_player_elo(
        winner_elo: float,
        loser_elo: float
) -> tuple[float, float]:
    new_winner_elo = calculate_new_elo(winner_elo, loser_elo, 1)
    new_loser_elo = calculate_new_elo(loser_elo, winner_elo, 0)
    return new_winner_elo, new_loser_elo

def update_surface_elo(
        winner_surface_elo: float,
        loser_surface_elo: float
) -> tuple[float, float]:
    return update_player_elo(
        winner_surface_elo,
        loser_surface_elo
    )