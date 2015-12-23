# -*- coding: utf-8 -*-

from flask import abort, redirect, url_for
import queries


def get_brewery_data(brewery_id):
    brewery = queries.get_brewery(brewery_id)
    if not brewery:
        abort(404)
    beers = queries.get_pol_beers_for_brewery(brewery_id)
    data = {
        'brewery': brewery,
        'beers': beers
    }
    title = brewery.name
    return data, title, None


def get_style_data(style_id):
    style = queries.get_style(style_id)
    if not style:
        abort(404)
    beers = queries.get_beers_for_style(style_id)
    data = {
        'style': style,
        'beers': beers
    }
    return data, style.name, None


def get_country(id):
    data = queries.get_country(id)
    return data, u'Øl fra ' + data['country'].name, None


def get_pol_shop_list():
    return {
        'shops': queries.get_pol_shops(),
        'municipalities': queries.get_all_municipalities()
    }


def get_pol_shop_data(shop_id):
    shop = queries.get_pol_shop(shop_id)
    if shop is None:
        abort(404)
    beers = queries.get_beers_for_shop(shop_id)
    data = {
        'shop': shop,
        'beers': beers
    }
    return data, shop.name, None


def get_pol_beer(beer_id):
    pol_beer = queries.get_pol_beer(beer_id)
    if not pol_beer:
        abort(404)
    if pol_beer.ratebeer is None:
        return None, None, redirect(url_for('fix_beer', id=beer_id))

    serialized = pol_beer.serialize()
    stock = queries.get_total_pol_beer_stock(beer_id)

    serialized['stock'] = stock
    return serialized, pol_beer.ratebeer.name, None


def get_beer_fix_data(beer_id):
    pol_beer = queries.get_pol_beer(beer_id)
    if not pol_beer:
        abort(404)
    rb_beer = pol_beer.ratebeer
    return {
        'pol_beer': pol_beer.serialize(),
        'rb_beer': rb_beer.serialize() if rb_beer is not None else None
    }
