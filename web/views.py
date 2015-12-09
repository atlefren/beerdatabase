# -*- coding: utf-8 -*-

from flask import render_template, abort, json, redirect, url_for, request
from flask.views import View

from web import app
import queries


@app.template_filter('ratebeer_url')
def get_ratebeer_url(ratebeer_beer):
    # return ratebeer_url(ratebeer_beer.id, ratebeer_beer.shortname)
    pass


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/pol_beers/')
def pol_beers():
    pol_beers = queries.get_pol_beers_list()
    return render_template('pol_beer_list.html', json=json.dumps(pol_beers))


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


@app.route('/search')
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


def fix_beer(pol_beer, rb_beer=None):

    data = {
        'pol_beer': pol_beer.serialize(),
        'rb_beer': rb_beer.serialize() if rb_beer is not None else None
    }

    return render_template('fix_beer.html', json=json.dumps(data))


@app.route('/pol_beers/unmatched/')
def unmatched_beers():
    unmatched = queries.get_unmatched_pol_beers()
    return render_template('unmatched.html', json=json.dumps(unmatched))


@app.route('/pol_beers/match_suggestions/')
def match_suggestions():
    suggestions = queries.get_unresolved_pol_suggestions()
    return render_template(
        'match_suggestions.html',
        json=json.dumps(suggestions)
    )


@app.route('/beers/<int:id>')
def beer(id):
    beer = queries.get_beer(id)
    if not beer:
        abort(404)

    if len(beer.pol_beers) == 0:
        return u'Ikke på polet'

    if len(beer.pol_beers) > 1:
        return u'Flere på polet'

    return redirect(url_for('pol_beer', id=beer.pol_beers[0].id))


@app.route('/pol_beers/<int:id>')
def pol_beer(id):
    pol_beer = queries.get_pol_beer(id)
    if not pol_beer:
        abort(404)
    if pol_beer.ratebeer is None:
        return fix_beer(pol_beer)

    serialized = pol_beer.serialize()
    stock = queries.get_total_pol_beer_stock(id)

    serialized['stock'] = stock

    return render_template(
        'pol_beer.html',
        json=json.dumps(serialized)
    )


@app.route('/pol_beers/<int:id>/report')
def pol_beer_report(id):
    pol_beer = queries.get_pol_beer(id)
    if not pol_beer:
        abort(404)
    return fix_beer(pol_beer, pol_beer.ratebeer)


@app.route('/styles/')
def style_list():
    # TODO limit to available styles at polet
    styles = queries.get_style_list()
    return render_template('style_list.html', json=json.dumps(styles))


@app.route('/styles/<int:id>')
def style(id):
    style = queries.get_style(id)
    if not style:
        abort(404)
    beers = queries.get_beers_for_style(id)
    return render_template(
        'style.html',
        json=json.dumps(beers),
        style=style,
        num=len(beers)
    )


@app.route('/breweries/')
def brewery_list():
    breweries = queries.get_breweries_at_polet()
    return render_template('brewery_list.html', json=json.dumps(breweries))


@app.route('/breweries/<int:brewery_id>')
def brewery(brewery_id):
    brewery = queries.get_brewery(brewery_id)
    if not brewery:
        abort(404)
    beers = queries.get_pol_beers_for_brewery(brewery_id)
    return render_template(
        'brewery.html',
        json=json.dumps(beers),
        brewery=brewery,
        num=len(beers)
    )


@app.route('/pol_shops/')
def pol_shops():
    shops = queries.get_pol_shops()
    municipalities = queries.get_all_municipalities()
    return render_template(
        'pol_shops.html',
        json=json.dumps(shops),
        municipalities_json=json.dumps(municipalities)
    )


@app.route('/pol_shops/<int:shop_id>')
def pol_shop(shop_id):
    shop = queries.get_pol_shop(shop_id)
    if shop is None:
        abort(404)
    beers = queries.get_beers_for_shop(shop_id)
    return render_template(
        'pol_shop.html',
        json=json.dumps(shop),
        beers_json=json.dumps(beers)
    )


class GenericView(View):

    def __init__(self, data_func, jsbundle, div_name, init_func, title):
        self.data_func = data_func
        self.jsbundle = jsbundle
        self.div_name = div_name
        self.init_func = init_func
        self.title = title

    def dispatch_request(self, id=None):

        if id is not None:
            data = self.data_func(id)
        else:
            data = self.data_func()

        return render_template(
            'generic_js_template.html',
            json=json.dumps(data),
            div_name=self.div_name,
            jsbundle=self.jsbundle,
            init_func=self.init_func,
            title=self.title
        )


app.add_url_rule(
    '/countries/<string:id>',
    view_func=GenericView.as_view(
        'country',
        title='Land',
        data_func=queries.get_country,
        jsbundle='country_bundle',
        div_name='country',
        init_func='bd.renderBeersInCountryList'
    )
)


app.add_url_rule(
    '/countries/',
    view_func=GenericView.as_view(
        'country_list',
        title='Land',
        data_func=queries.get_countries,
        jsbundle='country_list_bundle',
        div_name='country_list',
        init_func='bd.renderCountryList'
    )
)
