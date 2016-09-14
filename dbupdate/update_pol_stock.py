# -*- coding: utf-8 -*-

from beertools.get_pol_stock_for_pol import get_pol_stock_for_pol

from db import Database


def find_in_list(dicts, key, value):
    try:
        return (item for item in dicts if item[key] == value).next()
    except StopIteration:
        return None


def save_stock(stock_by_pol, db):
    sql = '''
        INSERT INTO pol_stock (shop_id, pol_beer_id, stock, updated)
        VALUES (%(shop_id)s, %(pol_beer_id)s, %(stock)s, %(updated)s)
    '''
    db.run_upserts(sql, stock_by_pol)


def update_pol_stock(conn_str=None):
    db = Database(conn_str)
    beer_ids = [beer['id'] for beer in db.get_pol_beers()]
    shops = [pol['id'] for pol in db.get_pol_shops()]

    for shop_id in shops:
        stock_for_pol = get_pol_stock_for_pol(shop_id)
        stock_by_pol = []
        for stock in stock_for_pol:
            beer_id = stock['product_id']
            if beer_id in beer_ids:
                stock_by_pol.append({
                    'shop_id': shop_id,
                    'pol_beer_id': beer_id,
                    'stock': stock['stock'],
                    'updated': stock['updated']
                })
        save_stock(stock_by_pol, db)

    db.add_log('pol_stock')

if __name__ == '__main__':
    update_pol_stock()
