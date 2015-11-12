# -*- coding: utf-8 -*-

from flask import render_template, current_app, abort, json
from sqlalchemy.sql import func

from web import app
from models import PoletBeer, BeerStyle, RatebeerBeer, RatebeerBrewery


@app.template_filter('ratebeer_url')
def get_ratebeer_url(ratebeer_beer):
    # return ratebeer_url(ratebeer_beer.id, ratebeer_beer.shortname)
    pass

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
    if pol_beer.ratebeer is None:
        return u'Dette ølet er ikke matched med ratebeer, hjelp?'
    return render_template('pol_beer.html', json=json.dumps(pol_beer))


@app.route('/pol_beers/<int:id>/report')
def pol_beer_report(id):
    return 'Ok, kommer snart!'


@app.route('/styles/')
def style_list():
    # TODO limit to available styles at polet
    styles = current_app.db_session.query(BeerStyle).all()
    styles_json = json.dumps(styles)
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
