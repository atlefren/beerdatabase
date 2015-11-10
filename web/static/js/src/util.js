var bd = this.bd || {};
bd.Util = {};
(function (ns) {
    'use strict';

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

}(bd.Util));