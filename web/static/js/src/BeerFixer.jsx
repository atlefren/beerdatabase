var bd = this.bd || {};
(function (ns) {
    'use strict';

    var PolBeerOverview = React.createClass({
        render: function () {
            return (
                <div className="row">
                    <div className='six columns'>
                        <h3>Øl fra polet</h3>
                        <table className='u-full-width'>
                            <tbody>
                                <tr>
                                    <th>Bryggeri</th>
                                    <td>{this.props.beer.producer}</td>
                                </tr>
                                <tr>
                                    <th>Navn</th>
                                    <td>{this.props.beer.name}</td>
                                </tr>
                            </tbody>
                        </table>
                        <table>
                            <tr>
                                <th>Abv</th>
                                <th>Farge</th>
                                <th>Emballasje</th>
                            </tr>
                            <tr>
                                <td>{this.props.beer.abv}</td>
                                <td>{this.props.beer.color}</td>
                                <td>{this.props.beer.packaging}</td>
                            </tr>
                        </table>
                    </div>
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
                brewery: _.clone(this.props.beer.brewery),
            }
        },

        render: function () {

            var details;
            if (this.state.beer.id) {
                details = (
                     <table className='u-full-width'>
                        <tr>
                            <th>Ølstil</th>
                            <th>Abv</th>
                            <th>Ibu</th>
                            <th>Alias</th>
                        </tr>
                        <tr>
                            <td>{this.state.beer.style.name}</td>
                            <td>{this.state.beer.abv}</td>
                            <td>{this.state.beer.ibu}</td>
                            <td>{this.state.beer.alias}</td>
                        </tr>
                    </table>
                );
            }

            var beerDisabled = !_.has(this.state.brewery, 'id');
            return (
                <div className="row">
                    <div className='six columns'>
                        <h3>Øl fra Ratebeer</h3>
                        <table className='u-full-width'>
                            <tbody>
                                <tr>
                                    <th>Bryggeri</th>
                                    <td><input className='u-full-width' type="text" value={this.state.brewery.name} /></td>
                                </tr>
                                <tr>
                                    <th>Navn</th>
                                    <td>
                                        <input
                                            className='u-full-width'
                                            type="text"
                                            disabled={beerDisabled}
                                            value={this.state.beer.name} />
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
        render: function () {
            console.log(this.props.enabled)
            return (
                <div className="row">
                    <div className='u-full-width'>
                        <div class="row">
                        <textarea />
                        </div>
                        <div class="row">
                        <button type="buttton" className="button-primary" disabled={!this.props.enabled}>Send</button>
                        </div>
                    </div>
                </div>
            );
        }
    });

    var BeerFixer = React.createClass({

        getInitialState: function () {
            return {
                canSubmit: false
            };
        },

        render: function () {
            return (
                <div>
                    <PolBeerOverview beer={this.props.pol_beer} />
                    <RbBeerOverview beer={this.props.rb_beer} />
                    <FeedbackForm enabled={this.state.canSubmit}/>
                </div>
            );
        }

    });

    ns.renderBeerFixer = function(pol_beer, rb_beer, component) {
        React.render(<BeerFixer pol_beer={pol_beer} rb_beer={rb_beer}/>, component);
    };

}(bd));
