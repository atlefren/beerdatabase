# -*- coding: utf-8 -*-
import json
import os
from collections import defaultdict

from db import Database


def read_json(filename):
    path = os.path.dirname(os.path.realpath(__file__))
    with open(path + '/' + filename, 'r') as file:
        return json.loads(file.read())


def create_multipoly(polys):
    return {
        'type': 'MultiPolygon',
        'coordinates': [poly['coordinates'] for poly in polys]
    }


def insert_fylke(db):
    fc = read_json('data/fylker.geojson')
    fylker_coll = defaultdict(list)
    for feature in fc['features']:
        fylker_coll[feature['properties']['fylkesnr']].append(feature)

    fylker = []
    for key, fylke in fylker_coll.iteritems():
        polys = [f['geometry'] for f in fylke]

        feature = fylke[0]
        fylker.append({
            'fylkesnr': feature['properties']['fylkesnr'],
            'name': feature['properties']['navn'],
            'geom': json.dumps(create_multipoly(polys))
        })
    sql = '''
        INSERT INTO fylke (fylkesnr, name, geom)
        VALUES (%(fylkesnr)s, %(name)s, ST_SetSRID(ST_GeomFromGeoJSON(%(geom)s), 4326))
        ON CONFLICT (fylkesnr) DO UPDATE
        SET (fylkesnr, name, geom) =
        (%(fylkesnr)s, %(name)s, ST_SetSRID(ST_GeomFromGeoJSON(%(geom)s), 4326));
    '''
    db.run_upserts(sql, fylker)


def insert_kommune(db):
    fc = read_json('data/kommuner.geojson')
    komm_coll = defaultdict(list)
    for feature in fc['features']:
        komm_coll[feature['properties']['komm']].append(feature)

    kommuner = []
    for key, kommune in komm_coll.iteritems():
        polys = [k['geometry'] for k in kommune]
        feature = kommune[0]
        kommuner.append({
            'kommnr': feature['properties']['komm'],
            'name': feature['properties']['navn'],
            'geom': json.dumps(create_multipoly(polys))
        })
    sql = '''
        INSERT INTO kommune (kommnr, name, geom)
        VALUES (%(kommnr)s, %(name)s, ST_SetSRID(ST_GeomFromGeoJSON(%(geom)s), 4326))
        ON CONFLICT (kommnr) DO UPDATE
        SET (kommnr, name, geom) =
        (%(kommnr)s, %(name)s, ST_SetSRID(ST_GeomFromGeoJSON(%(geom)s), 4326));
    '''
    db.run_upserts(sql, kommuner)


def update_adminareas(conn_str=None):
    db = Database(conn_str)
    insert_fylke(db)
    insert_kommune(db)


if __name__ == '__main__':
    update_adminareas()
