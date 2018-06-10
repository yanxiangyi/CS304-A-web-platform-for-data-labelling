//== Class definition
var WizardDemo = function () {
    //== Base elements
    var wizardEl = $('#m_wizard');
    var formEl = $('#m_form');
    var validator;
    var wizard;

    //== Private functions
    var initWizard = function () {
        //== Initialize form wizard
        wizard = wizardEl.mWizard({
            startStep: 1
        });

        //== Validation before going to next page
        wizard.on('beforeNext', function (wizard) {
            if (validator.form() !== true) {
                return false;  // don't go to the next step
            }
        })

        //== Change event
        wizard.on('change', function (wizard) {
            mApp.scrollTop();
        });
    }

    var initValidation = function () {
        validator = formEl.validate({
            //== Validate only visible fields
            ignore: ":hidden",

            //== Validation rules
            rules: {
                //=== Client Information(step 1)
                //== Client details
                name: {
                    required: true
                },
                //=== Client Information(step 2)
                //== Account Details
                file: {
                    required: true,
                },
                docs: {
                    required: true,
                },
                //=== Confirmation(step 4)
                accept: {
                    required: true
                }
            },

            //== Validation messages
            messages: {
                'account_communication[]': {
                    required: 'You must select at least one communication option'
                },
                accept: {
                    required: "You must accept the Terms and Conditions agreement!"
                }
            },

            //== Display error  
            invalidHandler: function (event, validator) {
                mApp.scrollTop();

                swal({
                    "title": "",
                    "text": "There are some errors in your submission. Please correct them.",
                    "type": "error",
                    "confirmButtonClass": "btn btn-secondary m-btn m-btn--wide"
                });
            },

            //== Submit valid form
            submitHandler: function (form) {

            }
        });
    }

    var initSubmit = function () {

        var btn = formEl.find('[data-wizard-action="submit"]');

        btn.on('click', function (e) {
            e.preventDefault();
            // alert(20);
            if (validator.form()) {
                //== See: src\js\framework\base\app.js
                mApp.progress(btn);
                //mApp.block(formEl); 

                //== See: http://malsup.com/jquery/form/#ajaxSubmit
                formEl.ajaxSubmit({

                    success: function () {
                        mApp.unprogress(btn);
                        //mApp.unblock(formEl);

                        swal({
                            "title": "",
                            "text": "The application has been successfully submitted!",
                            "type": "success",
                            "confirmButtonClass": "btn btn-secondary m-btn m-btn--wide"
                        });

                        setTimeout(function () {
                            window.location.href = history.back();
                        }, 2000);

                    }

                });
            }
            setTimeout(function () {
                window.location.href = history.back();
            }, 2000);
        });
    }

    return {
        // public functions
        init: function () {
            wizardEl = $('#m_wizard');
            formEl = $('#m_form');
            initWizard();
            initValidation();
            initSubmit();
        }
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
            document.getElementById('updater').innerHTML = parsedData.user_email;
        }
    });
    WizardDemo.init();
});