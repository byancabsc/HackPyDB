from app import create_app
from app.db.mssql import init_db_mssql
from app.db.postgressql import init_db_postgres
from app.db.mysql import init_db_mysql

app = create_app()

if __name__ == "__main__":
    init_db_mssql()  # Inicializa as tabelas se ainda não existirem
    init_db_postgres()  # Inicializa as tabelas se ainda não existirem
    init_db_mysql() # Inicializa as tabelas do mysql
    app.run(host="0.0.0.0", port=80, debug=True)
