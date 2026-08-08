import os
from dotenv import load_dotenv
from square.environment import SquareEnvironment
from ingestion.square_client import SquareIngestionClient
from ingestion.storage import save_sales_records

load_dotenv()

token = os.environ['SQUARE_PROD_ACCESS_TOKEN']
account_id = "TestBusinessAcc"

client = SquareIngestionClient(
    token=token,
    env=SquareEnvironment.PRODUCTION
)

# print("Calling catalog_lookup...")
# client.catalog_lookup()
# print("Done.")

# client.fetch_orders("2026-08-01T00:00:00Z", "2026-08-05T00:00:00Z")
records = client.fetch_orders("2025-06-01T00:00:00Z", "2026-06-30T00:00:00Z")
path = save_sales_records(records, account_id=account_id)
print(f"Data saved to: {path}")