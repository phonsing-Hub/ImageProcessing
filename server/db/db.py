import mysql.connector
from mysql.connector import Error


def create_connection():
    try:
        cnx = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="apl@992132",
            database="CPE422",
        )
        return cnx
    except Error as e:
        print(f"Error: {e}")
        return None

def execute_query(query, params=None):
    cnx = create_connection()
    if cnx is None:
        return None

    try:
        cur = cnx.cursor(dictionary=True)
        cur.execute(query, params)
        
        # Ensure all results are fetched before closing
        result = cur.fetchall()  # Fetches all rows in case there's any unread data
        cnx.commit()
        return result
    
    except Error as e:
        print(f"Error: {e}")
        return None
    
    finally:
        if cur:
            cur.close()
        if cnx.is_connected():
            cnx.close()

