//== Class definition

var DatatableRemoteAjaxDemo = function () {
    //== Private functions

    // basic demo
    var demo = function () {

        var datatable = $('.m_datatable').mDatatable({
            // datasource definition
            data: {
                type: 'remote',
                source: {
                    read: {
                        // sample GET method
                        method: 'GET',
                        url: 'http://47.106.34.103:5000/task1',
                        map: function (raw) {
                            // sample data mapping
                            //var temp = eval(raw);
                            var dataSet = raw.message.tasks;
                            // if (typeof raw.message !== 'undefined') {
                            //   dataSet = raw.message[tasks];
                            // }
                            console.log(dataSet);
                            return dataSet;
                            //return '{[{"description": "this is a test project","if_finished": 0,"number": 0,"priority": 1,"publish_date": 1527402240.0,"publisher": 1,"source_id": 11,"source_name": "test_proj"},{"description": "test_desc","if_finished": 0,"number": 1,"priority": 1,"publish_date": 1527409408.0,"publisher": 2,"source_id": 12,"source_name": "test"},{"description": "xiedn single option project","if_finished": 0,"number": 11,"priority": 2,"publish_date": 1527928320.0,"publisher": 1,"source_id": 13,"source_name": "xiednproj"}]}';
                        },
                    },
                },
                pageSize: 10,
                serverPaging: false,
                serverFiltering: false,
                serverSorting: false,
            },

            // layout definition
            layout: {
                scroll: false,
                footer: false
            },

            // column sorting
            sortable: true,

            pagination: true,

            toolbar: {
                // toolbar items
                items: {
                    // pagination
                    pagination: {
                        // page size select
                        pageSizeSelect: [10, 20, 30, 50, 100],
                    },
                },
            },

            search: {
                input: $('#generalSearch'),
            },

            // columns definition
            columns: [
                {
                    field: 'source_id',
                    title: 'Data ID',
                    // sortable: 'asc', // default sort
                    filterable: false, // disable or enable filtering
                    width: 150,
                    // basic templating support for column rendering,
                    //template: '{{source_id}} - {{source_name}}',
                }, {
                    field: 'source_name',
                    title: 'Data Name',
                    width: 150,
                }, {
                    field: 'publisher',
                    title: 'Uploader',
                }, {
                    field: 'publish_date',
                    title: 'Upload Time',
                    type: 'date',
                    // format: 'MM/DD/YYYY',
                }, {
                    field: 'number',
                    title: 'Percentage',
                    type: 'number',
                }, {
                    field: 'if_finished',
                    title: 'Status',
                    // callback function support for column rendering
                    template: function (row) {
                        var status = {
                            1: {'title': 'Done', 'class': 'm-badge--brand'},
                            2: {'title': 'Labeling', 'class': ' m-badge--metal'},
                            0: {'title': 'New', 'class': ' m-badge--primary'},
                        };
                        if (row.if_finished < 1 && row.if_finished > 0) {
                            return '<span class="m-badge ' + status[2].class +
                                ' m-badge--wide">' + status[2].title + '</span>';
                        }
                        return '<span class="m-badge ' + status[row.if_finished].class +
                            ' m-badge--wide">' + status[row.if_finished].title + '</span>';
                    },
                }, {
                    field: 'priority',
                    title: 'Priority',
                    // callback function support for column rendering
                    template: function (row) {
                        var status = {
                            1: {'title': 'III.Low', 'state': 'success'},
                            2: {'title': 'II.Normal', 'state': 'warning'},
                            3: {'title': 'I.High', 'state': 'danger'},
                        };
                        return '<span class="m-badge m-badge--' + status[row.priority].state + ' m-badge--dot"></span>&nbsp;<span class="m--font-bold m--font-' + status[row.priority].state + '">' + status[row.priority].title + '</span>';
                    },
                }, {
                    field: 'Actions',
                    width: 110,
                    title: 'Label',
                    sortable: false,
                    overflow: 'visible',
                    template: function (row, index, datatable) {
                        var dropup = (datatable.getPageSize() - index) <= 4 ? 'dropup' : '';
                        return '\
            <div>\
						<a href="textlabel.html" class="m-portlet__nav-link btn m-btn m-btn--hover-info m-btn--icon m-btn--icon-only m-btn--pill" title="Edit details">\
							<i class="la la-edit"></i>\
						</a>\
						</div>\
					';
                    },
                }],
        });

        $('#m_form_status').on('change', function () {
            datatable.search($(this).val().toLowerCase(), 'Status');
        });

        $('#m_form_type').on('change', function () {
            datatable.search($(this).val().toLowerCase(), 'Type');
        });

        $('#m_form_status, #m_form_type').selectpicker();

    };

    return {
        // public functions
        init: function () {
            demo();
        },
    };


}();

jQuery(document).ready(function () {
    $.ajax({
        type: 'GET',
        url: 'http://47.106.34.103:5000/profile',
        success: function (json) {
            var parsedData = json.message;
            document.getElementById('usrname').innerHTML = parsedData.user_name;
            document.getElementById('inner_usrname').innerHTML = parsedData.user_name;
            document.getElementById('inner_email').innerHTML = parsedData.user_email;
            // $.ajax({
            //     type: 'GET',
            //     url: 'http://47.106.34.103:5000/profile/' + user_email,
            //     success: function (json) {
            //         var parsedData = json.message;
            //         document.getElementById('usrname').innerHTML = parsedData.user_name;
            //         document.getElementById('inner_usrname').innerHTML = parsedData.user_name;
            //         document.getElementById('inner_email').innerHTML = parsedData.user_email;
            //         document.getElementById('figure1').innerHTML = parsedData.num_val;
            //         document.getElementById('figure2').innerHTML = parsedData.num_val_tp;
            //         document.getElementById('figure3').innerHTML = parsedData.num_acc;
            //         document.getElementById('figure4').innerHTML = parsedData.user_credit;
            //     }
            // });
        }
    });
    DatatableRemoteAjaxDemo.init();
});