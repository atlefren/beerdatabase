# -*- coding: utf-8 -*-

from flask import request, render_template, json

import queries


def get_param_list_str(param):
    val = request.args.get(param, None)
    if val is not None:
        return val.split(',')


def get_param_list_int(param):
    val = get_param_list_str(param)
    if val is not None:
        return [int(x) for x in val]


def get_param_list_float(param):
    val = get_param_list_str(param)
    if val is not None:
        return [float(x) for x in val]


search_defaults = {
    'style': None,
    'name': '',
    'overallScore': [0, 100],
    'styleScore': [0, 100],
    'price': [0, 200],
    'abv': [0, 50],
    'availableAt': ['polet']
}


def search():
    styles = queries.get_styles()
    search_params = {
        'styles': styles
    }

    search_defaults['style'] = [s.id for s in styles]

    search_values = {
        'style': get_param_list_int('style'),
        'name': request.args.get('name', None),
        'overallScore': get_param_list_int('overallScore'),
        'styleScore': get_param_list_int('styleScore'),
        'price': get_param_list_int('price'),
        'abv': get_param_list_float('abv'),
        'availableAt': get_param_list_str('availableAt'),
    }

    for key, search_value in search_values.iteritems():
        if search_value is None:
            search_values[key] = search_defaults[key]

    return render_template(
        'search.html',
        search_params=json.dumps(search_params),
        search_values=json.dumps(search_values),
    )
