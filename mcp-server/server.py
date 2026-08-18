from mcp.server import MCPServer
from pathlib import Path
import pandas as pd

mcp = MCPServer("agentic-business-insights")

_REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = _REPO_ROOT / "data"

def load_weekly(account_id: str) -> pd.DataFrame:
    path = DATA_DIR / account_id / "sales_weekly.parquet"
    if not path.exists():
        raise FileNotFoundError(f"cannot find weekly parquet for {account_id}")
    df = pd.read_parquet(path)
    return df

if __name__ == "__main__":
    mcp.run()