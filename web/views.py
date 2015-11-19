# -*- coding: utf-8 -*-

from flask import render_template, current_app, abort, json
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_

from web import app
from models import (PoletBeer, BeerStyle, RatebeerBeer, RatebeerBrewery,
                    RbPolBeerMapping, RatebeerCountry, PolShop, PolStock)


@app.template_filter('ratebeer_url')
def get_ratebeer_url(ratebeer_beer):
    # return ratebeer_url(ratebeer_beer.id, ratebeer_beer.shortname)
    pass


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/pol_beers/')
def pol_beers():
    pol_beers = current_app.db_session.query(PoletBeer).all()
    pol_beers_json = json.dumps([b.get_list_response() for b in pol_beers])
    return render_template('pol_beer_list.html', json=pol_beers_json)


def fix_beer(pol_beer, rb_beer=None):

    data = {
        'pol_beer': pol_beer.serialize(),
        'rb_beer': rb_beer.serialize() if rb_beer is not None else None
    }

    return render_template('fix_beer.html', json=json.dumps(data))


@app.route('/pol_beers/unmatched/')
def unmatched_beers():

    unmatched = current_app.db_session.query(PoletBeer.id, PoletBeer.name, PoletBeer.producer, func.count(RbPolBeerMapping.id))\
        .outerjoin(RbPolBeerMapping)\
        .filter(PoletBeer.ratebeer_id == None)\
        .group_by(PoletBeer.id, PoletBeer.name, PoletBeer.producer)\
        .all()

    unmatched = [{
        'id': b[0],
        'name': b[1],
        'brewery': b[2],
        'count': b[3]
    } for b in unmatched]
    return render_template('unmatched.html', json=json.dumps(unmatched))


@app.route('/pol_beers/match_suggestions/')
def match_suggestions():
    suggestions = current_app.db_session.query(RbPolBeerMapping)\
        .filter(RbPolBeerMapping.resolved == False)\
        .all()
    suggestions = [s.serialize() for s in suggestions]
    return render_template(
        'match_suggestions.html',
        json=json.dumps(suggestions)
    )


@app.route('/pol_beers/<int:id>')
def pol_beer(id):
    pol_beer = current_app.db_session.query(PoletBeer).get(id)
    if not pol_beer:
        abort(404)
    if pol_beer.ratebeer is None:
        return fix_beer(pol_beer)
    return render_template(
        'pol_beer.html',
        json=json.dumps(pol_beer.serialize())
    )


@app.route('/pol_beers/<int:id>/report')
def pol_beer_report(id):
    pol_beer = current_app.db_session.query(PoletBeer).get(id)
    return fix_beer(pol_beer, pol_beer.ratebeer)


@app.route('/styles/')
def style_list():
    # TODO limit to available styles at polet
    styles = current_app.db_session.query(BeerStyle, func.count())\
        .join(RatebeerBeer)\
        .join(PoletBeer)\
        .group_by(BeerStyle.id, BeerStyle.name)\
        .all()
    styles_json = json.dumps([{
        'id': r[0].id,
        'name': r[0].name,
        'count': r[1]
    } for r in styles])
    return render_template('style_list.html', json=styles_json)


@app.route('/styles/<int:id>')
def style(id):
    style = current_app.db_session.query(BeerStyle).get(id)
    if not style:
        abort(404)
    beers = current_app.db_session.query(PoletBeer)\
        .join(RatebeerBeer)\
        .filter(RatebeerBeer.style_id == id)\
        .all()
    beers_json = json.dumps([b.get_list_response() for b in beers])
    return render_template(
        'style.html',
        json=beers_json,
        style=style,
        num=len(beers)
    )


@app.route('/breweries/')
def brewery_list():
    breweries = current_app.db_session.query(RatebeerBrewery.id, RatebeerBrewery.name, RatebeerCountry.id, RatebeerCountry.name, func.count())\
        .join(RatebeerBeer)\
        .join(PoletBeer)\
        .join(RatebeerCountry)\
        .group_by(RatebeerBrewery.id, RatebeerBrewery.name, RatebeerCountry.id, RatebeerCountry.name)\
        .order_by(RatebeerBrewery.name)\
        .all()

    # TODO: incorporate in query
    breweries = [{
        'id': b[0],
        'name': b[1],
        'country': {'id': b[2], 'name': b[3]},
        'num_beers_polet': b[4]
    } for b in breweries]
    return render_template('brewery_list.html', json=json.dumps(breweries))


@app.route('/breweries/<int:id>')
def brewery(id):
    brewery = current_app.db_session.query(RatebeerBrewery).get(id)
    if not brewery:
        abort(404)
    beers = current_app.db_session.query(PoletBeer)\
        .join(RatebeerBeer)\
        .filter(RatebeerBeer.brewery_id == id)\
        .all()
    beers_json = json.dumps([b.get_list_response() for b in beers])
    return render_template(
        'brewery.html',
        json=beers_json,
        brewery=brewery,
        num=len(beers)
    )


@app.route('/pol_shops/')
def pol_shops():
    shops = current_app.db_session.query(PolShop).all()
    return render_template('pol_shops.html', shops=shops)


@app.route('/pol_shops/<int:id>')
def pol_shop(id):
    shop = current_app.db_session.query(PolShop).get(id)
    if shop is None:
        abort(404)
    beers = current_app.db_session.query(PoletBeer, PolStock.stock)\
        .join(PolStock)\
        .filter(PolStock.shop_id == id)\
        .order_by(PoletBeer.name)

    beers_json = json.dumps([b[0].get_list_response({'stock': b[1]}) for b in beers.all()])
    return render_template(
        'pol_shop.html',
        json=json.dumps(shop),
        beers_json=beers_json
    )
