jQuery(document).ready(function () {
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
})
;