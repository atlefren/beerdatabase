var bd = this.bd || {};
(function (ns) {
    'use strict';

    var columns = ns.getColumnsForTable(['name', 'style', 'rating', 'abv', 'price']);

    var BreweryPage = React.createClass({

        getNumBeerText: function () {
            if (this.props.beers.length) {
                return (
                    <p>
                        Det er pr nå registrert {this.props.beers.length} øl{' '}
                        fra {this.props.brewery.name} hos Vinmonopolet.
                    </p>
                );
            }
            return (
                <p>
                    Det er pr nå ikke registrert noen øl fra {' '}
                    {this.props.brewery.name} hos Vinmonopolet.
                </p>
            );
        },

        render: function () {

            var beerTable;
            if (this.props.beers.length) {
                beerTable = (
                    <ns.SortableTable
                        items={this.props.beers}
                        filterable={true}
                        columns={columns} />
                );
            }

            return (
                <div>
                    <p>
                        Fra <a href={'/countries/' + this.props.brewery.country.rb_id}>
                            {this.props.brewery.country.name}
                        </a>
                    </p>
                    {this.getNumBeerText()}
                    {beerTable}
                </div>
            );
        }
    });

    ns.renderBreweryPage = function (data, componentId, title) {
        var component = document.getElementById(componentId);
        ReactDOM.render(
            <ns.Container
                component={BreweryPage}
                brewery={data.brewery}
                beers={data.beers}
                title={title} />,
            component
        );
    };

}(bd));
