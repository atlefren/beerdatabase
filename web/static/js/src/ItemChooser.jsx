var bd = this.bd || {};
(function (ns) {
    'use strict';

    var SelectedItem = React.createClass({

        click: function () {
            this.props.deselect(this.props.item.id);
        },

        render: function () {
            return (
                <li className="list-group-item">
                    {this.props.item.name}
                    <span
                        onClick={this.click}
                        className="glyphicon glyphicon-remove pull-right remove-btn" />
                </li>
            );
        }
    });


    var SelectedItemList = React.createClass({

        render: function () {

            var items = _.map(this.props.items, function (item) {
                return (
                    <SelectedItem
                        item={item}
                        key={item.id}
                        deselect={this.props.deselect} />
                );
            }, this);

            return (
                <ul className="list-group">
                    {items}
                </ul>
            );
        }
    });


    ns.ItemChooser = React.createClass({

        getDefaultProps: function () {
            return {value: [], limit: 10};
        },

        getInitialState: function () {
            /*var selected = _.pluck(this.props.items, 'id');
            var allSelected = (selected.length === this.props.value.length);
            return {selected: this.props.value, allSelected: allSelected};
            */
            return null;
        },

        onChange: function (e) {
            var selected = _.clone(this.props.value);
            if (selected.length < this.props.limit) {
                var add = parseInt(e.target.value, 10);
                if (add ===  -1) {
                    return;
                }
                selected.push(add);
            } else {
                //display warning about max?
            }
            var allSelected = (selected.length === this.props.items.length);

            this.changed(selected);
        },

        changed: function (values) {
            this.props.changed(this.props.type, values);
        },

        deselectItem: function (itemId) {
            var selected = _.clone(this.props.value);
            selected.splice(selected.indexOf(itemId), 1);
            this.changed(selected);
        },

        render: function () {
            var unselectedItems = _.chain(this.props.items)
                .filter(function (item) {
                    return this.props.value.indexOf(item.id) === -1;
                }, this)
                .map(function (item) {
                    return (
                        <option
                            key={item.id}
                            value={item.id}>
                            {item.name}
                        </option>
                    );
                })
                .value();

            unselectedItems.unshift((
                 <option
                    key="-1"
                    value="-1">
                    ---
                </option>
            ));

            var selectedItems = _.map(this.props.value, function (id) {
                return _.findWhere(this.props.items, {id: id});
            }, this);
            return (
                <div className="form-group">
                    <SelectedItemList
                        items={selectedItems}
                        deselect={this.deselectItem} />
                    <select
                        className="form-control"
                        onChange={this.onChange}
                        disabled={this.props.value.length >= 10}
                        multiple={false}>
                        {unselectedItems}
                    </select>
                </div>
            );
        }
    });

}(bd));
