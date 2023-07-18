import asyncio
import aiohttp
import aiofiles
import time


async def download(url_: str):
    start_ = time.time()
    async with aiohttp.ClientSession() as session:
        async with session.get(url_) as response:
            if response.status == 200:
                filename = url_.split('/')[-1]
                content = await response.read()
                async with aiofiles.open(f'{filename}', 'wb') as file:
                    await file.write(content)

                print(f'Download {(time.time() - start_):.3f} second')


async def async_(urls_: list):
    tasks = []
    for url in urls_:
        task = asyncio.create_task(download(url))
        tasks.append(task)
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    urls = ['https://w.forfun.com/fetch/b1/b1f74a00706ac59ec75daa8ab0ac8e90.jpeg',
            'https://w.forfun.com/fetch/3e/3e6d5f96bb0a293b7eb3866e91f2fd32.jpeg',
            'https://w.forfun.com/fetch/4d/4d42b9e87501949015561e292f50b76f.jpeg',
            'https://w.forfun.com/fetch/2f/2f8f26f82124652460ec0dfb35610901.jpeg',
            'https://w.forfun.com/fetch/02/02c6bb26b9418fce90a14f1340bdb033.jpeg',
            'https://w.forfun.com/fetch/02/02c6bb26b9418fce90a14f1340bdb033.jpeg',
            'https://w.forfun.com/fetch/d3/d35a1d74682aa448a83c422d4b2441f1.jpeg']
    start = time.time()
    asyncio.run(async_(urls))
    print(f'The program has ended: {(time.time() - start):.3f} second')
