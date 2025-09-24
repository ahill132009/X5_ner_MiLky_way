from perekrestok_api import PerekrestokAPI
from perekrestok_api import abstraction
import json

def main():
    with PerekrestokAPI() as Api:
        # geopos_handler = Api.Geolocation.current()
        # geopos = geopos_handler.json()
        # print(f'Текущий город сессии {geopos["content"]["city"]["name"]} ({geopos["content"]["city"]["id"]})')

        # # Получаем список категорий
        # categories = Api.Catalog.tree()
        # cat = categories.json()
        # print(f'Список категорий: {len(cat["content"]["items"])}')
        # with open('./parser/parse_perek_categories.json', 'w+', encoding="utf-8") as f:
        #     json.dump(cat["content"]["items"], f, indent=4, ensure_ascii=False) 

        # # Выводим первую категорию
        # cat_name = cat["content"]["items"][1]["category"]["title"]
        # cat_id = cat["content"]["items"][1]["category"]["id"]
        # print(f'Категория: {cat_name}, id: ({cat_id})')
        cat_name = "молочка"
        cat_id = 113

        filter = abstraction.CatalogFeedFilter()
        filter.CATEGORY_ID = cat_id
        products = Api.Catalog.feed(filter=filter, page=1)
        response_items = products.json()

        with open(f'./parser/parse_perek_{cat_name}_milk.json', 'w+', encoding="utf-8") as f:
            json.dump(response_items, f, indent=4, ensure_ascii=False) 

if __name__ == "__main__":
    main()