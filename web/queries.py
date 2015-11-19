# -*- coding: utf-8 -*-

from flask import current_app, json

from models import PoletBeer, PolShop, PolStock


def get_pol_shops():
    return json.dumps(current_app.db_session.query(PolShop).all())


def get_pol_shop(shop_id):
    shop = current_app.db_session.query(PolShop).get(shop_id)
    if shop is not None:
        return json.dumps(shop)
    return None


def get_beers_for_shop(shop_id):
    beers = current_app.db_session.query(PoletBeer, PolStock.stock)\
        .join(PolStock)\
        .filter(PolStock.shop_id == shop_id)\
        .order_by(PoletBeer.name)

    return json.dumps(
        [b[0].get_list_response({'stock': b[1]}) for b in beers.all()]
    )
