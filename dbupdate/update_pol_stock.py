# -*- coding: utf-8 -*-
from datetime import datetime

from beertools.polchecker import check_beer

from db import get_pol_beers, get_pol_shops, run_upserts


def find_in_list(dicts, key, value):
    try:
        return (item for item in dicts if item[key] == value).next()
    except StopIteration:
        return None


def save_stock(stock_by_pol):
    sql = '''
        INSERT INTO pol_stock (shop_id, pol_beer_id, stock, updated)
        VALUES (%(shop_id)s, %(pol_beer_id)s, %(stock)s, %(updated)s)
    '''
    run_upserts(sql, stock_by_pol)


def update_pol_stock():
    beers = get_pol_beers()
    shops = get_pol_shops()

    stock_by_pol = []
    for beer in beers:
        stocks = check_beer(beer['id'])
        for stock in stocks:
            shop = find_in_list(shops, 'name', stock['pol_name'])
            if shop is None:
                continue
            num = stock['stock']
            updated = stock['updated']
            stock_by_pol.append({
                'shop_id': shop['id'],
                'pol_beer_id': beer['id'],
                'stock': num,
                'updated': updated
            })
    save_stock(stock_by_pol)

if __name__ == '__main__':
    update_pol_stock()
