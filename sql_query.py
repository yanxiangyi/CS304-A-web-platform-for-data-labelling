class sql_conn:
    def __init__(self, conn):
        self.conn = conn
    def __search_user_by_name(self, username):
        result = self.conn.execute("select * from users;")
        for r in result:
            if r[1] == username :
                return r
        return (None,None,None,None,None)
    
    def __search_admin_by_name(self, adminname):
        result = self.conn.execute("select * from admin;")
        for r in result:
            if r[1] == adminname :
                return r
        return (None,None,None,None) # admin not found
    
    def __search_source_by_name(self, sourcename):
        result = self.conn.execute("select * from source;")
        for r in result:
            if r[1] == sourcename :
                return r
        return (None,None,None) # source not found
    
    #user*******************************************************************************
    def get_user_id(self, username):
        return self.__search_user_by_name(username)[0]
    
    def get_user_passwd(self, username):
        return self.__search_user_by_name(username)[2]
    
    def get_user_credit(self, username):
        return self.__search_user_by_name(username)[4]
    
    #admin******************************************************************************
    def get_admin_id(self, adminname):
        return self.__search_admin_by_name(adminname)[0]
    
    def get_admin_passwd(self, adminname):
        return self.__search_admin_by_name(adminname)[2]
    
    def get_admin_level(self, adminname):
        return self.__search_admin_by_name(adminname)[3]
    
    # source*****************************************************************************
    def get_source_id(self, sourcename):
        return self.__search_source_by_name(sourcename)[0]
    
    def get_source_category(self, sourcename):
        return self.__search_source_by_name(sourcename)[2].split(',')
    
'''
# test user 
print(c.get_user_id('jiangtk'))
print(c.get_user_passwd('jiangtk'))
print(c.get_user_credit('jiangtk'))
'''