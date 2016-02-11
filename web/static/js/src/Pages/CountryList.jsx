var bd = this.bd || {};
(function (ns) {
    'use strict';

    var columns = [
        {
            id: 'name',
            name: 'Navn',
            formatter: function (country) {
                return (<a href={'/countries/' + country.rb_id}>{country.name}</a>);
            },
            sortParams: 'name',
            isSorted: false,
            sortDirection: 'asc'
        },
        {
            id: 'count_pol',
            name: 'Antall øl på polet',
            formatter: function (country) {
                return country.count;
            },
            sortParams: 'count',
            isSorted: true,
            sortDirection: 'desc'
        }
    ];

    function createFeatureCollection(geoms) {
        return _.map(geoms, function (geom) {
            return {
                'type': 'Feature',
                'properties': {'iso_code': geom.iso_code},
                'geometry': geom.geom
            };
        });
    }

    function getCountriesWithBreweries(allCountries, countries) {
        var codes = _.pluck(countries, 'iso_code');
        return _.chain(allCountries)
            .filter(function (feature) {
                return codes.indexOf(feature.properties.iso_code) > -1;
            })
            .map(function (feature) {
                var c = _.find(countries, function (country) {
                    return country.iso_code === feature.properties.iso_code;
                });
                if (c) {
                    feature.properties.count = c.count;
                    feature.properties.rb_id = c.rb_id;
                }
                return feature;
            })
            .value();
    }

    ns.CountryOverview = React.createClass({

        getInitialState: function () {
            return {type: 'table'};
        },

        featureClicked: function (f) {
            console.log(f);
            window.location.href = '/countries/' + f.properties.rb_id;
        },

        showTable: function () {
            this.setState({type: 'table'});
        },

        showMap: function () {
            this.setState({type: 'map'});
        },

        render: function () {

            var component;
            if (this.state.type === 'map') {
                var range = [
                    _.min(this.props.countries, function (c) {return c.count; }).count,
                    _.max(this.props.countries, function (c) {return c.count; }).count
                ];
                component = (
                    <ns.CountryMap
                        allCountries={this.props.allCountries}
                        countriesWithBreweries={this.props.countriesWithBreweries}
                        range={range}
                        clicked={this.featureClicked}/>
                );
            } else {
                var component = (
                    <ns.SortableTable
                        items={this.props.countries}
                        columns={this.props.columns}
                        idProperty='rb_id'/>
                );
            }

            var tableClass = 'btn btn-default';
            if (this.state.type === 'table') {
                tableClass += ' active';
            }
            var mapClass = 'btn btn-default';
            if (this.state.type === 'map') {
                mapClass += ' active';
            }

            return (
                <div>
                    <nav className="navbar navbar-default">
                        <div className="container-fluid">
                            <form className="navbar-form">
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
                    {component}
                </div>
            );
        }
    });

    ns.renderCountryList = function (data, componentId, title) {
        var allCountries = createFeatureCollection(data.geoms);
        var countriesWithBreweries = getCountriesWithBreweries(allCountries, data.countries);

        var component = document.getElementById(componentId);

        ReactDOM.render(
            <ns.Container
                component={ns.CountryOverview}
                title={title}
                allCountries={allCountries}
                countriesWithBreweries={countriesWithBreweries}
                countries={data.countries}
                columns={columns}
                idProperty='rb_id' />,
            component
        );

    };

}(bd));
