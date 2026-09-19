import pandas as pd

# forecast n weeks for item by using its best performing model (lookup df)
def forecast_demand(df: pd.DataFrame, model_selection_df: pd.DataFrame, item: str, horizon_weeks: int):
    if horizon_weeks <= 0 or horizon_weeks > 12:
        raise ValueError("pred window must be greater than 0 and less than 12 weeks")

    # check if item searched exists
    if item not in df["item"].nunique():
        return (f"item not found in sales history - {item}")
    
