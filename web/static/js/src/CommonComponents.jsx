var bd = this.bd || {};
(function (ns) {
    'use strict';

    ns.LoadIndicator = React.createClass({

        getDefaultProps: function () {
            return {text: 'Søker'}
        },

        render: function () {
            return (
                <p>
                    <i className="fa fa-spinner fa-spin fa-3x"></i>
                    {' '}
                    {this.props.text}...
                </p>
            );
        }
    });

}(bd));
