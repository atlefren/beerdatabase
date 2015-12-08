# -*- coding: utf-8 -*-

from flask import current_app
from sqlalchemy.sql import func

from models import (PoletBeer, PolShop, PolStock, RatebeerBrewery,
                    RatebeerBeer, RatebeerCountry, BeerStyle, RbPolBeerMapping,
                    Municipality)


def get_pol_beers_list():
    pol_beers = current_app.db_session.query(PoletBeer).all()
    return [b.get_list_response() for b in pol_beers]


def get_pol_beer(beer_id):
    return current_app.db_session.query(PoletBeer).get(beer_id)


def get_beer(beer_id):
    return current_app.db_session.query(RatebeerBeer).get(beer_id)


def get_styles():
    return current_app.db_session.query(BeerStyle).all()


def get_total_pol_beer_stock(beer_id):
    return current_app.db_session\
        .query(func.sum(PolStock.stock).label('stock'))\
        .filter(PolStock.pol_beer_id == beer_id)\
        .scalar()


def get_style_list():
    styles = current_app.db_session.query(BeerStyle, func.count())\
        .join(RatebeerBeer)\
        .join(PoletBeer)\
        .group_by(BeerStyle.id, BeerStyle.name)\
        .all()
    return [{
        'id': r[0].id,
        'name': r[0].name,
        'count': r[1]
    } for r in styles]


def get_style(style_id):
    return current_app.db_session.query(BeerStyle).get(style_id)


def get_beers_for_style(style_id):
    beers = current_app.db_session.query(PoletBeer)\
        .join(RatebeerBeer)\
        .filter(RatebeerBeer.style_id == style_id)\
        .all()
    return [b.get_list_response() for b in beers]


def get_breweries_at_polet():
    breweries = current_app.db_session.query(RatebeerBrewery.id, RatebeerBrewery.name, RatebeerCountry.id, RatebeerCountry.name, func.count())\
        .join(RatebeerBeer)\
        .join(PoletBeer)\
        .join(RatebeerCountry)\
        .group_by(RatebeerBrewery.id, RatebeerBrewery.name, RatebeerCountry.id, RatebeerCountry.name)\
        .order_by(RatebeerBrewery.name)\
        .all()

    # TODO: incorporate in query
    return [{
        'id': b[0],
        'name': b[1],
        'country': {'id': b[2], 'name': b[3]},
        'num_beers_polet': b[4]
    } for b in breweries]


def get_pol_beers_for_brewery(brewery_id):
    beers = current_app.db_session.query(PoletBeer)\
        .join(RatebeerBeer)\
        .filter(RatebeerBeer.brewery_id == brewery_id)\
        .all()
    return [b.get_list_response() for b in beers]


def get_brewery(brewery_id):
    return current_app.db_session.query(RatebeerBrewery).get(brewery_id)


def get_pol_shops():
    return current_app.db_session\
        .query(PolShop)\
        .order_by(PolShop.name)\
        .all()


def get_pol_shop(shop_id):
    return current_app.db_session.query(PolShop).get(shop_id)


def get_beers_for_shop(shop_id):

    beers = current_app.db_session.query(PoletBeer, PolStock)\
        .join(PolStock)\
        .filter(PolStock.shop_id == shop_id)

    return [b[0].get_list_response({
        'stock': b[1].stock,
        'updated': b[1].updated.isoformat()
    }) for b in beers.all()]


def get_unmatched_pol_beers():
    unmatched = current_app.db_session.query(PoletBeer.id, PoletBeer.name, PoletBeer.producer, func.count(RbPolBeerMapping.id))\
        .outerjoin(RbPolBeerMapping)\
        .filter(PoletBeer.ratebeer_id == None)\
        .group_by(PoletBeer.id, PoletBeer.name, PoletBeer.producer)\
        .all()

    return [{
        'id': b[0],
        'name': b[1],
        'brewery': b[2],
        'count': b[3]
    } for b in unmatched]


def get_unresolved_pol_suggestions():
    suggestions = current_app.db_session.query(RbPolBeerMapping)\
        .filter(RbPolBeerMapping.resolved == False)\
        .all()
    return [s.serialize() for s in suggestions]


def get_all_municipalities():
    return current_app.db_session.query(Municipality)\
        .order_by(Municipality.kommnr)\
        .all()
