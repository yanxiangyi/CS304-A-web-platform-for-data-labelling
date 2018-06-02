# `sql_conn` Usage

### 1. Object

- Creation :

  `cnx = connection.MySQLConnection(user = '', password = '', host = '', database = '')`

  `c = sql_conn(cnx)`

- Close : `c.close()`



### 2. Method

**ER Diagram of database**

![](./db_er.png)

**All methods return `None` if fails unless otherwise stated**

#### 2.1 User Utility

- `get_all_user(self)`
    
  return all users
   
- `get_user(self, userid=None, username=None, user_email=None)`

  return all the information of the corresponding user
  
- `ger_user_number(self)`

  return the total number of users

- `get_user_id(self, username=None, user_email=None)` 

- `get_user_email(self, userid=None, username=None)`

- `get_user_name(self, userid=None, user_email=None)`

- `get_user_passwd(self, userid=None, username=None, user_email=None)`

- `get_user_credit(self, userid=None, username=None, user_email=None)`

- `get_user_nb_accept(self, userid=None, username=None, user_email=None)`
  
   return number of accepted answer of the user
   
- `get_user_nb_answer(self, userid=None, username=None, user_email=None)`

   return the user's total number of answers 

- `get_user_nb_val(self, userid=None, username=None, user_email=None)`

- `get_user_nb_val_tp(self, userid=None, username=None, user_email=None)`
    
   return `val_tp` of the user
   
- `get_user_val_acc(self,userid=None, username=None, user_email=None)`

   return the validation accuracy 
   
- `get_user_accept_rate(self,userid=None, username=None, user_email=None)`

   return the accept rate 

- `get_user_signin_time(self, userid=None, username=None, user_email=None)`

- `insert_user(self, username, user_email, passwd, signin_time=get_timestamp(), credits=0, nb_accept=0, nb_answer=0, nb_examined=0)`

  - default `signin_time` is current time
  - default `credits` is 0
  - default `nb_accept`, `nb_answer` and `nb_examined` are 0, i.e. the default number of accepted answer is 0.
  - insertion operations return : **1** success; **0** already exist; **-1** fail

- `user_exist(self, userid=None, username=None, user_email=None)`

  return `True` if the user exists otherwise `False`

#### 2.2 Admin Utility

- `get_admin(self, adminid=None, adminname=None, admin_email=None)`

  return all the information of the corresponding admin

- `get_admin_id(self, adminname=None, admin_email=None)`

- `get_admin_name(self, adminid=None, admin_email=None)`

- `get_admin_passwd(self, adminid=None, adminname=None, admin_email=None)`

- `get_admin_access_level(self, adminid=None, adminname=None, admin_email=None)`

  return **1** if normal admin; **2** if super admin

- `insert_admin(self, email_addr, adminname, passwd, access_level=1)`

  - default `access_level` is 1, i.e. normal admin
  - insertion operations return : **1** success; **0** already exist; **-1** fail
  
- `get_admin_source(self, adminid=None, adminname=None, admin_email=None)`

  return all sources published by the admin

#### 2.3 Source Utility

- `get_source_number(self)`

   return the total number of sources
   
- `get_all_source(self)`

   return all source information
   
- `get_source(self, sourcename=None, sourceid=None)`

  return all the information of the corresponding source
  
- `get_source_id(self, sourcename)`

- `get_source_nb_json`

  return json file count of the source

- `get_source_finished(self, sourcename=None, sourceid=None)`

  return `True` is the source task is finished, otherwise `False`

- `get_source_publisherid(self, sourcename=None, sourceid=None)`

  return the `adminid` of the source's publisher

- `get_source_desc(self, sourcename=None, sourceid=None)`

  return the description of the source

- `get_source_priority(self, sourcename=None, sourceid=None)`

- `insert_source(self, sourcename,finished=0, publisher='NULL', description='', publish_time=get_timestamp(), priority=1)`

  - default `finished` : False
  - default `publisher` : NULL
  - default `description` : ''
  - default `publish_time` : current time
  - default `priority` : 1
  - insertion operations return : **1** success; **0** already exist; **-1** fail
  - Note that `sourcename` shoule be unique

- `get_recent_source(self, limit=5)`

  return recent published source. Default 5 latest.
  
- `get_source_by_priority(self, priority)`

  return all sources have given priority

#### 2.4 Data Utility

**Combination of `data_source` and `data_index` should be UNIQUE**

- `load_data(self, root_path, sourceid=None, sourcename=None)`

  - load all the raw data file (in `.json` format) from folder path into database
  - return **1** success; **0** fail; **-1** insertion fail
  
- `get_textdataid(self, data_index, sourceid=None, sourcename=None)`

  need both `data_index` and source information to retrieve `dataid`.
  
- `get_textdata_datapath(self, data_index, sourceid=None, sourcename=None)`

- `get_textdata_finallabelid(self, data_index, sourceid=None, sourcename=None)`

- `update_final_labelid(self, data_index, labelid, sourceid=None, sourcename=None)`

  - need either `sourceid` or `sourcename`
  - return **1** success; **0** source of label not found; **-1** fail
  
  
#### 2.5 Label Utility

**Combination of `dataid` and `userid` should be UNIQUE**

- `get_labeldate(self, dataid, userid=None, username=None, user_email=None)`

  need at least one of the value of `userid`, `username` and `user_email` to get the result.

- `get_labelpath(self, dataid, userid=None, username=None, user_email=None)`

- `get_label_content(self, dataid, userid=None, username=None, user_email=None)`

- `get_label_correct(self, dataid, userid=None, username=None, user_email=None)`
  
  - return **0** not determined; **1** correct; **-1** incorrect.




