var bd = this.bd || {};
(function (ns) {
    'use strict';
    var shoppingListStore = function () {
        var callbacks = [];
        if (!localStorage.shoppingList) {
            localStorage.shoppingList = JSON.stringify([]);
        }

        var hasBeer = function (id) {
            return JSON.parse(localStorage.shoppingList).indexOf(id) !== -1;
        };

        var getCount = function () {
            return JSON.parse(localStorage.shoppingList).length;
        };

        var notify = function () {
            var count = getCount();
            _.each(callbacks, function (cb) {
                cb(count);
            });
        };

        return {
            hasBeer: hasBeer,
            addCallback: function (cb) {
                callbacks.push(cb);
            },
            getCount: getCount,
            isSupported: typeof(Storage) !== 'undefined',
            toggleBeer: function (id) {
                if (!hasBeer(id)) {
                    var list = JSON.parse(localStorage.shoppingList);
                    list.push(id);
                    localStorage.shoppingList = JSON.stringify(list);
                    notify();
                    return true;
                }
                list = _.reject(JSON.parse(localStorage.shoppingList), function (beerId) {
                    return beerId === id;
                });
                localStorage.shoppingList = JSON.stringify(list);
                notify();
                return false;
            },
            getList: function () {
                return JSON.parse(localStorage.shoppingList);
            }
        };
    };

    ns.shoppingListStore = shoppingListStore();

    var ShoppingListCount = React.createClass({

        componentDidMount: function () {
            this.props.shoppingListStore.addCallback(this.countChanged);
        },

        countChanged: function (count) {
            this.setState({count: count});
        },

        getInitialState: function () {
            return {count: this.props.shoppingListStore.getCount()};
        },

        render: function () {
            if (this.state.count === 0) {
                return (<span></span>);
            }
            return (
                <span className="badge">{this.state.count}</span>
            );
        }
    });

    ns.setupShoppingListCount = function (containerId) {
        if (!ns.shoppingListStore.isSupported) {
            return;
        }
        var component = document.getElementById(containerId);
        ReactDOM.render(
            <ShoppingListCount shoppingListStore={ns.shoppingListStore} />,
            component
        );
    };
}(bd));
