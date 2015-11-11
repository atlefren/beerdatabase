var bd = this.bd || {};
(function (ns) {
    'use strict';

    var BeerOverview = React.createClass({

        getHelpMsg: function () {
            var t = _.template('<strong>Hjelp:</strong> Dette ølet heter<strong><%= beer.name %></strong> og er brygget ' +
                    'av <strong><%= beer.producer %></strong> ifølge Vinmonopolet. Hvis dette ikke stemmer ' +
                    'kan det godt skyldes en feilmatching, fint om du kan si fra om feilen <a href="/pol_beers/<%= beer.id %>/report">her</a>.');
            return t({beer: this.props.beer});
        },

        render: function () {
            var beer = this.props.beer;
            var rbbeer = this.props.beer.ratebeer;
            var report_link = '/pol_beers/' + beer.id + '/report';

            return (
                <div>
                    <h1>{rbbeer.name}</h1>

                    <p>Brygget av {rbbeer.brewery.name}</p> 

                    <div className="row">
                        <div className="one column">
                            <div><strong>Overall</strong></div>
                            <div>{ns.Util.valueOrNa(rbbeer.score_overall)}</div>
                            <div>Style</div>
                            <div>{ns.Util.valueOrNa(rbbeer.score_style)}</div>
                        </div>
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

                    <a href="">Mer hos Ratebeer</a> 
                    <a href="">Mer hos Vinmonopolet</a> 
                    <a href="">Mer hos Apéritif.no</a>

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

                    <p>{this.getHelpMsg()}</p>
                </div>
            );
        }

    });


    ns.renderBeerOverview = function(beer, component) {
        React.render(<BeerOverview beer={beer} />, component);
    };

}(bd));