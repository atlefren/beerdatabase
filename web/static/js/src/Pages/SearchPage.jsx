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

    var Slider = React.createClass({

        getInitialState: function () {
            return {
                min: this.props.min,
                max: this.props.max
            };
        },

        componentDidMount: function () {
            var element = ReactDOM.findDOMNode(this);
            noUiSlider.create(element, {
                start: [this.props.initMin, this.props.initMax],
                connect: true,
                step: this.props.step,
                range: {
                    min: this.props.min,
                    max: this.props.max
                }
            });

            element.noUiSlider.on('update', this.sliderChanged);
        },

        sliderChanged: function (values, handle) {
            var min = parseFloat(values[0]);
            var max = parseFloat(values[1]);
            if (min !== this.state.min || max !== this.state.max) {
                this.setState({min: min, max: max});
                this.props.change(min, max);
            }
        },

        render: function () {
            return (<div className="slider noUi-extended" />);
        }
    });

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

    var SelectedStyle = React.createClass({

        click: function () {
            this.props.deselect(this.props.style.id);
        },

        render: function () {
            return (
                <li className="list-group-item">
                    {this.props.style.name}
                    <span
                        onClick={this.click}
                        className="glyphicon glyphicon-remove pull-right remove-btn" />
                </li>
            );
        }
    });


    var SelectedStyleList = React.createClass({

        render: function () {

            var styles = _.map(this.props.styles, function (style) {
                return (
                    <SelectedStyle
                        style={style}
                        key={style.id}
                        deselect={this.props.deselect} />
                );
            }, this);

            return (
                <ul className="list-group">
                    {styles}
                </ul>
            );
        }
    });


    var StyleChooser = React.createClass({

        getDefaultProps: function () {
            return {value: []};
        },

        getInitialState: function () {
            var selected = _.pluck(this.props.styles, 'id');
            var allSelected = (selected.length === this.props.value.length);
            return {selected: this.props.value, allSelected: allSelected};
        },

        onChange: function (e) {
            var selected = _.clone(this.state.selected);
            if (selected.length < 10) {
                var add = parseInt(e.target.value, 10);
                if (add ===  -1) {
                    return;
                }
                selected.push(add);
            } else {
                //display warning about max?
            }
            var allSelected = (selected.length === this.props.styles.length);
            this.setState({selected: selected, allSelected: allSelected});
            this.changed(selected);
        },

        changed: function (values) {
            this.props.changed(this.props.type, values);
        },

        deselectStyle: function (styleId) {
            var selected = _.clone(this.state.selected);
            selected.splice(selected.indexOf(styleId), 1);

            var allSelected = (selected.length === this.props.styles.length);
            this.setState({selected: selected, allSelected: allSelected});
            this.changed(selected);
        },

        render: function () {
            var unselectedStyles = _.chain(this.props.styles)
                .filter(function (style) {
                    return this.state.selected.indexOf(style.id) === -1;
                }, this)
                .map(function (style) {
                    return (
                        <option
                            key={style.id}
                            value={style.id}>
                            {style.name}
                        </option>
                    );
                })
                .value();

            unselectedStyles.unshift((
                 <option
                    key="-1"
                    value="-1">
                    ---
                </option>
            ));

            var selectedStyles = _.filter(this.props.styles, function (style) {
                return this.state.selected.indexOf(style.id) > -1;
            }, this);


            return (
                <fieldset>
                    <legend>Stil</legend>
                    <div className="form-group">

                        <SelectedStyleList
                            styles={selectedStyles}
                            deselect={this.deselectStyle} />
                        <select
                            className="form-control"
                            onChange={this.onChange}
                            disabled={this.state.selected.length >= 10}
                            multiple={false}>
                            {unselectedStyles}
                        </select>
                    </div>
                </fieldset>
            );
        }
    });

    function getFromArr(arr, idx, fallback) {
        if (_.isUndefined(arr)) {
            return fallback;
        }
        var val = arr[idx];
        if (!_.isUndefined(val)) {
            return val;
        }
        return fallback;
    }

    var SliderFieldSet = React.createClass({

        getDefaultProps: function () {
            return {
                min: 0,
                max: 100,
                step: 1,
                displayPostfix: ''
            };
        },

        getInitialState: function () {
            var min = this.props.min;
            var max = this.props.max;
            if (this.props.value && this.props.value.length === 2) {
                min = this.props.value[0];
                max = this.props.value[1];
            }
            return {min: min, max: max};
        },

        sliderChanged: function (min, max) {
            this.setState({min: min, max: max});
            if (this.props.changed) {
                this.props.changed(this.props.type, [min, max]);
            }
        },

        render: function () {

            var min = this.state.min;
            var max = this.state.max;
            if (this.props.step < 1 && this.min) {
                min = min.toFixed(1);
                max = max.toFixed(1);
            }

            var label;
            if (this.props.label) {
                label = (<label>{this.props.label}</label>);
            }
            var legend;
            if (this.props.legend) {
                legend = (<legend>{this.props.legend}</legend>);
            }
            return (
                <fieldset>
                    {legend}
                    <div className="form-group">
                        {label}
                        <div>
                            <div>
                                {min}{this.props.displayPostfix}
                                {' '}
                                til
                                {' '}
                                {max}{this.props.displayPostfix}
                            </div>
                            <Slider
                                {...this.props}
                                initMin={getFromArr(this.props.value, 0, this.props.min)}
                                initMax={getFromArr(this.props.value, 1, this.props.max)}
                                change={this.sliderChanged} />
                        </div>
                    </div>
                </fieldset>
            );
        }
    });


    var CheckboxComponent = React.createClass({

        getInitialState: function () {
            return {checked: this.props.selected};
        },

        toggle: function (e) {
            var checked = e.target.checked;
            this.setState({checked: checked});
            this.props.onChange(this.props.type, checked);
        },

        render: function () {
            return (
                <div className="checkbox">
                    <label>
                        <input
                            type="checkbox"
                            onChange={this.toggle}
                            checked={this.state.checked} />
                        {' '}
                        {this.props.name}
                    </label>
                </div>
            );
        }
    });

    var AvailableAtChooser = React.createClass({

        getDefaultProps: function () {
            var options = [
                {name: 'Polet', key: 'polet'}/*,
                {name: 'Gulating', key: 'gulating'}*/
            ];
            return {options: options, value: []};
        },

        getInitialState: function () {
            var initValue = this.props.value;
            var selected = _.chain(this.props.options)
                .filter(function (option) {
                    return (initValue.indexOf(option.key) !== -1);
                })
                .map(function (option) {
                    return option.key;
                })
                .value();
            return {selected: selected};
        },

        onChange: function (key, selected) {
            var prevSelected = _.clone(this.state.selected);
            var index = prevSelected.indexOf(key);

            if (selected && index === -1) {
                prevSelected.push(key);
            }
            if (!selected && index > -1) {
                prevSelected.splice(index, 1);
            }
            this.setState({selected: prevSelected});

            this.props.changed(this.props.type, prevSelected);
        },

        render: function () {

            var checkboxes = _.map(this.props.options, function (option) {
                var selected = this.state.selected.indexOf(option.key) !== -1;
                return (
                    <CheckboxComponent
                        onChange={this.onChange}
                        name={option.name}
                        type={option.key}
                        key={option.key}
                        selected={selected} />
                    );
            }, this);

            return (
                <fieldset>
                    <legend>Tilgjengelig på</legend>
                    {checkboxes}
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
                    <a href={url} className="list-group-item">{search.name}</a>
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
                                value={this.props.initValues.name}
                                changed={this.valueChanged} />
                            <StyleChooser 
                                type="style"
                                value={this.props.initValues.style}
                                changed={this.valueChanged}
                                styles={this.props.searchParams.styles} />
                            <fieldset>
                                <legend>Score</legend>
                                <SliderFieldSet
                                    type="overallScore"
                                    label="Overall"
                                    value={this.props.initValues.overallScore}
                                    min={0}
                                    max={100}
                                    changed={this.valueChanged} />
                                <SliderFieldSet
                                    type="styleScore"
                                    label="Style"
                                    value={this.props.initValues.styleScore}
                                    min={0}
                                    max={100}
                                    changed={this.valueChanged} />
                            </fieldset>
                            <SliderFieldSet
                                type="price"
                                value={this.props.initValues.price}
                                legend="Pris"
                                min={10}
                                max={200}
                                displayPostfix=" kr"
                                changed={this.valueChanged} />
                            <SliderFieldSet
                                type="abv"
                                value={this.props.initValues.abv}
                                legend="Alkohol"
                                min={0}
                                max={50}
                                displayPostfix="%"
                                step={0.5}
                                changed={this.valueChanged} />
                            <AvailableAtChooser
                                type="availableAt"
                                value={this.props.initValues.availableAt}
                                changed={this.valueChanged} />
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
            return {beers: [], queryNumber: 0};
        },

        componentDidMount: function () {
            if (this.props.startWithSearch) {
                this.doSearch(this.props.initValues);
            }
        },

        doSearch: function (params) {
            var queryNumber = this.state.queryNumber + 1;
            this.setState({isSearching: true, queryNumber: queryNumber});
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
                initValues={data.init_values} />,
            container
        );
    };
}(bd));
