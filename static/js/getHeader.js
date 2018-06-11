jQuery(document).ready(function () {
    $.ajax({
        type: 'GET',
        url: 'http://47.106.34.103:5000/profile',
        success: function (json) {
            // alert(json.code);
            if (json.code == 0) {
                // if (1 == 1) {
                var aa = json.message.user_name;
                var bb = json.message.user_email;
                $("#headerRef").append("<div class=\"m-stack__item m-topbar__nav-wrapper\">\n" +
                    "                        <ul class=\"m-topbar__nav m-nav m-nav--inline\">\n" +
                    "                            <!--Hello profile-->\n" +
                    "                            <li class=\"m-nav__item m-topbar__user-profile m-topbar__user-profile--img  m-dropdown\n" +
                    "                             m-dropdown--medium m-dropdown--arrow m-dropdown--header-bg-fill m-dropdown--align-right\n" +
                    "                              m-dropdown--mobile-full-width m-dropdown--skin-light\"\n" +
                    "                                data-dropdown-toggle=\"click\">\n" +
                    "                                <!--user-->\n" +
                    "                                <a href=\"#\" class=\"m-nav__link m-dropdown__toggle header__references_support\">\n" +
                    "\t\t\t\t\t\t\t\t\t\t\t\t\t<span class=\"m-topbar__userpic m--hide\">\n" +
                    "\t\t\t\t\t\t\t\t\t\t\t\t\t\t<img src=\"../static/img/user4.jpg\"\n" +
                    "                                                             class=\"m--img-rounded m--marginless m--img-centered\"\n" +
                    "                                                             alt=\"\"/>\n" +
                    "\t\t\t\t\t\t\t\t\t\t\t\t\t</span>\n" +
                    "                                    <span class=\"m-topbar__welcome\">\n" +
                    "\t\t\t\t\t\t\t\t\t\t\t\t\t\tHello,&nbsp;\n" +
                    "\t\t\t\t\t\t\t\t\t\t\t\t\t</span>\n" +
                    "                                    <span class=\"m-topbar__username\" id = \"usrname\">\n" + aa + "</span>\n" +
                    "                                </a>\n" +
                    "\n" +
                    "                                <!--Opened profile-->\n" +
                    "                                <div class=\"m-dropdown__wrapper\">\n" +
                    "                                    <span class=\"m-dropdown__arrow m-dropdown__arrow--right m-dropdown__arrow--adjust\"></span>\n" +
                    "                                    <div class=\"m-dropdown__inner\">\n" +
                    "                                        <div class=\"m-dropdown__header m--align-center\"\n" +
                    "                                             style=\"background: url(../static/img/user_profile_bg.jpg); background-size: cover;\">\n" +
                    "                                            <div class=\"m-card-user m-card-user--skin-dark\">\n" +
                    "                                                <div class=\"m-card-user__pic\">\n" +
                    "                                                    <img src=\"../static/img/user4.jpg\"\n" +
                    "                                                         class=\"m--img-rounded m--marginless\" alt=\"\"/>\n" +
                    "                                                </div>\n" +
                    "                                                <div class=\"m-card-user__details\">\n" +
                    "\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<span class=\"m-card-user__name m--font-weight-500\" id=\"inner_usrname\">\n"+aa+"</span>\n" +
                    "                                                    <a href=\"\"\n" +
                    "                                                       class=\"m-card-user__email m--font-weight-300 m-link\" id=\"inner_email\">\n" + bb + " </a>\n" +
                    "                                                </div>\n" +
                    "                                            </div>\n" +
                    "                                        </div>\n" +
                    "\n" +
                    "                                        <div class=\"m-dropdown__body\">\n" +
                    "                                            <div class=\"m-dropdown__content\">\n" +
                    "                                                <ul class=\"m-nav m-nav--skin-light\">\n" +
                    "                                                    <!--profile-->\n" +
                    "                                                    <li class=\"m-nav__separator m-nav__separator--fit\"></li>\n" +
                    "                                                    <!--logout-->\n" +
                    "                                                    <li class=\"m-nav__item\">\n" +
                    "                                                        <a href=\"/logout\"\n" +
                    "                                                           class=\"btn m-btn--pill btn-secondary m-btn m-btn--custom m-btn--label-brand m-btn--bolder\">\n" +
                    "                                                            Logout\n" +
                    "                                                        </a>\n" +
                    "                                                    </li>\n" +
                    "                                                </ul>\n" +
                    "                                            </div>\n" +
                    "                                        </div>\n" +
                    "                                    </div>\n" +
                    "                                </div>\n" +
                    "                            </li>\n" +
                    "                            <!--Notification-->\n" +
                    "\n" +
                    "                        </ul>\n" +
                    "\n" +
                    "                    </div>\n" +
                    "                    <a href=\"./\" class=\"header__references_purchase\" target=\"_blank\">\n" +
                    "                        Main Page\n" +
                    "                    </a>");
            } else {
                $("#headerRef").append("<a href=\"./register.html\" class=\"header__references_support\" target=\"_blank\">\n" +
                    "                        Signup\n" +
                    "                    </a>\n" +
                    "                    <a href=\"./login.html\" class=\"header__references_purchase\" target=\"_blank\">\n" +
                    "                        Login\n" +
                    "                    </a>");

            }
        }
    });
});