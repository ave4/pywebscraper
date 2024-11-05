#!/usr/bin/env python
import json
import requests
from bs4 import BeautifulSoup
import argparse

base_url = 'https://quotes.toscrape.com'
url = '/page/'

def save_function(data, filename):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile, ensure_ascii=False)

def url_downloader(url):
    try:
        r = requests.get(url)
        if not r.status_code == 200:
                print(f'{url}: status {r.status_code}')
        return r
    except Exception as e:
        print(e)

def parser_html(html):
    quotes_dict = []
    try:
        soup = BeautifulSoup(html.content, features='xml')
        quotes = soup.find_all('div', class_='quote')
        for div in quotes:
            quotes_dict.append({
            'text': div.find(class_='text').text,
            'author': div.find(class_='author').text,
            'tags': div.find(class_='tags').find(class_='keywords')['content']
        })
        return quotes_dict
    except Exception as e:
        print(e)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                    prog='HTML scraper for quotes.toscrape.com',
                    description='And writes data to json')
    parser.add_argument('page')
    parser.add_argument('jsoname')
    opts = parser.parse_args()
    save_function(parser_html(url_downloader(f'{base_url}{url}{opts.page}')), opts.jsoname)



