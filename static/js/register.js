//== Class Definition
var SnippetLogin = function () {

    var login = $('#m_login');

    var showErrorMsg = function (form, type, msg) {
        var alert = $('<div class="m-alert m-alert--outline alert alert-' + type + ' alert-dismissible" role="alert">\
			<button type="button" class="close" data-dismiss="alert" aria-label="Close"></button>\
			<span></span>\
		</div>');

        form.find('.alert').remove();
        alert.prependTo(form);
        alert.animateClass('fadeIn animated');
        alert.find('span').html(msg);
    }

    //== Private Functions

    var displaySignUpForm = function () {
        login.removeClass('m-login--forget-password');
        login.removeClass('m-login--signin');

        login.addClass('m-login--signup');
        login.find('.m-login__signup').animateClass('flipInX animated');
    }

    var displaySignInForm = function () {
        login.removeClass('m-login--forget-password');
        login.removeClass('m-login--signup');

        login.addClass('m-login--signin');
        login.find('.m-login__signin').animateClass('flipInX animated');
    }

    var displayForgetPasswordForm = function () {
        login.removeClass('m-login--signin');
        login.removeClass('m-login--signup');

        login.addClass('m-login--forget-password');
        login.find('.m-login__forget-password').animateClass('flipInX animated');
    }

    var handleFormSwitch = function () {
        $('#m_login_forget_password').click(function (e) {
            e.preventDefault();
            displayForgetPasswordForm();
        });

        $('#m_login_forget_password_cancel').click(function (e) {
            e.preventDefault();
            displaySignInForm();
        });

        $('#m_login_signup').click(function (e) {
            e.preventDefault();
            displaySignUpForm();
        });

        $('#m_login_signup_cancel').click(function (e) {
            e.preventDefault();
            displaySignInForm();
        });
    }

    var handleSignInFormSubmit = function () {
        $('#m_login_signin_submit').click(function (e) {
            e.preventDefault();
            var btn = $(this);
            var form = $(this).closest('form');

            form.validate({
                rules: {
                    email: {
                        required: true,
                        email: true
                    },
                    password: {
                        required: true
                    }
                }
            });

            if (!form.valid()) {
                return;
            }

            btn.addClass('m-loader m-loader--right m-loader--light').attr('disabled', true);

            var eMail = document.getElementById("s_email").value;

            var passWord = document.getElementById("s_password").value;

            // userName = userName.split('@')[0];

            form.ajaxSubmit({
                type: "GET",
                url: "http://47.106.34.103:5000/login/email/" + eMail + "/password/" + passWord,
                // data:{username:"11510693",password:"wangzehuai1234"},
                // success: function(response, status, xhr, $form) {
                success: function (json) {
                    // similate 2s dela
                    // alert(json.code);
                    if (json.code == 0) {
                        // alert("Welcome, someone");
                        window.location.href = "http://www.baidu.com";
                    } else {
                        setTimeout(function () {
                            btn.removeClass('m-loader m-loader--right m-loader--light').attr('disabled', false);
                            form.clearForm();
                            form.validate().resetForm();
                            // displaySignInForm();
                            var signInForm = login.find('.m-login__signup form');
                            signInForm.clearForm();
                            signInForm.validate().resetForm();
                            showErrorMsg(signInForm, 'danger', json.message);
                        }, 1000);
                    }
                }
            });
        });
    }

    var handleSignUpFormSubmit = function () {
        $('#m_login_signup_submit').click(function (e) {
            e.preventDefault();

            var btn = $(this);
            var form = $(this).closest('form');

            form.validate({
                rules: {
                    username: {
                        required: true
                    },
                    email: {
                        required: true,
                        email: true
                    },
                    password: {
                        required: true
                    },
                    rpassword: {
                        required: true
                    },
                    agree: {
                        required: true
                    }
                }
            });

            if (!form.valid()) {
                return;
            }

            btn.addClass('m-loader m-loader--right m-loader--light').attr('disabled', true);

            var uMail = document.getElementById("u_email").value;

            var uName = document.getElementById("u_name").value;

            var uPd = document.getElementById("u_password").value;

            var uPd2 = document.getElementById("u_password2").value;

            if (uPd != uPd2) {
                btn.removeClass('m-loader m-loader--right m-loader--light').attr('disabled', false);
                // form.clearForm();
                // form.validate().resetForm();
                // displaySignUpForm();
                var signUpForm = login.find('.m-login__signin form');
                // signUpForm.clearForm();
                // signUpForm.validate().resetForm();
                showErrorMsg(signUpForm, 'danger', "Different input passwords.");
                return;
            }

            form.ajaxSubmit({
                type: "GET",
                url: "http://47.106.34.103:5000/register/email/" + uMail + "/username/" + uName + "/password/" + uPd,
                success: function (json) {
                    // similate 2s delay
                    if (json.code == 0) {
                        setTimeout(function () {
                            btn.removeClass('m-loader m-loader--right m-loader--light').attr('disabled', false);
                            form.clearForm();
                            form.validate().resetForm();

                            // display signup form
                            displaySignUpForm();
                            var signInForm = login.find('.m-login__signup form');
                            signInForm.clearForm();
                            signInForm.validate().resetForm();
                            showErrorMsg(signInForm, 'info', 'Thank you. Now please sign in your account.');
                        }, 1000);
                        // window.location.href = "http://www.baidu.com";
                    } else {
                        setTimeout(function () {
                            btn.removeClass('m-loader m-loader--right m-loader--light').attr('disabled', false);
                            form.clearForm();
                            form.validate().resetForm();
                            // displaySignUpForm();
                            var signUpForm = login.find('.m-login__signin form');
                            signUpForm.clearForm();
                            signUpForm.validate().resetForm();
                            showErrorMsg(signUpForm, 'danger', json.message);
                        }, 1000);
                    }
                }
            });
        });
    }

    var handleForgetPasswordFormSubmit = function () {
        $('#m_login_forget_password_submit').click(function (e) {
            e.preventDefault();

            var btn = $(this);
            var form = $(this).closest('form');

            form.validate({
                rules: {
                    email: {
                        required: true,
                        email: true
                    }
                }
            });

            if (!form.valid()) {
                return;
            }

            var mMail = document.getElementById("m_email").value;

            btn.addClass('m-loader m-loader--right m-loader--light').attr('disabled', true);

            form.ajaxSubmit({
                url: 'http://47.106.34.103:5000/forget/email/' + mMail,
                success: function (json) {
                    if (json.code == 0) {
                        setTimeout(function () {
                            btn.removeClass('m-loader m-loader--right m-loader--light').attr('disabled', false); // remove
                            form.clearForm(); // clear form
                            form.validate().resetForm(); // reset validation states
                            // display signup form
                            displaySignUpForm();
                            var signInForm = login.find('.m-login__signup form');
                            signInForm.clearForm();
                            signInForm.validate().resetForm();
                            showErrorMsg(signInForm, 'info', 'Cool! Password recovery instruction has been sent to your email.');
                        }, 1000);
                    }else{
                        setTimeout(function () {
                            btn.removeClass('m-loader m-loader--right m-loader--light').attr('disabled', false);
                            form.clearForm();
                            form.validate().resetForm();
                            // displaySignUpForm();
                            var signUpForm = login.find('.m-login__forget-password form');
                            signUpForm.clearForm();
                            signUpForm.validate().resetForm();
                            showErrorMsg(signUpForm, 'danger', json.message);
                        }, 1000);
                    }
                }
            });
        });
    }

    //== Public Functions
    return {
        // public functions
        init: function () {
            handleFormSwitch();
            handleSignInFormSubmit();
            handleSignUpFormSubmit();
            handleForgetPasswordFormSubmit();
        }
    };
}();

//== Class Initialization
jQuery(document).ready(function () {
    SnippetLogin.init();
    // document.getElementById("m_login_signup").click();
});