# -*- coding: utf-8 -*-

from flask import current_app, json, request, Response

from web import app
from models import (RatebeerBeer, RatebeerBrewery, RbPolBeerMapping, PoletBeer)


api_prefix = '/api/v1'


def get_limit():
    limit = request.args.get('limit', 10, type=int)
    return limit if limit <= 100 else 100


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
def search():
    query = request.args.get('q')
    db = current_app.db_session
    res = db.query(RatebeerBeer).filter(RatebeerBeer.name.ilike('%' + query + '%'))

    brewery_id = request.args.get('brewery', None)
    if brewery_id:
        res = res.filter(RatebeerBeer.brewery_id == brewery_id)
    x = res.limit(get_limit()).all()
    return Response(json.dumps(x), content_type='application/json')


@app.route(api_prefix + '/suggestions/', methods=['POST'])
def add_suggestion():
    data = request.json
    print data
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

    suggestion = current_app.db_session.query(RbPolBeerMapping)\
        .get(id)
    suggestion.resolved = True

    pol_beer = current_app.db_session.query(PoletBeer)\
        .get(data.get('pol_id', None))
    pol_beer.ratebeer_id = data.get('rb_id', None)

    current_app.db_session.commit()

    suggestions = current_app.db_session.query(RbPolBeerMapping)\
        .filter(RbPolBeerMapping.resolved == False)\
        .all()

    return Response(
        json.dumps(suggestions),
        content_type='application/json',
        status=200
    )
