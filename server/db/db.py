import mysql.connector
from mysql.connector import Error

# ฟังก์ชันสำหรับสร้างการเชื่อมต่อ
def create_connection():
    try:
        cnx = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="apl@992132",
            database="CPE422"
        )
        return cnx
    except Error as e:
        print(f"Error: {e}")
        return None

# ฟังก์ชันสำหรับการ query
def execute_query(query, params=None):
    cnx = create_connection()
    if cnx is None:
        return None

    try:
        cur = cnx.cursor()
        cur.execute(query, params)
        cnx.commit()  # สำหรับ query ที่มีการเปลี่ยนแปลงข้อมูล
        return cur.fetchall()  # สำหรับ query ที่เลือกข้อมูล
    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        if cnx.is_connected():
            cur.close()
            cnx.close()
