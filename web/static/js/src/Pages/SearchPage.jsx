var bd = this.bd || {};
(function (ns) {
    'use strict';

    var predefSearches = [
        {name: 'Beste humleøl', overallScore: [95, 100], style: [114, 81, 17, 18, 121], styleScore: [95, 100], initialSort: 'rating'},
        {name: 'Beste Stout/porter', overallScore: [95, 100], style: [63, 22, 79, 24, 113, 5, 6, 23, 16], styleScore: [95, 100], initialSort: 'rating'},
        {name: 'Beste surøl', overallScore: [90, 100], style: [77, 14, 73, 78, 52, 119, 118, 61, 117], styleScore: [50, 100], initialSort: 'rating'},
        {name: 'Frukt- / krydderøl', style: [14, 40, 120, 57, 122]},
        {name: 'Hveteøl', style: [48, 61, 100, 25, 19, 7, 82, 85]}
    ];

    var NameSearcher = React.createClass({

        getDefaultProps: function () {
            return {value: ''};
        },

        getInitialState: function () {
            return {value: this.props.value};
        },

        onChange: function (e) {
            var value = e.target.value;
            this.setState({value: value});
            this.props.changed(this.props.type, value);
        },

        render: function () {
            return (
                <fieldset>
                    <legend>Navn</legend>
                    <div className="form-group">
                        <input
                            type="text"
                            onChange={this.onChange}
                            className="form-control"
                            value={this.state.value} />
                    </div>
                </fieldset>
            );
        }
    });

    var PredefinedSearches = React.createClass({

        render: function () {
            var searches = _.map(this.props.searches, function (search) {
                var query = _.chain(['style', 'overallScore', 'styleScore', 'initialSort'])
                    .map(function (prop) {
                        if (!_.has(search, prop)) {
                            return;
                        }
                        var val = search[prop];
                        if (_.isArray(val)) {
                            val = val.join(',');
                        }
                        return prop +'=' + encodeURIComponent(val);
                    })
                    .compact()
                    .value();
                var url = '/search?' + query.join('&'); 
                return (
                    <a
                        href={url}
                        key={url}
                        className="list-group-item">
                        {search.name}
                    </a>
                );
            });
            return (
                <fieldset>
                    <legend>Standardsøk</legend>
                    <div className="list-group">
                        {searches}
                    </div>
                </fieldset>
            );
        }
    });

    var PolChooser  = React.createClass({

        getInitialState: function () {
            return {searching: false, error: null};
        },

        gotPol: function (res) {
            this.setState({searching: false, error: null});
            this.props.changed(this.props.type, _.chain(res).pluck('id').first(5).value());
        },

        gotUserPosition: function (e) {
            var lat = e.coords.latitude;
            var lon = e.coords.longitude;
            bd.api.getNearbyPolShops(lat, lon, this.gotPol);
        },

        positionError: function () {
            this.setState({error: 'Kunne ikke hente posisjon', searching: false});
        },

        getClosest: function () {
            this.setState({searching: true, error: false});
            navigator.geolocation.getCurrentPosition(this.gotUserPosition, this.positionError);
        },

        render: function () {

            var button;
            if (this.state.searching) {
                button = (<i className="fa fa-spinner fa-spin fa-2x"></i>);
            } else {
                button = (
                    <button
                        className="btn"
                        type="button"
                        onClick={this.getClosest}>
                        Nærmeste pol
                    </button>
                );
            }
            var error;
            if (this.state.error) {
                error = (<div className="alert alert-danger" role="alert">{this.state.error}</div>);
            }

            return (
                <div>
                    <ns.ItemChooser {...this.props} />
                    {button}
                    {error}
                </div>
            );
        }
    });

    var SearchField = React.createClass({

        getDefaultProps: function () {
            return {showMobileSearch: true};
        },

        getInitialState: function () {
            var state = _.clone(this.props.initValues);
            state.showMobileSearch = this.props.showMobileSearch;
            return state;
        },

        valueChanged: function (key, value) {
            var data = _.clone(this.state);
            if (_.isEqual(value, data[key])) {
                return;
            }
            data[key] = value;
            this.setState(data);
            this.props.onSearch(data);
        },

        showSearch: function () {
            this.setState({showMobileSearch: true});
        },

        hideSearch: function () {
            this.setState({showMobileSearch: false});
        },

        render: function () {
            var searchClass = 'hidden-xs hidden-sm';
            if (this.state.showMobileSearch) {
                searchClass = 'mobile-search';
            }

            return (
                <div>
                    <button
                        className="btn btn-default hidden-lg hidden-md btn-spaced"
                        onClick={this.showSearch}
                        type="button">
                        <span className="glyphicon glyphicon-search" aria-hidden="true"></span>
                        {' '}
                        Filtrer
                    </button>

                    <div className={searchClass}>
                        <h3 className="hidden-lg hidden-md">Søk</h3>
                        <button
                            className="btn btn-default hidden-lg hidden-md search-close"
                            onClick={this.hideSearch}
                            type="button">
                            Søk
                        </button>
                        <p>Antall treff:{' '}{this.props.numHits}</p>
                        <form>
                            <NameSearcher
                                type="name"
                                value={this.state.name}
                                changed={this.valueChanged} />
                            <fieldset>
                                <legend>Stil</legend>
                                <ns.ItemChooser
                                    type="style"
                                    value={this.state.style}
                                    changed={this.valueChanged}
                                    items={this.props.searchParams.styles} />
                            </fieldset>
                            <fieldset>
                                <legend>Score</legend>
                                <ns.SliderFormGroup
                                    type="overallScore"
                                    label="Overall"
                                    value={this.state.overallScore}
                                    min={0}
                                    max={100}
                                    changed={this.valueChanged} />
                                <ns.SliderFormGroup
                                    type="styleScore"
                                    label="Style"
                                    value={this.state.styleScore}
                                    min={0}
                                    max={100}
                                    changed={this.valueChanged} />
                            </fieldset>
                            <fieldset>
                                <legend>Pris</legend>
                                <ns.SliderFormGroup
                                    type="price"
                                    value={this.state.price}
                                    legend=""
                                    min={10}
                                    max={200}
                                    displayPostfix=" kr"
                                    changed={this.valueChanged} />
                            </fieldset>
                            <fieldset>
                                <legend>Alkohol</legend>
                                <ns.SliderFormGroup
                                    type="abv"
                                    value={this.state.abv}
                                    legend=""
                                    min={0}
                                    max={50}
                                    displayPostfix="%"
                                    step={0.5}
                                    changed={this.valueChanged} />
                            </fieldset>
                            <fieldset>
                                <legend>Tilgjengelig på pol</legend>
                                <PolChooser
                                    type="pol"
                                    value={this.state.pol}
                                    changed={this.valueChanged}
                                    items={this.props.searchParams.pol}/>
                            </fieldset>
                            <PredefinedSearches searches={predefSearches}/>
                        </form>
                    </div>
                </div>
            );
        }
    });

    var columnIds = ['brewery', 'style', 'rating', 'abv', 'price'];
    var resultColumns = ns.getColumnsForTable(columnIds);
    resultColumns.unshift({
        id: 'name',
        name: 'Navn',
        formatter: function (beer) {
            if (beer.pol_id) {
                return (
                    <a href={'/pol_beers/' + beer.pol_id}>
                        {beer.name}
                    </a>
                );
            }
            return beer.name;
        },
        sortParams: 'name',
        isSorted: true,
        sortDirection: 'asc'
    });


    var SearchPage = React.createClass({

        getInitialState: function () {
            return {beers: [], queryNumber: 0, params: {}};
        },

        componentDidMount: function () {
            if (this.props.startWithSearch) {
                this.doSearch(this.props.initValues);
            }
        },

        doSearch: function (params) {
            var queryNumber = this.state.queryNumber + 1;
            this.setState({
                isSearching: true,
                queryNumber: queryNumber,
                params: params
            });
            ns.Util.setQueryParams(params);
            ns.api.fullsearchBeer(params, _.bind(function (res) {
                if (queryNumber === this.state.queryNumber) {
                    this.gotSearchResults(res);
                }
            }, this), this.searchError);
        },

        gotSearchResults: function (beers) {
            this.setState({beers: beers, isSearching: false});
        },

        searchError: function () {
            this.setState({beers: []});
        },

        onSort: function (columnId, direction) {
            console.log(columnId);
            var params = _.clone(this.state.params);
            params.initialSort = columnId;
            params.initialSortDir = direction;
            ns.Util.setQueryParams(params);
            this.setState(params);
        },

        render: function () {
            var results;
            if (this.state.isSearching) {
                results = (<ns.LoadIndicator text="Søker" />);
            } else if (this.state.beers === null) {
                results = (<p>Gjør et søk</p>);
            } else if (this.state.beers.length === 0) {
                results = (<p>Ingen treff</p>);
            } else {
                results = (
                    <ns.SortableTable
                        initialSort={this.props.initialSort}
                        initialSortDir={this.props.initialSortDir}
                        onSort={this.onSort}
                        items={this.state.beers}
                        columns={resultColumns} />
                );
            }
            return (
                <div className="row">
                    <div id="search_field" className="col-md-3 static">
                        <SearchField
                            showMobileSearch={!this.props.startWithSearch}
                            onSearch={this.doSearch}
                            numHits={this.state.beers.length}
                            searchParams={this.props.searchParams}
                            initValues={this.props.initValues} />
                    </div>
                    <div id="search_results" className="col-md-9 static">
                        {results}
                    </div>
                </div>
            );
        }
    });

    ns.renderSearchPage = function (data, containerId) {
        var container = document.getElementById(containerId);
        ReactDOM.render(
            <SearchPage
                searchParams={data.search_params}
                startWithSearch={data.startWithSearch}
                initialSort={data.initialSort}
                initialSortDir={data.initialSortDir}
                initValues={data.init_values} />,
            container
        );
    };
}(bd));
