# -*- coding: utf-8 -*-

import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from flask.ext.jsontools import JsonSerializableBase

from util import ratebeer_url

Base = declarative_base(cls=(JsonSerializableBase,))


class BeerStyle(Base):
    __tablename__ = 'style'
    id = sa.Column('id', sa.Integer, primary_key=True)
    name = sa.Column('name', sa.Unicode(255))


class RatebeerBeer(Base):
    __tablename__ = 'rb_beer'
    id = sa.Column('id', sa.Integer, primary_key=True)
    name = sa.Column('name', sa.Unicode(255))
    shortname = sa.Column('shortname', sa.Unicode(255))
    alias = sa.Column('alias', sa.Boolean)
    retired = sa.Column('retired', sa.Boolean)
    style_id = sa.Column('style_id', sa.Integer, sa.ForeignKey('style.id'))
    style = relationship('BeerStyle', lazy=False)
    score_overall = sa.Column('score_overall', sa.Float)
    score_style = sa.Column('score_style', sa.Float)
    abv = sa.Column('abv', sa.Float)
    ibu = sa.Column('ibu', sa.Float)
    brewery_id = sa.Column('brewery_id', sa.Integer, sa.ForeignKey('rb_brewery.id'), nullable=False)
    brewery = relationship('RatebeerBrewery', lazy=False)
    pol_beers = relationship('PoletBeer', lazy=False, back_populates='ratebeer')

    def __init__(self):
        pass

    @property
    def url(self):
        print "!"
        return ratebeer_url(self.id, self.shortname)


class RatebeerBrewery(Base):
    __tablename__ = 'rb_brewery'
    id = sa.Column('id', sa.Integer, primary_key=True)
    name = sa.Column('name', sa.Unicode(255))
    country = sa.Column('country', sa.Integer)
    subregion = sa.Column('subregion', sa.Integer)
    city = sa.Column('city', sa.Unicode(255))

    def __init__(self):
        pass

    def get_list_response(self, count=None):
        return {
            'id': self.id,
            'name': self.name,
            'country': self.country,
            'num_beers_polet': count
        }


class PoletBeer(Base):
    __tablename__ = 'pol_beer'
    id = sa.Column('id', sa.Integer, primary_key=True)
    name = sa.Column('name', sa.Unicode(255))
    store_category = sa.Column('store_category', sa.Unicode(100))
    produktutvalg = sa.Column('produktutvalg', sa.Unicode(100))
    producer = sa.Column('producer', sa.Unicode(100))
    distributor = sa.Column('distributor', sa.Unicode(100))
    varenummer = sa.Column('varenummer', sa.Integer)
    abv = sa.Column('abv', sa.Float)
    volume = sa.Column('volume', sa.Float)
    color = sa.Column('color', sa.Unicode(100))
    smell = sa.Column('smell', sa.Unicode(100))
    taste = sa.Column('taste', sa.Unicode(100))
    method = sa.Column('method', sa.Unicode(255))
    cork_type = sa.Column('cork_type', sa.Unicode(100))
    packaging_type = sa.Column('packaging_type', sa.Unicode(100))
    price = sa.Column('price', sa.Float)
    country = sa.Column('country', sa.Unicode(100))
    district = sa.Column('district', sa.Unicode(100))
    subdistrict = sa.Column('subdistrict', sa.Unicode(100))
    url = sa.Column('url', sa.Unicode(100))
    vintage = sa.Column('vintage', sa.Unicode(100))
    ingredients = sa.Column('ingredients', sa.Unicode(255))
    pairs_with_1 = sa.Column('pairs_with_1', sa.Unicode(255))
    pairs_with_2 = sa.Column('pairs_with_2', sa.Unicode(255))
    pairs_with_3 = sa.Column('pairs_with_3', sa.Unicode(255))
    storage_notes = sa.Column('storage_notes', sa.Unicode(255))
    sweetness = sa.Column('sweetness', sa.Integer)
    freshness = sa.Column('freshness', sa.Integer)
    bitterness = sa.Column('bitterness', sa.Integer)
    richness = sa.Column('richness', sa.Integer)
    ratebeer_id = sa.Column('ratebeer_id', sa.Integer, sa.ForeignKey('rb_beer.id'), nullable=True)
    ratebeer = relationship('RatebeerBeer', lazy=False, back_populates='pol_beers')

    def __init__(self):
        pass

    def get_list_response(self):
        has_rb = self.ratebeer is not None
        return {
            'name': self.ratebeer.name if has_rb else self.name,
            'brewery': self.ratebeer.brewery.name if has_rb else self.producer,
            'brewery_id': self.ratebeer.brewery.id if has_rb else None,
            'style': self.ratebeer.style.name if has_rb else None,
            'style_id': self.ratebeer.style.id if has_rb else None,
            'abv': self.ratebeer.abv if has_rb else None,
            'price': self.price,
            'score_overall': self.ratebeer.score_overall if has_rb else None,
            'score_style': self.ratebeer.score_style if has_rb else None,
            'has_rb': has_rb,
            'id': self.id,
        }
