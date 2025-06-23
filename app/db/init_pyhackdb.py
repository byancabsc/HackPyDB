import psycopg2
import os
import time

def get_app_db_connection():
    """
    Função para estabelecer conexão com o banco de dados PostgreSQL da APLICAÇÃO.
    As credenciais são obtidas das variáveis de ambiente definidas no docker-compose.yml
    para o serviço 'postgres_app'.
    """
    return psycopg2.connect(
                host=os.getenv('DB_HOST', 'postgres_app'),
                database=os.getenv('DB_NAME', 'pyhackdb_system_db'),
                user=os.getenv('DB_USER', 'postgres'),
                password=os.getenv('DB_PASS', 'postgres'),
                port=int(os.getenv('DB_PORT', 5432))
            )

def init_app_db_postgres():
    """
    Inicializa o esquema do banco de dados PostgreSQL para a aplicação principal.
    Cria a tabela 'users' para autenticação de alunos.
    """
    conn = None
    cur = None
    try:
        conn = get_app_db_connection()
        if conn is None:
            print("[ERRO] Não foi possível obter conexão com o DB da aplicação para inicialização.")
            return

        cur = conn.cursor()


        # Criação da tabela 'users' para autenticação de alunos
        cur.execute(''' 
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        print("[INFO] Tabela 'users' verificada/criada.")

        # Opcional: Inserir um usuário administrador padrão se a tabela estiver vazia
        cur.execute("SELECT COUNT(*) FROM users;")
        if cur.fetchone()[0] == 0:
            # Em um sistema real, a senha deveria ser HASHED e SALTED.
            # Aqui é para fins de exemplo e estudo.
            admin_username = os.getenv('ADMIN_USERNAME', 'admin')
            admin_password = os.getenv('ADMIN_PASSWORD', 'adminpass')
            admin_email = os.getenv('ADMIN_EMAIL', 'admin@pyhackdb.com')

            cur.execute(
                "INSERT INTO users (username, password, email) VALUES (%s, %s, %s);",
                (admin_username, admin_password, admin_email)
            )
            print(f"[INFO] Usuário administrador padrão '{admin_username}' inserido.")

        # Adicione outras tabelas necessárias para sua aplicação aqui, por exemplo:
        # cur.execute('''
        #     CREATE TABLE IF NOT EXISTS cursos (
        #         id SERIAL PRIMARY KEY,
        #         nome VARCHAR(255) NOT NULL,
        #         descricao TEXT
        #     );
        # ''')
        # print("[INFO] Tabela 'cursos' verificada/criada.")


        conn.commit()
        print("[OK] Banco de dados 'pyhackdb_system_db' (para a aplicação) inicializado com sucesso!")

    except psycopg2.Error as e:
        print(f"[ERRO] Falha ao inicializar o esquema do DB da aplicação (PostgreSQL): {e}")
        if conn:
            conn.rollback() # Desfaz qualquer transação em caso de erro
    except Exception as e:
        print(f"[ERRO] Erro inesperado ao inicializar o DB da aplicação: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
            print("[INFO] Conexão ao DB da aplicação fechada.")
