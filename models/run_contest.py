# connects our 3 isolated components - metrics, split & baselines
# uses our parquet & outputs analysis of models invoked and which one is best performing / wins "contest"

import pandas as pd
from pathlib import Path
from models.split import split_dataset, TEST_WEEKS
from models.baselines import naive
from models.metrics import mae_calc, mape_calc

_REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = _REPO_ROOT / "data"

def model_analysis():
    # load weekly parq as df
    path = DATA_DIR / "TestBusinessAcc" / "sales_weekly.parquet" # replace hardcoded acc name
    df = pd.read_parquet(path)

    # filter regular tier items only - models can only train on dataset w regular sales
    regular_items = df[df["tier"] == "regular"]
    items = regular_items["item"].unique()
    print(f"loaded {len(regular_items)} rows, w {len(items)} unique items")


