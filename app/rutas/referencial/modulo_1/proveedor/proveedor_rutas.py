from flask import Blueprint, render_template, request,redirect , url_for, jsonify, flash
from flask import current_app as app

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



@proveedormod.route('/editar-proveedor/<id_proveedor>')
def editar_proveedor(id_proveedor):
        pdao = PaisDao()
        provdto = provdao.getProveedoresByIdProveedor(id_proveedor)
        if  provdto is None:
                flash('Error al obtener proveedor', 'warning')
                return redirect(url_for('proveedormod.index_proveedor'))

     
        lista_paises = [{'id':item[0], 'descripcion':item[1]} for item in pdao.getPaisesConCiudad()]
        return render_template('editar-proveedor.html', lista_paises = lista_paises if lista_paises else [],provdto = provdto)


        


        
     
    
@proveedormod.route('/save-proveedor', methods=['POST'])
def save_proveedor():
        ruc = request.json.get('id')['txtruc']
        identificador_ruc = request.json.get('id')['txtid']
        razon = request.json.get('id')['txtrazon']
        apellido = request.json.get('id')['txtapellido']
        direccion = request.json.get('id')['txtdirección']
        email = request.json.get('id')['txtemail']
        telefono = request.json.get('id')['txttelefono']
        id_ciudad = request.json.get('id')['selciudad']
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

# Operaciones REST

@proveedormod.route('/v1/get-proveedores') 
def get_proveedores():
        return jsonify({ 'data':provdao.getProveedores() })         

@proveedormod.route('/v1/delete-proveedor', methods=['DELETE']) 
def delete_proveedor():
        id_proveedor=request.json.get('id')
        if id_proveedor:
                isDelete = provdao.deleteProveedor(id_proveedor)
        else:
                return {'success':None , 'error':None },400
        
        if isDelete:
                return {'success':'Borrado exitoso', 'error': None},200 
        else:
              return  {'success': None, 'error':'No se pudo Guardar consulte al administrador' },500

@proveedormod.route('/v1/update-proveedor', methods=['PUT'])
def update_proveedor():
        ruc = request.json.get('txtruc')
        identificador_ruc = request.json.get('txtid')
        razon = request.json.get('txtrazon')
        apellido = request.json.get('txtapellido')
        direccion = request.json.get('txtdireccion')
        email = request.json.get('txtemail')
        telefono = request.json.get('txttelefono')
        id_ciudad = request.json.get('selciudad')
        usuario_actual = 1 
        id_proveedor = request.json.get('id_proveedor')
        if not id_proveedor:
                app.logger.info({'success': None, 'error':'Falta id , consulte al administrador' })
                return  {'success': None, 'error':'Falta id , consulte al administrador' },400


        if not ruc or not identificador_ruc or not razon or not apellido or not direccion or not email or not telefono or not id_ciudad:
                return  {'success': None, 'error':'Error en cuerpo json ' },400

        dto = ProveedorDto(id_proveedor, ruc, identificador_ruc, razon, apellido, direccion, email, telefono, id_ciudad, None,None)

        isUpdate = provdao.updateProveedor(dto)
        if isUpdate:
                return {'success':'Registro actualizado', 'error': None},200 
        else:
                return  {'success': None, 'error':'No se pudo actualizar consulte al administrador' },500
  