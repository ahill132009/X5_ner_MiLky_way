from pyaterochka_api import PyaterochkaAPI, PurchaseMode
import asyncio


async def main():
    async with PyaterochkaAPI(proxy="") as API:
        # RUS: Вводим геоточку (самого магазина или рядом с ним) и получаем инфу о магазине
        # ENG: Enter a geolocation (of the store or near it) and get info about the store
        # find_store = await API.find_store(longitude=37.63156, latitude=55.73768)
        # print(f"Store info output: {find_store!s:.100s}...\n")

        # RUS: Выводит список всех категорий на сайте
        # ENG: Outputs a list of all categories on the site
        catalog = await API.Catalog.tree(subcategories=True, mode=PurchaseMode.DELIVERY)
        rjson = catalog.json()
        print(f"Categories list output: {catalog!s:.100s}...\n")

        # RUS: Выводит список всех товаров выбранной категории (ограничение 100 элементов, если превышает - запрашивайте через дополнительные страницы)
        # ENG: Outputs a list of all items in the selected category (limiting to 100 elements, if exceeds - request through additional pages)
        # Страниц не сущетвует, использовать желаемый лимит (до 499) / Pages do not exist, use the desired limit (up to 499)
        items = await API.Catalog.products_list(rjson[0]['id'], limit=5)
        print(f"Items list output: {items!s:.100s}...\n")

        # RUS: Выводит информацию о товаре (по его plu - id товара).
        # Функция в первый раз достаточно долгая, порядка 5-9 секунды, последующие запросы около 2 секунд (если браузер не был закрыт)
        # ENG: Outputs information about the product (by its plu - product id).
        # The function is quite long the first time, about 5-9 seconds, subsequent requests take about 2 seconds (if the browser was not closed)
        info = await API.Catalog.Product.info(43347)
        print(f"Product output: {info["props"]["pageProps"]["props"]['productStore']!s:.100s}...\n")

        # RUS: Влияет исключительно на функцию выше (product_info), если включено, то после отработки запроса браузер закроется и кеши очищаются.
        # Не рекомендую включать, если вам все же нужно освободить память, лучше использовать API.close(session=False, browser=True)
        # ENG: Affects only the function above (product_info), if enabled, the browser will close after the request is processed and caches are cleared.
        # I do not recommend enabling it, if you still need to free up memory, it is better to use API.close(session=False, browser=True)
        API.autoclose_browser = True

        # RUS: Напрямую передается в aiohttp, так же учитывается в браузере. В первую очередь нужен для использования системного `HTTPS_PROXY`.
        # Но системный прокси применяется, только если не указали иное напрямую в `API.proxy`.
        # ENG: Directly passed to aiohttp, also taken into account in the browser. Primarily needed for using the system `HTTPS_PROXY`.
        # But the system proxy is applied only if you did not specify otherwise directly in `API.proxy`.
        API.trust_env = True

        # # RUS: Выводит список последних промо-акций/новостей (можно поставить ограничитель по количеству, опционально)
        # # ENG: Outputs a list of the latest promotions/news (you can set a limit on the number, optionally)
        # news = await API.get_news(limit=5)
        # print(f"News output: {news!s:.100s}...\n")

        # # RUS: Если требуется, можно настроить вывод логов в консоль
        # # ENG: If required, you can configure the output of logs in the console
        # API.debug = True

        # # RUS: Скачивает картинку товара (возвращает BytesIO или None)
        # # ENG: Downloads the product image (returns BytesIO or None)
        # image = await API.download_image(url=items['products'][0]['image_links']['normal'][0])
        # with open(image.name, 'wb') as f:
        #     f.write(image.getbuffer())

        # # RUS: Можно указать свой таймаут (браузер может его интерпретировать как x2 т.к. там 2 итерации скачивания)
        # # ENG: You can specify your own timeout (the browser may interpret it as x2 since there are 2 iterations of downloading)
        # API.timeout = 127

        # # RUS: Так же как и debug, в рантайме можно переназначить прокси
        # # ENG: As with debug, you can reassign the proxy in runtime
        # # API.proxy = "user:password@host:port"
        # # RUS: Изменения происходят сразу же, кроме product_info, т.к. за него отвечает браузер
        # # ENG: Changes take effect immediately, except for product_info, as it is handled by the browser
        # await API.rebuild_connection(session=False, browser=True)
        # await API.product_info(43347)


if __name__ == '__main__':
    asyncio.run(main())