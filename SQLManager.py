import pymysql

class SQLManager(object):

    def __init__(self, host, user, password, dbname):
        db = pymysql.connect(host, user, password, dbname, charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor)
        self.__cursor = db.cursor()

    def save_admin_login(self, admin_id, timestamp, clid = None):
        if clid is not None:
            self.__save_admin_clid(admin_id, clid)

        query = "INSERT INTO activity SET activity_adminid = ?, activity_starttime = ?"
        self.__cursor.execute(query % admin_id % timestamp)

    def save_admin_logout(self, clid, timestamp):
        query = "UPDATE activity SET activity_endtime = ? WHERE activity_endtime = null AND activity_adminid = (SELECT admin_id FROM admin WHERE clid = ?)"
        self.__cursor.execute(query % timestamp, clid)

    def get_admins(self):
        query = "SELECT admin_name, admin_uid FROM admin"
        self.__cursor.execute(query)
        return self.__cursor.fetchall()

    def __save_admin_clid(self, admin_id, clid):
        query = "UPDATE admin SET admin_clid = ? WHERE admin_id = ?"
        self.__cursor.execute(query % clid % admin_id)