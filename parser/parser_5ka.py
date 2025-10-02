from pyaterochka_api import PyaterochkaAPI, PurchaseMode
import asyncio
import json
import os
from tqdm import tqdm
import time
from pathlib import Path
import re

base_path = "/home/mikhail/Documents/Хакатоны/X5_ner_MiLky_way/parser/parsed_catalog_5ka"

async def main():
    async with PyaterochkaAPI(proxy="") as API:
        with open("/home/mikhail/Documents/Хакатоны/X5_ner_MiLky_way/parser/5ka_catalog.json", 'r') as f:
            catalog = json.load(f)
        folder = Path(base_path)
        pattern = re.compile(r"^brands_(.+)_(.+)\.json$")
        category_names = set()
        for file in folder.glob("brands_*.json"):
            match = pattern.match(file.name)
            if match:
                category_name = match.group(1)
                category_id = match.group(2)
                category_names.add(category_name)
        for lvl1 in range(len(catalog)):
            for lvl2 in range(len(catalog[lvl1]['categories'])):
                await asyncio.sleep(2)
                category_id = catalog[lvl1]['categories'][lvl2]['id']
                category_name = catalog[lvl1]['categories'][lvl2]['name']
                if category_name in category_names:
                    continue
                items_raw = await API.Catalog.products_list(category_id, limit=499)
                try:
                    items = items_raw.json()
                except Exception as msg:
                    print(f'items: {str(items_raw)[:100]}')
                    print(f"Got an error in items_raw.json(), msg: {msg} in {category_name}, \
                          id: {category_id}, status code: {items_raw.status_code}")
                    continue
                
                try:
                    # запишем бренды только 1 раз
                    file_name = f'brands_{category_name}_{category_id}.json'
                    file_path = os.path.join(base_path, file_name)
                    if not os.path.exists(file_path):
                        with open(file_path, encoding="utf-8", mode="w+") as f:
                            json.dump(items["filters"][1]["list_values"]["all"], f, ensure_ascii=False, indent=4)
                            print(f"Wrote file {file_name}")
                    else:
                        print(f"File {file_name} already exists — skipped.")
                except Exception as msg:
                    print(f"Got an error in brands, msg: {msg} in {category_name}, id: {category_id}")
                    continue
                
                try:
                    #запишем продукты
                    file_name = f'products_list_{category_name}_{category_id}.json'
                    file_path = os.path.join(base_path, file_name)
                    if not os.path.exists(file_path):
                        products_to_json = []
                        for i in range(len(items["products"])):
                            product = items["products"][i]
                            product_json = {"product_info": {
                                "plu": product["plu"],
                                "name": product["name"],
                                "property": product["property_clarification"]
                                } 
                            }
                            products_to_json.append(product_json)
                        products_list_json = {
                            "category_id": category_id,
                            "category_name": category_name,
                            "products_list": products_to_json
                        }

                        with open(file_path, encoding="utf-8", mode="w+") as f:
                            json.dump(products_list_json, f, ensure_ascii=False, indent=4)
                            print(f"Wrote file {file_name}")
                    else:
                        print(f"File {file_name} already exists — skipped.")
                except Exception as msg:
                    print(f"Got an error in products_list, msg: {msg} in {category_name}, id: {category_id}")
                    continue


if __name__ == '__main__':
    asyncio.run(main())