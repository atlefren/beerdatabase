# -*- coding: utf-8 -*-

from flask import render_template, abort, json

from web import app
import queries


@app.template_filter('ratebeer_url')
def get_ratebeer_url(ratebeer_beer):
    # return ratebeer_url(ratebeer_beer.id, ratebeer_beer.shortname)
    pass


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/pol_beers/')
def pol_beers():
    pol_beers = queries.get_pol_beers_list()
    return render_template('pol_beer_list.html', json=json.dumps(pol_beers))


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


@app.route('/pol_beers/<int:id>')
def pol_beer(id):
    pol_beer = queries.get_pol_beer(id)
    if not pol_beer:
        abort(404)
    if pol_beer.ratebeer is None:
        return fix_beer(pol_beer)
    return render_template(
        'pol_beer.html',
        json=json.dumps(pol_beer.serialize())
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
    return render_template('pol_shops.html', shops=shops)


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
