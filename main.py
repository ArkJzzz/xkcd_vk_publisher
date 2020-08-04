#!/usr/bin/python3
__author__ = 'ArkJzzz (arkjzzz@gmail.com)'

# Import
import logging
import requests
import json
import random
from os import getenv
from os import remove

from dotenv import load_dotenv

from download_picture import download_picture


logger = logging.getLogger(__file__)


def main():
    # init
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

    download_picture_logger = logging.getLogger('download_picture')
    download_picture_logger.addHandler(console_handler)
    download_picture_logger.setLevel(logging.DEBUG)

    load_dotenv()
    vk_user_id = getenv('VK_USER_ID')
    vk_group_id = getenv('VK_CLUB_ID')
    vk_app_token = getenv('VK_APP_ACCESS_TOKEN')
    
    # do
    xkcd_comics = get_random_xkcd_comics()
    logger.debug(xkcd_comics)

    comics_img_url = xkcd_comics['img']
    filename = download_picture(comics_img_url, 'comics_image')
    logger.debug(filename)

    result_of_publication = publish_img_to_vk_group_wall(vk_app_token, 
                                    vk_group_id, filename, xkcd_comics)
    logger.debug(result_of_publication)

    remove(filename)


def get_random_xkcd_comics():
    last_xkcd_comics = get_xkcd_comics()
    last_xkcd_comics_num = last_xkcd_comics['num']
    random_number = random.randrange(last_xkcd_comics_num)
    random_last_xkcd_comics = get_xkcd_comics(random_number)

    return random_last_xkcd_comics


def get_xkcd_comics(comics_id=''):
    url_base = 'https://xkcd.com/'
    url_comics_path = '{comics_id}/info.0.json'.format(
            comics_id=comics_id
        )
    url = requests.compat.urljoin(url_base, url_comics_path)
    response = requests.get(url)
    response.raise_for_status()

    return response.json()


def get_groups_vk_user(vk_app_token, vk_user_id):
    url = 'https://api.vk.com/method/{method}'.format(
            method='groups.get',
        )

    headers = {}
    payload = {
        'user_id': vk_user_id,
        'extended': '1',
        'filter': 'admin',
        'fields': '',
        'offset': '',
        'count': '',
        'access_token': vk_app_token,
        'v': '5.122'
    }

    response = requests.get(url, headers=headers, params=payload)
    response.raise_for_status()
    response = response.json()

    return response['response']


def publish_img_to_vk_group_wall(vk_app_token, vk_group_id, filename, 
                                xkcd_comics):
    '''Публикация изображения на стене групы Вконтакте

    Изображение на стене во Вконтакте публикуется в несколько этапов:
        1. Получение адреса сервера для загрузки фото
        2. Передача файла на сервер
        3. Сохранение результата
        4. Публикация записи
    '''
    
    wall_upload_serwer = get_wall_upload_serwer(vk_app_token, vk_group_id)
    upload_url = wall_upload_serwer['upload_url']
    logger.info('Адрес сервера получен')

    photo_upload_result = upload_photo_to_server(filename, upload_url)
    logger.info('Изображение загружено на сервер')

    save_wall_photo_result = save_wall_photo(vk_group_id, vk_app_token, 
                                        photo_upload_result, xkcd_comics)
    save_wall_photo_result = save_wall_photo_result['response'][0]
    logger.info('Изображение сохранено на сервере')

    post_wall_photo_result = post_wall_photo(vk_app_token, vk_group_id, 
                                        save_wall_photo_result)
    logger.info('Опубликована запись {}, {}'.format(
            post_wall_photo_result['post_id'],
            save_wall_photo_result['text'],
        )
    )

    return {post_wall_photo_result['post_id']: save_wall_photo_result['text']}


def get_wall_upload_serwer(vk_app_token, vk_group_id):
    '''Получение адреса сервера Вконтакте для загрузки фото'''

    url = 'https://api.vk.com/method/{method}'.format(
            method='photos.getWallUploadServer',
        )
    headers = {}
    payload = {
        'group_id': vk_group_id,
        'access_token': vk_app_token,
        'v': '5.122'
    }
    response = requests.get(url, headers=headers, params=payload)
    response.raise_for_status()
    response = response.json()

    return response['response']


def upload_photo_to_server(filename, upload_url):
    '''Передача файла на сервер Вконтакте'''

    files = {'photo': open(filename, 'rb')}
    response = requests.post(upload_url, files=files)
    response.raise_for_status()

    return response.json()


def save_wall_photo(vk_group_id, vk_app_token, photo_upload_result, 
                                                            xkcd_comics):
    '''Сохранение результата загрузки файла'''

    url = 'https://api.vk.com/method/{method}'.format(
            method='photos.saveWallPhoto',
        )
    message = '\"{}\"\n{}'.format(
            xkcd_comics['title'],
            xkcd_comics['alt'],
        )
    headers = {}
    payload = {
        'group_id': vk_group_id,
        'photo': photo_upload_result['photo'],
        'server': photo_upload_result['server'],
        'hash': photo_upload_result['hash'],
        'caption': message,
        'access_token': vk_app_token,
        'v': '5.122'
    }
    response = requests.get(url, headers=headers, params=payload)
    response.raise_for_status()

    return response.json()


def post_wall_photo(vk_app_token, vk_group_id, save_wall_photo_result):
    '''Публикация записи с загруженным изображением'''

    url = 'https://api.vk.com/method/{method}'.format(
            method='wall.post',
        )
    attachments = 'photo{owner_id}_{photo_id}'.format(
                owner_id=save_wall_photo_result['owner_id'],
                photo_id=save_wall_photo_result['id'],
            )
    payload = {
        'owner_id': '-{}'.format(vk_group_id),
        'from_group': 1,
        'message': save_wall_photo_result['text'],
        'attachments': attachments,
        'signed': 0,
        'mute_notifications': 0,
        'copyright': 'https://xkcd.com',
        'access_token': vk_app_token,
        'v': '5.122',
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    response = response.json()

    return response['response']


if __name__ == '__main__':
    main()