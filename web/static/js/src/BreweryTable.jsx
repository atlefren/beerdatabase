var bd = this.bd || {};
(function (ns) {
    'use strict';

    var columns = [
        {
            id: 'name',
            name: 'Navn',
            formatter: function (brewery) {
                return (<a href={'/breweries/' + brewery.id}>{brewery.name}</a>);
            },
            sortParams: 'name',
            isSorted: true,
            sortDirection: 'asc'
        },
        {
            id: 'country',
            name: 'Land',
            formatter: function (brewery) {
                return brewery.country.name;
            },
            sortParams: ['country', 'name'],
            isSorted: false,
            sortDirection: 'asc'
        },
        {
            id: 'num_beers',
            name: 'Antall øl på polet',
            formatter: function (brewery) {
                return brewery.num_beers_polet;
            },
            sortParams: 'num_beers_polet',
            isSorted: false,
            sortDirection: 'desc'
        }
    ];

    function getColumnsForTable(columnIds) {
        return _.filter(columns, function (column) {
            return (columnIds.indexOf(column.id) > -1);
        });
    }

    ns.renderBreweyTable = function(breweryList, columnIds, component) {
        breweryList = breweryList.sort(ns.Util.getSorter(['name'], false));
        var columnsForTable = getColumnsForTable(columnIds);
        React.render(<ns.SortableTable items={breweryList} columns={columnsForTable} />, component);
    }

}(bd));