from flask import Blueprint, render_template, request,redirect , url_for, jsonify, flash


iniciomod = Blueprint('iniciomod',__name__, template_folder='templates')

@iniciomod.route('/')
@iniciomod.route('/inicio')
def inicio():
        return render_template('inicio.html')