from flask import Blueprint, render_template, request,redirect , url_for, jsonify, flash
from app.dao.referencial.pais.PaisDao import PaisDao
from app.dao.referencial.proveedor.ProveedorDao import ProveedorDao, ProveedorDto

proveedormod = Blueprint('proveedormod', __name__, template_folder='templates')
provdao = ProveedorDao()

@proveedormod.route('/index-proveedor')
def index_proveedor():
        return render_template('index-proveedor.html')

@proveedormod.route('/agregar-proveedor')
def agregar_proveedor():
        pdao = PaisDao()
        lista_paises = [{'id':item[0], 'descripcion':item[1]} for item in pdao.getPaisesConCiudad()]
        return render_template('agregar-proveedor.html', lista_paises = lista_paises if lista_paises else [])


        
     
    
@proveedormod.route('/save-proveedor', methods=['POST'])
def save_proveedor():
        ruc = request.form['txtruc']
        identificador_ruc = request.form['txtid']
        razon = request.form['txtrazon']
        apellido = request.form['txtapellido']
        direccion = request.form['txtdirección']
        email = request.form['txtemail']
        telefono = request.form['txttelefono']
        id_ciudad = request.form['selciudad']
        usuario_actual = 1
        dto = ProveedorDto(None,ruc,identificador_ruc,razon,apellido,direccion,email,telefono,id_ciudad,usuario_actual)
        isSave = False
        if dto.ruc and dto.identificador_ruc and dto.razon and dto.apellido and dto.direccion and dto.email and dto.telefono and dto.id_ciudad:
               isSave = provdao.insertProveedor(dto)
        if isSave:
                flash('Guardado exitoso', 'success')
                return redirect(url_for('proveedormod.index_proveedor'))
        else:
                flash('Error al guardar, consultar al admin', 'warning')
                return redirect(url_for('proveedormod.agregar_proveedor'))               
