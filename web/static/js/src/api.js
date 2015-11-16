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

}(bd.api));