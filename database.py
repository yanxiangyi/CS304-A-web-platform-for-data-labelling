import time



def get_timestamp():
    return float("{0:.2f}".format(time.time()))
    #return strftime("%Y-%m-%d %H:%M:%S", gmtime())


class sql_conn:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    def __search_user_by_name(self, username):
        self.cursor.execute("select * from users where username='{}';".format(username))
        return self.cursor.fetchone()  # None if it doesn't exist
    
    def __search_user_by_id(self, userid):
        self.cursor.execute("select * from users where userid={};".format(userid))
        return self.cursor.fetchone()  # None if it doesn't exist

    def __search_admin_by_name(self, adminname):
        result = self.cursor.execute("select * from admin where adminname='{}';".format(adminname))
        return self.cursor.fetchone()  # None if it doesn't exist

    def __search_source_by_name(self, sourcename):
        result = self.cursor.execute("select * from source where sourcename='{}';".format(sourcename))
        return self.cursor.fetchone()  # None if it doesn't exist

    def __insertion(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            return 1
        except:
            return -1

    def __get_by_option(self, tablename, target_col, col_val_dict):
        # search by either id or name 
        try:
            for col in col_val_dict.keys():
                if col_val_dict[col]!=None:   
                    pkcol = col
            self.cursor.execute("select {} from {} where {}='{}';".format(target_col, tablename, pkcol, col_val_dict[pkcol]))
            return self.cursor.fetchone()[0]
        except:
            return None
        
    
    
    # user*******************************************************************************
    def get_user_id(self, username=None, user_email=None):
        return self.__get_by_option('users', 'userid', {'username': username, 'email_address': user_email})

    def get_user_passwd(self, userid=None, username=None, user_email=None):
        return  self.__get_by_option('users', 'password', {'userid': userid, 'username': username, 'email_address':user_email})
        
    def get_user_email(self, userid=None, username=None):
        return self.__get_by_option('users', 'email_address', {'userid': userid, 'username': username})
    
    def get_user_name(self, userid=None, user_email=None):
        return self.__get_by_option('users', 'username', {'userid': userid, 'email_address': user_email})

    def get_user_credit(self, userid=None, username=None, user_email=None):
        return self.__get_by_option('users', 'credits', {'userid': userid, 'username': username, 'email_address':user_email})

    def insert_user(self, username, user_email, passwd, signin_time=get_timestamp(), credits=0):
        # insertion: 1 success, 0: already exist, -1: fail
        if self.__search_user_by_name(username) == None:
#             if signin_time == 0:  # signin_time default: current time
#                 signin_time = get_timestamp()
            sql = "INSERT INTO `se_proj`.`users` (`username`,`email_address`,`password`,`signin_date`,`credits`) VALUES ('{}','{}','{}','{}','{}');" \
                .format(username, user_email, passwd, signin_time, credits)
            return self.__insertion(sql)
        else:
            return 0

    def user_exist(self, userid=None, username=None, user_email=None):
        result = self.__get_by_option('users','*', {'userid': userid, 'username': username, 'email_address':user_email})
        return True if result!=None else False

        
    # admin******************************************************************************
    def get_admin_id(self, adminname=None, admin_email=None):
        return self.__get_by_option('admin', 'adminid', {'email_address': admin_email, 'adminname': adminname})

    def get_admin_name(self, adminid=None, admin_email=None):
        return self.__get_by_option('admin', 'adminname', {'email_address': admin_email, 'adminid': adminid})
    
    def get_admin_passwd(self, adminid=None, adminname=None, admin_email=None):
        return self.__get_by_option('admin', 'password', {'adminid': adminid, 'adminname': adminname, 'email_address': admin_email})
        
    def get_admin_access_level(self, adminid=None, adminname=None, admin_email=None):
        # normal or super
        return self.__get_by_option('admin', 'access_level', {'adminid': adminid, 'adminname': adminname, 'email_address': admin_email})
        
    def insert_admin(self, email_addr, adminname, passwd, access_level=1):
        # insertion: 1 success, 0: already exist, -1: fail
        if self.__search_admin_by_name(adminname) == None:
            sql = "INSERT INTO `se_proj`.`admin` (`email_address`,`adminname`,`password`,`access_level`) VALUES ('{}','{}','{}','{}');" \
                .format(email_addr, adminname, passwd, access_level)
            return self.__insertion(sql)
        else:
            return 0

    # source*****************************************************************************
    def get_source_id(self, sourcename):
        self.cursor.execute("select sourceid from source where sourcename='{}';".format(sourcename))
        return self.cursor.fetchone()[0]  # None if it doesn't exist

    def get_source_finished(self, sourcename=None, sourceid=None):
        result = self.__get_by_option('source', 'finished', {'sourceid': sourceid, 'sourcename': sourcename})
        return True if result==1 else False
    
    def get_source_publisherid(self, sourcename=None, sourceid=None):
        #return admin id
        return self.__get_by_option('source', 'publisher', {'sourceid': sourceid, 'sourcename': sourcename})
    
    def get_source_desc(self, sourcename=None, sourceid=None):
        return self.__get_by_option('source', 'description',{'sourceid': sourceid, 'sourcename': sourcename})
    
    def get_source_priority(self, sourcename=None, sourceid=None):
        return self.__get_by_option('source', 'priority', {'sourceid': sourceid, 'sourcename': sourcename})
    
    def insert_source(self, sourcename,finished=0, publisher='NULL', description='', publish_time=get_timestamp(), priority=1):
        # insertion: 1 success, 0: already exist, -1: fail
        if self.__search_source_by_name(sourcename) == None:
            
            sql = "INSERT INTO `se_proj`.`source` (`sourcename`,`finished`,`publisher`,`description`,`publish_date`, `priority`)\
            VALUES ('{}',{}, {},'{}',{},{});" .format(sourcename, finished, publisher, description, publish_time, priority)
            #print(sql)
            return self.__insertion(sql)
        else:
            return 0

    
    def close(self):
        self.cursor.close()
        self.conn.close()