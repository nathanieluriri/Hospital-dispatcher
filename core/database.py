import sqlite3
database_name ="db.db"


class DBFunctions:
    def __init__(self, table_name):
        self.table_name = table_name

    @staticmethod
    def __insert(table_name: str, data: dict):
        # Basic validation (optional but recommended)
        if not table_name.isidentifier():
            raise ValueError("Invalid table name")

        keys = ", ".join(data.keys())
        placeholders = ", ".join("?" for _ in data)
        values = tuple(data.values())

        query = f"INSERT INTO {table_name} ({keys}) VALUES ({placeholders})"

        with sqlite3.connect(database_name) as conn:
            cursor = conn.cursor()
            cursor.execute(query, values)
            return cursor.lastrowid
            
            
    @staticmethod
    def __update(table_name: str, data: dict, filter_dict: dict):
        # Basic validation
        if not table_name.isidentifier():
            raise ValueError("Invalid table name")

        # Build SET part of query
        set_clause = ", ".join([f"{k} = ?" for k in data.keys()])
        # Build WHERE part of query
        where_clause = " AND ".join([f"{k} = ?" for k in filter_dict.keys()])

        # Combine all values
        values = list(data.values()) + list(filter_dict.values())

        query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"

        with sqlite3.connect(database_name) as conn:
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
            return cursor.rowcount
        
    @staticmethod
    def __delete(table_name: str, filter_dict: dict,):
        if not table_name.isidentifier():
            raise ValueError("Invalid table name")

        where_clause = " AND ".join([f"{k} = ?" for k in filter_dict])
        values = list(filter_dict.values())

        query = f"DELETE FROM {table_name} WHERE {where_clause}"

        with sqlite3.connect(database_name) as conn:
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
            return cursor.rowcount  # Number of rows deleted
        
                
    def insert_one(self,data:dict)->str:
            """inserts data into the datatbase 

            Args:
                data (dict): this is the data you are inserting

            Returns:
                str: unique id
            """
            id = self.__insert(table_name=self.table_name,data=data)
            return id
        
    def update_one(self,filter_dict:dict,data:dict)->int:
        """updates one table

        Args:
            filter_dict (dict): filter_dict is used to find the table you want to update
            data (dict): this is the stuff that is going to replace or update whatever is there already

        Returns:
            int: Number of rows affected 
        """
        value = self.__update(filter_dict=filter_dict,table_name=self.table_name,data=data)
        return value
    

    
    def delete_one(self,filter_dict:dict)->int:
        """deletes by finding what should be deleted 

        Args:
            filter_dict (dict): any key value pair in the database

        Returns:
            int: number of rows affected
        """
        rows = self.__delete(table_name=self.table_name,filter_dict=filter_dict)
        return rows
    

    def find(self)->list:
        """Returns a list to iterate over multiple documents (unlike find_one).

        Raises:
            ValueError: _description_

        Returns:
            list: iterate over to view the documents
        """
        if not self.table_name.isidentifier():
            raise ValueError("Invalid table name")  # Prevent SQL injection

        with sqlite3.connect(database_name) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            query = f"SELECT * FROM {self.table_name}"
            cursor.execute(query)
            results = cursor.fetchall()

            return [dict(row) for row in results]
        
    def find_one(self,filter_dict:dict)->dict:
        """returns a single document from the filter

        Args:
            filter_dict (dict): this is how we find what you are looking for

        Raises:
            ValueError: if you don't enter anything in filter or its not a dictionary 

        Returns:
            dict: returns the data from the database in a dictionary
        """
        if not filter_dict:
            raise ValueError("Filter dictionary cannot be empty.")
        with sqlite3.connect(database_name) as conn:
            conn.row_factory = sqlite3.Row  # Optional: return dict-like rows
            cursor = conn.cursor()
            where_clause = " AND ".join(f"{key} = ?" for key in filter_dict)
            values = tuple(filter_dict.values())
            # Use parameterized query with ?
            query = f"SELECT * FROM {self.table_name} WHERE {where_clause} LIMIT 1"
            cursor.execute(query, values)
            row = cursor.fetchone()
            return dict(row) if row else None
        
        

class DBWrapper:
    def __getattr__(self, table_name):
        return DBFunctions(table_name=table_name)
        
        


db = DBWrapper()

