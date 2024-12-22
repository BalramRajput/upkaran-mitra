import sqlite3

class Database:
    def __init__(self, db_name):
        self.db_name = db_name

    def connect(self):
        try:
            conn = sqlite3.connect(self.db_name)
            return conn
        except sqlite3.Error as e:
            print(f"Failed to connect to the database: {e}")
            return None
    
    #for insert/update/delete
    def execute_write_query(self, query, params=()):
        conn = self.connect()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, params)
                if cursor:
                    conn.commit()
                    id = cursor.lastrowid
                else:
                    id = None
            except sqlite3.Error as e:
                print(f"Failed to execute Query: {e}")
                id = None
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
        return id
            
    
    #for single select queries
    def execute_select_one_query(self, query, params=()):
        conn = self.connect()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, params)
                if cursor:
                    result = cursor.fetchone()
                else:
                    result = None
            except sqlite3.Error as e:
                print(f"Failed to execute Query: {e}")
                result = None
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
        return result
    
    def execute_select_all_query(self, query, params=()):
        conn = self.connect()
        conn.row_factory = sqlite3.Row  # This enables column access by name
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, params)
                if cursor:
                    rows = cursor.fetchall()
                    records = [dict(row) for row in rows]  # Convert rows to dictionaries
                else:
                    records = []
            except sqlite3.Error as e:
                print(f"Failed to execute Query: {e}")
                records = []
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
        return records