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
        atomic.get('/api/v1/search/brewery/?q=' + encodeURIComponent(val.q))
            .success(function (data, xhr) {
                callback(data);
            })
            .error(function (data, xhr) {
                console.error(data);
            });
    };

    ns.searchBeer = function (val, callback) {
        var url = '/api/v1/search/beer/?q=' + encodeURIComponent(val.q);
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
        atomic.post('/api/v1/suggestions/', data)
            .success(callback)
            .error(function (data, xhr) {
                console.error(data);
            });
    }

}(bd.api));