var bd = this.bd || {};
(function (ns) {
    'use strict';

    var columns = [
        {
            id: 'name',
            name: 'Navn',
            formatter: function (beer) {
                return (
                    <a href={'/pol_beers/' + beer.id}>
                        {beer.name}
                    </a>
                );
            },
            sortParams: 'name',
            isSorted: true,
            sortDirection: 'asc'
        },
        {
            id: 'brewery',
            name: 'Bryggeri',
            formatter: function (beer) {
                return (
                    <a href={'/breweries/' + beer.brewery_id}>
                        {beer.brewery}
                    </a>
                );
            },
            sortParams: 'brewery',
            isSorted: false,
            sortDirection: 'asc'
        },
        {
            id: 'style',
            name: 'Stil',
            formatter: function (beer) {
                return (
                    <a href={'/styles/' + beer.style_id}>
                        {ns.Util.valueOrNa(beer.style)}
                    </a>
                );
            },
            sortParams: 'style',
            isSorted: false,
            sortDirection: 'asc'
        },
        {
            id: 'rating',
            name: 'Rating',
            formatter: function (beer) {
                if (beer.score_overall && beer.score_style) {
                    return beer.score_overall + ' (' + beer.score_style + ')';
                }
                return '-';
            },
            sortParams: 'score_overall',
            isSorted: false,
            sortDirection: 'desc'
        },
        {
            id: 'abv',
            name: 'ABV',
            formatter: function (beer) {
                return ns.Util.fixedOrNa(beer.abv, 2);
            },
            sortParams: 'abv',
            isSorted: false,
            sortDirection: 'desc'
        },
        {
            id: 'price',
            name: 'Pris',
            formatter: function (beer) {
                return ns.Util.fixedOrNa(beer.price, 2);
            },
            sortParams: 'price',
            isSorted: false,
            sortDirection: 'desc'
        }
    ];

    function getColumnsForTable(columnIds) {

        return _.filter(columns, function (column) {
            return (columnIds.indexOf(column.id) > -1);
        });
    }

    ns.renderPolBeerTable = function(beerList, columnIds, component) {
        beerList = beerList.sort(ns.Util.getSorter(['name'], false));
        var columnsForTable = getColumnsForTable(columnIds);
        ReactDOM.render(<ns.SortableTable items={beerList} columns={columnsForTable} />, component);
    }

}(bd));