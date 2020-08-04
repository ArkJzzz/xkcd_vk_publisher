#!usr/bin/python3

__author__ = 'ArkJzzz (arkjzzz@gmail.com)'


import requests
import os
import sys
import argparse
import logging

logger = logging.getLogger('download_picture')


def download_picture(url, filename=None):
    '''
    Функция принимает на вход url картинки и скачивает эту картинку.
    '''
    logger.debug(url)

    network_filename = url.split('/')[-1]
    extension = network_filename.split('.')[-1]
    if filename == None:
        filename = network_filename.split('.')[-2]
    file_path = '{filename}.{extension}'.format(
            filename=filename,
            extension=extension,
        )
    logger.debug(file_path)

    response = requests.get(url, verify=False)
    response.raise_for_status()

    with open(file_path, 'wb') as file:
        file.write(response.content)

    return file_path

 

def main():
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
            fmt='%(asctime)s %(name)s:%(lineno)d - %(message)s',
            datefmt='%Y-%b-%d %H:%M:%S (%Z)',
            style='%',
        )
    console_handler.setFormatter(formatter)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)

    parser = argparse.ArgumentParser(
        description='Программа принимает на вход url картинки, директорию, куда её сохранить и опционально имя файла, а затем скачивает эту картинку'
        )
    parser.add_argument('url', help='ссылка на картинку')
    parser.add_argument('directory', help='куда сохранять')
    parser.add_argument('-n', '--filename', help='имя файла')
    args = parser.parse_args()

    try:
        download_picture(args.url, args.directory, args.filename)
    except HTTPError:
        logging.error('HTTPError: Not Found', exc_info=True)


if __name__ == "__main__":
    main()