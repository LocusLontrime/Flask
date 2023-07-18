import argparse
import asyncio
import os
from t2_async import async_
from t2_threading import threading_
from t2_process import multiprocessing_


def read_from_file(file_path: str):
    with open(file_path, 'r') as file:
        urls_ = [_.strip() for _ in file.readlines()]

    print(f'{urls_}')
    return urls_


def main():
    argparse_ = argparse.ArgumentParser()
    argparse_.add_argument('-f', '--file', type=str, help='File path')
    argparse_.add_argument('-m', '--mode', choices=['a', 'm', 't'], type=str, help='async, multiprocessing, threading')
    ap = argparse_.parse_args()
    print(f'path: {os.path.join(ap.file)}')
    urls_ = read_from_file(os.path.join(ap.file))

    if ap.mode == 'a':
        asyncio.run(async_(urls_))
    elif ap.mode == 'm':
        multiprocessing_(urls_)
    elif ap.mode == 't':
        threading_(urls_)


if __name__ == '__main__':
    main()