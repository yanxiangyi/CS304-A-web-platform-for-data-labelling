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
        result = self.execute("select * from admin;")
        for r in result:
            if r[1] == adminname :
                return r
        return (None,None,None,None) # admin not found
    
    def __search_source_by_name(self, sourcename):
        result = self.execute("select * from source;")
        for r in result:
            if r[1] == sourcename :
                return r
        return (None,None,None) # source not found
    
    #user*******************************************************************************
    def get_user_id(self, username):
        return __search_user_by_name(self, username)[0]
    
    def get_user_passwd(self, username):
        return __search_user_by_name(self, username)[2]
    
    def get_user_credit(self, username):
        return __search_user_by_name(self, username)[4]
    
    #admin******************************************************************************
    def get_admin_passwd(self, adminname):
        return __search_admin_by_name(self, adminname)[2]
    
    def get_admin_level(self, adminname):
        return __search_admin_by_name(self, adminname)[3]
    
    # source*****************************************************************************
    def get_source_id(self, sourcename):
        return __search_source_by_name(self, sourcename)[0]
    
    def get_source_category(self, sourcename):
        # return string list
        return __search_source_by_name(self, sourcename)[2].split(',')