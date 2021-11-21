import os
import sys
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv
import argparse


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('url')

    return parser


def shorten_link(secret_token, long_url):
    headers = {
        'Authorization': f'Bearer {secret_token}'
    }
    payload = {
        'long_url': long_url
    }
    response = requests.post('https://api-ssl.bitly.com/v4/bitlinks', headers=headers, json=payload)
    response.raise_for_status()
    return response.json()['link']


def count_clicks(secret_token, bitlink):
    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary',
        headers={'Authorization': secret_token}, params={'units': -1}
    )
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(secret_token, check_bitlink):
    headers = {
        'Authorization': f'Bearer {secret_token}'
    }
    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{check_bitlink}',
        headers=headers)
    return response.ok


def main():
    load_dotenv()

    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])
    url = namespace.url
    parsed = urlparse(url)
    test_bitlink = parsed.netloc + parsed.path
    bitlink_token = os.getenv("BITLINK_TOKEN")

    if is_bitlink(bitlink_token, test_bitlink):
        try:
            print('Количество кликов', count_clicks(bitlink_token, test_bitlink))

        except requests.exceptions.HTTPError:
            exit('Ошибка')
    else:
        try:
            print('Битлинк', shorten_link(bitlink_token, url))
        except requests.exceptions.HTTPError:
            exit('Ошибка создания Битлинка!')


if __name__ == '__main__':
    main()
