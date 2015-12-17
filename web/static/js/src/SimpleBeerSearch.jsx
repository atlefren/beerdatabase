var bd = this.bd || {};
(function (ns) {
    'use strict';

    var SimpleBeerSearch = React.createClass({

        selectBeer: function (beer) {
            window.location.href = '/beers/' + beer.id;
        },

        render: function () {
            return (
                <ns.Autocomplete 
                    placeholder="Finn øl"
                    autocompleteSearch={ns.api.searchBeer}
                    select={this.selectBeer} />
            );
        }
    });

    ns.setupSimpleBeerSearch = function (container) {
        ReactDOM.render(<SimpleBeerSearch />, container);
    };
}(bd));
