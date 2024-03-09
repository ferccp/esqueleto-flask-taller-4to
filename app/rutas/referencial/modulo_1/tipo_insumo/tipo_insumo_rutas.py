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

@tipoinsumomod.route('/editar-tipo-insumo/<id>') #decorador de la url
def editar_tipo_insumo(id):
        tipoinsumoencontrado = tpdao.getTipoInsumoById(id)
        if tipoinsumoencontrado:
                return render_template('editar-tipo-insumo.html', tipoinsumoencontrado = tipoinsumoencontrado)
        else:
                flash('no se puede generar la vista editar, favor llamar al admi urgente','warning')
                return redirect(url_for('tipoinsumomod.index_tipo_insumo'))



@tipoinsumomod.route('/update-tipo-insumo', methods = ['POST'])
def update_tipo_insumo():
        id = request.form['idtxttipoinsumo']
        descripcion = request.form['txttipoinsumo']
        isUpdate = False
        if descripcion != None and len(descripcion.strip()) > 0:
                isUpdate = tpdao.updateTipoInsumo(id, descripcion)
        if isUpdate:
                flash('Registro actualizado correctamente','sucess')
                return redirect(url_for('tipoinsumomod.index_tipo_insumo'))
        else:
                flash('Ocurrio un error al editar comunicarse con el  admin','warning')
                return redirect(url_for('tipoinsumomod.editar_tipo_insumo',id=id))            

@tipoinsumomod.route('/delete-tipo-insumo/<id>')
def delete_tipo_insumo(id):
        isDelete = tpdao.deleteTipoInsumo(id)
        if isDelete:
                flash('Registro eliminado','sucess')
                return redirect(url_for('tipoinsumomod.index_tipo_insumo'))
        else:
                flash('error no se pudo eliminar','warning')
                return redirect(url_for('tipoinsumomod.index_tipo_insumo'))





