var bd = this.bd || {};
(function (ns) {
    'use strict';


    var ResultView = React.createClass({

        render: function () {

            if (this.props.searching) {
                return (
                    <ul className="list-group quicksearch-results">
                        <li className="list-group-item">
                            <i className="fa fa-spinner fa-spin"></i>&nbsp;Søker
                        </li>
                    </ul>
                );
            }
            var items = _.map(this.props.results, function (result, i) {
                var className = 'list-group-item';
                if (i === this.props.selectedIdx) {
                    className += ' active';
                }
                return (
                    <a
                        href="#"
                        className={className}
                        onClick={_.bind(function (e) {
                            e.preventDefault();
                            this.props.selectIdx(i);
                        }, this)}
                        key={result.id}>
                        {result.name}
                    </a>
                );
            }, this);
            if (this.props.searchVal && this.props.searchVal !== '') {
                var searchUrl = '/search?name=' + encodeURIComponent(this.props.searchVal);
                items.push((
                    <a
                        href={searchUrl}
                        className="list-group-item"
                        key="all">
                        Vis alle resultater
                    </a>
                ));
            }
            return (
                <div className="list-group quicksearch-results">
                    {items}
                </div>
            );
        }
    });

    var res = [
        {id: 1, name: 'test 1'},
        {id: 2, name: 'test 2'},
        {id: 3, name: 'test 3'},
        {id: 4, name: 'test 4'},
        {id: 5, name: 'test 5'},
        {id: 6, name: 'test 6'},
        {id: 7, name: 'test 7'},
        {id: 8, name: 'test 8'},
        {id: 9, name: 'test 9'},
        {id: 10, name: 'test 10'}
    ];

    function getNext(length, current) {
        if (current === length - 1) {
            return 0;
        }
        return current + 1;
    }

    function getPrev(length, current) {
        if (current === 0) {
            return length - 1;
        }
        return current - 1;
    }

    var SimpleBeerSearch = React.createClass({

        getInitialState: function () {
            return {
                searchVal: '',
                results: null,
                searching: false,
                selectedIdx: -1
            };
        },

        submit: function (e) {
            e.preventDefault();
        },

        selectIdx: function (idx) {
            this.setState({selectedIdx: idx});
            var beer = this.state.results[idx];
            window.location.href = '/pol_beers/' + beer.pol_id;
        },

        doSearch: function (value) {
            if (value === '') {
                this.gotResults([]);
            } else {
                this.setState({searching: true});
                this.props.search(value, this.gotResults);
            }
        },

        gotResults: function (results) {
            this.setState({
                results: results,
                searching: false,
                selectedIdx: -1
            });
        },

        handleChange: function (e) {
            this.setState({searchVal: e.target.value});
            this.doSearch(e.target.value);
        },

        onKeyDown: function (e) {
            if (e.which === 13 || e.which === 9) { //enter or tab
                this.selectIdx(this.state.selectedIdx);
                e.preventDefault();
            } else if (e.which === 40) { //down
                this.setState({
                    selectedIdx: getNext(this.state.results.length, this.state.selectedIdx)
                });
            } else if (e.which === 38) { //up
                this.setState({
                    selectedIdx: getPrev(this.state.results.length, this.state.selectedIdx)
                });
            }
        },

        render: function () {
            return (
                <div className="container quicksearch">
                    <form onSubmit={this.submit}>
                        <div className="input-group">
                            <input
                                value={this.state.searchVal}
                                onChange={this.handleChange}
                                onKeyDown={this.onKeyDown}
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
                    <ResultView
                        searching={this.state.searching}
                        selectIdx={this.selectIdx}
                        searchVal={this.state.searchVal}
                        selectedIdx={this.state.selectedIdx}
                        results={this.state.results} />
                </div>
            );
        }
    });

    ns.setupSimpleBeerSearch = function (container) {
        ReactDOM.render(<SimpleBeerSearch search={bd.api.autocompleteSearch} />, container);
    };
}(bd));
