var bd = this.bd || {};
bd.Util = {};
(function (ns) {
    'use strict';

    ns.createQueryParameterString = function (params) {
        return _.map(params, function (value, key) {
            if (_.isArray(value)) {
                value = value.join(',');
            }
            return encodeURIComponent(key) + '=' + encodeURIComponent(value);
        }).join('&');
    };

    ns.setQueryParams = function (params) {
        if (history.pushState) {
            var newurl = window.location.protocol + '//' + window.location.host + window.location.pathname + '?' + ns.createQueryParameterString(params);
            window.history.pushState({path: newurl}, '', newurl);
        }
    };

    ns.valueOrNa = function (value, naValue) {
        naValue = naValue || '-';
        if (value === null) {
            return naValue;
        }
        return value;
    };

    ns.fixedOrNa = function (value, decimals, naValue) {
        if (value === null) {
            return ns.valueOrNa(value, naValue);
        }
        return value.toFixed(decimals);
    };

    ns.getSorter = function (properties, desc) {
        if (!_.isArray(properties)) {
            properties = [properties];
        }
        var getVal = function (value) {
            return _.reduce(properties, function (acc, prop) {
                if (_.has(acc, prop)) {
                    return acc[prop];
                }
                return null;
            }, value);
        };

        return function (a, b) {
            var valA = getVal(a);
            var valB = getVal(b);
            if (valA === null) {
                return 1;
            }
            if (valB === null) {
                return 0;
            }
            var orderFactor = desc ? 1 : -1;
            if (valA < valB) {
                return 1 * orderFactor;
            }
            if (valA > valB) {
                return -1 * orderFactor;
            }
            return 0;
        };
    };

    //see http://stackoverflow.com/a/23619085
    ns.intersperse = function (arr, sep) {
        if (arr.length === 0) {
            return [];
        }

        return arr.slice(1).reduce(function (xs, x, i) {
            return xs.concat([sep, x]);
        }, [arr[0]]);
    };

}(bd.Util));
