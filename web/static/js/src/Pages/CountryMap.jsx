var bd = this.bd || {};
(function (ns) {
    'use strict';

    var NotFound = React.createClass({
        render: function () {
            return (<div>{'Fant ingen bryggerier'}</div>);
        }
    });

    function getName(brewery) {
        if (brewery.ratebeer) {
            return brewery.ratebeer.name;
        }
        if (brewery.operator) {
            return brewery.operator;
        }
        return brewery.name;
    }

    var BreweryInfo = React.createClass({

        render: function () {

            var address;
            if (this.props.brewery.street && this.props.brewery.housenumber && this.props.brewery.postcode && this.props.brewery.city) {
                address = (
                    <span>
                        <dt>Adresse</dt>
                        <dd>{this.props.brewery.street}{' '}{this.props.brewery.housenumber}{', '}{this.props.brewery.postcode}{' '}{this.props.brewery.city}</dd>
                    </span>
                );
            }
            var website;
            if (this.props.brewery.website) {
                website = (
                    <span>
                        <dt>Webside</dt>
                        <dd><a href={this.props.brewery.website} target="_blank">{this.props.brewery.website}</a></dd>
                    </span>
                );
            }
            var moreInfo;
            if (this.props.brewery.ratebeer_id) {
                moreInfo = (
                    <a href={'/breweries/' + this.props.brewery.ratebeer_id}>Se mer informasjon</a>
                );
            } else {
                moreInfo = (
                    <p>Vi har ikke klart å matche dette bryggeriet</p>
                );
            }

            return (
                <div className="well">
                    <button
                        type="button"
                        className="close"
                        onClick={this.props.close}
                        aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                    <h2>{getName(this.props.brewery)}</h2>
                    <dl>
                        <span>
                            <dt>Type</dt>
                            <dd>{this.props.brewery.amenity || 'Brewery'}</dd>
                        </span>
                        {address}
                        {website}
                    </dl>
                    {moreInfo}
                </div>
            );
        }
    });

    var CountryMap = React.createClass({

        getInitialState: function () {
            return {selectedBrewery: null};
        },

        brewerySelected: function (brewery) {
            this.setState({selectedBrewery: brewery});
        },

        deselectBrewery: function () {
            this.setState({selectedBrewery: null});
        },

        componentDidMount: function () {
            var element = ReactDOM.findDOMNode(this);
            var map = new L.Map(element, {zoomControl: false});
            new L.Control.Zoom({position: 'topright'}).addTo(map);
            var apikey = this.props.maptoken;
            var baseLayers = {
                'Kart': L.tileLayer.webatlas({
                    mapType: L.TileLayer.Webatlas.Type.VECTOR,
                    apikey: apikey
                }).addTo(map),
                'Foto': L.tileLayer.webatlas({
                    mapType: L.TileLayer.Webatlas.Type.AERIAL,
                    apikey: apikey
                }),
                'Hybrid': L.tileLayer.webatlas({
                    mapType: L.TileLayer.Webatlas.Type.HYBRID,
                    apikey: apikey
                })
            };
            L.control.layers(baseLayers, {}).addTo(map);
            var markers = _.map(this.props.breweries, function (brewery) {
                var l = L.geoJson(brewery.geom).getLayers()[0];
                var icon = L.MakiMarkers.icon({icon: 'beer', color: '#267FCA', size: 'm'});
                var marker = L.marker(l.getLatLng(), {title: getName(brewery), icon: icon});
                marker.on('click', _.bind(function () { this.brewerySelected(brewery); }, this));
                return marker;
            }, this);
            var markerGroup = L.markerClusterGroup({
                spiderfyOnMaxZoom: true,
                showCoverageOnHover: true,
                zoomToBoundsOnClick: true
            }).addTo(map);
            markerGroup.addLayers(markers);
            map.fitBounds(markerGroup.getBounds());
        },


        render: function () {
            if (this.state.selectedBrewery) {
                return (
                    <div className="fullscreenmap">
                        <div className="popup">
                            <BreweryInfo
                                close={this.deselectBrewery}
                                brewery={this.state.selectedBrewery} />
                        </div>
                    </div>
                );
            }
            return (
                <div className="fullscreenmap"></div>
            );
        }
    });

    ns.renderCountryMap = function (data, componentId, title) {
        title = 'Ølkart: ' + data.country;
        var component = document.getElementById(componentId);
        if (!data.breweries.length) {
            ReactDOM.render(
                <ns.Container
                    component={NotFound}
                    title={title} />,
                component
            );
        } else {
            ReactDOM.render(
                <CountryMap
                    maptoken={data.maptoken}
                    breweries={data.breweries} />,
                component
            );
        }
    };

}(bd));
