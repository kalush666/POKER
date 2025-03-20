import mysql.connector


def create_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="jonathan06",
            database="pokerdb"
        )
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None


def create_players_table():
    conn = create_connection()
    if not conn:
        return False

    cursor = conn.cursor()

    # Create players table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS players (
        id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        age INT NOT NULL,
        phone_number VARCHAR(15),
        email VARCHAR(100),
        score INT NOT NULL,
        date DATE NOT NULL,
        time TIME NOT NULL
    )
    """)

    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL UNIQUE,
        password VARCHAR(100) NOT NULL
    )
    """)

    conn.commit()
    cursor.close()
    conn.close()
    return True


def sign_up(username, password):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            raise
        finally:
            cursor.close()
            connection.close()


def login(username, password):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            result = cursor.fetchone()
            return result is not None
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
        finally:
            cursor.close()
            connection.close()
    return False