var bd = this.bd || {};
(function (ns) {
    'use strict';

    function getFromArr(arr, idx, fallback) {
        if (_.isUndefined(arr)) {
            return fallback;
        }
        var val = arr[idx];
        if (!_.isUndefined(val)) {
            return val;
        }
        return fallback;
    }

    var Slider = React.createClass({

        getInitialState: function () {
            return {
                min: this.props.min,
                max: this.props.max
            };
        },

        componentDidMount: function () {
            var element = ReactDOM.findDOMNode(this);
            noUiSlider.create(element, {
                start: [this.props.initMin, this.props.initMax],
                connect: true,
                step: this.props.step,
                range: {
                    min: this.props.min,
                    max: this.props.max
                }
            });

            element.noUiSlider.on('update', this.sliderChanged);
        },

        sliderChanged: function (values, handle) {
            var min = parseFloat(values[0]);
            var max = parseFloat(values[1]);
            if (min !== this.state.min || max !== this.state.max) {
                this.setState({min: min, max: max});
                this.props.change(min, max);
            }
        },

        render: function () {
            return (<div className="slider noUi-extended" />);
        }
    });

    ns.SliderFormGroup = React.createClass({

        getDefaultProps: function () {
            return {
                min: 0,
                max: 100,
                step: 1,
                displayPostfix: ''
            };
        },

        sliderChanged: function (min, max) {
            if (this.props.changed) {
                this.props.changed(this.props.type, [min, max]);
            }
        },

        getValues: function () {
            var min = this.props.min;
            var max = this.props.max;
            if (this.props.value && this.props.value.length === 2) {
                min = this.props.value[0];
                max = this.props.value[1];
            }
            if (this.props.step < 1 && this.min) {
                min = min.toFixed(1);
                max = max.toFixed(1);
            }
            return {min: min, max: max};
        },

        render: function () {
            var values = this.getValues();
            var min = values.min;
            var max = values.max;

            var label;
            if (this.props.label) {
                label = (<label>{this.props.label}</label>);
            }
            return (
                <div className="form-group">
                    {label}
                    <div>
                        <div>
                            {min}{this.props.displayPostfix} {' '}
                            til {' '} {max}{this.props.displayPostfix}
                        </div>
                        <Slider
                            {...this.props}
                            initMin={getFromArr(this.props.value, 0, this.props.min)}
                            initMax={getFromArr(this.props.value, 1, this.props.max)}
                            change={this.sliderChanged} />
                    </div>
                </div>
            );
        }
    });
}(bd));
