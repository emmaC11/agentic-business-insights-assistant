# connects our 3 isolated components - metrics, split & baselines
# uses our parquet & outputs analysis of models invoked and which one is best performing / wins "contest"

import pandas as pd
from pathlib import Path
from models.split import split_dataset, TEST_WEEKS
from models.baselines import naive, moving_average
from models.metrics import mae_calc, mape_calc

_REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = _REPO_ROOT / "data"
MODELS = {
    # model name + fn
    "naive": naive,
    "moving_average":moving_average
}

def main():
    # load weekly parq as df
    path = DATA_DIR / "TestBusinessAcc" / "sales_weekly.parquet" # replace hardcoded acc name
    df = pd.read_parquet(path)

    # filter regular tier items only - models can only train on dataset w regular sales
    regular_items = df[df["tier"] == "regular"]
    items = regular_items["item"].unique()
    print(f"loaded {len(regular_items)} rows, w {len(items)} unique items")

    rows = []
    for item in items:
        # 1 - find item in df, convert to numpy array (external components expect this dt), split into train & test
        item_df = regular_items[regular_items["item"] == item].sort_values("week_start")
        quantities = item_df["quantity"].to_numpy()
        train, test = split_dataset(quantities)

        # 2 - invoke model
        for model_name, model_fn in MODELS.items():
            pred = model_fn(train, h=TEST_WEEKS)
            item_mape = mape_calc(test, pred)
            item_mae = mae_calc(test, pred)

            # one row for each item
            rows.append({
                "item": item,
                "model": model_name,
                "mape": item_mape,
                "mae": item_mae
            })

    # 3 - save output to df for analysis & provide summary
    model_invocation_results = pd.DataFrame(rows)
    out_dir = _REPO_ROOT / "data" / "TestBusinessAcc" / "models" # replace hardcoded acc name
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "run_contest_results.parquet"
    model_invocation_results.to_parquet(out_path)

    # 4 - summary
    for model_name in MODELS:
        subset = model_invocation_results[(model_invocation_results["model"] == model_name)]
        print(f"\n{model_name}: n={len(subset)}")
        print(f"mean MAPE: {subset['mape'].mean():.4f} ({subset['mape'].mean() * 100:.2f}%)")
        print(f"mean MAE:  {subset['mae'].mean():.2f} units")

if __name__ == "__main__":
    main()
  



