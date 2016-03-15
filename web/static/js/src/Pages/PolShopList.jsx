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
            isSorted: false,
            sortDirection: 'asc'
        }
    ];

    var FilterSelect = React.createClass({

        getDefaultProps: function () {
            return {idAttribute: 'id'};
        },

        handleChange: function (e) {
            var value = parseInt(e.target.value, 10);
            if (value === -1) {
                value = null;
            }
            this.props.setFilter(this.props.filterKey, value);
        },

        render: function () {
            var options = _.map(this.props.options, function (option) {
                var id = option[this.props.idAttribute];
                return (<option key={id} value={id}>{option.name}</option>);
            }, this);
            options.unshift((<option key="-1" value="-1">---</option>));
            var id = 'filter_' + this.props.filterKey;
            var selected = this.props.selected || -1;
            return (
                <div className="form-group">
                    <label htmlFor={id}>{this.props.label}</label>
                    <select
                        value={selected}
                        onChange={this.handleChange}
                        id={id}
                        className="form-control">
                        {options}
                    </select>
                </div>
            );
        }
    });


    var Map = React.createClass({

        shopLayer: null,

        map: null,

        componentDidMount: function () {
            L.Icon.Default.imagePath = '/static/js/lib/leaflet/dist/images/';
            var element = ReactDOM.findDOMNode(this);
            this.map = new L.Map(element);

            var apikey = this.props.maptoken;
            var baseLayers = {
                'Kart': L.tileLayer.webatlas({
                    mapType: L.TileLayer.Webatlas.Type.VECTOR,
                    apikey: apikey
                }).addTo(this.map),
                'Foto': L.tileLayer.webatlas({
                    mapType: L.TileLayer.Webatlas.Type.AERIAL,
                    apikey: apikey
                }),
                'Hybrid': L.tileLayer.webatlas({
                    mapType: L.TileLayer.Webatlas.Type.HYBRID,
                    apikey: apikey
                })
            };
            L.control.layers(baseLayers, {}).addTo(this.map);

            var markerClicked = this.markerClicked;
            this.shopLayer = L.geoJson([], {
                pointToLayer: function (featureData, latlng) {
                    return L.marker(latlng, {
                        title: featureData.properties.title
                    }).on('click', markerClicked);
                }
            }).addTo(this.map);
            this.setGeometries(this.props.items);
        },

        markerClicked: function (e) {
            window.location.href = '/pol_shops/' + e.target.feature.properties.id;
        },

        componentWillReceiveProps: function (nextProps) {
            if (_.has(nextProps, 'items')) {
                this.setGeometries(nextProps.items);
            }
        },

        setGeometries: function (items) {
            var features = _.map(items, function (item) {
                return {
                    type: 'Feature',
                    properties: {
                        title: item.name,
                        id: item.id
                    },
                    geometry: item.geom
                };
            });
            var fc = {type: 'FeatureCollection', features: features};
            this.shopLayer.clearLayers().addData(fc);
            this.map.fitBounds(this.shopLayer.getBounds(), {padding: [25, 25]});
        },

        render: function () {
            return (<div className="map"></div>);
        }
    });


    var PolShopList = React.createClass({

        getInitialState: function () {
            return {
                shops: this.props.shops,
                filteredShops: this.props.shops,
                loading: false,
                showing: 'all',
                timestamp: new Date().getTime(),
                municipalities: this.props.municipalities,
                filters: {},
                type: 'table'
            };
        },

        showAll: function () {
            this.setState({showing: 'all'});
            this.resetShops(this.props.shops);
        },

        showNearby: function () {
            if (this.state.showing === 'nearby') {
                return;
            }
            var filters = _.clone(this.state.filters);
            filters.fylkesnr = null;
            filters.kommnr = null;
            this.setState({loading: true, showing: 'nearby', filters: filters});
            navigator.geolocation.getCurrentPosition(this.gotUserPosition, console.log);
        },

        resetShops: function (shops) {
            var filteredShops = this.filter(shops, this.state.filters);
            this.setState({
                shops: shops,
                filteredShops: filteredShops,
                loading: false,
                timestamp: new Date().getTime()
            });
        },

        gotUserPosition: function (e) {
            var lat = e.coords.latitude;
            var lon = e.coords.longitude;
            bd.api.getNearbyPolShops(lat, lon, this.resetShops);
        },

        setFilter: function (key, value) {
            var filters = _.clone(this.state.filters);
            if (key === 'fylkesnr') {
                filters.kommnr = null;
                var municipalities = _.chain(this.props.municipalities)
                    .filter(function (municipality) {
                        return municipality.fylkesnr === value;
                    })
                    .sortBy(function (municipality) {
                        return municipality.name;
                    })
                    .value();
                this.setState({municipalities: municipalities});
            }

            filters[key] = value;
            var shops = this.filter(this.state.shops, filters);
            this.setState({
                filters: filters,
                filteredShops: shops,
                timestamp: new Date().getTime()
            });
        },

        filter: function (shops, filters) {
            if (_.isEmpty(filters)) {
                return shops;
            }
            return _.filter(shops, function (shop) {
                var filtered = _.map(filters, function (value, key) {
                    if (value === null) {
                        return true;
                    }
                    return shop[key] === value;
                });
                var include = filtered.indexOf(false) === -1;
                return include;
            });
        },

        showTable: function () {
            this.setState({type: 'table'});
        },

        showMap: function () {
            this.setState({type: 'map'});
        },

        render: function () {
            var supportsGeoloc = !!navigator.geolocation;
            var nearbyBtn;
            if (supportsGeoloc) {
                var nearbyClass = 'btn btn-default';
                if (this.state.showing === 'nearby') {
                    nearbyClass += ' active';
                }
                nearbyBtn = (
                    <button
                        onClick={this.showNearby}
                        className={nearbyClass}
                        type="button">
                        Pol nær meg
                    </button>
                );
            }

            var content;
            if (this.state.loading) {
                content = (<ns.LoadIndicator text="Laster" />);
            } else {
                if (this.state.filteredShops.length === 0) {
                    content = (<div>Ingen funnet</div>);
                } else if (this.state.type === 'table') {
                    content = (
                        <ns.SortableTable
                            key={this.state.timestamp}
                            items={this.state.filteredShops}
                            columns={columns} />
                    );
                } else if (this.state.type === 'map') {
                    content = (<Map items={this.state.filteredShops} maptoken={this.props.maptoken} />);
                }
            }

            var tableClass = 'btn btn-default';
            if (this.state.type === 'table') {
                tableClass += ' active';
            }
            var mapClass = 'btn btn-default';
            if (this.state.type === 'map') {
                mapClass += ' active';
            }


            var allClass = 'btn btn-default';
            if (this.state.showing === 'all') {
                allClass += ' active';
            }
            return (
                <div>
                    <nav className="navbar navbar-default">
                        <div className="container-fluid">
                            <form className="navbar-form navbar-left">
                                <div className="form-group">
                                    <div className="btn-group navbar-btn">
                                        <button 
                                            onClick={this.showAll}
                                            className={allClass}
                                            type="button">
                                            Alle Pol
                                        </button>
                                        {nearbyBtn}
                                    </div>
                                </div>
                                <FilterSelect
                                    setFilter={this.setFilter}
                                    label="Butikkkategori"
                                    selected={this.state.filters.category}
                                    filterKey="category"
                                    options={this.props.categories} />
                                <FilterSelect
                                    setFilter={this.setFilter}
                                    label="Fylke"
                                    selected={this.state.filters.fylkesnr}
                                    filterKey="fylkesnr"
                                    options={this.props.counties} />
                                <FilterSelect
                                    setFilter={this.setFilter}
                                    label="Kommune"
                                    filterKey="kommnr"
                                    selected={this.state.filters.kommnr}
                                    idAttribute="kommnr"
                                    options={this.state.municipalities} />
                            </form>
                            <form className="navbar-form navbar-right">
                                <div className="form-group">
                                    <div className="btn-group navbar-btn">
                                        <button
                                            onClick={this.showTable}
                                            className={tableClass}
                                            type="button">
                                            Tabell
                                        </button>
                                        <button
                                            onClick={this.showMap}
                                            className={mapClass}
                                            type="button">
                                            Kart
                                        </button>
                                    </div>
                                </div>
                            </form>
                        </div>
                    </nav>
                    {content}
                </div>
            );
        }
    });


    ns.renderPolShopList = function (data, componentId, title) {
        var component = document.getElementById(componentId);


        var categories = _.chain(data.shops)
            .pluck('category')
            .uniq()
            .map(function (category) {
                return {name: category, id: category};
            })
            .sortBy('id')
            .value();

        var counties = _.chain(data.municipalities)
            .map(function (municipality) {
                return {id: municipality.fylkesnr, name: municipality.fylke_name};
            })
            .uniq(false, function (county) {
                return county.id;
            })
            .value();

        ReactDOM.render(
            <ns.Container
                component={PolShopList}
                shops={data.shops}
                categories={categories}
                counties={counties} 
                municipalities={data.municipalities}
                maptoken={data.maptoken}
                title={title} />,
            component
        );
    };


}(bd));
