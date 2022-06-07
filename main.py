import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json


# get data from website
def get_data(name):
    url = 'https://store.steampowered.com/search/?term={}'.format(name)

    response = requests.get(url)
    return response.text


# processing data
def parse(data):
    # declaration variable
    result = []
    title = None
    released = None
    price = None
    discount = None

    soup = BeautifulSoup(data, 'html.parser')
    contents = soup.find('div', attrs={'id': 'search_resultsRows'})

    try:
        games = contents.find_all('a')
    except Exception:
        games = None

    if games is not None:
        for game in games:
            link = game['href']

            # parsing data
            try:
                title = game.find('span', {'class': 'title'}).text.strip()
                released = game.find('div', {'class': 'search_released'}).text.strip()
                price = game.find('div', {'class': 'search_price'}).text.strip()
                discount = game.find('div', {'class': 'search_discount'}).text.strip()
            except Exception:
                print('parsing data: Some requests not found')
                exit()

            # replace empty values to 'none'
            if released == '':
                released = 'none'

            if price == '':
                price = 'none'

            if discount == '':
                discount = 'none'

            # sorting data
            data_dict = {
                'title': title,
                'released': released,
                'price': price,
                'discount': discount,
                'link': link,
            }

            # append
            result.append(data_dict)
        return result
    else:
        return None


def output(datas: list):
    if datas is not None:
        for i in datas:
            print(i)
        print(f'\nTotal games : {len(datas)}')
    else:
        print('0 results match your search.')


def generate_file(result, filename):
    df = pd.DataFrame(result)
    df.to_excel(f'{filename}.xlsx', index=False)


def run(game):
    data = get_data(game)
    result = parse(data)
    generate_file(result, game)
    output(result)


if __name__ == '__main__':
    keyword = input('Input your keyword : ')
    run(keyword)
