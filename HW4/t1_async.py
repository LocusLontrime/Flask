import asyncio
import aiohttp
import time


async def download(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
            filename = 'asyncio_' + url.replace('https://', '').replace('.', '_').replace('/', '').replace('?', '_').replace('&', '_').replace('=', '_') + '.html'
            with open(filename, "w", encoding='utf-8') as f:
                f.write(text)


async def main(urls: list):
    tasks = []
    for url in urls:
        task = asyncio.create_task(download(url))
        tasks.append(task)
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    url_ = 'https://www.lamoda.ru/c/355/clothes-zhenskaya-odezhda/?sitelink=topmenuW&l=3&page='
    urls = []
    for _ in range(1, 100):
        urls.append(url_ + str(_))
    # print(f'{urls = }')
    start = time.time()
    asyncio.run(main(urls))
    print(f'{(time.time() - start):.3f} seconds')