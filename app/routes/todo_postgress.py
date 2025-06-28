from flask import Blueprint, request, redirect, render_template, session, url_for
from app.db.postgres_vuln import get_db_connection



todo_bp = Blueprint('todo', __name__)

@todo_bp.route('/todo_add', methods=['GET', 'POST'])
def adicionar_tarefa():
    
    if "username" not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        titulo = request.form.get('titulo')
        status = request.form.get('status')
        
        print(titulo,status)
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            #cursor.execute("INSERT INTO tarefas (titulo, status) VALUES (%s, %s)", (titulo, status)) # Secure Code
            query = f"INSERT INTO tarefas (titulo, status) VALUES ('{titulo}', '{status}')" #Insecure query
            cursor.execute(query) # Insecure query

            conn.commit()
        except Exception as e:
            print(f"Erro ao inserir tarefa: {e}")
        finally:
            cursor.close()
            conn.close()
        

        return redirect('/todo_add')  # <- ESSE RETURN TEM QUE EXISTIR

    # GET: renderiza a lista
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tarefas ORDER BY id DESC")
        tarefas = cursor.fetchall()
    except Exception as e:
        print(f"Erro ao buscar tarefas: {e}")
        tarefas = []
    finally:
        cursor.close()
        conn.close()

    return render_template("todo_task.html", tarefas=tarefas)

@todo_bp.route('/todo_find', methods=['GET'])
def buscar():
    
    if "username" not in session:
        return redirect(url_for('auth.login'))
    
    termo = request.args.get('q', '')


    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # VULNERABILIDADE SQL INJECTION AQUI
        query = f"SELECT * FROM tarefas WHERE titulo LIKE '%{termo}%'"
        cursor.execute(query)
        resultados = cursor.fetchall()
    except Exception as e:
        return f"Erro: {e}"
    finally:
        cursor.close()
        conn.close()

    # Retorna dados visíveis — ideal para sqlmap
    return render_template('todo_find.html', tarefas=resultados)
    #return str(resultados)

@todo_bp.route('/todo_concluir/<int:id>', methods=['POST'])
def concluir_tarefa(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tarefas SET status = 'concluido' WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/todo_find')

@todo_bp.route('/todo_pendente/<int:id>', methods=['POST'])
def pendente_tarefa(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tarefas SET status = 'pendente' WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/todo_find')

@todo_bp.route('/todo_excluir/<int:id>', methods=['POST'])
def excluir_tarefa(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tarefas WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/todo_find')



    