var bd = this.bd || {};
(function (ns) {
    'use strict';

    var columnNames = [
        'one column',
        'two columns',
        'three columns',
        'four columns',
        'five columns',
        'six columns',
        'seven columns',
        'eight columns',
        'nine columns',
        'ten columns',
        'eleven columns',
        'twelve columns'
    ];

    var StyleList = React.createClass({

        render: function () {
            var styles = _.map(this.props.styles, function (style) {
                var url = '/styles/' + style.id;
                return (
                    <li key={style.id}>
                        <a href={url}>{style.name}</a>
                    </li>
                );
            })
            return (<ul>{styles}</ul>);
        }
    })


    var StyleListWrapper = React.createClass({

        getDefaultProps: function() {
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

    ns.renderStyleList = function(styles, component) {
        ReactDOM.render(<StyleListWrapper styles={styles} valuesPrColumn={25}/>, component);
    };

}(bd));