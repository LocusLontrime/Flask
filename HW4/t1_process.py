import requests
import multiprocessing
import time


def download(url: str):
    response = requests.get(url)
    filename = 'process_' + url.replace('https://', '').replace('.', '_').replace('/', '').replace('?', '_').replace(
        '&', '_').replace('=', '_') + '.html'
    with open(f'{filename}', 'w', encoding='utf-8') as file:
        file.write(response.text)


def main(urls: list):
    processes = []
    for url in urls:
        process = multiprocessing.Process(target=download, args=(url,))
        processes.append(process)
        process.start()

    for p in processes:
        p.join()

    print(f'Finish')


if __name__ == '__main__':
    url_ = 'https://www.lamoda.ru/c/355/clothes-zhenskaya-odezhda/?sitelink=topmenuW&l=3&page='
    urls = []
    for _ in range(1, 100):
        urls.append(url_ + str(_))
    # print(f'{urls = }')
    start = time.time()
    main(urls)
    print(f'{(time.time() - start):.3f} seconds')