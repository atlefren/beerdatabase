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


    function getFromDict(dict, keys) {
        if (!_.isArray(keys)) {
            keys = [keys];
        }
        return _.reduce(keys, function (acc, prop) {
            if (_.has(acc, prop)) {
                return acc[prop];
            }
            return null;
        }, dict);
    }


    var FilterSelect = React.createClass({

        handleChange: function (e) {
            var value = e.target.value;
            this.setState({selected: value});
            if (value === '---') {
                value = null;
            }
            this.props.setFilter(this.props.filterKey, value);
        },

        getInitialState: function () {
            var options = _.clone(this.props.options);
            options.unshift('---');
            var selected = options[0];
            if (this.props.selected) {
                selected = this.props.selected;
            }
            return {options: options    , selected: selected};
        },

        render: function () {
              var options = _.map(this.state.options, function (value) {
                return (
                    <option
                        key={value}
                        value={value}>
                        {value}
                    </option>
                );
            });
            var id = 'filter_' + this.props.filterKey;
            return (
                <div className="form-group">
                    <label htmlFor={id}>{this.props.label}</label>
                    <select
                        onChange={this.handleChange}
                        className="form-control"
                        id={id}
                        value={this.state.selected}>
                        {options}
                    </select>
                </div>
            );
        }
    });





    var FilterRow = React.createClass({

        createFilter: function (column) {

            var options = _.chain(this.props.items)
                .map(function (item) {
                    return getFromDict(item, column.sortParams)
                })
                .uniq()
                .sortBy(function (val) {return val;})
                .value();

            var key = column.sortParams;
            if (_.isArray(key)) {
                key = key.join('___');
            }
            return (
                <FilterSelect
                    key={key}
                    setFilter={this.props.filter}
                    label={column.name}
                    selected={this.props.filterAttrs[key]}
                    filterKey={key}
                    options={options} />
            );
        },

        getFilters: function () {
            return _.chain(this.props.columns)
                .filter(function (column) {
                    return column.filterable;
                })
                .map(this.createFilter)
                .value();
        },

        render: function () {
            return (
                <nav className="navbar navbar-default">
                    <div className="container-fluid">
                        <form className="navbar-form navbar-left">
                            {this.getFilters()}
                        </form>
                    </div>
                </nav>
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

            var items = _.clone(this.props.items)
                .filter(function (item) {
                    var matched = _.map(filterAttrs, function (value, key) {
                        if (value !== null) {
                            var keys = key.split('___');
                            return getFromDict(item, keys) === value;
                        }
                        return true;
                    });

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
                return (
                    <TableHeaderCell
                        name={column.name}
                        columnId={column.id}
                        key={column.id}
                        onSort={this.onSort}
                        sortDirection={column.sortDirection}
                        isSorted={column.isSorted} />
                );
            }, this);

            var filterRow;
            if (this.props.filterable) {
                filterRow = (
                    <FilterRow
                        filter={this.filter}
                        items={this.props.items}
                        filterAttrs={this.state.filterAttrs}
                        columns={this.props.columns} />
                );
            }
            header.unshift((<th key="count">#</th>));

            return (
                <div>
                    {filterRow}
                    <div className="table-responsive">
                        <table className="table table-striped table-sortable">
                            <thead>
                                <tr >
                                   {header}
                                </tr>
                            </thead>
                            <tbody>
                                {rows}
                            </tbody>
                        </table>
                    </div>
                </div>
            );
        }
    });

}(bd));