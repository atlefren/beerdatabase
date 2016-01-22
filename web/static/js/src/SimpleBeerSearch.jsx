var bd = this.bd || {};
(function (ns) {
    'use strict';

    var SimpleBeerSearch = React.createClass({

        getInitialState: function () {
            return {searchVal: ''};
        },

        submit: function (e) {
            e.preventDefault();
            //TODO: show a dropdown instead
            window.location.href = '/search?name=' + encodeURIComponent(this.state.searchVal);
        },

        handleChange: function (e) {
            this.setState({searchVal: e.target.value});
        },

        render: function () {
            return (
                <div className="container quicksearch">
                    <form onSubmit={this.submit}>
                        <div className="input-group">
                            <input
                                value={this.state.searchVal}
                                onChange={this.handleChange}
                                type="text"
                                className="form-control"
                                placeholder="Søk etter øl" />
                            <span className="input-group-btn">
                                <button className="btn btn-default" type="submit">
                                    <span className="glyphicon glyphicon-search" aria-hidden="true"></span>
                                </button>
                            </span>
                        </div>
                    </form>
                </div>
            );
        }
    });

    ns.setupSimpleBeerSearch = function (container) {
        ReactDOM.render(<SimpleBeerSearch />, container);
    };
}(bd));
