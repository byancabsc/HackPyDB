from flask import Blueprint, render_template, request, redirect, session, url_for


vuln_bp = Blueprint('vuln', __name__, url_prefix='/vuln')

@vuln_bp.route('/sqli',methods=['GET', 'POST'])
def sqli_page():

    return render_template('vulns_panel/sqli.html')