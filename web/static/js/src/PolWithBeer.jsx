var bd = this.bd || {};
(function (ns) {
    'use strict';

    var columns = [
        {
            id: 'name',
            name: 'Navn',
            formatter: function (stock) {
                return (<a href={'/pol_shops/' + stock.pol_id}>{stock.name}</a>);
            },
            sortParams: 'name',
            isSorted: true,
            sortDirection: 'asc'
        },
        {
            id: 'amount',
            name: 'Antall',
            formatter: function (stock) {
                var updated = 'Oppdatert: ' + stock.updated;
                return (<span title={updated}>{stock.amount}</span>);
            },
            sortParams: ['amount'],
            isSorted: false,
            sortDirection: 'desc'
        },
        {
            id: 'komm',
            name: 'Kommune',
            formatter: function (stock) {
                return stock.komm;
            },
            sortParams: ['komm'],
            isSorted: false,
            filterable: true,
            sortDirection: 'asc'
        }
    ];

    ns.PolWithBeerList = React.createClass({

        getInitialState: function () {
            return {expanded: false, data: null, searching: false, numPol: null};
        },

        gotStores: function (data) {
            this.setState({
                data: data,
                searching: false,
                numPol: data.length
            });
        },

        toggle: function () {
            var expanded = !this.state.expanded;
            this.setState({expanded: expanded});
            if (expanded && !this.state.data) {
                this.setState({searching: true});
                var supportsGeoloc = !!navigator.geolocation;
                if (!supportsGeoloc) {
                    bd.api.getPolStoresWithBeer(this.props.beerId, null, null, this.gotStores);
                } else {
                    navigator.geolocation.getCurrentPosition(this.gotUserPosition, console.log);
                }
            }
        },

        gotUserPosition: function (e) {
            var lat = e.coords.latitude;
            var lon = e.coords.longitude;
            columns[0].isSorted = false;
            bd.api.getPolStoresWithBeer(this.props.beerId, lat, lon, this.gotStores);
        },

        render: function () {
            var bodyClass = 'panel-collapse collapse';
            if (this.state.expanded) {
                bodyClass += ' in';
            }

            var content;
            if (this.state.searching) {
                content = (<ns.LoadIndicator text="Laster" />);
            } else if (this.state.data && this.state.data.length) {
                content = (
                    <ns.SortableTable
                        filterable={true}
                        idProperty="pol_id"
                        items={this.state.data}
                        columns={columns} />
                );
            } else {
                content = 'Ingen pol har dette ølet (dog: det kan finnes i bestillingsutvalget. Sjekk polets sider).';
            }

            var heading = 'Pol som har dette ølet';
            if (this.state.numPol !== null) {
                heading += ' (' + this.state.numPol + ')';
            }

            return (
                <div className="panel panel-default">
                    <div className="panel-heading">
                        <h4 className="panel-title">
                            <a role="button" onClick={this.toggle}>
                              {heading}
                            </a>
                        </h4>
                    </div>
                    <div className={bodyClass}>
                        <div className="panel-body">
                            {content}
                        </div>
                    </div>
                </div>
            );
        }
    });

}(bd));