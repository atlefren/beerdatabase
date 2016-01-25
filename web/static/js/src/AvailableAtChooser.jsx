/*
    var CheckboxComponent = React.createClass({

        getInitialState: function () {
            return {checked: this.props.selected};
        },

        toggle: function (e) {
            var checked = e.target.checked;
            this.setState({checked: checked});
            this.props.onChange(this.props.type, checked);
        },

        render: function () {
            return (
                <div className="checkbox">
                    <label>
                        <input
                            type="checkbox"
                            onChange={this.toggle}
                            checked={this.state.checked} />
                        {' '}
                        {this.props.name}
                    </label>
                </div>
            );
        }
    });

    var AvailableAtChooser = React.createClass({

        getDefaultProps: function () {
            var options = [
                {name: 'Polet', key: 'polet'},
                {name: 'Gulating', key: 'gulating'}
            ];
            return {options: options, value: []};
        },

        getInitialState: function () {
            var initValue = this.props.value;
            var selected = _.chain(this.props.options)
                .filter(function (option) {
                    return (initValue.indexOf(option.key) !== -1);
                })
                .map(function (option) {
                    return option.key;
                })
                .value();
            return {selected: selected};
        },

        onChange: function (key, selected) {
            var prevSelected = _.clone(this.state.selected);
            var index = prevSelected.indexOf(key);

            if (selected && index === -1) {
                prevSelected.push(key);
            }
            if (!selected && index > -1) {
                prevSelected.splice(index, 1);
            }
            this.setState({selected: prevSelected});

            this.props.changed(this.props.type, prevSelected);
        },

        render: function () {

            var checkboxes = _.map(this.props.options, function (option) {
                var selected = this.state.selected.indexOf(option.key) !== -1;
                return (
                    <CheckboxComponent
                        onChange={this.onChange}
                        name={option.name}
                        type={option.key}
                        key={option.key}
                        selected={selected} />
                    );
            }, this);

            return (
                <fieldset>
                    <legend>Tilgjengelig på</legend>
                    {checkboxes}
                </fieldset>
            );
        }
    });
*/
