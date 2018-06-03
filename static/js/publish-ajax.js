//== Class definition

var DatatableRemoteAjaxDemo = function() {
    //== Private functions

    var daterangepickerInit = function () {

        if ($('#m_dashboard_daterangepicker').length == 0) {
            return;
        }

        var picker = $('#m_dashboard_daterangepicker');
        var start = moment();
        var end = moment();

        function cb(start, end, label) {
            var title = '';
            var range = '';

            if ((end - start) < 100) {
                title = 'Today:';
                range = start.format('MMM D');
            } else if (label == 'Yesterday') {
                title = 'Yesterday:';
                range = start.format('MMM D');
            } else {
                range = start.format('MMM D') + ' - ' + end.format('MMM D');
            }

            picker.find('.m-subheader__daterange-date').html(range);
            picker.find('.m-subheader__daterange-title').html(title);
        }

        picker.daterangepicker({
            startDate: start,
            endDate: end,
            opens: 'left',
            ranges: {
                'Today': [moment(), moment()],
                // 'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
                // 'Last 7 Days': [moment().subtract(6, 'days'), moment()],
                // 'Last 30 Days': [moment().subtract(29, 'days'), moment()],
                // 'This Month': [moment().startOf('month'), moment().endOf('month')],
                // 'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
            }
        }, cb);

        cb(start, end, '');
    }

    // basic demo
    var demo = function() {

        var datatable = $('.m_datatable').mDatatable({
            // datasource definition
            data: {
                type: 'remote',
                source: {
                    read: {
                        // sample GET method
                        method: 'GET',
                        url: 'http://47.106.34.103:5000/task',
                        map: function(raw) {
                            // sample data mapping
                            //var temp = eval(raw);
                            var dataSet = raw.message.tasks;
                            // if (typeof raw.message !== 'undefined') {
                            //   dataSet = raw.message[tasks];
                            // }
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
                    title: 'Task ID',
                    // sortable: 'asc', // default sort
                    filterable: false, // disable or enable filtering
                    width: 100,
                    // basic templating support for column rendering,
                    //template: '{{source_id}} - {{source_name}}',
                }, {
                    field: 'source_name',
                    title: 'Data Name',
                    width: 200,
                }, {
                    field: 'publisher',
                    title: 'Uploader',
                }, {
                    field: 'publish_date',
                    title: 'Upload Time',
                    type: 'date',
                    template: function (row) {
                        var date = new Date(row.publish_date * 1000);//如果date为13位不需要乘1000
                        var Y = date.getFullYear() + '-';
                        var M = (date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1) + '-';
                        var D = (date.getDate() < 10 ? '0' + (date.getDate()) : date.getDate()) + ' ';
                        var h = (date.getHours() < 10 ? '0' + date.getHours() : date.getHours()) + ':';
                        var m = (date.getMinutes() < 10 ? '0' + date.getMinutes() : date.getMinutes()) + ':';
                        var s = (date.getSeconds() < 10 ? '0' + date.getSeconds() : date.getSeconds());
                        return Y + M + D + h + m + s;

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
                    field: 'num_finished',
                    title: 'Status',
                    // callback function support for column rendering
                    template: function (row) {
                        var status = {
                            1: {'title': 'Done', 'class': 'm-badge--brand'},
                            2: {'title': 'Labeling', 'class': ' m-badge--metal'},
                            0: {'title': 'New', 'class': ' m-badge--primary'},
                        };
                        var finish = row.num_finished / row.number;
                        if (finish < 1 && finish > 0) {
                            return '<span class="m-badge ' + status[2].class +
                                ' m-badge--wide">' + status[2].title + '</span>';
                        }
                        return '<span class="m-badge ' + status[finish].class +
                            ' m-badge--wide">' + status[finish].title + '</span>';
                    },
                }, {
                    field: 'number',
                    title: 'Percentage',
                    template: function (row) {
                        var finish = row.num_finished / row.number;
                        return finish + '%';
                    },
                }],
        });

        $('#m_form_status').on('change', function() {
            datatable.search($(this).val().toLowerCase(), 'Status');
        });

        $('#m_form_type').on('change', function() {
            datatable.search($(this).val().toLowerCase(), 'Type');
        });

        $('#m_form_status, #m_form_type').selectpicker();

    };

    return {
        // public functions
        init: function() {
            daterangepickerInit();
            demo();
        },
    };
}();

jQuery(document).ready(function() {
    $.ajax({
        type: 'GET',
        url: 'http://47.106.34.103:5000/profile',
        success: function (json) {
            var parsedData = json.message;
            document.getElementById('usrname').innerHTML = parsedData.user_name;
            document.getElementById('inner_usrname').innerHTML = parsedData.user_name;
            document.getElementById('inner_email').innerHTML = parsedData.user_email;
        }
    });
    DatatableRemoteAjaxDemo.init();
});