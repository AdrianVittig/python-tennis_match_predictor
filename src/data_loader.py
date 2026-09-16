import pandas as pd

def load_matches(file_path):
    result = pd.read_csv(file_path)
    result["tourney_date"] = pd.to_datetime(
        result["tourney_date"].astype(str),
        format="%Y%m%d"
    )
    result = result.sort_values(
        by=["tourney_date", "tourney_id", "match_num"]
    ).reset_index(drop=True)
    return result