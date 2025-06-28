
from flask import Blueprint, render_template, request, redirect, session, url_for
from app.db.mssql import get_connection
import pyodbc


goals_bp = Blueprint('goals', __name__)

@goals_bp.route("/goal_add", methods=["GET", "POST"])

def add_goal():


    if "username" not in session:
        return redirect(url_for('auth.login'))



    if request.method == "POST":
        title = request.form["title"]
        score = request.form["score"]
        pomodoros = request.form["pomodoros"]

        try:
            #conn = pyodbc.connect(conn_str)
            conn = get_connection()
            cursor = conn.cursor()
            # Pegando user_id de forma segura
            cursor.execute("SELECT id FROM users WHERE username = ?", session["username"])
            user = cursor.fetchone()

                # Injeção possível aqui se não usar parâmetros
            query = f"""
                    INSERT INTO goals (title, productivity_score, pomodoro_count)
                    VALUES ('{title}', {score}, {pomodoros})
                """
            print("[DEBUG] Query:", query)
            cursor.execute(query)
            conn.commit()
        except Exception as e:
            return f"<h3>Erro: {str(e)}</h3>", 500
        finally:
            conn.close()

        return render_template("goal_add.html")
    return render_template("goal_add.html")



@goals_bp.route("/goal_view", methods=["GET", "POST"])
def view_goals():
    results = []
    term = ""
    conn = None
    if "username" not in session:
        return redirect(url_for('auth.login'))

    if request.method == "POST":
        term = request.form["search"]
    
    try:
        
        #conn = pyodbc.connect(conn_str)
        conn = get_connection()
        cursor = conn.cursor()

        # Vulnerável a SQLi
        query = f"""
            SELECT title, productivity_score, pomodoro_count
            FROM goals
            WHERE title LIKE '%{term}%'
        """
        print("[DEBUG] Query:", query)
        cursor.execute(query)
        results = cursor.fetchall()
        print(results)
    except Exception as e:
        return f"<h3>Erro: {str(e)}</h3>", 500
    finally:
        if conn:
            conn.close()
    print(term)
    return render_template("goal_view.html", results=results, term=term)
