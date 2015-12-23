# -*- coding: utf-8 -*-

from flask import render_template, json
from flask.views import View


class GenericView(View):

    def __init__(self, data_func, jsbundle, div_name, init_func, title):
        self.data_func = data_func
        self.jsbundle = jsbundle
        self.div_name = div_name
        self.init_func = init_func
        self.title = title

    def dispatch_request(self, id=None):

        if id is not None:
            d = self.data_func(id)
        else:
            d = self.data_func()

        if isinstance(d, tuple):
            data = d[0]
            title = d[1]
            redirect = d[2]
        else:
            data = d
            title = None
            redirect = None

        if redirect:
            return redirect

        if title is None:
            title = self.title

        return render_template(
            'generic_js_template.html',
            json=json.dumps(data),
            div_name=self.div_name,
            jsbundle=self.jsbundle,
            init_func=self.init_func,
            title=title
        )


def view_adder(app):

    def add_view(data):
        if data.get('view_type', None) == 'standard_view':
            app.add_url_rule(
                data.get('path', None),
                data.get('name', None),
                data.get('data_func', None)
            )
        else:
            app.add_url_rule(
                data.get('path', None),
                view_func=GenericView.as_view(
                    data.get('name', None),
                    title=data.get('title', None),
                    data_func=data.get('data_func', None),
                    jsbundle=data.get('name', '') + '_bundle',
                    div_name=data.get('name', None),
                    init_func=data.get('js_func', None)
                )
            )

    return add_view
