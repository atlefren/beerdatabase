var bd = this.bd || {};
(function (ns) {
    'use strict';

    var columns = [
        {
            id: 'name',
            name: 'Navn',
            formatter: function (country) {
                return (<a href={'/countries/' + country.iso_code}>{country.name}</a>);
            },
            sortParams: 'name',
            isSorted: false,
            sortDirection: 'asc'
        },
        {
            id: 'count',
            name: 'Antall øl på polet',
            formatter: function (country) {
                return country.count
            },
            sortParams: 'count',
            isSorted: true,
            sortDirection: 'desc'
        }
    ];

    bd.renderCountryList = function (countries, component) {
        ReactDOM.render(
            <ns.SortableTable items={countries} columns={columns} idProperty="rb_id"/>,
            component
        );
    };

}(bd));
