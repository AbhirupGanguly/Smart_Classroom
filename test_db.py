import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123"   # put your mysql password here
    )

    if conn.is_connected():
        print("✅ Successfully connected to MySQL!")

except mysql.connector.Error as e:
    print("❌ Error:", e)

finally:
    if 'conn' in locals() and conn.is_connected():
        conn.close()
        print("Connection closed.")