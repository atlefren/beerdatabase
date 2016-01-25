var bd = this.bd || {};
(function (ns) {
    'use strict';

    var columns = ns.getColumnsForTable(['name', 'brewery', 'rating', 'abv', 'price']);

    var StylePage = React.createClass({

        getNumBeerText: function () {
            if (this.props.beers.length) {
                return (
                    <p>
                        Det er pr nå registrert{' '}{this.props.beers.length}{' '}øl{' '}
                        av stilen{' '}{this.props.style.name}{' '}hos Vinmonopolet.
                    </p>
                );
            }
            return (
                <p>
                    Det er pr nå ikke registrert noen øl
                    av stilen{' '}{this.props.style.name}{' '}hos Vinmonopolet.
                </p>
            );
        },

        render: function () {

            var beerTable;
            if (this.props.beers.length) {
                beerTable = (
                    <ns.SortableTable
                        items={this.props.beers}
                        columns={columns} />
                );
            }

            return (
                <div>
                    {this.getNumBeerText()}
                    {beerTable}
                </div>
            );
        }
    });

    ns.renderStylePage = function (data, componentId, title) {
        var component = document.getElementById(componentId);
        ReactDOM.render(
            <ns.Container
                component={StylePage}
                style={data.style}
                beers={data.beers}
                title={title} />,
            component
        );
    };


}(bd));
