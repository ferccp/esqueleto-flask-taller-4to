from flask import Blueprint, render_template, request,redirect , url_for, jsonify, flash
from app.dao.referencial.pais.PaisDao import PaisDao

proveedormod = Blueprint('proveedormod', __name__, template_folder='templates')

@proveedormod.route('/index-proveedor')
def index_proveedor():
        return render_template('index-proveedor.html')

@proveedormod.route('/agregar-proveedor')
def agregar_proveedor():
        pdao = PaisDao()
        lista_paises = [{'id':item[0], 'descripcion':item[1]} for item in pdao.getPaises()]
        return render_template('agregar-proveedor.html', lista_paises =lista_paises if lista_paises else [])


        
     
        """
@proveedormod.route('/save-proveedor', methods=['POST'])
def save_proveedor():
        pass
           """