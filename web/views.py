# -*- coding: utf-8 -*-
import re

from flask import render_template, current_app
from beertools import polchecker

from web import app
from models import PoletBeer

RATEBEER_BASE_URL = 'http://www.ratebeer.com/beer'


def ratebeer_url(ratebeer_id, short_name):
    fixed_name = re.sub(
        '[^A-Za-z0-9\-]+',
        '',
        short_name.replace(' ', '-')
    )
    return "%s/%s/%s/" % (RATEBEER_BASE_URL, fixed_name, ratebeer_id)


@app.template_filter('ratebeer_url')
def get_ratebeer_url(ratebeer_beer):
    return ratebeer_url(ratebeer_beer.id, ratebeer_beer.shortname)


@app.route('/')
def index():
    pol_beers = current_app.db_session.query(PoletBeer).all()
    return render_template('index.html', pol_beers=pol_beers)


@app.route('/pol_beer/<int:id>')
def pol_beer(id):
    pol_beer = current_app.db_session.query(PoletBeer).get(id)
    available_at = polchecker.check_beer(pol_beer.id)
    return render_template('pol_beer.html', pol_beer=pol_beer, available_at=available_at)
