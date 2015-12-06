# -*- coding: utf-8 -*-
import json
import os

from db import Database


def read_json(filename):
    path = os.path.dirname(os.path.realpath(__file__))
    with open(path + '/' + filename, 'r') as file:
        return json.loads(file.read())


def insert_fylke(db):
    fc = read_json('data/fylker.geojson')
    fylker = []
    for feature in fc['features']:
        fylker.append({
            'fylkesnr': feature['properties']['fylkesnr'],
            'name': feature['properties']['navn'],
            'geom': json.dumps(feature['geometry'])
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
    kommuner = []
    for feature in fc['features']:
        kommuner.append({
            'kommnr': feature['properties']['komm'],
            'name': feature['properties']['navn'],
            'geom': json.dumps(feature['geometry'])
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
