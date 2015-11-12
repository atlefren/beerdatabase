var bd = this.bd || {};
(function (ns) {
    'use strict';

    var pairings = [
        'Skalldyr',
        'Lyst kjøtt',
        'Dessert, kake, frukt',
        'Fisk',
        'Aperitiff/avec',
        'Lam og sau',
        'Ost',
        'Småvilt og fugl',
        'Svinekjøtt',
        'Grønnsaker',
        'Storfe',
        'Storvilt'
    ];

    var ScoreDisplay = React.createClass({

        render: function () {
            return (
                <div className="one column score-box">
                    <strong>Score</strong>
                    <div className="styleHeader">Overall</div>
                    <div className="overallScore">{ns.Util.valueOrNa(this.props.beer.score_overall)}</div>
                    <div className="styleHeader">Style</div>
                    <div className="styleScore">{ns.Util.valueOrNa(this.props.beer.score_style)}</div>
                </div>
            );
        }

    });


    var ExternalLink = React.createClass({
        render: function () {
            return (
                <li className="navbar-item">
                    <a href={this.props.link.url} className="navbar-link">
                        <i className="fa fa-external-link-square"></i>{' '}
                        Mer hos {' '}{this.props.link.name}
                    </a>
                </li>
            );
        }
    });

    var ExternalLinks = React.createClass({

        render: function () {
            var links = _.map(this.props.links, function (link) {
                return (<ExternalLink link={link} />);
            });

            return (
                <ul className="navbar-list">
                    {links}
                </ul>
            );
        }
    });

    var BeerOverview = React.createClass({

        getHelpMsg: function () {
            var err_url = '/pol_beers/' + this.props.beer.id + '/report';
            return (
                <div className="alert alert-warning">
                    <strong>Hjelp:</strong>{' '}
                    Dette ølet heter {' '} <em>{this.props.beer.name}</em>{' '} og er brygget
                    av {' '} <em>{this.props.beer.producer}</em> {' '} ifølge Vinmonopolet.{' '}
                    Hvis dette ikke stemmer kan det godt skyldes en feilmatching,{' '}
                    fint om du kan si fra om feilen {' '} <a href={err_url}>her</a>.
                </div>
            );
        },

        getExternalLinks: function () {
            return [
                {name: 'Ratebeer', url: '#'},
                {name: 'Vinmonopolet', url: this.props.beer.url},
                {name: 'Apéritif.no', url: '#'}
            ];
        },

        render: function () {
            var beer = this.props.beer;
            var rbbeer = this.props.beer.ratebeer;
            var report_link = '/pol_beers/' + beer.id + '/report';

            return (
                <div>
                    <h1>{rbbeer.name}</h1>

                    <p>Brygget av{' '}{rbbeer.brewery.name}</p> 

                    <div className="row">
                        <ScoreDisplay beer={rbbeer} />
                        <div className="four columns">
                            <table className="u-full-width">
                                <tr>
                                    <th>Stil</th>
                                    <td>{rbbeer.style.name}</td>
                                </tr>
                                <tr>
                                    <th>Abv</th>
                                    <td>{ns.Util.fixedOrNa(rbbeer.abv, 2)}</td>
                                </tr>
                                <tr>
                                    <th>Ibu</th>
                                    <td>{ns.Util.valueOrNa(rbbeer.ibu)}</td>
                                </tr>
                                <tr>
                                    <th>Alias</th>
                                    <td>{rbbeer.alias}</td>
                                </tr>
                            </table>
                         </div>
                         <div className="four columns">
                            <table className="u-full-width">
                                <tr>
                                    <th>Pris</th>
                                    <td>{ns.Util.fixedOrNa(beer.price, 2)} kr</td>
                                </tr>
                                <tr>
                                    <th>Volum</th>
                                    <td>{ns.Util.fixedOrNa(beer.volume, 2)} l</td>
                                </tr>
                                <tr>
                                    <th>Butikkkatergori</th>
                                    <td>{ns.Util.valueOrNa(beer.store_category)}</td>
                                </tr>
                                <tr>
                                    <th>Produktutvalg</th>
                                    <td>{ns.Util.valueOrNa(beer.produktutvalg)}</td>
                                </tr>
                            </table>
                         </div>
                         <div className="four columns">
                         </div>
                    </div>

                    <ExternalLinks links={this.getExternalLinks()}/>

                    <table className="u-full-width">
                        <tr>
                            <th>Karakteristikk</th>
                            <td>{beer.sweetness} | {beer.freshness} | {beer.bitterness} | {beer.richness}</td>
                        </tr>
                        <tr>
                            <th>Passer til</th>
                            <td>{beer.pairs_with_1} | {beer.pairs_with_2} | {beer.pairs_with_3} </td>
                        </tr>
                        <tr>
                            <th>Lukt</th>
                            <td>{beer.smell}</td>
                        </tr>
                        <tr>
                            <th>Smak</th>
                            <td>{beer.taste}</td>
                        </tr>
                        <tr>
                            <th>Metode</th>
                            <td>{beer.method}</td>
                        </tr>
                        <tr>
                            <th>Lagringsgrad</th>
                            <td>{beer.storage_notes}</td>
                        </tr>
                    </table>

                    {this.getHelpMsg()}
                </div>
            );
        }

    });


    ns.renderBeerOverview = function(beer, component) {
        React.render(<BeerOverview beer={beer} />, component);
    };

}(bd));