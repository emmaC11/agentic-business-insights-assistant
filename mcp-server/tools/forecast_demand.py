import pandas as pd
import numpy as np
from models.baselines import naive, moving_average, ets

MODELS = {
    "naive": naive,
    "moving_average": moving_average,
    "ets": ets,
}

# forecast n weeks for item by using its best performing model (lookup df)
def forecast_demand(df: pd.DataFrame, model_selection_df: pd.DataFrame, item: str, horizon_weeks: int):
    if horizon_weeks <= 0 or horizon_weeks > 12:
        raise ValueError("pred window must be greater than 0 and less than 12 weeks")

    # check if item searched exists
    if item not in df["item"].unique():
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
        df[df["item"] == item]
        .sort_values("week_start")["quantity"] # target
        .to_numpy()
    )

    models_fn = MODELS[model_name]
    pred = models_fn(full_series, h=horizon_weeks)

    # round pred, cannot have a decimal of an item 
    pred_rounded = np.round(pred).astype(int)
    total = int(pred_rounded.sum())

    weekly_pred = ''
    for week, qty in enumerate(pred_rounded):
        weekly_pred += (f"\n -week {week + 1}: {qty} units")

    return (
        f"Forecast for {item} - next {horizon_weeks} weeks:"
        f"{weekly_pred}"
        f"-Total: {total} units"
        f"-Model: {model_name} (MAPE: {mape * 100:.2f}%, MAE: {mae} units)"
    )
    
