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


def search():

    styles = queries.get_styles()

    search_params = {
        'styles': styles
    }

    search_values = {
        'style': get_param_list_int('style'),
        'name': request.args.get('name', None),
        'overallScore': get_param_list_int('overallScore'),
        'styleScore': get_param_list_int('styleScore'),
        'price': get_param_list_int('price'),
        'abv': get_param_list_float('abv'),
        'availableAt': get_param_list_str('availableAt'),
    }

    if search_values.get('style') is None:
        search_values['style'] = [s.id for s in styles]
    if search_values.get('name') is None:
        search_values['name'] = ''
    if search_values.get('overallScore') is None:
        search_values['overallScore'] = [0, 100]
    if search_values.get('styleScore') is None:
        search_values['styleScore'] = [0, 100]
    if search_values.get('price') is None:
        search_values['price'] = [0, 200]
    if search_values.get('abv') is None:
        search_values['abv'] = [0, 50]
    if search_values.get('availableAt') is None:
        search_values['availableAt'] = ['polet']

    return render_template(
        'search.html',
        search_params=json.dumps(search_params),
        search_values=json.dumps(search_values),
    )
