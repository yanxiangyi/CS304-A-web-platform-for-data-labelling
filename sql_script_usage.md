# `sql_conn` Usage

### 1. Object

- Creation :

  `cnx = connection.MySQLConnection(user = '', password = '', host = '', database = '')`

  `c = sql_conn(cnx)`

- Close : `c.close()`



### 2. Method

**ER Diagram of database**

https://github.com/yanxiangyi/CS304-A-web-platform-for-data-labelling/blob/master/db_er.png

**All methods return `None` unless otherwise stated**

#### 2.1 User Utility

- `get_user_id(self, username=None, user_email=None)` 

- `get_user_email(self, userid=None, username=None)`

- `get_user_name(self, userid=None, user_email=None)`

- `get_user_passwd(self, userid=None, username=None, user_email=None)`

- `get_user_credit(self, userid=None, username=None, user_email=None)`

- `insert_user(self, username, user_email, passwd, signin_time=get_timestamp(), credits=0)`

  - default `signin_time` is current time
  - insertion operations return : **1** success; **0** already exist; **-1** fail

- `user_exist(self, userid=None, username=None, user_email=None)`

  return `True` if the user exists otherwise `False`

#### 2.2 Admin Utility

- `get_admin_id(self, adminname=None, admin_email=None)`

- `get_admin_name(self, adminid=None, admin_email=None)`

- `get_admin_passwd(self, adminid=None, adminname=None, admin_email=None)`

- `get_admin_access_level(self, adminid=None, adminname=None, admin_email=None)`

  return **1** if normal admin; **2** if super admin

- `insert_admin(self, email_addr, adminname, passwd, access_level=1)`

  - default `access_level` is 1, i.e. normal admin
  - insertion operations return : **1** success; **0** already exist; **-1** fail

#### 2.3 Source Utility

- `get_source_id(self, sourcename)`

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





