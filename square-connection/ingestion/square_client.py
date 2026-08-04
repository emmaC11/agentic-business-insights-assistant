from square import Square
from square.environment import SquareEnvironment
from square.core.api_error import ApiError
from datetime import datetime, timedelta, timezone
from ingestion.sales_data_model import SalesRecord
import logging

logger = logging.getLogger(__name__)

class SquareIngestionClient:
    def __init__(self, token, env):
        self._client = Square(environment=env, token=token)


    def catalog_lookup(self) -> dict:
        count = 0
        """
        create connection between items & categories -> {"item": name, "category": name}
        need to create lookup as they are not returned in the same API
        call once & cache in __init__
        """

        """
        obj.type == 
        """

        # define ds type & initialize
        categories: dict[str, str] = {} # {cat_id: category}
        items: dict[str, str] = {} # {item_name: cat_id}
        variations: dict[str, str] = {} #{var_id: item_id}

        for obj in self._client.catalog.list(
            types="ITEM,ITEM_VARIATION,CATEGORY"
        ):

            # categories
            # populates category dict with id & cat name
            if obj.type == "CATEGORY":
                cat_data = getattr(obj, "category_data", None)
                if cat_data:
                    categories[obj.id] = cat_data.name

            # items
            # populates item dict with item name & cat id
            if obj.type == "ITEM":
                item_data = getattr(obj, "item_data", None)
                cats = getattr(item_data, "categories", None)
                if cats:
                    cat_id = cats[0].id
                else:
                    None
                items[obj.id] = {"name": item_data.name, "cat_id": cat_id}
     

            # item variations
            # populates variations dict with mapping of variation ID to parent item ID
            if obj.type == "ITEM_VARIATION":
                var_data = getattr(obj, "item_variation_data", None)
                if var_data:
                    item_id = getattr(var_data, "item_id", None)
                    variations[obj.id] = item_id


        # print(categories)
        # print(len(categories))
        print(variations)
        


