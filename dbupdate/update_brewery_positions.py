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
        props = brewery['properties']
        match = brewery_matcher.match_name(unicode(props['operator']))
        if match is None:
            match = brewery_matcher.match_name(unicode(props['name']))
        add = {
            'osm_id': brewery['id'],
            'ratebeer_id': None,
            'website': props['website'],
            'amenity': props['amenity'],
            'housenumber': props['housenumber'],
            'city': props['city'],
            'postcode': props['postcode'],
            'street': props['street'],
            'country': props['country'],
            'name': props['name'],
            'operator': props['operator'],
            'geom': json.dumps(brewery['geometry'])
        }
        if match is not None:
            add['ratebeer_id'] = match['id']
        matches.append(add)

    return matches

SQL = '''
        INSERT INTO rb_brewery_position (osm_id, ratebeer_id, website, amenity, housenumber, city, postcode, street, country, name, operator, geom)
        VALUES (%(osm_id)s, %(ratebeer_id)s, %(website)s, %(amenity)s, %(housenumber)s, %(city)s, %(postcode)s, %(street)s, %(country)s, %(name)s, %(operator)s,  ST_SetSRID(ST_GeomFromGeoJSON(%(geom)s), 4326))
        ON CONFLICT (osm_id) DO UPDATE
        SET (osm_id, ratebeer_id, website, amenity, housenumber, city, postcode, street, country, name, operator, geom) = (%(osm_id)s, %(ratebeer_id)s, %(website)s, %(amenity)s, %(housenumber)s, %(city)s, %(postcode)s, %(street)s, %(country)s, %(name)s, %(operator)s,  ST_SetSRID(ST_GeomFromGeoJSON(%(geom)s), 4326));
    '''


def update_brewery_positions(conn_str=None):
    db = Database(conn_str)
    countries = {'154': 'NO'}

    matches = []
    for rb_id, iso_code in countries.iteritems():
        matches += map_breweries_for_country(db, rb_id, iso_code)
    db.run_upserts(SQL, matches)

    ids = [m['osm_id'] for m in matches]
    delete_sql = '''
        DELETE FROM rb_brewery_position where osm_id NOT IN %s;
    '''
    db.execute_sql(delete_sql, tuple(ids))

    db.add_log('osm')

if __name__ == '__main__':
    update_brewery_positions()
