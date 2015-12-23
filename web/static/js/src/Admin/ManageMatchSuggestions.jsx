var bd = this.bd || {};
(function (ns) {
    'use strict';

    function hasRbBrewery(suggestion) {
        return !(suggestion.pol_beer.ratebeer === null);
    }

    var MatchHandlerMixin = {

        confirmSuggestion: function (e) {
            ns.api.confirmSuggestion(this.props.suggestion, this.props.updated);
        },

        rejectSuggestion: function (e) {
            ns.api.rejectSuggestion(this.props.suggestion, this.props.updated);
        }
    };

    var NoMatchElement = React.createClass({

        mixins: [MatchHandlerMixin],

        render: function () {
            var suggestion = this.props.suggestion;
            return (
                <tr key={suggestion.id}>
                    <td>{suggestion.pol_beer.producer}</td>
                    <td>
                        <a href={suggestion.pol_beer.url} target="_blank">
                            {suggestion.pol_beer.name}
                        </a>
                    </td>
                    <td>{suggestion.rb_beer.brewery.name}</td>
                    <td>{suggestion.rb_beer.name}</td>
                    <td>{suggestion.comment}</td>
                    <td>
                        <i
                            onClick={this.confirmSuggestion}
                            className="fa fa-check-circle fa-2x" />
                        &nbsp;
                        <i
                            onClick={this.rejectSuggestion}
                            className="fa fa-minus-circle fa-2x" />
                    </td>
                </tr>
            );
        }
    });

    var NoMatchList = React.createClass({

        render: function () {

            if (!this.props.suggestions.length) {
                return (<p>Ingen forslag.</p>);
            }

            var list = _.map(this.props.suggestions, function (suggestion) {
                return (
                    <NoMatchElement
                        updated={this.props.updated}
                        suggestion={suggestion}
                        key={suggestion.id} />
                );
            }, this);

            return (
                <table className="table">
                    <thead>
                        <tr>
                            <th>Bryggeri Polet</th>
                            <th>Navn Polet</th>
                            <th>Bryggeri Ratebeer</th>
                            <th>Navn Ratebeer</th>
                            <th>Kommentar</th>
                            <th>Aksjoner</th>
                        </tr>
                    </thead>
                    <tbody>
                        {list}
                    </tbody>
                </table>
            );
        }

    });

    var ChangeElement = React.createClass({

        mixins: [MatchHandlerMixin],

        render: function () {
            var suggestion = this.props.suggestion;
            return (
                <tr key={suggestion.id}>
                    <td>{suggestion.pol_beer.producer}</td>
                    <td>
                        <a href={suggestion.pol_beer.url} target="_blank">
                            {suggestion.pol_beer.name}
                        </a>
                    </td>
                    <td>{suggestion.pol_beer.ratebeer.brewery.name}</td>
                    <td>{suggestion.pol_beer.ratebeer.name}</td>
                    <td>{suggestion.rb_beer.brewery.name}</td>
                    <td>{suggestion.rb_beer.name}</td>
                    <td>{suggestion.comment}</td>
                    <td>
                        <i
                            onClick={this.confirmSuggestion}
                            title="Godkjenn"
                            className="fa fa-check-circle fa-2x" />
                        &nbsp;
                        <i
                            onClick={this.rejectSuggestion}
                            title="Avvis"
                            className="fa fa-minus-circle fa-2x" />
                    </td>
                </tr>
            );
        }
    });

    var ChangesList = React.createClass({

        render: function () {

            if (!this.props.suggestions.length) {
                return (<p>Ingen forslag.</p>);
            }

            var list = _.map(this.props.suggestions, function (suggestion) {
                return (
                    <ChangeElement
                        updated={this.props.updated}
                        suggestion={suggestion}
                        key={suggestion.id} />
                );
            }, this);

            return (
                <table className="table">
                    <thead>
                        <tr>
                            <th>Bryggeri Polet</th>
                            <th>Navn Polet</th>
                            <th>Bryggeri Ratebeer</th>
                            <th>Navn Ratebeer</th>
                            <th>Nytt Bryggeri Ratebeer</th>
                            <th>Nytt Navn Ratebeer</th>
                            <th>Kommentar</th>
                            <th>Aksjoner</th>
                        </tr>
                    </thead>
                    <tbody>
                        {list}
                    </tbody>
                </table>
            );
        }

    });

    var BeerFixSuggestions = React.createClass({

        getInitialState: function () {
            return {suggestions: this.props.suggestions};
        },

        updated: function (newList) {
            this.setState({suggestions: newList});
        },

        render: function () {
            var noMatch = _.reject(this.state.suggestions, hasRbBrewery);
            var changes = _.filter(this.state.suggestions, hasRbBrewery);

            return (
                <div>
                    <h2>Uten match</h2>
                    <NoMatchList suggestions={noMatch} updated={this.updated} />
                    <h2>Endringer</h2>
                    <ChangesList suggestions={changes} updated={this.updated} />
                </div>
            );
        }
    });

    ns.renderBeerFixSuggestions  = function (suggestions, componentId) {
        var component = document.getElementById(componentId);
        ReactDOM.render(
            <ns.Container
                component={BeerFixSuggestions}
                suggestions={suggestions}
                title="Matcheforslag" />,
            component
        );
    };

}(bd));
