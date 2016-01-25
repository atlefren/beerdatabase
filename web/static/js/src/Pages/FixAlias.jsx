var bd = this.bd || {};
(function (ns) {
    'use strict';

    var AliasFixer = React.createClass({
        render: function () {
            return (<p>Kommer snart!</p>);
        }
    });

    ns.renderAliasFixer = function (data, componentId) {
        var component = document.getElementById(componentId);

        ReactDOM.render(
            <ns.Container
                component={AliasFixer}
                rb_beer={data}
                title={'Fiks ølmatching'} />,
            component
        );
    };

}(bd));

