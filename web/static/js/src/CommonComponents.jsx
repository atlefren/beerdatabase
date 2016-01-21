var bd = this.bd || {};
(function (ns) {
    'use strict';

    ns.LoadIndicator = React.createClass({

        getDefaultProps: function () {
            return {text: 'Søker'};
        },

        render: function () {
            return (
                <p>
                    <i className="fa fa-spinner fa-spin fa-3x"></i>
                    <br />
                    {this.props.text}...
                </p>
            );
        }
    });

    ns.Container = React.createClass({
        render: function () {
            var componentProps = _.omit(this.props, 'component', 'title');
            var Component = this.props.component;

            return (
                <div>
                    <h1>{this.props.title}</h1>
                    <Component {...componentProps} />
                </div>
            );
        }
    });

}(bd));
