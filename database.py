
from time import gmtime, strftime



def get_time():
    return strftime("%Y-%m-%d %H:%M:%S", gmtime())


class sql_conn:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    def __search_user_by_name(self, username):
        self.cursor.execute("select * from users where username='{}';".format(username))
        result = self.cursor.fetchone()
        return result  # None if it doesn't exist

    def __search_admin_by_name(self, adminname):
        self.cursor.execute("select * from admin where adminname='{}';".format(adminname))
        result = self.cursor.fetchone()
        return result.fetchone()  # None if it doesn't exist

    def __search_source_by_name(self, sourcename):
        self.cursor.execute("select * from source where sourcename='{}';".format(sourcename))
        result = self.cursor.fetchone()
        return result.fetchone()  # None if it doesn't exist

    def __insertion(self, sql):
        try:
            self.cursor.execute(sql)
            return 1
        except:
            return -1

    # user*******************************************************************************
    def get_user_id(self, username):
        self.cursor.execute("select userid from users where username='{}';".format(username))
        result = self.cursor.fetchone()
        if result is None:
            return None
        return result[0]

    def get_user_passwd(self, userid=None, username=None, useremail=None):
        if userid != None:
            self.cursor.execute("select password from users where userid={};".format(userid))
            result = self.cursor.fetchone()
            if result is None:
                return None
            return result[0]
        elif username != None:
            self.cursor.execute("select password from users where username='{}';".format(username))
            result = self.cursor.fetchone()
            if result is None:
                return None
            return result[0]
        elif useremail != None:
            self.cursor.execute("select password from users where email_address='{}';".format(useremail))
            result = self.cursor.fetchone()
            if result is None:
                return None
            return result[0]
        return None

    def get_user_credit(self, userid=None, username=None, useremail=None):
        if userid != None:
            self.cursor.execute("select credits from users where userid={};".format(userid))
            result = self.cursor.fetchone()
            if result is None:
                return None
            return result[0]
        elif username != None:
            self.cursor.execute("select credits from users where username='{}';".format(username))
            result = self.cursor.fetchone()
            if result is None:
                return None
            return result[0]
        elif useremail != None:
            self.cursor.execute("select credits from users where email_address='{}';".format(useremail))
            result = self.cursor.fetchone()
            if result is None:
                return None
            return result[0]
        return None

    def insert_user(self, username, passwd, credits=0):
        # insertion: 1 success, 0: already exist, -1: fail
        if self.__search_user_by_name(username) == None:
            sql = "INSERT INTO `se_proj`.`users` (`username`,`password`,`signin_date`,`credits`) VALUES ('{}','{}','{}','{}');" \
                .format(username, passwd, get_time(), credits)
            return self.__insertion(sql)
        else:
            return 0

    # admin******************************************************************************
    def get_admin_id(self, adminname):
        self.cursor.execute("select adminid from admin where adminname='{}';".format(adminname))
        result = self.cursor.fetchone()
        if result is None:
            return None
        return result[0]

    def get_admin_passwd(self, adminid=None, adminname=None, adminemail=None):
        if adminid != None:
            self.cursor.execute("select password from admin where adminid={};".format(adminid))
            result = self.cursor.fetchone()
            if result is None:
                return None
            return result[0]
        elif adminname != None:
            self.cursor.execute("select password from admin where adminname='{}';".format(adminname))
            result = self.cursor.fetchone()
            if result is None:
                return None
            return result[0]
        elif adminemail != None:
            self.cursor.execute("select password from admin where email_address='{}';".format(adminemail))
            result = self.cursor.fetchone()
            if result is None:
                return None
            return result[0]
        return None

    def get_admin_access_level(self, adminid=None, adminname=None, adminemail=None):
        # normal or super
        if adminid != None:
            self.cursor.execute("select access_level from admin where adminid={};".format(adminid))
            result = self.cursor.fetchone()
            if result is None:
                return None
            return result[0]
        elif adminname != None:
            self.cursor.execute("select access_level from admin where adminname='{}';".format(adminname))
            result = self.cursor.fetchone()
            if result is None:
                return None
            return result[0]
        elif adminemail != None:
            self.cursor.execute("select access_level from admin where email_address='{}';".format(adminemail))
            result = self.cursor.fetchone()
            if result is None:
                return None
            return result[0]
        return None

    def insert_admin(self, adminname, passwd, access_level=1):
        # insertion: 1 success, 0: already exist, -1: fail
        if self.__search_admin_by_name(adminname) == None:
            sql = "INSERT INTO `se_proj`.`admin` (`adminname`,`password`,`access_level`) VALUES ('{}','{}','{}');" \
                .format(adminname, passwd, access_level)
            return self.__insertion(sql)
        else:
            return 0

    # source*****************************************************************************
    def get_source_id(self, sourcename):
        self.cursor.execute("select sourceid from source where sourcename='{}';".format(sourcename))
        result = self.cursor.fetchone()
        if result is None:
            return None
        return result[0]

    def get_source_label(self, sourceid=None, sourcename=None):
        # return string list
        if sourceid != None or sourcename != None:
            if sourceid != None:
                self.cursor.execute("select label from source where sourceid={};".format(sourceid))
            elif sourcename != None:
                self.cursor.execute(
                    "select label from source where sourcename='{}';".format(sourcename))
            return self.cursor.fetchone()[0].split(',') if self.cursor.fetchone()[0] != None else None
        else:
            return

    def insert_source(self, sourcename, label):
        # label should be a string list
        # insertion: 1 success, 0: already exist, -1: fail
        if self.__search_source_by_name(sourcename) == None:
            s = ''
            for l in label:
                s += str(l) + ','
            s = s[:-1]
            sql = "INSERT INTO `se_proj`.`source` (`sourcename`,`label`) VALUES ('{}','{}');" \
                .format(sourcename, s)
            return self.__insertion(sql)
        else:

            return 0

    # data********************************************************************************
    def get_all_image_data(self):
        # 0:dataid, 1:datatype, 2:priority, 3:datapath, 4:datasource, 5:publish_by(admin), 6:publish_date, 7:final_labelid
        self.cursor.execute("select * from image_data;")
        return self.cursor.fetchall()

    def get_all_text_data(self):
        # 0:dataid, 1:datatype, 2:priority, 3:datacontent, 4:datasource, 5:publish_by(admin), 6:publish_date, 7:final_labelid
        self.cursor.execute("select * from text_data;")
        return self.cursor.fetchall()

    def get_image_label_by_dataid(self, image_dataid):
        # 0:labelid, 1:dataid, 2:userid, 3:labeldate, 4:labelinfo, 5:labelpath
        self.cursor.execute("select * from image_label where dataid={};".format(image_dataid))
        return self.cursor.fetchall()

    def get_text_label_by_dataid(self, text_dataid):
        # 0:labelid, 1:dataid, 2:userid, 3:labeldate, 4:labelinfo
        self.cursor.execute("select * from text_label where dataid={};".format(text_dataid))
        return self.cursor.fetchall()