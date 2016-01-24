# -*- coding: utf-8 -*-

from flask import current_app, json, request, Response
from sqlalchemy.sql.expression import and_
from sqlalchemy.sql import text

from web import app
from models import (RatebeerBeer, RatebeerBrewery, RbPolBeerMapping, PoletBeer,
                    PolStock, PolShop)


api_prefix = '/api/v1'


def get_limit():
    limit = request.args.get('limit', 10, type=int)
    return limit if limit <= 100 else 100


@app.route(api_prefix + '/search/autocomplete/')
def autocomplete_search():
    name = request.args.get('name', None)

    query = current_app.db_session.query(RatebeerBeer)\
        .join(PoletBeer)\
        .filter(RatebeerBeer.name.ilike('%' + name + '%'))\
        .limit(10)
    beer_list = [b.get_list_response() for b in query.all()]
    return Response(json.dumps(beer_list), content_type='application/json')


@app.route(api_prefix + '/search/full/')
def full_search():
    query = current_app.db_session.query(RatebeerBeer)

    at_polet = False
    available_at = request.args.get('availableAt', None)
    if available_at is not None:
        available_at = available_at.split(',')
        if 'polet' in available_at:
            at_polet = True
            query = query.join(PoletBeer)
        else:
            return Response(json.dumps([]), content_type='application/json')

    name = request.args.get('name', None)
    if name is not None:
        query = query.filter(RatebeerBeer.name.ilike('%' + name + '%'))

    styles = request.args.get('style', None)
    if styles is not None:
        styles = [int(s) for s in styles.split(',') if s != '']
        if len(styles) > 0:
            query = query.filter(RatebeerBeer.style_id.in_(styles))

    overall_score = request.args.get('overallScore', None)
    if overall_score is not None:
        score_limit = [int(s) for s in overall_score.split(',')]
        if len(score_limit) == 2:
            query = query.filter(and_(
                RatebeerBeer.score_overall >= score_limit[0],
                RatebeerBeer.score_overall <= score_limit[1]
            ))

    style_score = request.args.get('styleScore', None)
    if style_score is not None:
        score_limit = [int(s) for s in style_score.split(',')]
        if len(score_limit) == 2:
            query = query.filter(and_(
                RatebeerBeer.score_style >= score_limit[0],
                RatebeerBeer.score_style <= score_limit[1]
            ))

    price = request.args.get('price', None)
    if price is not None and at_polet:
        price_limit = [int(s) for s in price.split(',')]
        if len(price_limit) == 2:
            query = query.filter(and_(
                PoletBeer.price >= price_limit[0],
                PoletBeer.price <= price_limit[1]
            ))

    abv = request.args.get('abv', None)
    if abv is not None:
        abv_limit = [float(s) for s in abv.split(',')]
        if len(score_limit) == 2:
            query = query.filter(and_(
                RatebeerBeer.abv >= abv_limit[0],
                RatebeerBeer.abv <= abv_limit[1]
            ))

    query = query.order_by(RatebeerBeer.name)

    beer_list = [b.get_list_response() for b in query.all()]
    return Response(json.dumps(beer_list), content_type='application/json')


@app.route(api_prefix + '/search/brewery/')
def search_brewery():
    query = request.args.get('q')
    db = current_app.db_session
    res = db.query(RatebeerBrewery).filter(
        RatebeerBrewery.name.ilike('%' + query + '%')
    )
    x = res.limit(get_limit()).all()
    return Response(json.dumps(x), content_type='application/json')


@app.route(api_prefix + '/search/beer/')
def search_beer():
    query = request.args.get('q')
    db = current_app.db_session
    res = db.query(RatebeerBeer).filter(RatebeerBeer.name.ilike('%' + query + '%'))

    brewery_id = request.args.get('brewery', None)
    if brewery_id:
        res = res.filter(RatebeerBeer.brewery_id == brewery_id)
    beers = res.limit(get_limit()).all()
    beers = [beer.serialize() for beer in beers]
    return Response(json.dumps(beers), content_type='application/json')


