var bd = this.bd || {};
(function (ns) {
    'use strict';

    var BeerListElement = React.createClass({

        remove: function () {
            this.props.onRemove(this.props.beer.id);
        },

        render: function () {
            var beer = this.props.beer.ratebeer;
            return (
                <li className="list-group-item">
                    <h4 className="list-group-item-heading">
                        <a href={'/pol_beers/' + this.props.beer.id}>
                            {beer.name}
                        </a>
                        <span
                            onClick={this.remove}
                            className="glyphicon glyphicon-remove pull-right remove-btn pull-right" />
                    </h4>
                    <p className="list-group-item-text">
                        {beer.brewery.name}, {beer.brewery.country.name}.{' '}
                        {beer.style.name},{' '}{ns.Util.fixedOrNa(beer.abv, 2)}%
                        <span className="pull-right">{this.props.beer.price}{' '}kr</span>
                    </p>
                </li>
            );
        }
    });

    var AvailabilityList = React.createClass({

        render: function () {
            return (
                <p>Her skal det komme en liste over hvilke pol som har ølene i 
                handlelista di!</p>
            );
        }
    });

    var ShoppingList = React.createClass({

        componentDidMount: function () {
            var ids = this.props.shoppingListStore.getList();
            if (ids.length > 0) {
                bd.api.getShoppingList(ids, this.gotList);
            } else {
                this.gotList([]);
            }
        },

        gotList: function (beers) {
            this.setState({beers: beers, loading: false});
        },

        getInitialState: function () {
            return {beers: [], loading: true};
        },

        removeBeer: function (id) {
            this.props.shoppingListStore.toggleBeer(id);
            this.setState({
                beers: _.reject(this.state.beers, function (beer) {
                    return beer.id === id;
                })
            });
        },

        render: function () {
            if (this.state.beers.length === 0 && !this.state.loading) {
                return (<p>Du har ingen øl i handlelista</p>);
            }
            var beers = _.map(this.state.beers, function (beer) {
                return (
                    <BeerListElement
                        key={beer.id}
                        beer={beer}
                        onRemove={this.removeBeer} />
                );
            }, this);

            return (
                <div>
                    <div className="row">
                        <div className="col-md-6">
                            <ul className="list-group">{beers}</ul>
                        </div>
                    </div>
                    <AvailabilityList beers={this.state.beers} />
                </div>
            );
        }
    });

    ns.renderShoppingList = function (data, componentId) {
        var component = document.getElementById(componentId);

        ReactDOM.render(
            <ns.Container
                component={ShoppingList}
                shoppingListStore={ns.shoppingListStore}
                rb_beer={data}
                title={'Handleliste'} />,
            component
        );
    };

}(bd));

