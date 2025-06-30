# app/routes/general.py
from flask import Blueprint, render_template

general_bp = Blueprint('general', __name__)

@general_bp.route('/about')
def about():
    return render_template('about.html')

# Você pode adicionar outras rotas de páginas estáticas aqui (ex: /contact)