import os
from dotenv import load_dotenv
from square.environment import SquareEnvironment
from ingestion.square_client import SquareIngestionClient

load_dotenv()

token = os.environ['SQUARE_PROD_ACCESS_TOKEN']

client = SquareIngestionClient(
    token=token,
    env=SquareEnvironment.PRODUCTION
)

# print("Calling catalog_lookup...")
# client.catalog_lookup()
# print("Done.")

client.fetch_orders("2026-08-01T00:00:00Z", "2026-08-05T00:00:00Z")