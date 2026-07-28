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

        # define ds type & initialize
        categories: dict[str, str] = {}
        items: dict[str, str] = {}
        variations: dict[str, str] = {}

        for obj in self._client.catalog.list(
            types="ITEM,ITEM_VARIATION,CATEGORY"
        ):

            # print('call reaching endpoint')
            # print(f'catalog object -> \n {obj}')
            # print(f'catalog object type -> {obj.type}')
            # if obj.type == "CATEGORY":
            #     print(f'catalog category -> {obj}')
            #     if count >= 1:
            #         break
            #     count += 1

            # if obj.type == "ITEM":
                # print(f'catalog item -> \n {obj}')
                # if count >= 1:
                #     break
                # count += 1

            if obj.type == "ITEM_VARIATION":
                print(f'catalog item variation \n -> {obj}')
                if count == 1:
                    break
                count += 1
        


