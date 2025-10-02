from perekrestok_api import PerekrestokAPI
from perekrestok_api import abstraction
import json
import time
from logger import setup_logger


def fetch_items(api, cat_id):
    # Получаем список товаров
    page = 1
    filter = abstraction.CatalogFeedFilter()
    filter.CATEGORY_ID = cat_id
    while page < 10_000:
        products = api.Catalog.feed(filter=filter, page=page)
        response_items = products.json()
        for item in response_items["content"]["items"]:
            try:
                yield {
                    "title": item["title"], 
                    "masterData": {
                        "slug": item["masterData"]["slug"],
                        "plu": item["masterData"]["plu"],
                        "unitName": item["masterData"]["unitName"],
                        "weight": item["masterData"]["weight"],
                        "volume": item["masterData"]["volume"]
                    },
                    "primaryCategory": {
                        "title": item["primaryCategory"]["title"],
                        "id": item["primaryCategory"]["id"]
                    }
                    }
            except:
                logger.warning(f"json failed for item {item['title']}")
                yield {}
        if response_items["content"]["paginator"]["nextPageExists"] == False:
            break
        time.sleep(1)
        page += 1


def main():
    with PerekrestokAPI() as Api:
        logger = setup_logger()
        # geopos_handler = Api.Geolocation.current()
        # geopos = geopos_handler.json()
        # print(f'Текущий город сессии {geopos["content"]["city"]["name"]} ({geopos["content"]["city"]["id"]})')
    

        # Получаем список категорий
        categories = Api.Catalog.tree()
        categories = categories.json()
        for i_cat in range(len(categories["content"]["items"])):
            cat_name = categories["content"]["items"][i_cat]["category"]["title"]
            cat_id = categories["content"]["items"][i_cat]["category"]["id"]
            logger.debug(f"start logging for cat_name:cat_id -> {cat_name}:{cat_id}")

        
            items_for_category = []
            for item in fetch_items(Api, cat_id):
                items_for_category.append(item)
            
            wrapped = {f"cat_name": {
                "cat_id": cat_id,
                "items": items_for_category
            }
                       }
            with open(f'./parser/parsed_catalog_perek/parse_perek_{cat_name}_items.json', 'w+', encoding="utf-8") as f:
                json.dump(wrapped, f, indent=4, ensure_ascii=False) 
            logger.debug(f"saved itemd for {cat_name}")


if __name__ == "__main__":
    main()