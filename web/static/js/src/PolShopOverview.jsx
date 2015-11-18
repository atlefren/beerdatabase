var bd = this.bd || {};
(function (ns) {
    'use strict';

    var PolShopOverview = React.createClass({

        render: function () {
            return (
                <div className='row'>
                    <h2>{this.props.shop.name}</h2>
                    <div className='six columns'>
                    </div>
                    <div className='six columns'></div>
                </div>
            );
        }

    });

    ns.renderPolShopOverview = function(polShop, component) {
        ReactDOM.render(<PolShopOverview shop={polShop} />, component);
    };

}(bd));