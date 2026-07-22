from square import Square
from square.environment import SquareEnvironment
from square.core.api_error import ApiError
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
import os

load_dotenv()

client = Square(
    environment=SquareEnvironment.PRODUCTION,
    token=os.environ['SQUARE_PROD_ACCESS_TOKEN']
)

try:
    response = client.locations.list()
    for location in response.locations:
        loc_id = location.id
        print(f"{location.id}: ", end="")
        print(f"{location.name}, ", end="")
        print(f"{location.address}, ", end="")

except ApiError as e:
    for error in e.errors:
        print(error.category)
        print(error.code)
        print(error.detail)

try:
    # catalog api
    res = client.catalog.list(types="ITEM,CATEGORY")
    item_count = 0
    for obj in res:
        # print(f'id -> {obj.id}')
        # print(f'type -> {obj.type}')
        if obj.type == "ITEM":
            print(f'item name -> {obj.item_data.name}')
            item_count += 1
            if item_count >= 5:
                break

        if obj.type == "CATEGORY":
            print(f'category name -> {obj.category_data.name}')
                
except ApiError as e:
    for error in e.errors:
        print(error.category)
        print(error.code)
        print(error.detail)


# 2 APIS required for forecasting model
# 1 -> lListCatalog, acts as lookup to what items exist
# 2 -> SearchOrders, every completed transaction, what was sold, how many etc, feeds forecasting model
end_time = datetime.now(timezone.utc).isoformat()
start_time = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()

response = client.orders.search(
    location_ids=[f"{loc_id}"],
    query={
        "filter": {
            "state_filter": {"states": ["COMPLETED"]},
            "date_time_filter": {
                "closed_at": {"start_at": start_time, "end_at": end_time}
            },
        },
    },
    limit=10,
)

print(f'order count in period -> {len(response.orders)}')
for order in response.orders:
    print(f"closed: {order.closed_at}")
    for li in order.line_items:
        print(f"  {li.name} x {li.quantity} — catalog_id: {li.catalog_object_id} \n")

