from flask.ext.assets import Bundle

from web import app

from react import jsx

transformer = jsx.JSXTransformer()


def react_filter(_in, out, **kw):
    ins = _in.read()
    print ins
    out.write(transformer.transform_string(ins))


js_filters = []
css_filters = []

minify = not app.debug

if minify:
    # Use jsmin and cssmin when not running in debug
    js_filters.append('jsmin')
    css_filters.append('cssmin')

css_base = Bundle(
    'js/lib/fontawesome/css/font-awesome.css',
    Bundle(
        'js/lib/skeleton/css/normalize.css',
        'js/lib/skeleton/css/skeleton.css',
        'css/base.css',
        filters=css_filters
    ),
    filters=['cssrewrite'],
    output='gen/css_base.css'
)


js_beer_list = Bundle(
    'js/lib/underscore/underscore-min.js',
    'js/lib/react/react.min.js',
    Bundle(
        'js/src/util.js',
        'js/src/PolBeerTable.jsx',
        filters=js_filters
    ),
    filters=[react_filter],
    output='beerlist.js'
)
