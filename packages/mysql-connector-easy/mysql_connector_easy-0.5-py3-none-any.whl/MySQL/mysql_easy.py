
# ========================= #

# === [ Create _ connect DB ] === #

from mysql.connector import connect

# =============================== #

class MySQL :
    def __init__(self,
                 username:str,
                 password:str,
                 database:str,
                 host:str="localhost"
    ) :
        self.host = host # get host from user  
        self.username = username # get db username from user 
        self.password = password # get db password from user
        self.databasee_name = database # get db  name from user
        "''''''''''''''''''''''''"
        self.connect_database = self.connect_database
        self.database = self.connect_database
    # ========================= #
    def connect_database(self) :
        try :
            database = connect(
                host = self.host ,
                user = self.username ,
                password = self.password ,
                database = self.databasee_name
            )
            return database
        except Exception as Error :
            raise Exception(Error)
    # ========================= #

class Table(MySQL) :
    def __init__(self, username: str, password: str, database: str ,host: str = "localhost",table_name : str = "None",**kwargs):
        super().__init__(username, password, database, host)
        self.table_name = table_name ,
        self.table_keys = kwargs
        # ======================= #
        # Creaate table : .... 
        keys = list(self.table_keys.keys())
        keys_ = []
        for i in keys:
            keys_.append(f"{i} {self.table_keys[i]}")
        command = f"""CREATE TABLE IF NOT EXISTS {self.table_name[0]} (
        {', '.join(keys_)}
        )
        """
        try :
            db = self.database()
            cursor = db.cursor()
            cursor.execute(command)
            db.commit() 
            return 
        except Exception as Error :
            raise Error
    # ======================= #
    "Insert vlaue into db"      # Insert one value #
    def insert_value(self,**kwargs) :
        try :
            db = self.database()
            cursor = db.cursor()
            sql = f"INSERT INTO {self.table_name[0]} ({', '.join(list(kwargs.keys()))}) VALUE ({', '.join(['%s'] * len(kwargs)) })"
            cursor.execute(sql, tuple(kwargs.values())) 
            db.commit()
        except Exception as Error :
            raise Exception(Error)
    # ======================= #
    "Insert vlaue into db"      # Insert many value #
    def insert_values(self,values:list) :
        try :
            db = self.database()
            cursor = db.cursor()
            sql = f"INSERT INTO {self.table_name[0]} ({', '.join(list(self.table_keys.keys()))}) VALUE ({', '.join(['%s'] * len(self.table_keys)) })"
            cursor.executemany(sql, values) 
            db.commit()
        except Exception as Error :
            raise Exception(Error)

    "get all datas in the db"
    def get_values(self) -> list :
        try :
            db = self.database()
            cursor = db.cursor()
            cursor.execute(f"SELECT * FROM {self.table_name[0]}")
            result = cursor.fetchall()
            return result
        except Exception as Error :
            raise Error
    # ======================= #
    def get_value(self,key:str,value:str) :
        try :
            db = self.database()
            cursor = db.cursor()
            cursor.execute(f"SELECT * FROM {self.table_name[0]} WHERE {key} = %s",(value,))
            result = cursor.fetchall()
            return result
        except Exception as Error :
            raise Error
    # ======================= #
    def delete_values(self,key:str,value:str) :
        try :
            db = self.database()
            cursor = db.cursor()
            cursor.execute(f"DELETE FROM {self.table_name[0]} WHERE {key} = %s", (value,))
            db.commit()
            return True
        except Exception as Error :
            raise Error
# ================== #
