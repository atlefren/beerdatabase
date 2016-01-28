# -*- coding: utf-8 -*-

from flask.ext.assets import Bundle
from react import jsx

from web import app

transformer = jsx.JSXTransformer()


def react_filter(_in, out, **kw):
    out.write(transformer.transform_string(_in.read()))


js_filters = []
css_filters = []

minify = not app.debug

react = 'js/lib/react/react.js'
react_dom = 'js/lib/react/react-dom.js'

if minify:
    # Use jsmin and cssmin when not running in debug
    js_filters.append('jsmin')
    css_filters.append('cssmin')
    react = 'js/lib/react/react.min.js'

css_base = Bundle(
    'js/lib/fontawesome/css/font-awesome.css',
    Bundle(
        'js/lib/bootstrap/dist/css/bootstrap.min.css',
        'js/lib/nouislider/distribute/nouislider.min.css',
        'css/base_bs.css',
        'css/auocomplete_bs.css',
        filters=css_filters
    ),
    filters=['cssrewrite'],
    output='gen/css_base.css'
)


base_bundle = Bundle(
    'js/lib/underscore/underscore-min.js',
    'js/lib/jquery/dist/jquery.min.js',
    'js/lib/bootstrap/dist/js/bootstrap.min.js',
    'js/lib/atomic-fixed.js',
    react,
    react_dom,
    Bundle(
        'js/src/util.js',
        'js/src/api.js',
        'js/src/CommonComponents.jsx',
        'js/src/Autocomplete.jsx',
        'js/src/SimpleBeerSearch.jsx',
        'js/src/shoppingListStore.js',
        filters=js_filters
    )
)


def react_bundle(bundle, filename):
    return Bundle(
        base_bundle,
        bundle,
        filters=[react_filter],
        output='gen/' + filename
    )

index_bundle = react_bundle(
    Bundle(),
    'index.js'
)

brewery_list_bundle = react_bundle(
    Bundle(
        'js/src/SortableTable.jsx',
        'js/src/Pages/BreweryTable.jsx',
        filters=js_filters
    ),
    'brewery_list.js'
)

brewery_bundle = react_bundle(
    Bundle(
        'js/src/SortableTable.jsx',
        'js/src/PolBeerTable.jsx',
        'js/src/Pages/BreweryPage.jsx',
        filters=js_filters
    ),
    'brewery.js'
)

style_list_bundle = react_bundle(
    Bundle(
        'js/src/Pages/StyleList.jsx',
        filters=js_filters
    ),
    'style_list.js'
)

style_bundle = react_bundle(
    Bundle(
        'js/src/SortableTable.jsx',
        'js/src/PolBeerTable.jsx',
        'js/src/Pages/StylePage.jsx',
        filters=js_filters
    ),
    'style.js'
)


country_list_bundle = react_bundle(
    Bundle(
        'js/src/SortableTable.jsx',
        'js/src/Pages/CountryList.jsx',
        filters=js_filters
    ),
    'country_list.js'
)

country_bundle = react_bundle(
    Bundle(
        'js/src/SortableTable.jsx',
        'js/src/PolBeerTable.jsx',
        'js/src/Pages/BeersInCountryList.jsx',
        filters=js_filters
    ),
    'country.js'
)

pol_beer_bundle = react_bundle(
    Bundle(
        'js/lib/Chart.js/src/Chart.Core.js',
        'js/lib/Chart.js/src/Chart.Line.js',
        'js/lib/react-chartjs/dist/react-chartjs.js',
        'js/src/SortableTable.jsx',
        'js/src/PolWithBeer.jsx',
        'js/src/Pie.jsx',
        'js/src/Pages/BeerOverview.jsx',
        filters=js_filters
    ),
    'pol_beer.js'
)

pol_shop_list_bundle = react_bundle(
    Bundle(
        'js/src/SortableTable.jsx',
        'js/src/Pages/PolShopList.jsx',
        filters=js_filters
    ),
    'pol_shop_list.js'
)

pol_shop_bundle = react_bundle(
    Bundle(
        'js/src/SortableTable.jsx',
        'js/src/PolBeerTable.jsx',
        'js/src/Pages/PolShopOverview.jsx',
        filters=js_filters
    ),
    'pol_shop.js'
)

search_bundle = react_bundle(
    Bundle(
        'js/src/SortableTable.jsx',
        'js/src/PolBeerTable.jsx',
        'js/src/ItemChooser.jsx',
        'js/src/SliderFormGroup.jsx',
        'js/lib/nouislider/distribute/nouislider.min.js',
        'js/src/Pages/SearchPage.jsx',
        filters=js_filters
    ),
    'search.js'
)

unmatched_bundle = react_bundle(
    Bundle(
        'js/src/SortableTable.jsx',
        'js/src/PolBeerTable.jsx',
        'js/src/Pages/UnmatchedPolPage.jsx',
        filters=js_filters
    ),
    'unmatched.js'
)

fix_beer_bundle = react_bundle(
    Bundle(
        'js/src/Pages/BeerFixer.jsx',
        filters=js_filters
    ),
    'fix_beer.js'
)

match_suggestions_bundle = react_bundle(
    Bundle(
        'js/src/Admin/ManageMatchSuggestions.jsx',
        filters=js_filters
    ),
    'match_suggestions.js'
)

shoppinglist_bundle = react_bundle(
    Bundle(
        'js/src/Pages/Shoppinglist.jsx',
        filters=js_filters
    ),
    'shoppinglist.js'
)
