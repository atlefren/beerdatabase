# -*- coding: utf-8 -*-
import json

from beertools import get_osm_breweries, BreweryNameMatcher

from db import Database


def map_breweries_for_country(db, rb_id, iso_code):
    breweries_osm = get_osm_breweries('NO')
    breweries_rb = db.get_rb_breweries_for_country(rb_id)
    brewery_matcher = BreweryNameMatcher(breweries_rb)
    matches = []
    for brewery in breweries_osm['features']:
        match = brewery_matcher.match_name(unicode(brewery['properties']['name']))
        if match is not None:
            matches.append({
                'osm_id': brewery['id'],
                'ratebeer_id': match['id'],
                'geom': json.dumps(brewery['geometry'])
            })
    return matches


SQL = '''
        INSERT INTO rb_brewery_position (osm_id, ratebeer_id, geom)
        VALUES (%(osm_id)s, %(ratebeer_id)s, ST_SetSRID(ST_GeomFromGeoJSON(%(geom)s), 4326))
        ON CONFLICT (osm_id) DO UPDATE
        SET (osm_id, ratebeer_id, geom) = (%(osm_id)s, %(ratebeer_id)s, ST_SetSRID(ST_GeomFromGeoJSON(%(geom)s), 4326));
    '''


def update_brewery_positions(conn_str=None):
    db = Database(conn_str)
    countries = {'154': 'NO'}

    matches = []
    for rb_id, iso_code in countries.iteritems():
        matches += map_breweries_for_country(db, rb_id, iso_code)
    db.run_upserts(SQL, matches)
    db.add_log('osm')

if __name__ == '__main__':
    update_brewery_positions()
