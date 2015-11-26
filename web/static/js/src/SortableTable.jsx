var bd = this.bd || {};
(function (ns) {
    'use strict';

    var DataRow = React.createClass({
        render: function () {

            var columns = _.map(this.props.columns, function (column, i) {
                return (<td key={i}>{column.formatter(this.props.item)}</td>);
            }, this);

            return (
                <tr key={this.props.item.id}>
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
            return (
                <th
                    className="sortable"
                    onClick={this.sort}>
                    {this.props.name}&nbsp;{sort}
                </th>
            );
        }

    });

    ns.SortableTable = React.createClass({

        getInitialState: function () {
            return {
                columns: this.props.columns,
                items: this.props.items
            };
        },

        onSort: function (columnId, direction) {
            var desc = (direction === 'desc');
            var col = _.find(this.state.columns, function (column) {
                return (column.id === columnId);
            });
            var items = _.clone(this.props.items)
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
                items: items
            });
        },

        render: function () {
            var rows = _.map(this.state.items, function (item, i) {
                return (<DataRow item={item} key={item.id} columns={this.state.columns} />);
            }, this);


            var header = _.map(this.state.columns, function (column) {
                return (<TableHeaderCell
                            name={column.name}
                            columnId={column.id}
                            key={column.id}
                            onSort={this.onSort}
                            sortDirection={column.sortDirection}
                            isSorted={column.isSorted} />
                );
            }, this);

            return (
                <table className="u-full-width table-sortable">
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

}(bd));