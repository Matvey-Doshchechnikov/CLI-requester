import asyncio
import aiohttp
from typing import List, Dict


async def check_url_methods(url: str) -> Dict[str, int]:
    methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD']
    results = {}

    async with aiohttp.ClientSession() as session:
        for method in methods:
            try:
                async with session.request(method, url) as response:
                    if response.status != 405:
                        results[method] = response.status
            except aiohttp.ClientError:
                print(f"Ошибка при обработке {method} запроса для {url}")
    return results


async def process_strings(strings: List[str]) -> Dict[str, Dict[str, int]]:
    results = {}

    for string in strings:
        if string.startswith("http://") or string.startswith("https://"):
            print(f"Обрабатываю ссылку: {string}")
            methods_results = await check_url_methods(string)
            if methods_results:
                results[string] = methods_results
        else:
            print(f"Строка '{string}' не является ссылкой.")
    return results


def cli_app(strings: List[str]):
    result = asyncio.run(process_strings(strings))
    print(result)


if __name__ == "__main__":
    import sys
    cli_app(sys.argv[1:])
