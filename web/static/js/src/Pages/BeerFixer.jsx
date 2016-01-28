var bd = this.bd || {};
(function (ns) {
    'use strict';

    var PolBeerOverview = React.createClass({
        render: function () {
            return (
                <div className="row">
                    <div className='col-md-6'>
                        <h3>Øl fra polet</h3>
                        <table className='table'>
                            <tbody>
                                <tr>
                                    <th>Bryggeri</th>
                                    <td>{this.props.beer.producer}</td>
                                </tr>
                                <tr>
                                    <th>Navn</th>
                                    <td>{this.props.beer.name}</td>
                                </tr>
                                <tr>
                                    <th>Polets vareside</th>
                                    <td><a href={this.props.beer.url} target="_blank">Link</a></td>
                                </tr>
                            </tbody>
                        </table>
                        <table className='table'>
                            <tbody>
                                <tr>
                                    <th>Abv</th>
                                    <th>Farge</th>
                                    <th>Emballasje</th>
                                </tr>
                                <tr>
                                    <td>{ns.Util.fixedOrNa(this.props.beer.abv, 2)}</td>
                                    <td>{this.props.beer.color}</td>
                                    <td>{this.props.beer.packaging}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            );
        }
    });

    function parseRatebeerUrl(url) {
        if (url.indexOf('ratebeer.com/beer/') !== -1) {
            var data = [];
            var getKeyValue = function (a, b, c, d) {
                data.push(b);
            };
            url.replace(/\/(\d+)/g, getKeyValue);
            return parseInt(_.last(data), 10);
        }
        return null;
    }

    var RatebeerUrlMatcher = React.createClass({

        getInitialState: function () {
            return {validUrl: true, url: this.props.value};
        },

        gotError: function () {
            this.setState({validUrl: false});
        },

        foundBeer: function (beer) {
            this.props.selectBrewery(beer.brewery);
            this.props.selectBeer(beer);
        },

        getBeer: function (id) {
            bd.api.getRatebeerBeer(id, this.foundBeer, this.gotError);
        },

        onChange: function (e) {
            var url = e.target.value;
            var id = parseRatebeerUrl(url);
            if (id || url === '') {
                this.setState({url: url, validUrl: true});
                this.getBeer(id);
            } else {
                this.setState({url: url, validUrl: false});
            }
        },

        focus: function () {
            this.setState({url: '', validUrl: true});
        },

        render: function () {
            return (
                <div className={'form-group' + (this.state.validUrl ? '' : ' has-error')}>
                    <input
                        type="text"
                        className="form-control"
                        placeholder="Url"
                        onFocus={this.focus}
                        onChange={this.onChange}
                        value={this.state.url} />
                </div>
            );
        }
    });

    var RbBeerOverview = React.createClass({

        getInitialState: function () {

            if (!this.props.beer) {
                return {
                    beer: {name: '', style: {name: ''}},
                    brewery: {name: ''}
                };
            }

            return {
                beer: _.clone(this.props.beer),
                brewery: _.clone(this.props.beer.brewery)
            };
        },

        selectBrewery: function (brewery) {
            this.setState({brewery: brewery, beer: {name: '', style: {name: ''}}});
        },

        selectBeer: function (beer) {
            this.setState({beer: beer});
            this.props.onSelect(beer);
        },

        render: function () {

            var details;
            if (this.state.beer.id) {
                details = (
                     <table className='table'>
                        <tbody>
                            <tr>
                                <th>Ølstil</th>
                                <th>Abv</th>
                                <th>Ibu</th>
                                <th>Ratebeer Url</th>
                                <th>Alias</th>
                            </tr>
                            <tr>
                                <td>{this.state.beer.style.name}</td>
                                <td>{ns.Util.fixedOrNa(this.state.beer.abv, 2)}</td>
                                <td>{this.state.beer.ibu}</td>
                                <td><a href={this.state.beer.url} target="_blank">Link</a></td>
                                <td>{this.state.beer.alias ? 'Ja' : 'Nei'}</td>
                            </tr>
                        </tbody>
                    </table>
                );
            }
            var beerDisabled = !_.has(this.state.brewery, 'id');
            var beerSearchParams;
            if (!beerDisabled) {
                beerSearchParams = {brewery: this.state.brewery.id};
            }
            return (
                <div className="row">
                    <div className='col-md-6'>
                        <h3>Øl fra Ratebeer</h3>
                        <table className='table'>
                            <tbody>
                                <tr>
                                    <th>Bryggeri</th>
                                    <td>
                                         <ns.Autocomplete
                                            placeholder="Bryggeri"
                                            ref="brewery"
                                            key={this.state.brewery.id}
                                            initialVal={this.state.brewery.name}
                                            autocompleteSearch={ns.api.searchBrewery}
                                            select={this.selectBrewery} />
                                    </td>
                                </tr>
                                <tr>
                                    <th>Navn</th>
                                    <td>
                                        <ns.Autocomplete
                                            placeholder="øl"
                                            ref="beer"
                                            initialVal={this.state.beer.name}
                                            key={this.state.beer.id}
                                            selectedItem={this.state.beer}
                                            extraParams={beerSearchParams}
                                            disabled={beerDisabled}
                                            autocompleteSearch={ns.api.searchBeer}
                                            select={this.selectBeer} />
                                    </td>
                                </tr>
                                <tr>
                                    <th>Ratebeer-url</th>
                                    <td>
                                        <RatebeerUrlMatcher
                                            key={this.state.beer.id}
                                            value={this.state.beer.url}
                                            selectBrewery={this.selectBrewery}
                                            selectBeer={this.selectBeer}/>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                       {details}
                    </div>
                </div>
            );
        }
    });

    var FeedbackForm = React.createClass({

        getInitialState: function () {
            return {comment: ''};
        },

        changeComment: function (e) {
            this.setState({comment: e.target.value});
        },

        onClick: function () {
            this.props.onClick(this.state.comment);
        },

        render: function () {
            return (
                <div className="row">
                    <div className='col-md-6'>
                        <div>
                            Kommentar:
                            <textarea
                                value={this.state.comment}
                                onChange={this.changeComment}
                                className='form-control' />
                        </div>
                        <div>
                            <button
                                type="button"
                                className="btn btn-primary btn-spaced"
                                onClick={this.onClick}
                                disabled={!this.props.enabled}>
                                Send
                            </button>
                        </div>
                    </div>
                </div>
            );
        }
    });

    var BeerFixer = React.createClass({

        getInitialState: function () {
            return {
                rbBeer: this.props.rb_beer,
                canSubmit: false,
                mappingId: null
            };
        },

        beerSelected: function (beer) {
            var canSubmit = !!beer;
            this.setState({
                rbBeer: beer,
                canSubmit: canSubmit
            });
        },

        sent: function (e) {
            this.setState({mappingId: e.id});
        },

        onClick: function (comment) {
            ns.api.postMatch(this.props.pol_beer.id, this.state.rbBeer.id, comment, this.sent);
        },

        render: function () {

            if (this.state.mappingId) {
                return (
                    <div>
                        <p>Ditt forslag til rettelse er registrert og vil snart bli behandlet</p>
                    </div>
                );
            }
            return (
                <div>
                    <PolBeerOverview beer={this.props.pol_beer} />
                    <RbBeerOverview
                        onSelect={this.beerSelected}
                        beer={this.state.rbBeer} />
                    <FeedbackForm
                        onClick={this.onClick}
                        enabled={this.state.canSubmit}/>
                </div>
            );
        }

    });

    ns.renderBeerFixer = function (data, componentId) {
        var component = document.getElementById(componentId);

        ReactDOM.render(
            <ns.Container
                component={BeerFixer}
                pol_beer={data.pol_beer}
                rb_beer={data.rb_beer}
                title={'Fiks ølmatching'} />,
            component
        );
    };

}(bd));

