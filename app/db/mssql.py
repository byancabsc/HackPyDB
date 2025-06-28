import pyodbc

conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=sqlserver;"
    "DATABASE=master;"
    "UID=sa;"
    "PWD=YourStrong!Passw0rd"
)

def get_connection():
    return pyodbc.connect(conn_str)

def init_db_mssql():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='goals' AND xtype='U')
            CREATE TABLE goals (
                id INT IDENTITY(1,1) PRIMARY KEY,
                title NVARCHAR(255),
                productivity_score INT,
                pomodoro_count INT
            )
        ''')

        conn.commit()
    except Exception as e:
        print("[ERRO] Falha ao criar tabelas:", e)
    finally:
        conn.close()