@app.route(api_prefix + '/suggestions/', methods=['POST'])
def add_suggestion():
    data = request.json
    mapping = RbPolBeerMapping(
        pol_id=data.get('polId', None),
        rb_id=data.get('ratebeerId', None),
        comment=data.get('comment', None)
    )
    current_app.db_session.add(mapping)
    current_app.db_session.commit()
    return Response(
        json.dumps(mapping),
        content_type='application/json',
        status=201
    )


@app.route(api_prefix + '/suggestions/<int:id>', methods=['DELETE'])
def remove_suggestion(id):
    suggestion = current_app.db_session.query(RbPolBeerMapping)\
        .get(id)
    suggestion.resolved = True
    current_app.db_session.commit()

    suggestions = current_app.db_session.query(RbPolBeerMapping)\
        .filter(RbPolBeerMapping.resolved == False)\
        .all()

    return Response(
        json.dumps(suggestions),
        content_type='application/json',
        status=200
    )


@app.route(api_prefix + '/suggestions/<int:id>', methods=['PUT'])
def confirm_suggestion(id):
    data = request.json

    pol_beer = current_app.db_session.query(PoletBeer)\
        .get(data.get('pol_id', None))
    pol_beer.ratebeer_id = data.get('rb_id', None)

    suggestions = current_app.db_session.query(RbPolBeerMapping)\
        .filter(and_(
            RbPolBeerMapping.rb_beer_id == pol_beer.ratebeer_id,
            RbPolBeerMapping.pol_beer_id == pol_beer.id
        ))\
        .all()
    for suggestion in suggestions:
        suggestion.resolved = True

    current_app.db_session.commit()

    suggestions = current_app.db_session.query(RbPolBeerMapping)\
        .filter(RbPolBeerMapping.resolved == False)\
        .all()
    suggestions = [s.serialize() for s in suggestions]

    return Response(
        json.dumps(suggestions),
        content_type='application/json',
        status=200
    )


@app.route(api_prefix + '/pol_beer/<int:beer_id>/stock/', methods=['GET'])
def get_stock_for_beer(beer_id):
    lat = request.args.get('lat', None)
    lon = request.args.get('lon', None)

    shops = current_app.db_session.query(PolShop, PolStock)\
        .filter(PolStock.shop_id == PolShop.id)\
        .filter(PolStock.pol_beer_id == beer_id)

    if lat and lon:
        lat = float(lat)
        lon = float(lon)

        shops = shops.order_by(
            "geog <-> ST_GeographyFromText('SRID=4326;POINT(%s %s)')" % (lon, lat)
        )
    else:
        shops = shops.order_by(PolShop.name)

    data = [{
        'pol_id': s[0].id,
        'name': s[0].name,
        'amount': s[1].stock,
        'updated': s[1].updated.isoformat(),
        'komm': s[0].komm_name,
        'fylke': s[0].fylke_name,
    } for s in shops.all()]

    return Response(
        json.dumps(data),
        content_type='application/json',
        status=200
    )


@app.route(api_prefix + '/pol_shops/', methods=['GET'])
def get_pol_shops():

    lat = request.args.get('lat', None)
    lon = request.args.get('lon', None)

    if lat and lon:
        lat = float(lat)
        lon = float(lon)

    order = "geog <-> ST_GeographyFromText('SRID=4326;POINT(%s %s)')" % (lon, lat)

    shops = current_app.db_session.query(PolShop)\
        .order_by(order)\
        .limit(10)\
        .all()

    return Response(
        json.dumps(shops),
        content_type='application/json',
        status=200
    )


@app.route(api_prefix + '/pol_beer/<int:beer_id>/stockhistory/', methods=['GET'])
def get_pol_stock_history(beer_id):
    connection = current_app.db_session.connection()
    history = connection.execute(
        text('SELECT sum(stock), updated::date from pol_stock where pol_beer_id = :beer_id group by updated::date order by updated'),
        beer_id=beer_id
    )

    return Response(
        json.dumps([{'stock': s[0], 'updated': s[1].isoformat()} for s in history]),
        content_type='application/json',
        status=200
    )
