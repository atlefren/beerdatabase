var bd = this.bd || {};
(function (ns) {
    'use strict';

    var UnmatchedPage = React.createClass({

        render: function () {
            return (
                <div>
                    <div className='alert alert-warning'>
                        <strong>Hjelp:</strong>
                        <p>Disse ølene fra Vinmopoltets lister har vi ikke klart å automatisk matche
                        med noen øl fra Ratebeer. Hvis du tror du kan hjelpe til, klikk på 
                        ølnavnet, så kan du søke i Ratebeer-databasen og foreslå en match. Takk!
                        </p>
                    </div>
                    <ns.SortableTable
                        items={this.props.beers}
                        columns={this.props.columns} />
                </div>
            );
        }
    });


    ns.renderUnmatchedPolBeersPage  = function (beers, componentId) {
        var component = document.getElementById(componentId);
        var columns  =  ns.getColumnsForTable(['name', 'brewery', 'num_unmatched']);
        ReactDOM.render(
            <ns.Container
                component={UnmatchedPage}
                beers={beers}
                columns={columns}
                title="Umatcha øl" />,
            component
        );
    };
}(bd));
