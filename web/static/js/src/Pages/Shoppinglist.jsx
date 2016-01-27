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

            if (_.isEmpty(this.props.shops)) {
                return (
                    <div className="alert alert-warning" role="alert">
                        Ingen pol har disse ølene (dog: det kan finnes i bestillingsutvalget. Sjekk polets sider).
                    </div>
                );
            }

            var shops = _.chain(this.props.shops)
                .map(function (shop) {
                    var hasBeers = _.pluck(shop.beers, 'pol_beer_id');
                    shop.shop.missing = _.filter(this.props.beers, function (beer) {
                        return hasBeers.indexOf(beer.id) === -1;
                    });
                    return shop;
                }, this)
                .filter(function (shop) {
                    return shop.shop.missing.length < this.props.beers.length;
                }, this)
                .sortBy(function (shop) {
                    return -shop.beers.length;
                })
                .map(function (shop) {
                    return shop.shop;
                }, this)
                .map(function (shop) {
                    var missing, fraction;
                    if (shop.missing.length > 0) {
                        fraction = this.props.beers.length - shop.missing.length + '/' + this.props.beers.length;
                        var missingBeers = _.map(shop.missing, function (beer) {
                            return (
                                <span key={beer.id}>
                                    <a href={'/pol_beers/' + beer.id}>
                                        {beer.name}
                                    </a>
                                </span>
                            );
                        });
                        missingBeers = bd.Util.intersperse(missingBeers, ', ');
                        missing = (
                            <div>
                                <small>
                                    Mangler:{' '}{missingBeers}
                                </small>
                            </div>
                        );
                    }

                    var bg;
                    var frac = (this.props.beers.length - shop.missing.length) / this.props.beers.length;
                    if (frac === 1) {
                        bg = 'bg-success';
                    } else if (frac >= 0.5) {
                        bg = 'bg-warning';
                    } else {
                        bg = 'bg-danger';
                    }

                    return (
                        <tr key={shop.id} className={bg}>
                            <td>
                                <a href={'/pol_shops/' + shop.id}>{shop.name}</a>
                                {missing}
                            </td>
                            <td>{shop.missing.length === 0 ? 'Alle' : fraction}</td>
                        </tr>
                    );
                }, this)
                .value();

            return (
                <table className="table">
                    <thead>
                        <tr>
                            <th>Butikk</th>
                            <th>Antall øl</th>
                        </tr>
                    </thead>
                    <tbody>
                        {shops}
                    </tbody>
                </table>
            );
        }
    });

    var ShoppingList = React.createClass({

        componentDidMount: function () {
            var ids = this.props.shoppingListStore.getList();
            if (ids.length > 0) {
                bd.api.getShoppingList(ids, this.gotList);
            } else {
                this.gotList({beers: [], shops: []});
            }
        },

        gotList: function (data) {
            this.setState({
                beers: data.beers,
                loading: false,
                shops: data.shops
            });
        },

        getInitialState: function () {
            return {beers: [], loading: true, shops: []};
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

            var availabilityList;
            if (!this.state.loading) {
                availabilityList = (
                    <AvailabilityList beers={this.state.beers} shops={this.state.shops} />
                );
            }
            return (
                <div>
                    <div className="row">
                        <div className="col-md-6">
                            <ul className="list-group">{beers}</ul>
                        </div>
                    </div>
                    {availabilityList}
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

