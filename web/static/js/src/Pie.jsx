var bd = this.bd || {};
(function (ns) {
    'use strict';

    var SVGComponent = React.createClass({
        render: function() {
            return (
                <svg
                    version='1.1'
                    xmlns='http://www.w3.org/2000/svg'
                    {...this.props}>
                    {this.props.children}
                </svg>
            );
        }
    });

    ns.Pie = React.createClass({

        getDefaultProps: function () {
            return {size: 20};
        },

        getSvg: function () {
            var size = 20;
            var value = this.props.value * 10;
            var radius  = this.props.size / 2

            if (value >= 100) {
                return (
                    <SVGComponent height={size} width={size} >
                        <circle r={radius} cx={radius} cy={radius} />
                    </SVGComponent> 
                );
            }

            var x = Math.cos((2 * Math.PI) / (100 / value));
            var y = Math.sin((2 * Math.PI) / (100 / value));

            //should the arc go the long way round?
            var longArc = (value <= 50) ? 0 : 1;

            var d = [
                'M' + radius + ' ' + radius,
                'L' + radius + ' ' + 0,
                'A' + radius + ' ' + radius,
                '0 ' + longArc,
                '1 ' + (radius + y * radius),
                (radius - x*radius),
                'z'
            ];

            d = d.join(' ');
            return (
                <SVGComponent height={size} width={size}>
                    <path d={d} />
                </SVGComponent>
            );
        },

        render: function () {
            if (!this.props.value) {
                return null;
            }
            return (
                <div className="pie">
                    <span> {this.props.name}</span>
                    {this.getSvg()}
                </div>
            );
        }
    });

}(bd));
