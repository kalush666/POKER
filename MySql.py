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

    conn.commit()
    cursor.close()
    conn.close()
    return True

create_players_table()