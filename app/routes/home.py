from flask import Blueprint, render_template, request, redirect, url_for, session


home_bp = Blueprint('/', __name__)


@home_bp.route("/")
def home():
    return redirect(url_for('auth.login'))