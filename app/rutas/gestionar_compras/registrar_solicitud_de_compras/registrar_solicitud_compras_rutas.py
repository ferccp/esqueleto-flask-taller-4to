from flask import Blueprint, render_template, request,redirect , url_for, jsonify, flash
from flask import current_app as app

rscmod = Blueprint('rscmod',__name__, template_folder='templates')

@rscmod.route('/index-registrar-solicitud-compras')
def index_registrar_solicitud_compras():
        pass

@rscmod.route('/formulario-registrar-solicitud-compras')
def formulario_registrar_solicitud_compras():
        return render_template('formulario-registrar-solicitud-de-compras.html')
# REST



