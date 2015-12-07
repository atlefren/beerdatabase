var bd = this.bd || {};
bd.api = bd.api || {};
(function (ns) {
    'use strict';

    var API_BASE = '/api/v1/';

    ns.confirmSuggestion = function (suggestion, callback) {
        var data = {
            pol_id: suggestion.pol_beer_id,
            rb_id: suggestion.rb_beer_id
        };

        atomic.put(API_BASE + 'suggestions/' + suggestion.id, data)
            .success(function (data, xhr) {
                callback(data);
            })
            .error(function (data, xhr) {
                console.error(data);
            });
    };

    ns.rejectSuggestion = function (suggestion, callback) {
        atomic.delete(API_BASE + 'suggestions/' + suggestion.id)
            .success(function (data, xhr) {
                callback(data);
            })
            .error(function (data, xhr) {
                console.error(data);
            });
    };

    ns.searchBrewery = function (val, callback) {
        atomic.get(API_BASE + 'search/brewery/?q=' + encodeURIComponent(val.q))
            .success(function (data, xhr) {
                callback(data);
            })
            .error(function (data, xhr) {
                console.error(data);
            });
    };

    ns.searchBeer = function (val, callback) {
        var url = API_BASE + 'search/beer/?q=' + encodeURIComponent(val.q);
        if (_.has(val, 'brewery')) {
            url += '&brewery=' + encodeURIComponent(val.brewery);
        }
        atomic.get(url)
            .success(function (data, xhr) {
                callback(data);
            })
            .error(function (data, xhr) {
                console.error(data);
            });
    };

    ns.postMatch = function (polId, rbId, comment, callback) {
        var data = {
            ratebeerId: rbId,
            polId: polId,
            comment: comment
        };
        atomic.post(API_BASE + 'suggestions/', data)
            .success(callback)
            .error(function (data, xhr) {
                console.error(data);
            });
    };

    ns.fullsearchBeer = function (params, success, error) {
        atomic.get(API_BASE + 'search/full/?' + bd.Util.createQueryParameterString(params))
            .success(function (data, xhr) {
                success(data);
            })
            .error(function (data, xhr) {
                console.error(data);
                error(data);
            });
    };

    ns.getPolStoresWithBeer = function (beerId, success, error) {
        atomic.get(API_BASE + 'pol_beer/' + beerId +'/stock/')
            .success(function (data, xhr) {
                success(data);
            })
            .error(function (data, xhr) {
                console.error(data);
                error(data);
            });
    };

    ns.getNearbyPolShops = function (lat, lon, success, error) {
        atomic.get(API_BASE + 'pol_shops/?lat=' + lat + '&lon=' + lon)
            .success(function (data, xhr) {
                success(data);
            })
            .error(function (data, xhr) {
                console.error(data);
                error(data);
            });
    };

}(bd.api));