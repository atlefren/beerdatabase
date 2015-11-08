# -*- coding: utf-8 -*-
from collections import defaultdict
import json

import psycopg2
from beertools import read_pol_beers, BreweryNameMatcher, BeerNameMatcher
from beertools.util import parse_pol_abv

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)


def find_in_list(dicts, key, value):
    return (item for item in dicts if item[key] == value).next()


def findall_in_list(dicts, key, value):
    return [item for item in dicts if item[key] == value]


def get_pol_beers():
    with open('data/polet.json', 'r') as infile:
        return json.loads(infile.read())


def get_breweries_polet(beers_polet):
    breweries = list(set([product['Produsent'] for product in beers_polet]))
    return sorted(breweries)


def get_connection():
    conn_string = "host='localhost' dbname='beer' user='beer' password='beer'"
    return psycopg2.connect(conn_string)


def match_pol_breweries(breweries_pol, breweries_rb):
    grouped = defaultdict(list)

    brewery_matcher = BreweryNameMatcher(breweries_rb)
    for brewery_pol in breweries_pol:
        match = brewery_matcher.match_name(unicode(brewery_pol))
        if match is not None:
            grouped[match['id']].append(brewery_pol)
    return grouped


def get_rb_beers_for_brewery(brewery_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        'SELECT id, name, retired, abv FROM rb_beer WHERE brewery_id=%s',
        (brewery_id,)
    )
    beers = []
    for row in cur.fetchall():
        beers.append({
            'id': row[0],
            'name': row[1],
            'retired': row[2],
            'abv': row[3]
        })
    cur.close()
    conn.close()
    return beers


def get_rb_breweries():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, name FROM rb_brewery')
    breweries = []
    for row in cur.fetchall():
        breweries.append({
            'id': row[0],
            'name': row[1]
        })
    cur.close()
    conn.close()
    return breweries


if __name__ == '__main__':

    beers_polet = get_pol_beers()

    breweries_rb = get_rb_breweries()
    breweries_pol = get_breweries_polet(beers_polet)

    matched_pol_rb = match_pol_breweries(breweries_pol, breweries_rb)

    for rb_beer_id, pol_breweries in matched_pol_rb.iteritems():
        rb_brewery = find_in_list(breweries_rb, 'id', rb_beer_id)['name']
        rb_beers_for_brewery = get_rb_beers_for_brewery(rb_beer_id)
        beer_matcher = BeerNameMatcher(
            rb_brewery,
            rb_beers_for_brewery,
            skip_retired=True
        )
        for pol_brewery in pol_breweries:
            pol_beers = findall_in_list(beers_polet, 'Produsent', pol_brewery)

            for pol_beer in pol_beers:
                pol_beer_name = pol_beer['Varenavn']
                abv = parse_pol_abv(pol_beer['Alkohol'])
                beer_match = beer_matcher.match_name(pol_beer_name, abv=abv)
                if beer_match is None:
                    nameline = '%s - %s' % (pol_brewery, pol_beer_name)
                    print nameline
                else:
                    print beer_match['id']
