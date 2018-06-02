//== Class definition
var Dashboard = function () {

    //== Support Tickets Chart.
    //** Based on Morris plugin - http://morrisjs.github.io/morris.js/
    var supportTickets = function () {
        if ($('#m_chart_support_tickets').length == 0) {
            return;
        }

        Morris.Donut({
            element: 'm_chart_support_tickets',
            data: [{
                label: "Margins",
                value: 20
            },
                {
                    label: "Profit",
                    value: 70
                },
                {
                    label: "Lost",
                    value: 10
                }
            ],
            labelColor: '#a7a7c2',
            colors: [
                mUtil.getColor('accent'),
                mUtil.getColor('brand'),
                mUtil.getColor('danger')
            ]
            //formatter: function (x) { return x + "%"}
        });
    }

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

    return {
        //== Init demos
        init: function () {
            supportTickets();
            daterangepickerInit();


        }
    };
}();

//== Class initialization on page load
jQuery(document).ready(function () {
    $.ajax({
        type: 'GET',
        url: 'http://47.106.34.103:5000/profile',
        success: function (json) {
            // user_email = json.message
            // user_email='jiangtk@sb.com';
            var parsedData = json.message;
            document.getElementById('usrname').innerHTML = parsedData.user_name;
            document.getElementById('inner_usrname').innerHTML = parsedData.user_name;
            document.getElementById('inner_email').innerHTML = parsedData.user_email;
            document.getElementById('figure1').innerHTML = parsedData.num_val;
            document.getElementById('figure2').innerHTML = parsedData.num_val_tp;
            document.getElementById('figure3').innerHTML = parsedData.num_acc;
            document.getElementById('figure4').innerHTML = parsedData.user_credit;
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
    $.ajax({
        type: 'GET',
        url: 'http://47.106.34.103:5000/recent_task',
        success: function (json) {
            var temps = new Array();
            temps[0] = "info";
            temps[1] = "warning";
            temps[2] = "brand";
            temps[3] = "success";
            temps[4] = "danger";
            for (let i = 0; i < json.message.task_num; i++) {
                $("#broadcast").append(" <div class=\"m-timeline-3__item m-timeline-3__item--"+temps[i]+"\">\n" +
                    "<span class=\"m-timeline-3__item-time\">\n" +
                    json.message.tasks[i].publish_date +
                    "</span>\n" +
                    "<div class=\"m-timeline-3__item-desc\">\n" +
                    "<span class=\"m-timeline-3__item-text\">\n" +
                    json.message.tasks[i].source_name +
                    "</span><br><span class=\"m-timeline-3__item-user-name\">\n" +
                    "<a href=\"#\"\n" +
                    "class=\"m-link m-link--metal m-timeline-3__item-link\">\n" +
                    json.message.tasks[i].publisher +
                    "</a></span></div></div>");
            }
        }
    });

    Dashboard.init();
});