# -*- coding: utf-8 -*-

from flask import render_template, abort, redirect, url_for

from generic_view import view_adder
from web import app
from search import search
import queries
import data


def find_rb_beer(id):
    beer = queries.get_beer(id)
    if not beer:
        abort(404)

    if len(beer.pol_beers) == 0:
        return u'Ikke på polet'

    if len(beer.pol_beers) > 1:
        return u'Flere på polet'

    return redirect(url_for('pol_beer', id=beer.pol_beers[0].id))


def index():
    return render_template('index.html')

pages = [
    {
        'path': '/',
        'name': 'index',
        'view_type': 'standard_view',
        'data_func': index,
    },
    {
        'path': '/search/',
        'name': 'search',
        'view_type': 'standard_view',
        'data_func': search
    },
    {
        'path': '/breweries/',
        'name': 'brewery_list',
        'title': 'Bryggerier',
        'data_func': data.queries.get_breweries_at_polet,
        'js_func': 'bd.renderBreweryListPage'
    },
    {
        'path': '/breweries/<int:id>',
        'name': 'brewery',
        'data_func': data.get_brewery_data,
        'js_func': 'bd.renderBreweryPage'
    },
    {
        'path': '/styles/',
        'name': 'style_list',
        'title': u'Ølstiler',
        'data_func': data.queries.get_style_list,
        'js_func': 'bd.renderStyleList'
    },
    {
        'path': '/styles/<int:id>',
        'name': 'style',
        'data_func': data.get_style_data,
        'js_func': 'bd.renderStylePage'
    },
    {
        'path': '/countries/',
        'name': 'country_list',
        'title': 'Land',
        'data_func': queries.get_countries,
        'js_func': 'bd.renderCountryList'
    },
    {
        'path': '/countries/<string:id>',
        'name': 'country',
        'data_func': data.get_country,
        'js_func': 'bd.renderBeersInCountryList'
    },
    {
        'path': '/pol_shops/',
        'name': 'pol_shop_list',
        'title': u'Polutsalg',
        'data_func': data.get_pol_shop_list,
        'js_func': 'bd.renderPolShopList'
    },
    {
        'path': '/pol_shops/<int:id>',
        'name': 'pol_shop',
        'data_func': data.get_pol_shop_data,
        'js_func': 'bd.renderPolShopOverview'
    },
    {
        'path': '/pol_beers/<int:id>',
        'name': 'pol_beer',
        'data_func': data.get_pol_beer,
        'js_func': 'bd.renderBeerOverview'
    },
    {
        'path': '/pol_beers/unmatched/',
        'name': 'unmatched',
        'title': u'Umatcha øl',
        'data_func': queries.get_unmatched_pol_beers,
        'js_func': 'bd.renderUnmatchedPolBeersPage'
    },
    {
        'path': '/pol_beers/<int:id>/report',
        'name': 'fix_beer',
        'title': u'Fiks ølmatching',
        'data_func': data.get_beer_fix_data,
        'js_func': 'bd.renderBeerFixer'
    },
    {
        'path': '/admin/pol_match',
        'name': 'match_suggestions',
        'title': u'Matcheforslag',
        'data_func': queries.get_unresolved_pol_suggestions,
        'js_func': 'bd.renderBeerFixSuggestions'
    },
    {
        'path': '/beers/<int:id>',
        'name': 'find_rb_beer',
        'view_type': 'standard_view',
        'data_func': find_rb_beer
    }
]


add_view = view_adder(app)

for page in pages:
    add_view(page)
