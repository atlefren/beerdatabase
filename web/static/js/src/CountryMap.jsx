var bd = this.bd || {};
(function (ns) {
    'use strict';

    var d3map = {};
    d3map.create = function (el, props, state) {

        var projection = d3.geo.naturalEarth()
            .scale(125)
            .translate([280, 400 / 2])
            .precision(.1);

        var svg = d3.select(el)
           .append('div')
           .classed('svg-container', true)
           .append('svg')
           .attr('preserveAspectRatio', 'xMinYMin meet')
           .attr('viewBox', '0 0 600 400')
           .classed('svg-content-responsive', true); 

        var path = d3.geo.path().projection(projection);
        var g = svg.append('g')
            .selectAll('path')
            .data(props.allCountries)
            .enter()
            .append('path')
            .attr('d', path)
            .style('fill', 'grey')
            .style('stroke', 'grey');

        var scale = d3.scale.quantize().domain(props.range).range(props.colors);

        var getColor = function (d) {
            return scale(d.properties.count);
        };

        var g = svg.append('g')
            .selectAll('path')
            .data(props.countriesWithBreweries)
            .enter()
            .append('path')
            .on('click', props.clicked)
            .attr('d', path)
            .style('fill', getColor)
            .style('stroke', getColor);
    };

    d3map.update = function (el, state) {};
    d3map.destroy = function (el) {};


    ns.CountryMap = React.createClass({

        getDefaultProps: function () {
            return {
                colors: [
                    '#c6dbef',
                    '#9ecae1',
                    '#6baed6',
                    '#4292c6',
                    '#2171b5',
                    '#08519c',
                    '#08306b'
                ]
            };
        },

        componentDidMount: function () {
            var el = ReactDOM.findDOMNode(this);
            d3map.create(el, this.props, this.getMapState());
        },

        componentDidUpdate: function () {
            var el = ReactDOM.findDOMNode(this);
            d3map.update(el, this.getMapState());
        },

        getMapState: function () {
            return {};
        },

        componentWillUnmount: function () {
            var el = ReactDOM.findDOMNode(this);
            d3map.destroy(el);
        },

        render: function () {
            return (
              <div className="d3map"></div>
            );
        }
    });
}(bd));
