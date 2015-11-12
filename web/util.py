# -*- coding: utf-8 -*-
import re


RATEBEER_BASE_URL = 'http://www.ratebeer.com/beer'


def ratebeer_url(ratebeer_id, short_name):
    fixed_name = re.sub(
        '[^A-Za-z0-9\-]+',
        '',
        short_name.replace(' ', '-')
    )
    return "%s/%s/%s/" % (RATEBEER_BASE_URL, fixed_name, ratebeer_id)
