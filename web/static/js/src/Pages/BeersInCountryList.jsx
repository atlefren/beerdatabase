var bd = this.bd || {};
(function (ns) {
    'use strict';

    var CountryDetail = React.createClass({
        render: function () {
            return (
                <div>
                </div>
            );
        }
    });

    bd.renderBeersInCountryList = function (data, componentId, title) {
        var component = document.getElementById(componentId);

        var columnIds = ['name', 'brewery', 'style', 'rating', 'abv', 'price'];
        var columnsForTable = ns.getColumnsForTable(columnIds);

        ReactDOM.render(
            <ns.Container
                component={ns.SortableTable}
                items={data.beers}
                columns={columnsForTable}
                title={title} />,
            component
        );
    };

}(bd));
