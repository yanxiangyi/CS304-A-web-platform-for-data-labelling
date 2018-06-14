import time
import os
import json
import datetime
import random
from shutil import copyfile,make_archive, rmtree
import fault_tolerance

'''
clear database

update text_data set final_labelid = NULL where  dataid>0;
update users set nb_answer =0 where userid>0;
update users set nb_accept =0 where userid>0;
update users set credits =0 where userid>0;
DELETE FROM text_label where labelid>0;
update source set nb_finished = 0 where sourceid>0;

'''


def get_timestamp():
    return float("{0:.2f}".format(time.time()))
    # return strftime("%Y-%m-%d %H:%M:%S", gmtime())

def timestamp_ealier_than(begin, days):
    return int((begin - datetime.timedelta(days=days)).strftime("%s"))

class sql_conn:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()
        self.ft_params = {'init_acc':0.5, 'nb_bel_ratio':1e-3, 'threshold':{'off':0,'low':0.51, 'high':0.8}}
        self.__ft_degree_dict = {0:'off',1:'low',2:'high'}

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

    def __get_by_mul_cond(self, tablename, target_col, col_val_dict, fetchone=False):
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
            if fetchone:
                return self.cursor.fetchone()[0]
            else:
                return self.cursor.fetchall()
        except:
            return None
    def __set_col_addup(self, tablename, target_col, cond_col, cond, addoffset):
        # cond can be either value or tuple
        try:
            sql = "update {} set {}={}+{} where {} ".format(tablename, target_col, target_col, addoffset,cond_col)
            if type(cond) is int:
                sql += "={};".format(cond)
            elif type(cond) is str:
                sql += "='{}';".format(cond)
            elif type(cond) is tuple:
                sql += "in {};".format(cond)
            print(sql)
            return self.__insertion(sql) #return -1 if execution fail
        except:
            return 0
        
    def __set_col(self, tablename, target_col, cond_col, cond, value):
        # cond can be either value or tuple
        try:
            sql = "update {} set {}={} where {} ".format(tablename, target_col, value, cond_col)
            if type(cond) is int:
                sql += "={};".format(cond)
            elif type(cond) is str:
                sql += "='{}';".format(cond)
            elif type(cond) is tuple:
                sql += "in {};".format(cond)
            print(sql)
            return self.__insertion(sql) #return -1 if execution fail
        except:
            return 0

    def get_by_cond_tuple(self, tablename, target_col, cond_col, tup):
        try:
            sql = "select {} from {} where {} in {};".format(target_col, tablename, cond_col, tup)
            print(sql)
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except:
            return None
    # user*******************************************************************************
    def get_all_user(self):
        user_list = self.__exe_sql("select * from users;")
        result = []
        for user in user_list:
            
            [user_id, user_email, user_name, password, signup_time, user_credit, nb_answer, nb_accept, _,_] = user
            acc =  nb_accept/nb_answer if nb_answer!=0 else 0
            result.append({"user_email": user_email, "user_name": user_name, "signin_date":signup_time, 
                           "user_credit": user_credit, "nb_answer": nb_answer, "acc":acc})
        return result
    
    
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
        
    def set_user_nb_answer(self, userid, addoffset=1):
        # return : **1** success; **0** fail; **-1** fail
        return self.__set_col_addup('users', 'nb_answer', 'userid', userid, addoffset)
    
    def set_user_nb_accept(self, userid, addoffset=1):
        return self.__set_col_addup('users', 'nb_answer', 'userid', userid, 1)

    def get_user_accept_rate(self, userid=None, username=None, user_email=None):
        total = self.get_user_nb_answer(userid, username, user_email)
        if total != 0:
            return self.get_user_nb_accept(userid, username, user_email) / self.get_user_nb_answer(userid, username,
                                                                                                   user_email)
        else:
            return 0


    def insert_user(self, username, user_email, passwd, signin_time=get_timestamp(), credits=0, nb_accept=0,
                    nb_answer=0):
        # insertion: 1 success, 0: already exist, -1: fail
        if self.__search_user_by_name(username) == None:
            sql = "INSERT INTO `se_proj`.`users` (`username`,`email_address`,`password`,`signin_date`,`credits`) VALUES ('{}','{}','{}','{}','{}');" \
                .format(username, user_email, passwd, signin_time, credits)
            return self.__insertion(sql)
        else:
            return 0

    def user_exist(self, userid=None, username=None, user_email=None):
        result = self.__get_by_option('users', '*',
                                      {'userid': userid, 'username': username, 'email_address': user_email})
        return True if result != None else False
    
    def get_user_credits_rank(self, user_email):
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
    
    def get_user_mainpage_pan(self, user_email):
        result = {1:0,2:0,3:0}
        try:
            # return [(priority, count), (priority, count), ...]
            userid = self.get_user_id(user_email=user_email)
            sql = "select x.priority, count(*) from \
            (select  distinct(td.datasource), s.priority from text_label tl \
            join text_data td on tl.dataid=td.dataid join source s on s.sourceid = td.datasource \
            where userid={}) x group by x.priority;".format(userid)
            tup =  self.__exe_sql(sql)
            for t in tup:
                result[t[0]]=t[1]
            return result
        except:
            return result
    
    def __user_label_later_number(self, ts_list, tr):
        cnt = 0
        for ts in ts_list:
            if ts[0]>tr:
                cnt += 1
        return cnt
    def get_user_mainpage_pan_history(self, user_email):
        userid = self.get_user_id(user_email=user_email)
        sql = "select labeldate from text_label where userid={} order by labeldate desc;".format(userid) 
        ts_list = self.__exe_sql(sql)
        days_list = [1,3,7,30]
        result = []
        now = datetime.datetime.now()
        for d in days_list:
            ts_tr = timestamp_ealier_than(now, d) #threshold
            result.append(self.__user_label_later_number(ts_list, ts_tr))
            
        result.append(len(ts_list))
        return result
        
    # admin*****************************************************************************
    def get_admin(self, adminid=None, adminname=None, admin_email=None):
        return self.__get_by_option('admin', '*',  
                                    {'adminid': adminid, 'adminname': adminname, 'email_address': admin_email},
                                    head=False)
            
    def get_admin_nb_task(self, adminid):
        sql = "select sum(nb_json) from se_proj.source where publisher ={};".format(adminid)
        return self.__exe_sql(sql)[0][0]
        
            
    def get_adminid(self, email_addr):
        return self.__get_by_option('admin', 'adminid',  
                                    {'email_address': email_addr},head=False)[0]
    def get_all_admin(self):
        admin_list = self.__exe_sql("select * from admin;")
        result = []
        for admin in admin_list:
            [adminid,email_address, adminname, _, _] = admin
            nb_task = self.get_admin_nb_task(adminid)
            
            
            nb_source = len(self.get_admin_source(admin_email=email_address))
            result.append({"admin_email":email_address, "adminname":adminname,  
                          "nb_source":nb_source, "nb_task":int(nb_task if nb_task!=None else 0)})

        return result
        
    def get_admin_passwd(self, admin_email=None):
        return self.__get_by_option('admin', 'password',
                                    {'email_address': admin_email})
    
    def get_admin_access_level(self, admin_email):
        return self.__get_by_option('admin', 'access_level',
                                    {'email_address': admin_email})
    def insert_admin(self, email_addr, adminname, passwd, access_level=1):
        # insertion: 1 success, 0: already exist, -1: fail
        if self.__search_admin_by_name(adminname) == None:
            sql = "INSERT INTO `se_proj`.`admin` (`email_address`,`adminname`,`password`,`access_level`) VALUES ('{}','{}','{}','{}');" \
                .format(email_addr, adminname, passwd, access_level)
            return self.__insertion(sql)
        else:
            return 0
        
    def get_admin_source(self, admin_email=None):
        adminid = self.__get_by_option('admin', 'adminid', {'email_address': admin_email})
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
    
    def get_source_nb_json(self, sourceid):
        return self.__exe_sql("select nb_json from source where sourceid={};".format(sourceid))[0][0]

    def insert_source(self, sourcename, finished=0, publisher='NULL', description='', publish_time=get_timestamp(),
                      priority=1, ft_degree=0):
        # insertion: 1 success, 0: already exist, -1: fail
        if self.__search_source_by_name(sourcename) == None:
            if ft_degree not in [0,1,2]:  #illegal 
                ft_degree = 0  #default 0
            
            sql = "INSERT INTO `se_proj`.`source` (`sourcename`,`nb_finished`,`publisher`,`description`,`publish_date`, `priority`, `fault_tolerance_degree`) \
            VALUES ('{}',{}, {},'{}',{},{},{});".format(sourcename, finished, publisher, description, publish_time,
                                                     priority, ft_degree)
            print(sql)
            return self.__insertion(sql)
        else:
            return 0
        
    def get_source_ftdgree(self, sourcename=None, sourceid=None):
        return self.__get_by_option('source', 'fault_tolerance_degree', {'sourcename':sourcename, 'sourceid':sourceid})
        
        
    def get_recent_source(self, limit=5):
        return self.__exe_sql("select * from source order by publish_date desc limit {};".format(limit))
    
    def get_source_by_priority(self, priority):
        # priority should be 1 2 or 3
        return self.__exe_sql("select * from se_proj.source where priority ={};".format(priority))

    def update_source_nb_finished(self, sourceid):
        sql = "update source set nb_finished= (select count(*) from text_data where datasource={} and final_labelid is not NULL) where sourceid={};".format(sourceid, sourceid)
        print(sql)
        return self.__insertion(sql)
    
    def get_data_final_label(self, dataid):
        # get the label_content of the data's final_labelid referenced to 
        sql = "select tl.label_content from text_data td join text_label tl \
        on td.final_labelid = tl.labelid where td.dataid={};".format(dataid)
        return self.__exe_sql(sql)
    
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
        # return 0 fail, -1 set nb_json fail
        sourceid = self.__get_by_option('source', 'sourceid', {'sourceid': sourceid, 'sourcename': sourcename})
        try:
            _, _, files = next(os.walk(root_path))
            if(1 != self.__set_col('source', 'nb_json', 'sourceid', sourceid, len(files))):
                return -1
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
    
    def fetch_data(self, sourcename, user_email, nb=5):
        userid=self.get_user_id(user_email=user_email)
        sourceid = self.get_source_id(sourcename=sourcename)

        sql = "select dataid,datasource, data_index, data_path from text_data \
        where datasource={} and final_labelid is NULL and dataid not in \
        (select td.dataid from text_data td \
        join text_label tl on td.dataid=tl.dataid \
        where tl.userid={} and td.datasource={});".format(sourceid, userid, sourceid)
        print(sql)
        
        
        l = self.__exe_sql(sql)
        
        if len(l)>nb:
            l = random.sample(l,nb)
        result = []
        #set_trace()
        for i in l:
            with open(i[-1]) as f:
                #print(i[-1])
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

    def get_label_correct(self, dataid, userid=None, username=None, user_email=None):
        # return 0 not determined, 1 correct, -1 not correct
        return self.__get_label_sth('correct', userid, username, user_email)
    
    def set_label_correct(self, labelid, value=1):
        #set correct to the value
        # labelid can be either int or int tuple
        # return 1 if success
        return self.__set_col('text_label','correct', 'labelid', labelid, value)
    
    
    def insert_label(self, user_email, json_list, save_dir='/home/se2018/label/', label_date=get_timestamp(), correct=0):
        # insert label , save label json file from the same user of the same project
