from flask import Blueprint, render_template, request, redirect, url_for, session


home_bp = Blueprint('home_blueprint', __name__) # Mudei o nome do Blueprint para algo mais descritivo


@home_bp.route("/")
def home():
    # Agora, em vez de redirecionar para o login, ele vai renderizar a home.html
    return render_template('home.html')