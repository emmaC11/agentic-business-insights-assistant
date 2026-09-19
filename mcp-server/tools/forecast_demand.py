import pandas as pd

# forecast n weeks for item by using its best performing model (lookup df)
def forecast_demand(df: pd.DataFrame, model_selection_df: pd.DataFrame, item: str, horizon_weeks: int):
    if horizon_weeks <= 0 or horizon_weeks > 12:
        raise ValueError("pred window must be greater than 0 and less than 12 weeks")

    # check if item searched exists
    if item not in df["item"].nunique():
        return (f"item not found in sales history - {item}")

    # check item is in regular tier (baseline models built using 'regular' tier)
    tier = df[df["item"] == item]["tier"].iloc[0] # return raw string over pandas series
    if tier != "regular":
        return (f"item is not in regualr tier, only items in regualr tiers can be forecasted") # add tool to fetch regular tiered items?

    # use lookup df to get model outputs for specific item
    item_model_row = model_selection_df[model_selection_df["item"] == item]
    model_name = item_model_row["model_winner"]
    mape = item_model_row["mape"]
    mae = item_model_row["mae"]

    # refit/retrain model w full 58 week history -> train - 50, test - 8
    full_series = (
        df[df["item" == item]]
        .sort_values("week_start")["quanitity"] # target
        .to_numpy()
    )

    models_fn = model_name
    pred = models_fn(full_series, h=horizon_weeks)
    
