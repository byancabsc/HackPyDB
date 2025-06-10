from flask import Flask, request, redirect
import mysql.connector

app = Flask(__name__)

@app.route('/missao')

def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, mission_name, status FROM missions")
    missions = cursor.fetchall()

    cursor.execute("SELECT message FROM flag LIMIT 1")
    flag = cursor.fetchone()

    conn.close()

    html = '''
        <h1>AdministraÃ§Ã£o de MissÃµes</h1>

        <h2>MissÃµes Cadastradas</h2>
        <table border="1" cellpadding="5">
            <tr><th>ID</th><th>Nome da MissÃ£o</th><th>Status</th></tr>
    '''
    for m in missions:
        html += f"<tr><td>{m[0]}</td><td>{m[1]}</td><td>{m[2]}</td></tr>"

    html += "</table>"

    html += '''
        <h2>Adicionar Nova MissÃ£o</h2>
        <form method="POST" action="/add">
            Nome da MissÃ£o: <input name="mission_name" required>
            Status: <input name="status" required>
            <input type="submit" value="Adicionar">
        </form>
    '''

    return html

@app.route('/add_mission', methods=['POST'])
def add_mission():
    mission_name = request.form.get('mission_name')
    status = request.form.get('status')

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # VulnerÃ¡vel a SQL Injection (intencional)
    query = f"INSERT INTO missions (mission_name, status) VALUES ('{mission_name}', '{status}')"
    cursor.execute(query)
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/search_mission')
def search():
    mission_name = request.args.get('mission_name', '')
    conn = get_db_connection()
    cursor = conn.cursor()

    # VulnerÃ¡vel a SQL Injection
    query = f"SELECT id, mission_name, status FROM missions WHERE mission_name LIKE '%{mission_name}%'"
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    # Adiciona formulÃ¡rio de busca
    html = """
    <h2>Buscar MissÃµes</h2>
    <form method="get" action="/search">
        <input type="text" name="mission_name" placeholder="Nome da missÃ£o">
        <button type="submit">Buscar</button>
    </form>
    """

    if not results:
        html += "<p>Nenhuma missÃ£o encontrada</p>"
        return html

    html += "<h2>Resultados da Busca</h2><table border='1' cellpadding='5'>"
    html += "<tr><th>ID</th><th>Nome da MissÃ£o</th><th>Status</th></tr>"
    for r in results:
        html += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    html += "</table>"

    return html


if __name__ == "__main__":
    # Rodar em 0.0.0.0 para aceitar conexÃµes externas (ex: Docker)
    app.run(host='0.0.0.0', port=5000, debug=True)