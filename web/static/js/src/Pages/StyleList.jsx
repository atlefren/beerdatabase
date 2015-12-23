var bd = this.bd || {};
(function (ns) {
    'use strict';

    var columnNames = [
        'col-md-1',
        'col-md-2',
        'col-md-3',
        'col-md-4',
        'col-md-5',
        'col-md-6',
        'col-md-7',
        'col-md-8',
        'col-md-9',
        'col-md-8',
        'col-md-10',
        'col-md-11',
        'col-md-12'
    ];

    var StyleList = React.createClass({

        render: function () {
            var styles = _.map(this.props.styles, function (style) {
                var url = '/styles/' + style.id;
                return (
                    <a
                        key={style.id}
                        className="list-group-item"
                        href={url}>
                        <span className="badge">{style.count}</span>
                        {style.name}
                    </a>
                );
            });
            return (
                <div className="list-group">
                    {styles}
                </div>
            );
        }
    });


    var StyleListWrapper = React.createClass({

        getDefaultProps: function () {
            return {
                valuesPrColumn: 35
            };
        },

        render: function () {
            var numElements = this.props.styles.length;
            var valuesPrColumn = this.props.valuesPrColumn;
            var numColumns = Math.ceil(numElements / this.props.valuesPrColumn);
            var columnSize = Math.floor(12 / numColumns);

            var columnClass = columnNames[columnSize - 1];
            var columns = _.map(_.range(numColumns), function (i) {
                var start = i * valuesPrColumn;
                var stop =  start + valuesPrColumn;
                var styles = this.props.styles.slice(start, stop);
                return (
                    <div className={columnClass} key={i}>
                        <StyleList styles={styles}/>
                    </div>
                );
            }, this);

            return (<div className="row">{columns}</div>);
        }

    });

    ns.renderStyleList = function (styles, componentId, title) {
        var component = document.getElementById(componentId);
        ReactDOM.render(
            <ns.Container
                component={StyleListWrapper}
                styles={styles}
                valuesPrColumn={25}
                title={title} />,
            component
        );
    };

}(bd));