#         try:
        if 1:
            if(json_list == []):
                return 1
            #set_trace()
            userid=self.get_user_id(user_email=user_email)
            if(userid == None):
                print("user not found")
                return -1
            proj_name = json_list[0]['projectName']
            save_dir = save_dir+'{}/'.format(proj_name)
            
            
            self.set_user_nb_answer(userid, addoffset = len(json_list))
            
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
                
            for j in json_list:
                #save the file
                save_path = save_dir+str(j['index'])+'_'+str(userid)+'_label.json'
                with open(save_path, 'w') as outfile:
                    json.dump(j, outfile)

                sourceid = self.get_source_id(sourcename=proj_name)
                ftdegree = self.get_source_ftdgree(sourceid=sourceid)
                
                label_content = []
                for subtask in j['task']:
                    #set_trace()
                    label_content.append(subtask['label'])

                    
                
                label_content = str(label_content).replace("'", "`")
                ft_flag = self._pre_ft_processing(j['dataid'], label_content)
                print("ft_flag : {}".format(ft_flag))
                
                correct = max(0, ft_flag)# ft_flag=0->correct=0; ft_flag=1->correct=1; ft_flag=-1->correct=0;
                
                sql = "INSERT INTO text_label(`dataid`,`userid`,`labeldate`,`label_path`,`label_content`,`correct`) VALUES \
                ({},{},{},'{}','{}',{});".format(j['dataid'], userid, label_date, save_path, label_content, correct)
                
                
                if ft_flag == 1:
                    # set user nb_accept and credits
                    sql = "update users set nb_accept = nb_accept+1 , credits=credits+1 where userid = ;".format(userid)
                    
                #print(sql)
                if(self.__insertion(sql)== -1):
                    return 0
                
                # fault tolerance
                if ft_flag == -1:
                    ft_degree = self.get_source_ftdgree(sourceid= sourceid)
                    print("goto ft process, sourceid = {}, ft_degree = {}".format(sourceid, ft_degree))
                    re = self.fault_tol_process(j['dataid'],sourceid, ft_degree) 
                    if re not in [0,1]:
                        return re
                    
            return 1
