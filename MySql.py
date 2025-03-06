import mysql.connector
import hashlib


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


def create_tables():
    """Create necessary tables if they don't exist"""
    conn = create_connection()
    if not conn:
        return False

    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        balance DECIMAL(10, 2) DEFAULT 1000.00,
        date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Create game_history table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS game_history (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        session_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        starting_balance DECIMAL(10, 2),
        ending_balance DECIMAL(10, 2),
        hands_played INT DEFAULT 0,
        hands_won INT DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    # Create financial_goals table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS financial_goals (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        goal_name VARCHAR(100) NOT NULL,
        target_amount DECIMAL(10, 2) NOT NULL,
        current_amount DECIMAL(10, 2) DEFAULT 0.00,
        date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        target_date DATE,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    cursor.close()
    conn.close()
    return True


def hash_password(password):
    """Simple password hashing"""
    return hashlib.sha256(password.encode()).hexdigest()


def sign_up(username, password):
    # Create tables if they don't exist
    create_tables()

    conn = create_connection()
    if not conn:
        return False

    cursor = conn.cursor()
    hashed_password = hash_password(password)

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)",
                       (username, hashed_password))
        conn.commit()
        result = True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        result = False
    finally:
        cursor.close()
        conn.close()

    return result


def login(username, password):
    conn = create_connection()
    if not conn:
        return None

    cursor = conn.cursor(dictionary=True)
    hashed_password = hash_password(password)

    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s",
                   (username, hashed_password))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user


def update_balance(user_id, new_balance):
    conn = create_connection()
    if not conn:
        return False

    cursor = conn.cursor()

    try:
        cursor.execute("UPDATE users SET balance = %s WHERE id = %s",
                       (new_balance, user_id))
        conn.commit()
        result = True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        result = False
    finally:
        cursor.close()
        conn.close()

    return result


def save_game_session(user_id, starting_balance, ending_balance, hands_played, hands_won):
    conn = create_connection()
    if not conn:
        return False

    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO game_history 
        (user_id, starting_balance, ending_balance, hands_played, hands_won) 
        VALUES (%s, %s, %s, %s, %s)
        """, (user_id, starting_balance, ending_balance, hands_played, hands_won))
        conn.commit()
        result = True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        result = False
    finally:
        cursor.close()
        conn.close()

    return result


def create_financial_goal(user_id, goal_name, target_amount, target_date=None):
    conn = create_connection()
    if not conn:
        return False

    cursor = conn.cursor()

    try:
        if target_date:
            cursor.execute("""
            INSERT INTO financial_goals 
            (user_id, goal_name, target_amount, target_date) 
            VALUES (%s, %s, %s, %s)
            """, (user_id, goal_name, target_amount, target_date))
        else:
            cursor.execute("""
            INSERT INTO financial_goals 
            (user_id, goal_name, target_amount) 
            VALUES (%s, %s, %s)
            """, (user_id, goal_name, target_amount))
        conn.commit()
        result = True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        result = False
    finally:
        cursor.close()
        conn.close()

    return result
