var bd = this.bd || {};
(function (ns) {

    var BeerRow = React.createClass({
        render: function () {
            var beerLink = '/pol_beer/' + this.props.beer.id;
            return (
                <tr>
                    <td><a href={beerLink}>{this.props.beer.name}</a></td>
                    <td>{this.props.beer.producer}</td>
                    <td>-</td>
                    <td>-</td>
                    <td>-</td>
                </tr>
            );
        }
    });

    var BeerRowRatebeer = React.createClass({
        render: function () {
            var rb = this.props.beer.ratebeer;
            var beerLink = '/pol_beer/' + this.props.beer.id;
            var score;
            if (rb.score_overall && rb.score_style) {
                score = rb.score_overall + ' (' + rb.score_style + ')';
            }
            return (
                <tr>
                    <td><a href={beerLink}>{rb.name}</a></td>
                    <td>{rb.brewery.name}</td>
                    <td>{rb.style.name}</td>
                    <td>{score}</td>
                    <td>{rb.abv}%</td>
                </tr>
            );
        }
    });

    var BeerTable = React.createClass({

        render: function () {

            var rows = _.map(this.props.beers, function (beer) {
                if (beer.ratebeer) {
                    return (<BeerRowRatebeer beer={beer} />);
                }
                return (<BeerRow beer={beer} />);
            });

            return (
                <table className="u-full-width">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Brewery</th>
                            <th>Style</th>
                            <th>Score</th>
                            <th>Abv</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows}
                    </tbody>
                </table>
            )
        }
    });


    ns.renderPolBeerTable = function(beerList, component) {
        console.log(beerList);
        React.render(<BeerTable beers={beerList} />, component);
    }

}(bd));