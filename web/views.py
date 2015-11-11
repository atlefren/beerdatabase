# -*- coding: utf-8 -*-
import re


from flask import render_template, current_app, abort, json
from beertools import polchecker
from sqlalchemy.sql import func
from sqlalchemy import and_

from web import app
from models import PoletBeer, BeerStyle, RatebeerBeer, RatebeerBrewery

RATEBEER_BASE_URL = 'http://www.ratebeer.com/beer'


def ratebeer_url(ratebeer_id, short_name):
    fixed_name = re.sub(
        '[^A-Za-z0-9\-]+',
        '',
        short_name.replace(' ', '-')
    )
    return "%s/%s/%s/" % (RATEBEER_BASE_URL, fixed_name, ratebeer_id)


@app.template_filter('ratebeer_url')
def get_ratebeer_url(ratebeer_beer):
    return ratebeer_url(ratebeer_beer.id, ratebeer_beer.shortname)


@app.route('/pol_beers/')
def index():
    pol_beers = current_app.db_session.query(PoletBeer).all()
    pol_beers_json = json.dumps([b.get_list_response() for b in pol_beers])
    return render_template('pol_beer_list.html', json=pol_beers_json)


@app.route('/pol_beers/<int:id>')
def pol_beer(id):
    pol_beer = current_app.db_session.query(PoletBeer).get(id)
    if not pol_beer:
        abort(404)
    available_at = polchecker.check_beer(pol_beer.id)
    return render_template('pol_beer.html', pol_beer=pol_beer, available_at=available_at)


@app.route('/styles/')
def style_list():
    # TODO limit to available styles at polet
    styles = current_app.db_session.query(BeerStyle).all()
    styles_json = json.dumps(styles)
    return render_template('style_list.html', json=styles_json)


@app.route('/styles/<int:id>')
def style(id):
    style = current_app.db_session.query(BeerStyle).get(id)
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
    breweries = current_app.db_session.query(RatebeerBrewery, func.count())\
        .join(RatebeerBeer)\
        .join(PoletBeer)\
        .group_by(RatebeerBrewery)\
        .order_by(RatebeerBrewery.name)\
        .all()

    # TODO: incorporate in query
    breweries = [b[0].get_list_response(count=b[1]) for b in breweries]
    return render_template('brewery_list.html', breweries=breweries)


@app.route('/breweries/<int:id>')
def brewery(id):
    brewery = current_app.db_session.query(RatebeerBrewery).get(id)
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
