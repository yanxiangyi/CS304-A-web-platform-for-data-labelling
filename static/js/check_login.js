jQuery(document).ready(function () {
    $.ajax({
        type: 'GET',
        url: 'http://47.106.34.103:5000/profile',
        success: function (json) {
            if(json.code === 1){
                swal({
                    title: json.message,
                    text: 'Jump to mainpage in 5 seconds.',
                    timer: 5000,
                    onOpen: function() {
                        swal.showLoading()
                    }
                }).then(function(result) {
                    if (result.dismiss === 'timer') {
                        console.log('I was closed by the timer')
                    }
                })
            }else{
                var parsedData = json.message;
                document.getElementById('usrname').innerHTML = parsedData.user_name;
                document.getElementById('inner_usrname').innerHTML = parsedData.user_name;
                document.getElementById('inner_email').innerHTML = parsedData.user_email;
            }
        }
    });
});