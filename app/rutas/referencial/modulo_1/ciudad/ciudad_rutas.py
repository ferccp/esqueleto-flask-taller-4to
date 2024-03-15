from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from app.dao.referencial.ciudad.CiudadDao import CiudadDao

ciumod = Blueprint('ciudad', __name__, template_folder='templates')

@ciumod.route('/index-ciudad')
def index_ciudad():
    cdao = CiudadDao()
    lista = cdao.getCiudades()
    diccionario = []
    if len(lista) > 0:
        for item in lista:
            diccionario.append(
                {
                    'id': item[0],
                    'descripcion': item[1]
                }
            )
    return render_template('index-ciudades.html', ciudades=diccionario)

@ciumod.route('/agregar-ciudad')
def agregar_ciudad():
    return render_template('agregar-ciudad.html')


@ciumod.route('/save-ciudad', methods=['POST'])
def save_ciudad():
    cdao = CiudadDao()
    txtciudad = request.form['txtciudad']
    isSaved = False
    if txtciudad != None and len(txtciudad.strip()) > 0:
        isSaved = cdao.insertCiudad(txtciudad.strip().upper())
    if isSaved:
        flash("Exito, se salvo correctamente", "success")
        return redirect(url_for('ciudad.index_ciudad'))
    else:
        flash("No se pudo guardar, consulta al adm", "warning")
        return redirect(url_for('ciudad.agregar_ciudad'))

@ciumod.route('/editar-ciudad/<id>')
def editar_ciudad(id):
    cdao = CiudadDao()
    ciudadFound = cdao.getCiudadById(id)
    if ciudadFound:
        return render_template('editar-ciudad.html', ciudad=ciudadFound)
    return redirect(url_for('ciudad.index_ciudad'))

@ciumod.route('/update-ciudad', methods=['POST'])
def update_ciudad():
    cdao = CiudadDao()
    idtxtciudad = request.form['idtxtciudad']
    txtciudad = request.form['txtciudad']
    isUpdated = False
    if idtxtciudad == None or len(idtxtciudad.strip()) == 0:
        return redirect(url_for('index_ciudad'))
    
    if txtciudad != None and len(txtciudad.strip()) > 0:
        isUpdated = cdao.updateCiudad(idtxtciudad.strip(), txtciudad.strip().upper())
    if isUpdated:
        return redirect(url_for('ciudad.index_ciudad'))
    else:
        return redirect(url_for('ciudad.editar_ciudad', id=idtxtciudad))

@ciumod.route('/delete-ciudad/<id>')
def delete_ciudad(id):
    cdao = CiudadDao()
    isDelete = cdao.deleteCiudad(id)
    if isDelete:
        flash("Exito, Se elimino", "success")
    else:
        flash("Error, Se elimino", "warning")
    return redirect(url_for('ciudad.index_ciudad'))

# REST
@ciumod.route('/get-ciudad')
def getCiudad():
    cdao = CiudadDao()
    lista = cdao.getCiudades()
    diccionario = []
    if len(lista) > 0:
        for item in lista:
            diccionario.append(
                {
                    'id': item[0],
                    'descripcion': item[1]
                }
            )
        return jsonify(diccionario)
    else:
        return 'no hay ciudades'
    



@ciumod.route('/get-ciudad-by-idpais/<id>')
def get_ciudad_by_idpais(id):
    cdao = CiudadDao()
    lista = cdao.getCiudadByIdPais(id)
    return jsonify([{'id':item['id'], 'text': item['descripcion']} for item in lista]), 200 if lista else 404
