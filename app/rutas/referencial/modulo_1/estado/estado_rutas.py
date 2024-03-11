from flask import Blueprint, render_template, request,redirect , url_for, jsonify, flash
from app.dao.referencial.estado.EstadoDao import EstadoDao

estadomod = Blueprint('estadomod', __name__, template_folder='templates')
edao = EstadoDao()

@estadomod.route('/index-estado')
def index_estado():
        lista = edao.getEsatdo()
        diccionario = []
        if len(lista) > 0:
                for item in lista:
                        diccionario.append({
                                'id' : item[0],
                                'descripcion' : item[1]
                        })
        return render_template('index-estado.html',lista_estado = diccionario)

@estadomod.route('/agregar-estado')
def agregar_estado():
        return render_template('agregar-estado.html')

@estadomod.route('/save-estado', methods=['POST'])
def save_estado():
        estado = request.form['txtestado']
        isSave = False
        if estado != None and len(estado.strip()) > 0:
                isSave = edao.inserEstado(estado)
        if isSave:
                flash('Se guardo correctamente','success')
                return redirect(url_for('estadomod.index_estado')) 
        else:
                flash('no se puedo guardar, consulta con el administrado','warning')
                return redirect(url_for('estadomod.agregar_estado'))                



@estadomod.route('/editar-estado/<id>')
def editar_estado(id):
        estadoecontrado = edao.getTipoInsumoById(id)
        if estadoecontrado:
                return render_template('editar-estado.html', estadoecontrado = estadoecontrado)
        else:
                flash('no se puede generar la vista editar, favor llamar al admi urgente','warning')
                return redirect(url_for('estadomod.index_estado'))   

@estadomod.route('/update-estado', methods = ['POST'])
def update_estado():
        id = request.form['idtxtestado']
        estado = request.form['txttdescripcion']
        isUpdate = False
        if estado != None and len(estado.strip()) > 0:
                isUpdate = edao.updateEstado(id, estado)
        if isUpdate:
                flash('Registro actualizado correctamente','sucess')
                return redirect(url_for('estadomod.index_estado'))
        else:
                flash('Ocurrio un error al editar comunicarse con el  admin','warning')
                return redirect(url_for('estadomod.editar_estado',id=id))   


         
@estadomod.route('/delete-estado/<id>')
def delete_estado(id):
        isDelete = edao.deleteEstado(id)
        if isDelete:
                flash('Registro eliminado','sucess')
                return redirect(url_for('estadomod.index_estado'))
        else:
                flash('error no se pudo eliminar','warning')
                return redirect(url_for('estadomod.index_estado'))
     

        
