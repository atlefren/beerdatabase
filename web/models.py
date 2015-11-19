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


class RatebeerCountry(Base):
    __tablename__ = 'rb_countries'
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
        return ratebeer_url(self.id, self.shortname)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'shortname': self.shortname,
            'alias': self.alias,
            'retired': self.retired,
            'style_id': self.style_id,
            'style': self.style,
            'score_overall': self.score_overall,
            'score_style': self.score_style,
            'abv': self.abv,
            'ibu': self.ibu,
            'url': self.url,
            'brewery': self.brewery,
        }


class RatebeerBrewery(Base):
    __tablename__ = 'rb_brewery'
    id = sa.Column('id', sa.Integer, primary_key=True)
    name = sa.Column('name', sa.Unicode(255))
    country_id = sa.Column('country', sa.Integer, sa.ForeignKey('rb_countries.id'))
    country = relationship('RatebeerCountry', lazy=False)
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

    def get_list_response(self, extra_data=None):
        has_rb = self.ratebeer is not None
        res = {
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
        if isinstance(extra_data, dict):
            res.update(extra_data)
        return res

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'store_category': self.store_category,
            'produktutvalg': self.produktutvalg,
            'producer': self.producer,
            'distributor': self.distributor,
            'varenummer': self.varenummer,
            'abv': self.abv,
            'volume': self.volume,
            'color': self.color,
            'smell': self.smell,
            'taste': self.taste,
            'method': self.method,
            'cork_type': self.cork_type,
            'packaging_type': self.packaging_type,
            'price': self.price,
            'country': self.country,
            'district': self.district,
            'subdistrict': self.subdistrict,
            'url': self.url,
            'vintage': self.vintage,
            'ingredients': self.ingredients,
            'pairs_with_1': self.pairs_with_1,
            'pairs_with_2': self.pairs_with_2,
            'pairs_with_3': self.pairs_with_3,
            'storage_notes': self.storage_notes,
            'sweetness': self.sweetness,
            'freshness': self.freshness,
            'bitterness': self.bitterness,
            'richness': self.richness,
            'ratebeer': self.ratebeer.serialize() if self.ratebeer is not None else None,
        }


class RbPolBeerMapping(Base):
    __tablename__ = 'pol_to_rb_mapping'
    id = sa.Column('id', sa.Integer, primary_key=True)
    comment = sa.Column('comment', sa.Unicode(255))
    resolved = sa.Column('resolved', sa.Boolean, default=False)
    rb_beer_id = sa.Column('rb_beer_id', sa.Integer, sa.ForeignKey('rb_beer.id'), nullable=False)
    rb_beer = relationship('RatebeerBeer', lazy=False)
    pol_beer_id = sa.Column('pol_beer_id', sa.Integer, sa.ForeignKey('pol_beer.id'), nullable=False)
    pol_beer = relationship('PoletBeer', lazy=False)

    def __init__(self, pol_id=None, rb_id=None, comment=None):
        self.rb_beer_id = rb_id
        self.pol_beer_id = pol_id
        self.comment = comment

    def serialize(self):
        return {
            'id': self.id,
            'comment': self.comment,
            'rb_beer_id': self.rb_beer_id,
            'pol_beer_id': self.pol_beer_id,
            'pol_beer': self.pol_beer.serialize(),
            'rb_beer': self.rb_beer.serialize() if self.rb_beer is not None else None
        }


class PolShop(Base):
    __tablename__ = 'pol_shop'
    id = sa.Column('id', sa.Integer, primary_key=True)
    name = sa.Column('name', sa.Unicode(100))
    street_address = sa.Column('street_address', sa.Unicode(100))
    street_zipcode = sa.Column('street_zipcode', sa.Integer)
    street_place = sa.Column('street_place', sa.Unicode(100))
    post_address = sa.Column('post_address', sa.Unicode(100))
    post_zipcode = sa.Column('post_zipcode', sa.Integer)
    post_place = sa.Column('post_place', sa.Unicode(100))
    phone = sa.Column('phone', sa.Unicode(30))
    category = sa.Column('category', sa.Integer)
    lon = sa.Column('lon', sa.Float)
    lat = sa.Column('lat', sa.Float)


class PolStock(Base):
    __tablename__ = 'pol_stock'
    id = sa.Column('id', sa.Integer, primary_key=True)
    stock = sa.Column('stock', sa.Integer)
    updated = sa.Column('updated', sa.DateTime)
    shop_id = sa.Column('shop_id', sa.Integer, sa.ForeignKey('pol_shop.id'), nullable=False)
    pol_beer_id = sa.Column('pol_beer_id', sa.Integer, sa.ForeignKey('pol_beer.id'), nullable=False)
