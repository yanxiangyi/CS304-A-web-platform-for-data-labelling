//== Class definition
var Dashboard = function () {

    //== Support Tickets Chart.
    //** Based on Morris plugin - http://morrisjs.github.io/morris.js/
    var supportTickets = function () {
        if ($('#m_chart_support_tickets').length == 0) {
            return;
        }

        $.ajax({
            type: 'GET',
            url: 'http://47.106.34.103:5000/pan',
            success: function (json) {
                var parsedData = json.message;
                Morris.Donut({
                    element: 'm_chart_support_tickets',
                    data: [{
                        label: "High",
                        value: parsedData["1"]
                    }, {
                        label: "Mid",
                        value: parsedData["2"]
                    }, {
                        label: "Low",
                        value: parsedData["3"]
                    }],
                    labelColor: '#a7a7c2',
                    colors: [
                        mUtil.getColor('success'),
                        mUtil.getColor('info'),
                        mUtil.getColor('danger')
                    ]
                    //formatter: function (x) { return x + "%"}
                });
            }
        });

    }

    var daterangepickerInit = function () {
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
            var parsedData = json.message;
            document.getElementById('figure1').innerHTML = parsedData.num_answer;
            document.getElementById('figure2').innerHTML = parsedData.num_val_tp;
            document.getElementById('figure3').innerHTML = parsedData.num_acc;
            document.getElementById('figure4').innerHTML = parsedData.user_credit;
            document.getElementById('progress1').style.width = (parsedData.percentage_involved * 100).toFixed(2) + "%";
            document.getElementById('show_progress1').innerHTML = (parsedData.percentage_involved * 100).toFixed(2) + "%";
            var temp2 = "0%";
            if (parsedData.num_val_tp != 0) {
                temp2 = ((parsedData.num_val_tp / parsedData.num_val) * 100).toFixed(2) + "%";
            }
            document.getElementById('progress2').style.width = temp2;
            document.getElementById('show_progress2').innerHTML = temp2;
            var temp3 = "0%";
            if (parsedData.num_acc != 0) {
                temp3 = ((parsedData.num_acc / parsedData.num_answer) * 100).toFixed(2) + "%";
            }
            document.getElementById('progress3').style.width = temp3;
            document.getElementById('show_progress3').innerHTML = temp3;
            document.getElementById('progress4').style.width = (parsedData.rank * 100).toFixed(2) + "%";
            document.getElementById('show_progress4').innerHTML = (parsedData.rank * 100).toFixed(2) + "%";

        }
    });
    $.ajax({
        type: 'GET',
        url: 'http://47.106.34.103:5000/pan_history',
        success: function (json) {
            var parsedData = json.message;
            document.getElementById('l1').innerHTML = parsedData[0];
            document.getElementById('l2').innerHTML = parsedData[1];
            document.getElementById('l3').innerHTML = parsedData[2];
            document.getElementById('l4').innerHTML = parsedData[3];
            document.getElementById('l5').innerHTML = parsedData[4];
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
            var tol_num = json.message.task_num;
            if (tol_num > 5) {
                tol_num = 5;
            }
            for (let i = 0; i < tol_num; i++) {
                $("#broadcast").append(" <div class=\"m-timeline-3__item m-timeline-3__item--" + temps[i] + "\">\n" +
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