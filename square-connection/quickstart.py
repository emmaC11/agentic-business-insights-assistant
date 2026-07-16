from square import Square
from square.environment import SquareEnvironment
from square.core.api_error import ApiError
from dotenv import load_dotenv
import os

load_dotenv()

client = Square(
    environment=SquareEnvironment.PRODUCTION,
    token=os.environ['SQUARE_PROD_ACCESS_TOKEN']
)

try:
    response = client.locations.list()
    for location in response.locations:
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

