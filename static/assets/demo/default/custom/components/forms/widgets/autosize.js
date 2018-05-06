//== Class definition

var Autosize = function () {
    
    //== Private functions
    var demos = function () {
        // basic demo
        var demo1 = $('#m_autosize_1');
        var demo2 = $('#m_autosize_2');
        var demo3 = $('#m_autosize_3');
        var demo4 = $('#m_autosize_4');
        var demo5 = $('#m_autosize_5');

        autosize(demo1);
        autosize.update(demo1);
        autosize(demo2);
        autosize.update(demo2);
        autosize(demo3);
        autosize.update(demo3);
        autosize(demo4);
        autosize.update(demo4);
        autosize(demo5);
        autosize.update(demo5);

    }

    return {
        // public functions
        init: function() {
            demos(); 
        }
    };
}();

jQuery(document).ready(function() {    
    Autosize.init();
});