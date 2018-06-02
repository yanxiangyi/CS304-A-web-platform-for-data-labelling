import time
import os
import json


def get_timestamp():
    return float("{0:.2f}".format(time.time()))
    # return strftime("%Y-%m-%d %H:%M:%S", gmtime())


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

    def __search_source_by_id(self, sourceid):
        result = self.cursor.execute("select * from source where sourceid='{}';".format(sourceid))
        return self.cursor.fetchone()  # None if it doesn't exist

    def __insertion(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            return 1
        except:
            return -1

    def __exe_sql(self, sql):
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except:
            return None

    def __get_by_option(self, tablename, target_col, col_val_dict, head=True):
        # search by one of the condition
        try:
            for col in col_val_dict.keys():
                if col_val_dict[col] != None:
                    pkcol = col
            self.cursor.execute(
                "select {} from {} where {}='{}';".format(target_col, tablename, pkcol, col_val_dict[pkcol]))
            if head:
                return self.cursor.fetchone()[0]
            else:
                return self.cursor.fetchone()
        except:
            return None

    def __get_by_mul_cond(self, tablename, target_col, col_val_dict):
        # search by multiple conditions
        try:
            sql = "select {} from {} where ".format(target_col, tablename)
            for i, col in enumerate(col_val_dict.keys()):
                if i != 0:
                    sql += " and "
                sql += "{} = '{}'".format(col, col_val_dict[col])

            sql += ";"
            # print(sql)
            self.cursor.execute(sql)
            return self.cursor.fetchone()[0]
        except:
            return None

    # user*******************************************************************************
    def get_all_user(self):
        return self.__exe_sql("select * from users;")

    def get_user(self, userid=None, username=None, user_email=None):
        return self.__get_by_option('users', '*', {'userid': userid, 'username': username, 'email_address': user_email},
                                    head=False)

    def get_user_number(self):
        return self.__exe_sql("select count(*) from users;")[0][0]

    def get_user_id(self, username=None, user_email=None):
        return self.__get_by_option('users', 'userid', {'username': username, 'email_address': user_email})

    def get_user_passwd(self, userid=None, username=None, user_email=None):
        return self.__get_by_option('users', 'password',
                                    {'userid': userid, 'username': username, 'email_address': user_email})

    def get_user_email(self, userid=None, username=None):
        return self.__get_by_option('users', 'email_address', {'userid': userid, 'username': username})

    def get_user_name(self, userid=None, user_email=None):
        return self.__get_by_option('users', 'username', {'userid': userid, 'email_address': user_email})

    def get_user_credit(self, userid=None, username=None, user_email=None):
        return self.__get_by_option('users', 'credits',
                                    {'userid': userid, 'username': username, 'email_address': user_email})

    def get_user_nb_accept(self, userid=None, username=None, user_email=None):
        return self.__get_by_option('users', 'nb_accept',
                                    {'userid': userid, 'username': username, 'email_address': user_email})

    def get_user_nb_answer(self, userid=None, username=None, user_email=None):
        return self.__get_by_option('users', 'nb_answer',
                                    {'userid': userid, 'username': username, 'email_address': user_email})

    def get_user_nb_val(self, userid=None, username=None, user_email=None):
        return self.__get_by_option('users', 'nb_val',
                                    {'userid': userid, 'username': username, 'email_address': user_email})

    def get_user_nb_val_tp(self, userid=None, username=None, user_email=None):
        return self.__get_by_option('users', 'nb_val_tp',
                                    {'userid': userid, 'username': username, 'email_address': user_email})

    def get_user_val_acc(self, userid=None, username=None, user_email=None):
        total = self.get_user_nb_val(userid, username, user_email)
        if total != 0:
            return self.get_user_nb_val_tp(userid, username, user_email) / total
        else:
            return 0

    def get_user_accept_rate(self, userid=None, username=None, user_email=None):
        total = self.get_user_nb_answer(userid, username, user_email)
        if total != 0:
            return self.get_user_nb_accept(userid, username, user_email) / self.get_user_nb_answer(userid, username,
                                                                                                   user_email)
        else:
            return 0

    def get_user_signin_time(self, userid=None, username=None, user_email=None):
        return self.__get_by_option('users', 'signin_date',
                                    {'userid': userid, 'username': username, 'email_address': user_email})

    def insert_user(self, username, user_email, passwd, signin_time=get_timestamp(), credits=0, nb_accept=0,
                    nb_answer=0, nb_examined=0):
        # insertion: 1 success, 0: already exist, -1: fail
        if self.__search_user_by_name(username) == None:
            sql = "INSERT INTO `se_proj`.`users` (`username`,`email_address`,`password`,`signin_date`,`credits`,`nb_accept`,`nb_answer`,`nb_examined`) VALUES ('{}','{}','{}','{}','{}',{},{},{});" \
                .format(username, user_email, passwd, signin_time, credits, nb_accept, nb_answer, nb_examined)
            return self.__insertion(sql)
        else:
            return 0

    def user_exist(self, userid=None, username=None, user_email=None):
        result = self.__get_by_option('users', '*',
                                      {'userid': userid, 'username': username, 'email_address': user_email})
        return True if result != None else False
    
    def get_user_credit_rank(self, user_email):
        userid = self.get_user_id(user_email=user_email)
        sql = "select i.rank from \
        (SELECT u.userid,\
        @curRank := @curRank + 1 AS rank  FROM  se_proj.users u, (SELECT @curRank := 0) r \
        ORDER BY  u.credits desc ) i where i.userid={};".format(userid)
        return int(self.__exe_sql(sql)[0][0])

    
    def get_user_source(self, user_email):
        userid = self.get_user_id(user_email=user_email)
        return self.__exe_sql("select distinct(td.datasource) from text_label tl \
        join text_data td on td.dataid=tl.dataid join users u  on tl.userid= u.userid where u.userid={};".format(userid))
    
    # admin******************************************************************************
    def get_admin(self, adminid=None, adminname=None, admin_email=None):
        return self.__get_by_option('admin', '*',
                                    {'adminid': adminid, 'adminname': adminname, 'email_address': admin_email},
                                    head=False)

    def get_admin_id(self, adminname=None, admin_email=None):
        return self.__get_by_option('admin', 'adminid', {'email_address': admin_email, 'adminname': adminname})

    def get_admin_name(self, adminid=None, admin_email=None):
        return self.__get_by_option('admin', 'adminname', {'email_address': admin_email, 'adminid': adminid})

    def get_admin_passwd(self, adminid=None, adminname=None, admin_email=None):
        return self.__get_by_option('admin', 'password',
                                    {'adminid': adminid, 'adminname': adminname, 'email_address': admin_email})

    def get_admin_access_level(self, adminid=None, adminname=None, admin_email=None):
        # normal or super
        return self.__get_by_option('admin', 'access_level',
                                    {'adminid': adminid, 'adminname': adminname, 'email_address': admin_email})

    def insert_admin(self, email_addr, adminname, passwd, access_level=1):
        # insertion: 1 success, 0: already exist, -1: fail
        if self.__search_admin_by_name(adminname) == None:
            sql = "INSERT INTO `se_proj`.`admin` (`email_address`,`adminname`,`password`,`access_level`) VALUES ('{}','{}','{}','{}');" \
                .format(email_addr, adminname, passwd, access_level)
            return self.__insertion(sql)
        else:
            return 0
        
    def get_admin_source(self, adminid=None, adminname=None, admin_email=None):
        if adminid==None:
            adminid = self.__get_by_option('admin', 'adminid', {'email_address': admin_email, 'adminname': adminname})
        return self.__exe_sql("select * from source where publisher={}".format(adminid))

    # source*****************************************************************************

    def get_source_number(self):
        return self.__exe_sql("select count(*) from source;")[0][0]

    def get_source(self, sourcename=None, sourceid=None):
        return self.__get_by_option('source', '*', {'sourceid': sourceid, 'sourcename': sourcename}, head=False)

    def get_all_source(self):
        return self.__exe_sql("select * from source;")

    def get_source_id(self, sourcename):
        return self.__get_by_option('source', 'sourceid', {'sourcename': sourcename})

    def get_source_finished(self, sourcename=None, sourceid=None):
        result = self.__get_by_option('source', 'finished', {'sourceid': sourceid, 'sourcename': sourcename})
        return True if result == 1 else False

    def get_source_publisherid(self, sourcename=None, sourceid=None):
        # return admin id
        return self.__get_by_option('source', 'publisher', {'sourceid': sourceid, 'sourcename': sourcename})

    def get_source_desc(self, sourcename=None, sourceid=None):
        return self.__get_by_option('source', 'description', {'sourceid': sourceid, 'sourcename': sourcename})

    def get_source_priority(self, sourcename=None, sourceid=None):
        return self.__get_by_option('source', 'priority', {'sourceid': sourceid, 'sourcename': sourcename})

    def insert_source(self, sourcename, finished=0, publisher='NULL', description='', publish_time=get_timestamp(),
                      priority=1):
        # insertion: 1 success, 0: already exist, -1: fail
        if self.__search_source_by_name(sourcename) == None:

            sql = "INSERT INTO `se_proj`.`source` (`sourcename`,`finished`,`publisher`,`description`,`publish_date`, `priority`)\
            VALUES ('{}',{}, {},'{}',{},{});".format(sourcename, finished, publisher, description, publish_time,
                                                     priority)
            # print(sql)
            return self.__insertion(sql)
        else:
            return 0
        
    def get_recent_source(self, limit=5):
        return self.__exe_sql("select * from source order by publish_date desc limit {};".format(limit))
    
    def get_source_by_priority(self, priority):
        # priority should be 1 2 or 3
        return self.__exe_sql("select * from se_proj.source where priority ={};".format(priority))

    # data *****************************************************************************
    def __insert_textdata(self, sourceid, data_index, data_path, final_labelid='NULL'):
        if self.__search_source_by_id(sourceid) != None:
            sql = "INSERT INTO `se_proj`.`text_data` (`datasource`,`data_index`,`data_path`,`final_labelid`) VALUES ({},{},'{}',{});" \
                .format(sourceid, data_index, data_path, final_labelid)
            return self.__insertion(sql)
        else:
            return 0

    def load_data(self, root_path, sourceid=None, sourcename=None):
        # load data(json file) from root folder into database
        sourceid = self.__get_by_option('source', 'sourceid', {'sourceid': sourceid, 'sourcename': sourcename})
        try:
            _, _, files = next(os.walk(root_path))
            for f in files:
                with open(os.path.join(root_path, f)) as js:
                    data_index = json.load(js)['index']
                if None != self.__get_by_mul_cond('text_data', 'dataid',
                                                  {'datasouce': sourceid, 'data_index': data_index}):
                    continue
                self.__insert_textdata(sourceid, data_index, os.path.join(root_path, f))
            return 1
        except:
            return 0

    def __get_textdata_sth(self, target_col, data_index, sourceid=None, sourcename=None):
        sourceid = self.__get_by_option('source', 'sourceid', {'sourceid': sourceid, 'sourcename': sourcename})
        return self.__get_by_mul_cond('text_data', target_col, {'datasource': sourceid, 'data_index': data_index})

    def get_textdataid(self, data_index, sourceid=None, sourcename=None):
        return self.__get_textdata_sth('dataid', data_index, sourceid, sourcename)

    def get_textdata_datapath(self, data_index, sourceid=None, sourcename=None):
        return self.__get_textdata_sth('data_path', data_index, sourceid, sourcename)

    def get_textdata_finallabelid(self, data_index, sourceid=None, sourcename=None):
        return self.__get_textdata_sth('final_labelid', data_index, sourceid, sourcename)

    def update_final_labelid(self, data_index, labelid, sourceid=None, sourcename=None):
        # 1:sucess -1:fail  0:souce or data not exist
        sourceid = self.__get_by_option('source', 'sourceid', {'sourceid': sourceid, 'sourcename': sourcename})
        dataid = self.get_textdataid(data_index, sourceid=sourceid)
        if sourceid != None and dataid != None:
            sql = "UPDATE `se_proj`.`text_data` SET `final_labelid`={} WHERE `dataid`={};".format(labelid, dataid)
            return self.__insertion(sql)
        else:
            return 0
    
    def fetch_data(self, sourcename, user_email, nb=5):
        userid=self.get_user_id(user_email=user_email)
        sourceid = self.get_source_id(sourcename=sourcename)
        
        l = self.__exe_sql("select td.dataid, td.datasource, td.data_index, td.data_path from text_data td \
        left join text_label tl on tl.dataid = td.dataid \
        where td.datasource ={} and td.final_labelid is NULL and (tl.userid!={} or tl.userid is NULL)\
        limit {};".format(sourceid, userid, nb))
        
        result = []
        for i in l:
            with open(i[-1]) as f:
                data = json.load(f)
            data['dataid'] = int(i[0])
            result.append(data)
        return result


    # label *****************************************************************************

    # index: dataid, userid
    def __get_label_sth(self, target_col, dataid, userid=None, username=None, user_email=None):
        if userid == None:
            userid = self.__get_by_option('users', 'userid', {'username': username, 'email_address': user_email})
        return self.__get_by_mul_cond('text_label', target_col, {'dataid': dataid, 'userid': userid})

    def get_labeldate(self, dataid, userid=None, username=None, user_email=None):
        return self.__get_label_sth('labeldate', userid, username, user_email)

    def get_labelpath(self, dataid, userid=None, username=None, user_email=None):
        return self.__get_label_sth('label_path', userid, username, user_email)

    def get_label_content(self, dataid, userid=None, username=None, user_email=None):
        return self.__get_label_sth('content', userid, username, user_email)

    def get_label_correct(self, dataid, userid=None, username=None, user_email=None):
        # return 0 not determined, 1 correct, -1 not correct
        return self.__get_label_sth('correct', userid, username, user_email)

    #def insert_label(self, userid, label_path, label_date=get_timestamp(), correct=0)
        
    def close(self):
        self.cursor.close()
        self.conn.close()