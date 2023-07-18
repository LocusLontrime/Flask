import requests
import threading
import time


def download(url: str):
    start_ = time.time()
    response = requests.get(url)
    if response.status_code == 200:
        filename = url.split('/')[-1]
        with open(f'{filename}', 'wb') as file:
            file.write(response.content)
        print(f'Download {filename}: {(time.time() - start_):.3f} second')


def threading_(urls_: list[str]):
    threads = []
    for url in urls_:
        thread = threading.Thread(target=download, args=[url])
        threads.append(thread)
        thread.start()

    for t in threads:
        t.join()


if __name__ == '__main__':
    urls = ['https://w.forfun.com/fetch/b1/b1f74a00706ac59ec75daa8ab0ac8e90.jpeg',
            'https://w.forfun.com/fetch/3e/3e6d5f96bb0a293b7eb3866e91f2fd32.jpeg',
            'https://w.forfun.com/fetch/4d/4d42b9e87501949015561e292f50b76f.jpeg',
            'https://w.forfun.com/fetch/2f/2f8f26f82124652460ec0dfb35610901.jpeg',
            'https://w.forfun.com/fetch/02/02c6bb26b9418fce90a14f1340bdb033.jpeg',
            'https://w.forfun.com/fetch/02/02c6bb26b9418fce90a14f1340bdb033.jpeg',
            'https://w.forfun.com/fetch/d3/d35a1d74682aa448a83c422d4b2441f1.jpeg']
    start = time.time()
    threading_(urls)
    print(f'The program has ended: {(time.time() - start):.3f} second')