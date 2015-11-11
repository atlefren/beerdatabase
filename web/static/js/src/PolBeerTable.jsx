var bd = this.bd || {};
(function (ns) {
    'use strict';

    function valueOrNa(value, naValue) {
        naValue = naValue || '-';
        if (value === null) {
            return naValue;
        }
        return value;
    }

    function fixedOrNa(value, decimals, naValue) {
        if (value === null) {
            return valueOrNa(value, naValue);
        }
        return value.toFixed(decimals);
    }


    var BeerRow = React.createClass({
        render: function () {

            var columns = _.map(this.props.columns, function (column) {
                return (<td>{column.formatter(this.props.beer)}</td>);
            }, this);

            return (
                <tr>
                    {columns}
                </tr>
            );
        }
    });

    var TableHeaderCell = React.createClass({

        sort: function () {

            var direction = this.props.sortDirection;
            if (this.props.isSorted) {
                if (this.props.sortDirection === 'asc') {
                    direction = 'desc';
                }
                if (this.props.sortDirection === 'desc') {
                    direction = 'asc';
                }
            }

            this.props.onSort(this.props.columnId, direction);
        },

        render: function () {

            var sort;
            if (this.props.isSorted) {
                if (this.props.sortDirection === 'desc') {
                    sort = (<i className="fa fa-caret-down"></i>);
                } else {
                    sort = (<i className="fa fa-caret-up"></i>);
                }
            }
            return (<th onClick={this.sort}>{this.props.name}&nbsp;{sort}</th>);
        }

    });

    var BeerTable = React.createClass({

        getInitialState: function () {
            return {
                columns: this.props.columns,
                beers: this.props.beers
            };
        },

        onSort: function (columnId, direction) {
            var desc = (direction === 'desc');
            var col = _.find(this.state.columns, function (column) {
                return (column.id === columnId);
            });
            var beers = _.clone(this.props.beers)
                            .sort(ns.Util.getSorter(col.sortParams, desc));

            var columns = _.map(this.state.columns, function (column) {
                column = _.clone(column);
                if (column.id === columnId) {
                    column.sortDirection = direction;
                    column.isSorted = true;
                } else {
                    column.isSorted = false;
                }
                return column;
            });
            this.setState({
                columns: columns,
                beers: beers
            });
        },

        render: function () {

            var rows = _.map(this.state.beers, function (beer, i) {
                return (<BeerRow beer={beer} columns={this.state.columns} />);
            }, this);


            var header = _.map(this.state.columns, function (column) {
                return (<TableHeaderCell
                            name={column.name}
                            columnId={column.id}
                            onSort={this.onSort}
                            sortDirection={column.sortDirection}
                            isSorted={column.isSorted} />
                );
            }, this);

            return (
                <table className="u-full-width">
                    <thead>
                        <tr>
                           {header}
                        </tr>
                    </thead>
                    <tbody>
                        {rows}
                    </tbody>
                </table>
            )
        }
    });

    var columns = [
        {
            id: 'name',
            name: 'Navn',
            formatter: function (beer) {
                var beerLink = '/pol_beers/' + beer.id;
                return (<a href={beerLink}>{beer.name}</a>);
            },
            sortParams: 'name',
            isSorted: true,
            sortDirection: 'asc'
        },
        {
            id: 'brewery',
            name: 'Bryggeri',
            formatter: function (beer) {
                return beer.brewery;
            },
            sortParams: 'brewery',
            isSorted: false,
            sortDirection: 'asc'
        },
        {
            id: 'style',
            name: 'Stil',
            formatter: function (beer) {
                return valueOrNa(beer.style);
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
                return fixedOrNa(beer.abv, 2);
            },
            sortParams: 'abv',
            isSorted: false,
            sortDirection: 'desc'
        },
        {
            id: 'price',
            name: 'Pris',
            formatter: function (beer) {
                return fixedOrNa(beer.price, 2);
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
        React.render(<BeerTable beers={beerList} columns={columnsForTable} />, component);
    }

}(bd));