#         except:
#             return -1
        

    def _pre_ft_processing(self, dataid, user_ans):
        # return 0 if incorrect, 1 if correct, -1 if not final yet, go for fault tolerance process
        final_label = self.get_data_final_label(dataid= dataid)
        if(final_label == []):
            # no final label, continue ft process
            return -1
        else:
            # the question is finaled, compare the user answer with the fianl answer 
            return int(user_ans == final_label[0][0])
        
        
    def fault_tol_process(self, dataid, sourceid, ft_degree):
        #return -1 if error, 0 if none is detected correct
        #return 1 if success
        
        ft_data = self.load_ft_data(dataid)
        nb_json = self.get_source_nb_json(sourceid= sourceid)
        correct_labelid = fault_tolerance.ft_algo(ft_data,nb_json,self.ft_params['threshold'][self.__ft_degree_dict[ft_degree]], self.ft_params['init_acc'], self.ft_params['nb_bel_ratio'])
        #save ft log
        log = {'data':ft_data, 'result':correct_labelid}
        with open('/home/se2018/Log/'+str(get_timestamp())+'.json', 'w') as file:
                file.write(json.dumps(log))
        
        print("correct answer: {}".format(correct_labelid))
        if correct_labelid!=None:
            #set correct=1 in table text_label
            if len(correct_labelid)==1:
                correct_labelid = correct_labelid[0]
                final_labelid = correct_labelid
            else:
                correct_labelid = tuple(correct_labelid)
                final_labelid = correct_labelid[0]
            if (-1 == self.set_label_correct(correct_labelid, value=1)):
                return 2 # set fail

            #add up user's nb_accept
            if type(correct_labelid) is int:
                sql = "update users set nb_accept = nb_accept+1 , credits=credits+1 where userid in \
                (select userid from text_label where labelid = {});".format(correct_labelid)
            elif type(correct_labelid) is tuple:
                sql = "update users set nb_accept = nb_accept+1 , credits=credits+1 where userid in \
                (select userid from text_label where labelid in {});".format(correct_labelid)
            print(sql)
            if(-1 == self.__insertion(sql)):
                return 3 # set fail
            

            #modify text_data to add final_labelid
        
            if 1!=self.__set_col('text_data','final_labelid', 'dataid', dataid, final_labelid):
                return 4
            
            #set number of finished
            if -1 == self.update_source_nb_finished(sourceid=sourceid):
                return 5
            
            return 1
        else:
            return 0
        
    def load_ft_data(self, dataid):
        # load data for fault tolerance
        # return [dataid, label_content, userid, user nb_accpet, user nb_answer ]
        sql = "SELECT tl.labelid, tl.label_content, tl.userid, u.nb_accept, u.nb_answer \
        FROM text_label tl join users u on u.userid=tl.userid where dataid={} ".format(dataid)
        return self.__exe_sql(sql)
    
    def download_label(self, sourcename, zip_path, root_path = '~/tmp'):
        try:
            sourceid = self.get_source_id(sourcename=sourcename)
            # get path
            #data_path = self.__get_by_mul_cond('text_data','data_path',{'datasource':sourceid}, fetchone=False)
            label_path = self.__get_finallabel_path(sourceid)

            if not os.path.exists(root_path):
                os.makedirs(root_path)
            #set_trace()

            for p in label_path:
                file_name = p[0].split('/')[-1]
                copyfile(p[0], os.path.join(root_path, file_name))

            # make zip
            make_archive(zip_path, 'zip', root_path)
            #delete tmp dir
            rmtree(root_path)
            
            return zip_path+'.zip'
        except:
            return ''
        

    
    def __get_finallabel_path(self, sourceid):
        sql = "select tl.label_path from text_data td join text_label tl on td.final_labelid = tl.labelid where td.datasource={};".format(sourceid)
        return self.__exe_sql(sql)
    
    def get_recapcha(self):
        try:
            sql = "select label_path from text_label where correct =1;"
            result = random.choice(self.__exe_sql(sql))[0]
            #print(result)
            with open(result) as js:
                file = json.load(js)
            return file
        except:
            return None
        
    def close(self):
        self.cursor.close()
        self.conn.close()
        
        
    