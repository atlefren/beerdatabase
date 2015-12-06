var bd = this.bd || {};
(function (ns) {
    'use strict';

    var columns = [
        {
            id: 'name',
            name: 'Navn',
            formatter: function (shop) {
                return (
                    <a href={'/pol_shops/' + shop.id}>
                        {shop.name}
                    </a>
                );
            },
            sortParams: 'name',
            isSorted: true,
            sortDirection: 'asc'
        },
        {
            id: 'category',
            name: 'Butikkkategori',
            formatter: function (shop) {
                return shop.category;
            },
            sortParams: 'category',
            isSorted: false,
            sortDirection: 'asc'
        },
        {
            id: 'komm_name',
            name: 'Kommune',
            formatter: function (shop) {
                return shop.komm_name;
            },
            sortParams: 'komm_name',
            isSorted: false,
            sortDirection: 'asc'
        },
        {
            id: 'fylke_name',
            name: 'Fylke',
            formatter: function (shop) {
                return shop.fylke_name;
            },
            sortParams: 'fylke_name',
            isSorted: true,
            sortDirection: 'asc'
        }
    ];

    var PolShopList = React.createClass({

        getInitialState: function () {
            return {
                shops: this.props.shops,
                loading: false,
                timestamp: new Date().getTime()
            };
        },

        showAll: function () {
            this.resetShops(this.props.shops);
        },

        showNearby: function () {
            this.setState({loading: true});
            navigator.geolocation.getCurrentPosition(this.gotUserPosition, console.log);
        },

        resetShops: function (shops) {
            this.setState({
                shops: shops,
                loading: false,
                timestamp: new Date().getTime()
            });
        },

        gotUserPosition: function (e) {
            var lat = e.coords.latitude;
            var lon = e.coords.longitude;
            bd.api.getNearbyPolShops(lat, lon, this.resetShops);
        },

        render: function () {
            var supportsGeoloc = !!navigator.geolocation;
            var nearbyBtn;
            if (supportsGeoloc) {
                nearbyBtn = (
                    <button
                        onClick={this.showNearby}
                        className="btn btn-default"
                        type="button">
                        Pol nær meg
                    </button>
                );
            }

            var content;
            if (this.state.loading) {
                content = (<ns.LoadIndicator text="Laster" />);
            } else {
                content = (
                    <ns.SortableTable
                        key={this.state.timestamp}
                        items={this.state.shops}
                        columns={columns} />
                );
            }

            return (
                <div>
                    <div className="btn-group"> 
                        <button onClick={this.showAll} className="btn btn-default" type="button">Alle Pol</button>
                        {nearbyBtn}
                    </div>
                    {content}
                </div>
            )
        }
    });


    ns.renderPolShopList = function (shops, component) {
        ReactDOM.render(<PolShopList shops={shops} />, component);
    };


}(bd));
