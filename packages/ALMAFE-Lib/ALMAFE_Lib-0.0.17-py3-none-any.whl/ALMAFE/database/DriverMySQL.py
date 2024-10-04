'''
Driver wrapper for mysql-connector-python
'''
import mysql.connector
from mysql.connector import Error

class DriverMySQL():
    '''
    Driver wrapper for mysql-connector-python
    Provides a uniform interface to SQL user code
    '''
    TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'

    def __init__(self, connectionInfo):
        '''
        Constructor
        :param connectionInfo: dictionary having the items needed to connect to MySQL server:
                {'host', 'user', 'passwd', 'database', 'port' : 3306, 'use_pure' : False }
        '''
        self.host = connectionInfo['host']
        self.user = connectionInfo['user']
        self.passwd = connectionInfo['passwd']
        self.database = connectionInfo['database']        
        self.port = connectionInfo.get('port', 3306)
        self.use_pure = connectionInfo.get('use_pure', False)
        self.cursor = None
        self.connect()          
        
    def connect(self):
        '''
        Connect to the database.
        
        use_pure=True will prevent BLOBs being returned as Unicode strings
          (which either fails when decoding or when comparing to bytes.)
        https://stackoverflow.com/questions/52759667/properly-getting-blobs-from-mysql-database-with-mysql-connector-in-python
        :return True/False
        '''
        self.connection = None
        try:
            self.connection = mysql.connector.connect(host=self.host, 
                                                      port=self.port, 
                                                      user=self.user, 
                                                      passwd=self.passwd, 
                                                      database=self.database,
                                                      use_pure=self.use_pure)
            return True
        except Error as e:
            print(f"MySQL error: {e}")
            return False

    def disconnect(self):
        '''
        Disconnect from the database.
        :return True/False
        '''
        try:
            if self.cursor:
                self.cursor.close()
            self.connection.close()
            self.connection = None
            self.cursor = None
            return True
        except Error as e:
            print(f"MySQL error: {e}")
            return False
        
    def is_connected(self) -> bool:
        return self.connection is not None
        
    def execute(self, query, params = None, commit = False, reconnect = True):
        '''
        Execute an SQL query.
        :param query: str
        :param params: tuple or dictionary params are bound to the variables in the operation. 
                       Specify variables using %s or %(name)s parameter style (that is, using format or pyformat style).
        :param commit: If True, commit INSERT/UPDATE/DELETE queries immediately.
        :param reconnect: If True and the connection seems to have gone away, reconnect and retry the query.
        :return True/False
        '''
        doRetry = False
        if not self.connection:
            self.connect()
        try:    
            self.cursor = self.connection.cursor()
            self.cursor.execute(query, params)
            if commit:
                self.connection.commit()
        except Error as e:
            if not reconnect:
                print(f"MySQL error: {e}")
                return False
            # this calls reconnect() internally:
            self.connection.ping(reconnect = True, attempts = 2)
            doRetry = True

        if doRetry:
            # and retry the query
            try:
                self.cursor = self.connection.cursor()
                self.cursor.execute(query, params)
                if commit:
                    self.connection.commit()
            except Error as e:
                print(f"MySQL error: {e}")
                return False
        return True
    
    def commit(self):
        '''
        Commit any previously executed but not yet committed INSERT/UPDATE/DELETE queries.
        :return True/False
        '''
        try:
            self.connection.commit()
            if self.cursor:
                self.cursor.close()
                self.cursor = None
            return True
        except Error as e:
            print(f"MySQL error: {e}")
            return False
        
    def rollback(self):
        '''
        Rollback any previously executed but not yet committed INSERT/UPDATE/DELETE queries.
        :return True/False
        '''
        try:
            self.connection.rollback()
            return True
        except Error as e:
            print(f"MySQL error: {e}")
            return False

    def fetchone(self):
        '''
        Fetch one row from the last SELECT query.
        :return tuple or False
        '''
        try:
            row = self.cursor.fetchone()
            return row
        except Error as e:
            print(f"MySQL error: {e}")
            return False    

    def fetchmany(self, chunkSize):
        '''
        Fetch multiple rows from the last SELECT query.
        :param chunkSize: max number of rows to fetch
        :return list of tuple or False
        '''
        try:
            result = self.cursor.fetchmany(chunkSize)
            return result
        except Error as e:
            print(f"MySQL error: {e}")
            return False
        
    def fetchall(self):
        '''
        Fetch all rows from the last SELECT query.
        :return list of tuple or False
        '''
        try:
            result = self.cursor.fetchall()
            return result
        except Error as e:
            print(f"MySQL error: {e}")
            return False
