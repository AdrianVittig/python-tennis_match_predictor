import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler

from src.data_loader import load_matches
from src.feature_engineering import (
    add_historical_features,
    build_training_dataset,
)


FEATURE_COLUMNS = [
    "elo_difference",
    "surface_elo_difference",
    "rank_difference",
    "win_rate_difference",
    "recent_form_difference",
    "surface_form_difference",
    "h2h_win_rate_difference",
    "matches_difference",
    "ace_rate_difference",
    "double_fault_rate_difference",
    "first_serve_percentage_difference",
    "first_serve_points_won_percentage_difference",
    "second_serve_points_won_percentage_difference",
    "break_points_saved_percentage_difference",
]


data_frames = []

for year in range(2020, 2026):
    file_path = f"data/raw/atp_matches_{year}.csv"
    data_frames.append(load_matches(file_path))


all_matches = pd.concat(
    data_frames,
    ignore_index=True
)

all_matches = all_matches.sort_values(
    by=[
        "tourney_date",
        "tourney_id",
        "match_num",
    ]
).reset_index(drop=True)


all_matches = add_historical_features(all_matches)

training_data_frame = build_training_dataset(all_matches)


training_data_frame = training_data_frame.dropna(
    subset=FEATURE_COLUMNS
)


train_data = training_data_frame[
    training_data_frame["tourney_date"].dt.year < 2024
]

validation_data = training_data_frame[
    training_data_frame["tourney_date"].dt.year == 2024
]

test_data = training_data_frame[
    training_data_frame["tourney_date"].dt.year == 2025
]


X_train = train_data[FEATURE_COLUMNS]
y_train = train_data["target"]

X_validation = validation_data[FEATURE_COLUMNS]
y_validation = validation_data["target"]

X_test = test_data[FEATURE_COLUMNS]
y_test = test_data["target"]


model = Pipeline([
    (
        "scaler",
        StandardScaler()
    ),
    (
        "logistic_regression",
        LogisticRegression(
            max_iter=1000
        )
    ),
])


model.fit(
    X_train,
    y_train
)


validation_predictions = model.predict(
    X_validation
)

validation_accuracy = accuracy_score(
    y_validation,
    validation_predictions
)


validation_baseline_predictions = (
    X_validation["rank_difference"] < 0
).astype(int)

validation_baseline_accuracy = accuracy_score(
    y_validation,
    validation_baseline_predictions
)


test_predictions = model.predict(
    X_test
)

test_accuracy = accuracy_score(
    y_test,
    test_predictions
)


test_baseline_predictions = (
    X_test["rank_difference"] < 0
).astype(int)

test_baseline_accuracy = accuracy_score(
    y_test,
    test_baseline_predictions
)


print("--------------------------------------------------------")
print("TRAINING MATCHES:", len(train_data))
print("VALIDATION MATCHES:", len(validation_data))
print("TEST MATCHES:", len(test_data))

print("--------------------------------------------------------")
print("2024 VALIDATION")
print("Model accuracy:", validation_accuracy)
print("Ranking baseline accuracy:", validation_baseline_accuracy)

print("--------------------------------------------------------")
print("2025 TEST")
print("Model accuracy:", test_accuracy)
print("Ranking baseline accuracy:", test_baseline_accuracy)

print("--------------------------------------------------------")