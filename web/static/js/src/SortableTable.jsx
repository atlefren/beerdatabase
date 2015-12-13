var bd = this.bd || {};
(function (ns) {
    'use strict';

    var DataRow = React.createClass({
        render: function () {

            var columns = _.map(this.props.columns, function (column, i) {
                return (<td key={i}>{column.formatter(this.props.item)}</td>);
            }, this);
            columns.unshift((<td key="num">{this.props.number}</td>));

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


    var FilterColumn = React.createClass({

        handleChange: function (e) {
            var value = e.target.value;
            this.setState({selected: value});
            if (value === '---') {
                value = null;
            }
            this.props.filter(this.props.filterKey, value);
        },

        getInitialState: function () {
            var values = _.clone(this.props.values);
            values.unshift('---');
            var selected = values[0];
            if (this.props.selected) {
                selected = this.props.selected;
            }
            return {values: values, selected: selected};
        },

        render: function () {
            var options = _.map(this.state.values, function (value) {
                return (
                    <option
                        key={value}
                        value={value}>
                        {value}
                    </option>
                );
            });

            return (
                <td>
                    <select
                        onChange={this.handleChange}
                        className="form-control"
                        value={this.state.selected}>
                        {options}
                    </select>
                </td>
            );
        }
    });

    var FilterRow = React.createClass({

        createFilterColumn: function (column) {
            if (!column.filterable) {
                return (<td></td>);
            }
            console.log(column);
            var values = _.chain(this.props.items)
                .map(function (item) {
                    return item[column.id];
                })
                .uniq()
                .sortBy(function (val) {return val;})
                .value();
            console.log(values);
            return (
                <FilterColumn
                    column={column}
                    selected={this.props.filterAttrs[column.id]}
                    filter={this.props.filter}
                    filterKey={column.id}
                    values={values} />
            );
        },

        render: function () {
            return (
                <tr>
                    <td></td>
                    {_.map(this.props.columns, this.createFilterColumn)}
                </tr>
            );
        }
    });

    ns.SortableTable = React.createClass({

        getDefaultProps: function () {
            return {idProperty: 'id', filterable: false};
        },

        getInitialState: function () {
            return {
                columns: this.props.columns,
                items: this.props.items,
                filterAttrs: {}
            };
        },

        filter: function (id, value) {
            var filterAttrs = _.clone(this.state.filterAttrs);
            filterAttrs[id] = value;
            console.log(id, value);

            var items = _.clone(this.props.items)
                .filter(function (item) {
                    var matched = _.map(filterAttrs, function (value, key) {
                        if (value !== null) {
                            return item[key] === value;
                        }
                        return true;
                    });
                    console.log(matched);
                    return matched.indexOf(false) === -1;
                });
            this.setState({items: items, filterAttrs: filterAttrs});
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

        toggleFilter: function () {
            this.setState({isFiltering: !this.state.isFiltering});
        },

        render: function () {
            var rows = _.map(this.state.items, function (item, i) {
                return (
                    <DataRow
                        number={i + 1}
                        item={item}
                        key={item[this.props.idProperty]}
                        columns={this.state.columns} />
                );
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

            var filterRow;
            if (this.props.filterable && this.state.isFiltering) {
                filterRow = (
                    <FilterRow
                        filter={this.filter}
                        items={this.props.items}
                        filterAttrs={this.state.filterAttrs}
                        columns={this.props.columns} />
                );
            }
            var filterBtn;
            if (this.props.filterable) {
                header.unshift((
                    <th>
                        <button
                            onClick={this.toggleFilter}
                            type="button"
                            className="btn btn-default">
                            <i className="fa fa-filter" /> Filtrer
                        </button>
                    </th>
                ));
            } else {
                header.unshift((<th>#</th>));
            }

            return (
                <table className="table table-striped table-sortable">
                    <thead>
                        <tr>
                           {header}
                        </tr>
                        {filterRow}
                    </thead>
                    <tbody>
                        {rows}
                    </tbody>
                </table>
            );
        }
    });

}(bd));