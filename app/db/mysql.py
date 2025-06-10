import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host='db',          # nome do serviço MySQL no Docker Compose
        user='root',
        password='root',
        database='vuln_db'
    )

def init_db():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100),
                password VARCHAR(100)
            )
        ''')

        cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin123')")
        cursor.execute("INSERT INTO users (username, password) VALUES ('user', 'user123')")

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS missions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                mission_name VARCHAR(255),
                status VARCHAR(100)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS flag (
                id INT AUTO_INCREMENT PRIMARY KEY,
                message VARCHAR(255)
            )
        ''')

        cursor.execute("INSERT INTO flag (message) VALUES ('FALTA MENOS DOQ FALATAVA')")

        conn.commit()

    except mysql.connector.Error as err:
        print(f"[ERRO] Falha ao criar tabelas ou inserir dados: {err}")

    finally:
        if conn:
            cursor.close()
            conn.close()
