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
                <div className='one column score-box'>
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
                <li className='navbar-item'>
                    <a href={this.props.link.url} className='navbar-link'>
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
                <ul className='navbar-list'>
                    {links}
                </ul>
            );
        }
    });

    var SVGComponent = React.createClass({
        render: function() {
            return (
                <svg
                    version='1.1'
                    xmlns='http://www.w3.org/2000/svg'
                    {...this.props}>
                    {this.props.children}
                </svg>
            );
        }
    });

    var Pie = React.createClass({

        getDefaultProps: function () {
            return {size: 20};
        },

        getSvg: function () {
            var size = 20;
            var value = this.props.value * 10;
            var radius  = this.props.size / 2

            if (value >= 100) {
                return (
                    <SVGComponent height={size} width={size} >
                        <circle r={radius} cx={radius} cy={radius} />
                    </SVGComponent> 
                );
            }

            var x = Math.cos((2 * Math.PI) / (100 / value));
            var y = Math.sin((2 * Math.PI) / (100 / value));

            //should the arc go the long way round?
            var longArc = (value <= 50) ? 0 : 1;

            var d = [
                'M' + radius + ' ' + radius,
                'L' + radius + ' ' + 0,
                'A' + radius + ' ' + radius,
                '0 ' + longArc,
                '1 ' + (radius + y * radius),
                (radius - x*radius),
                'z'
            ];

            d = d.join(' ');
            return (
                <SVGComponent height={size} width={size}>
                    <path d={d} />
                </SVGComponent>
            );
        },

        render: function () {
            if (!this.props.value) {
                return null;
            }
            return (
                <div className="pie">
                    <span className="label"> {this.props.name}</span>
                    {this.getSvg()}
                </div>
            );
        }

    })

    var BeerOverview = React.createClass({

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

                    <p>Brygget av{' '}<a href={'/breweries/' + rbbeer.brewery.id}>{rbbeer.brewery.name}</a></p> 

                    <div className='row'>
                        <ScoreDisplay beer={rbbeer} />
                        <div className='four columns'>
                            <table className='u-full-width'>
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
                         <div className='four columns'>
                            <table className='u-full-width'>
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
                         <div className='four columns'>
                         </div>
                    </div>

                    <ExternalLinks links={this.getExternalLinks()}/>

                    <table className='u-full-width'>
                        <tbody>
                            <tr>
                                <th>Karakteristikk</th>
                                <td>
                                    <Pie name="Sødme" value={beer.sweetness} />
                                    <Pie name="Friskhet" value={beer.freshness} />
                                    <Pie name="Bitterhet" value={beer.bitterness} />
                                    <Pie name="Fylde" value={beer.richness} />
                                </td>
                            </tr>
                            <tr>
                                <th>Passer til</th>
                                <td>{beer.pairs_with_1},{' '}{beer.pairs_with_2},{' '}{beer.pairs_with_3} </td>
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
                        </tbody>
                    </table>
                    {this.getHelpMsg()}
                </div>
            );
        }

    });


    ns.renderBeerOverview = function(beer, component) {
        ReactDOM.render(<BeerOverview beer={beer} />, component);
    };

}(bd));