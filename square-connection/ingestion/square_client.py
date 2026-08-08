from square import Square
from square.environment import SquareEnvironment
from square.core.api_error import ApiError
from datetime import datetime, timedelta, timezone
from ingestion.sales_data_model import SalesRecord
import logging
import os

logger = logging.getLogger(__name__)

class SquareIngestionClient:
    def __init__(self, token, env):
        self._client = Square(environment=env, token=token)
        self.account_id = "TestBusinessAcc"
        self.loc = [os.environ['LOCATION_ID']]


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

        # build lookup to create item & cat relationship
        lookup: dict = {}
        for var_id, item_id in variations.items():
            item_info = items.get(item_id, {})
            cat_id = item_info.get("cat_id")
            lookup[var_id] = {
                "item": item_info.get("name", "NA"),
                "category": categories.get(cat_id, "uncategorised")
            }

        return lookup

    def fetch_orders(self, startDate, endDate) -> list[SalesRecord]:
        """
        pull all completed orders between date ranges passed & return a SalesRecord object
        """

        # fetch catalog items
        catalog = self.catalog_lookup()

        # temp hardcoded 
        # startDate = "2026-08-01T00:00:00Z"
        # endDate = "2026-08-05T00:00:00Z"

        sales_records: list[SalesRecord] = []
        page = 0

        while True:
            body: dict = {
                "location_ids": self.loc,
                "query": {
                    "filter": {
                        "state_filter": {"states": ["COMPLETED"]},
                        "date_time_filter": {
                            "closed_at": {"start_at": startDate, "end_at": endDate}
                        },
                    },
                    "sort": {"sort_field": "CLOSED_AT", "sort_order": "ASC"},
                },
                "limit": 500,
            }

            # used claude to help build this logic
            response = self._client.orders.search(**body)
            page += 1
            orders = getattr(response, "orders", None) or []

            for order in orders:
                closed_at = getattr(order, "closed_at", None)
                if not closed_at:
                    continue

                order_date  = datetime.fromisoformat(closed_at.replace("Z", "+00:00"))
                location_id = getattr(order, "location_id", "unknown")

                for li in (getattr(order, "line_items", None) or []):
                    if getattr(li, "item_type", None) != "ITEM":
                        continue 

                    var_id = getattr(li, "catalog_object_id", None)
                    entry  = catalog.get(var_id, {}) if var_id else {}

                    item_name = entry.get("item") or getattr(li, "name", None) or "Unknown"
                    category  = entry.get("category", "Uncategorised")

                    try:
                        qty = float(getattr(li, "quantity", "0") or "0")
                    except ValueError:
                        qty = 0.0

                    gross = getattr(li, "gross_sales_money", None)
                    base  = getattr(li, "base_price_money", None)
                    if gross and qty > 0:
                        price_cents = round((getattr(gross, "amount", 0) or 0) / qty)
                    elif base:
                        price_cents = getattr(base, "amount", 0) or 0
                    else:
                        price_cents = 0

                    # create new sales record with order info
                    sales_records.append(SalesRecord(
                        account_id=self.account_id,
                        location_id=location_id,
                        item=item_name,
                        category=category,
                        date=order_date,
                        quantity=qty,
                        price_cents=price_cents,
                    ))

            cursor = getattr(response, "cursor", None)
            if not cursor:
                break

        return sales_records
        


