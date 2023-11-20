import mysql.connector

-- MySQL credentials
MYSQL_USER = "hbnb_dev"
MYSQL_PASSWORD = "hbnb_dev_pwd"

-- SQL statements
SQL_STATEMENTS = """
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';
"""

-- Connect to MySQL server
try:
    connection = mysql.connector.connect(
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        host='localhost',
        auth_plugin='mysql_native_password'
    )
    cursor = connection.cursor()

    # Execute SQL statements
    cursor.execute(SQL_STATEMENTS)
    connection.commit()

    print("MySQL server setup complete.")

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
