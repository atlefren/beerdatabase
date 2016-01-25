# -*- coding: utf-8 -*-

from flask import request, render_template, json

import queries


def get_param_list_str(param):
    val = request.args.get(param, None)
    if val is not None and val != '':
        return val.split(',')


def get_param_list_int(param):
    val = get_param_list_str(param)
    if val is not None:
        return [int(x) for x in val if val != '']


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
    pol = queries.get_pol()
    search_params = {
        'styles': styles,
        'pol': pol
    }

    search_defaults['style'] = []
    search_defaults['pol'] = []

    init_values = {
        'style': get_param_list_int('style'),
        'name': request.args.get('name', None),
        'overallScore': get_param_list_int('overallScore'),
        'styleScore': get_param_list_int('styleScore'),
        'price': get_param_list_int('price'),
        'abv': get_param_list_float('abv'),
        'availableAt': get_param_list_str('availableAt'),
        'pol': get_param_list_int('pol'),
    }

    from_query_params = False
    for key, search_value in init_values.iteritems():
        if search_value is None:
            init_values[key] = search_defaults[key]
        else:
            from_query_params = True

    data = {
        'search_params': search_params,
        'init_values': init_values,
        'startWithSearch': from_query_params,
        'initialSort': request.args.get('initialSort', None),
    }

    return render_template(
        'search.html',
        data=json.dumps(data)
    )
