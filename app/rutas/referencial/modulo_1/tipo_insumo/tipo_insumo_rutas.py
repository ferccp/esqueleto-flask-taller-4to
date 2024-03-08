from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash # se importa las librerias necesarias
from app.dao.referencial.tipo_insumo.TipoInsumoDao import TipoInsumoDao

tipoinsumomod = Blueprint('tipoinsumomod', __name__, template_folder='templates') #__name__ hilo del sistema principal
tpdao = TipoInsumoDao() 

@tipoinsumomod.route('/index-tipo-insumo')
def index_tipo_insumo():
        lista = tpdao.getTipoInsumo()
        diccionario = []
        if len(lista) > 0:
                for item in lista:
                        diccionario.append({
                                'id':item[0],
                                'descripcion':item[1]
                        })
        return render_template('index-tipo-insumo.html',lista_tipo_insumo = diccionario)

@tipoinsumomod.route('/agregar-tipo-insumo')
def agregar_tipo_insumo():
        return render_template('agregar-tipo-insumo.html')

@tipoinsumomod.route('/save-tipo-insumo', methods=['POST'])
def save_tipo_insumo():
        tipoInsumo = request.form['txttipoinsumo']
        isSave = False
        if tipoInsumo != None and len(tipoInsumo.strip()) > 0:
                isSave = tpdao.insertTipoInsumo(tipoInsumo)
        if isSave:
                flash('Se guardo correctamente','success')
                return redirect(url_for('tipoinsumomod.index_tipo_insumo'))        
        else:
                flash('no se puedo guardar, consulta con el administrado','warning')
                return redirect(url_for('tipoinsumomod.agregar_tipo_insumo'))
