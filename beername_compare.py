# -*- coding: utf-8 -*-
import json
from collections import defaultdict
import codecs

from beertools import BreweryNameMatcher
from beertools import BeerNameMatcher
from beertools.util import read_json, parse_pol_abv


def get_breweries_polet():
    with open('data/polet.json', 'r') as infile:
        data = json.loads(infile.read())

        breweries = list(set([product['Produsent'] for product in data]))
        return sorted(breweries), data


def get_breweries(beer_list, property_name):
    return sorted(list(set([beer[property_name] for beer in beer_list])))


def get_breweries_ratebeer():
    with open('data/ratebeer.json', 'r') as infile:
        data = json.loads(infile.read())
        breweries = list(set([product['brewery'] for product in data]))
        return sorted(breweries)


def get_beers(beer_list, brewery_name, attr_name):
    return [beer for beer in beer_list if beer[attr_name] == brewery_name]


def find_in_list(dicts, key, value):
    return (item for item in dicts if item[key] == value).next()


def findall_in_list(dicts, key, value):
    return [item for item in dicts if item[key] == value]


def get_textfile(filename):
    with codecs.open(filename, 'r', 'utf-8') as infile:
        return [unicode(line) for line in infile.read().splitlines()]


def find_in_fasit(name, fasit):
    for line in fasit:
        if line.startswith(name):
            return line


def compare_beers(pol_data, rb_beers, breweries_rb):

    fasit = get_textfile('beer_compare_fasit.txt')
    known_errors = get_textfile('err_polet.txt')

    breweries_pol = get_breweries(pol_data, 'Produsent')

    grouped = defaultdict(list)

    brewery_matcher = BreweryNameMatcher(breweries_rb)
    for brewery_pol in breweries_pol:
        match = brewery_matcher.match_name(brewery_pol)
        if match is not None:
            grouped[match['id']].append(brewery_pol)

    errors = []
    nomatches = []
    num_err = 0
    for key, value in grouped.iteritems():
        rb_brewery = find_in_list(breweries_rb, 'id', key)['name']
        rb_beers_for_brewery = findall_in_list(rb_beers, 'brewery_id', key)

        beer_matcher = BeerNameMatcher(rb_brewery, rb_beers_for_brewery, skip_retired=True)
        for pol_brewery in value:
            pol_beers = findall_in_list(pol_data, 'Produsent', pol_brewery)
            for pol_beer in pol_beers:
                pol_beer_name = pol_beer['Varenavn']
                abv = parse_pol_abv(pol_beer['Alkohol'])
                beer_match = beer_matcher.match_name(pol_beer_name, abv=abv)

                score = None
                if isinstance(beer_match, tuple):
                    score = beer_match[1]
                    beer_match = beer_match[0]

                nameline = None

                if beer_match is None:
                    nameline = '%s - %s' % (pol_brewery, pol_beer_name)

                    if nameline in known_errors:
                        num_err = num_err + 1
                    else:
                        f = find_in_fasit(nameline, fasit)
                        if f:
                            nomatches.append(f)
                        else:
                            nomatches.append(nameline)
                else:
                    nameline = '%s - %s :: %s - %s' % (pol_brewery, pol_beer_name, rb_brewery, beer_match['name'])
                    if nameline not in fasit:
                        if score is not None:
                            nameline = '%s (%s)' % (nameline, score)
                        errors.append(nameline)

    print '%s errors' % len(errors)
    print '%s nomatch' % len(nomatches)
    print '%s wrong from polet' % num_err
    with codecs.open('data/beer_errors.txt', 'w', 'utf-8') as err_file:
        err_file.write('NO MATCH\n\n')
        for error in nomatches:
            err_file.write('%s\n' % error)
        err_file.write('\n\nERR\n\n')
        for error in errors:
            err_file.write('%s\n' % error)


'''
    with open('data/beer_nomatch.txt', 'w') as nomatch:
        brewery_matcher = BreweryNameMatcher(breweries_rb)
        for brewery in breweries_pol:
            match = brewery_matcher.match_name(brewery)
            if match is not None:
                rb_beers = get_beers(rb_data, match['name'], 'brewery')
                beer_matcher = BeerNameMatcher(match['name'], rb_beers)

                nomatch.write(match['name'].encode('utf8') + '\n')
                pol_beers = get_beers(pol_data, brewery, 'Produsent')
                for pol_beer in pol_beers:
                    beer_match = beer_matcher.match_name(pol_beer['Varenavn'])
                    if not beer_match:
                        string = '\t%s ' % pol_beer['Varenavn']
                        nomatch.write(string.encode('utf8') + '\n')
'''
if __name__ == '__main__':
    pol_data = read_json('data/polet.json')
    rb_beers = read_json('data/rb_beers.json')
    rb_breweries = read_json('data/rb_breweries.json')
    compare_beers(pol_data, rb_beers, rb_breweries)
