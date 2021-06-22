import pymysql
from user_data import *
import logging
# 資料庫參數設定
class mySQL_ccisa():
    db_settings = {
        "host": "127.0.0.1",
        "port": 3306,

         "user": "root",
        "password": ", ## 密碼
        "db": "",  ## 資料表名稱
        "charset": "utf8"
    }
    
    def __init__(self, host, port):
        self.db_settings['host'] = host
        self.db_settings['port'] = port
        
    def connectDB( self, dbName ) :
        try :
            self.db_settings['db'] = dbName
            self.conn = pymysql.connect(**self.db_settings)
        except Exception as e :
            logging.error('Fail to connection mysql {}'.format(str(e)))
    def deconnectDB(self):
        self.conn.commit() 
        self.conn.close()

    def insert_db_data(self, user_data):
        try :
            arg = (( user_data.accept_receive, user_data.sign_up, user_data.company, user_data.name, user_data.title, user_data.phone, user_data.email ))
            with self.conn.cursor() as cursor:
                cursor.execute( "INSERT INTO `app_Nurture` (`accept_receive`, `sign_up`, `company`, `name`, `title`, `phone`, `email`) VALUES ( %s, %s, %s, %s, %s, %s, %s)",arg)
                #cursor.execute( "INSERT INTO `Customer_Profile` (`accept_receive`, `sign_up`, `company`, `name`, `title`, `phone`, `email`) VALUES ( %s, %s, %s, %s, %s, %s, %s)",arg)
            serial_num = self.conn.insert_id()
            self.conn.commit() 
         
            
            return serial_num
        except Exception as e :
            logging.error('Fail to insert mysql {}'.format(str(e)))
    def search_db_data(self, msg):
        try :
            #command = "SELECT * FROM `Customer_Profile`"
            command = "SELECT * FROM `app_Nurture`"
            with self.conn.cursor() as cursor:
                cursor.execute(command)
            self.conn.commit() 
            cursor.close()
        except Exception as e :
            logging.error('Fail to search mysql {}'.format(str(e)))
    

if __name__ == "__main__":
    user = User_Obj(
                u'同意拉', u'哪次不同意', u'資訊安全協會', u'打雜',u'海龍王彼得', u'091234567',''
                            )
    mySQL_ccisa = mySQL_ccisa("localhost",port=3306)
    mySQL_ccisa.connectDB( "ccisa_webfrom")
   # mySQL_ccisa = mySQL_ccisa("aclab.myds.me",port=3306)  
   # mySQL_ccisa.connectDB( "ccisadb")
    mySQL_ccisa.insert_db_data(user)
    mySQL_ccisa.deconnectDB()



