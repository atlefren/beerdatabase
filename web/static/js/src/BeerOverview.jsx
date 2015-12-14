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

    var Characteristics = React.createClass({

        characteristics: [
            {key: 'sweetness', 'name': 'Sødme'},
            {key: 'freshness', 'name': 'Friskhet'},
            {key: 'bitterness', 'name': 'Bitterhet'},
            {key: 'richness', 'name': 'Fylde'}
        ],

        render: function () {

            var characteristics = _.chain(this.characteristics)
                .filter(function (characteristic) {
                    return !!this.props.beer[characteristic.key];
                }, this)
                .map(function (characteristic) {
                    var c = this.props.beer[characteristic.key];
                    return (
                        <li key={characteristic.key}>
                            <ns.Pie
                                name={characteristic.name}
                                value={c} />
                        </li>
                    );
                }, this)
                .value();


            return (
                 <tr>
                    <th>Karakteristikk</th>
                    <td>
                        <ul className="list-inline pies">
                            {characteristics}
                        </ul>
                    </td>
                </tr>
            );
        }
    })

    var ScoreDisplay = React.createClass({

        render: function () {
            return (
                <div className='col-md-1 score-box'>
                    <strong>Score</strong>
                    <div className='styleHeader'>Overall</div>
                    <div className='overallScore'>{ns.Util.valueOrNa(this.props.beer.score_overall)}</div>
                    <div className='styleHeader'>Style</div>
                    <div className='styleScore'>{ns.Util.valueOrNa(this.props.beer.score_style)}</div>
                </div>
            );
        }
    });

    var ExternalLink = React.createClass({
        render: function () {
            return (
                <li>
                    <a href={this.props.link.url}>
                        <i className='fa fa-external-link-square'></i>{' '}
                        Mer hos {' '}{this.props.link.name}
                    </a>
                </li>
            );
        }
    });

    var ExternalLinks = React.createClass({

        render: function () {
            var links = _.map(this.props.links, function (link, i) {
                return (<ExternalLink link={link} key={i} />);
            });

            return (
                <ul className='list-inline externalLinks'>
                    {links}
                </ul>
            );
        }
    });

    var LineChart = window['react-chartjs'].Line;

    var StockHistory = React.createClass({

        render: function () {

            var data = _.pluck(this.props.history, 'stock');
            var labels = _.pluck(this.props.history, 'updated');

            var chartData = {
                labels: labels,
                datasets: [
                    {
                        data: data
                    }
                ]
            };
            return (
                <div>
                    <h4>Beholdningshistorikk</h4>
                    <LineChart
                        data={chartData}
                        options={{animation: false, bezierCurve: false}}
                        width="600"
                        height="200"/>
                </div>
            );
        }
    });

    var BeerOverview = React.createClass({

        getInitialState: function () {
            return {showStockHistory: false};
        },

        getHelpMsg: function () {
            var err_url = '/pol_beers/' + this.props.beer.id + '/report';
            return (
                <div className='alert alert-warning'>
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
                {name: 'Ratebeer', url: this.props.beer.ratebeer.url},
                {name: 'Vinmonopolet', url: this.props.beer.url}//,
                //{name: 'Apéritif.no', url: '#'}
            ];
        },

        gotStockHistory: function (history) {
            this.setState({
                showStockHistory: true,
                stockHistory: history
            });
        },

        toggleStockHistory: function () {

            if (this.state.showStockHistory) {
                this.setState({showStockHistory: false});
                return;
            }

            if (this.state.stockHistory) {
                this.gotStockHistory(this.state.stockHistory);
            } else {
                bd.api.getStockHistory(this.props.beer.id, this.gotStockHistory);
            }
        },

        render: function () {
            var beer = this.props.beer;
            var rbbeer = this.props.beer.ratebeer;
            var report_link = '/pol_beers/' + beer.id + '/report';

            var stockHistory;
            if (this.state.showStockHistory) {
                stockHistory = <StockHistory history={this.state.stockHistory} />
            }

            return (
                <div>
                    <h1>{rbbeer.name}</h1>

                    <p>
                        Brygget av{' '}
                        <a href={'/breweries/' + rbbeer.brewery.id}>{rbbeer.brewery.name}</a>
                        {' '}
                        (<a href={'/countries/' + rbbeer.brewery.country.rb_id}>{rbbeer.brewery.country.name}</a>)</p> 

                    <div className='row'>
                        <ScoreDisplay beer={rbbeer} />
                        <div className='col-md-4'>
                            <table className='table'>
                                <tbody>
                                    <tr>
                                        <th>Stil</th>
                                        <td>
                                            <a href={'/styles/' + rbbeer.style.id}>{rbbeer.style.name}</a>
                                        </td>
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
                                </tbody>
                            </table>
                         </div>
                         <div className='col-md-4'>
                            <table className='table'>
                                <tbody>
                                    <tr>
                                        <th>Pris</th>
                                        <td>{ns.Util.fixedOrNa(beer.price, 2)}{' '}kr</td>
                                    </tr>
                                    <tr>
                                        <th>Volum</th>
                                        <td>{ns.Util.fixedOrNa(beer.volume, 2)}{' '}l</td>
                                    </tr>
                                    <tr>
                                        <th>Butikkkatergori</th>
                                        <td>{ns.Util.valueOrNa(beer.store_category)}</td>
                                    </tr>
                                    <tr>
                                        <th>Produktutvalg</th>
                                        <td>{ns.Util.valueOrNa(beer.produktutvalg)}</td>
                                    </tr>
                                </tbody>
                            </table>
                         </div>
                         <div className='col-md-4'>
                         </div>
                    </div>

                    <ExternalLinks links={this.getExternalLinks()} />

                    <table className='table'>
                        <tbody>
                           <Characteristics beer={this.props.beer} />
                            <tr>
                                <th>Passer til</th>
                                <td>{[beer.pairs_with_1, beer.pairs_with_2, beer.pairs_with_3].join(' ')} </td>
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
                            <tr>
                                <th>Totalt antall på polet</th>
                                <td>
                                    {(beer.stock || 0).toLocaleString()} flasker/bokser
                                    {' '}<button type="button" className="btn btn-default btn-xs" onClick={this.toggleStockHistory}><i className="fa fa-area-chart"></i> Historikk</button>
                                </td>
                            </tr>
                        </tbody>
                    </table>

                    {stockHistory}

                    <ns.PolWithBeerList beerId={this.props.beer.id}/>
                    {this.getHelpMsg()}
                </div>
            );
        }
    });


    ns.renderBeerOverview = function(beer, component) {
        ReactDOM.render(<BeerOverview beer={beer} />, component);
    };

}(bd));