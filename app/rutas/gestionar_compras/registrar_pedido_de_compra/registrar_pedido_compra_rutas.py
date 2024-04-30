from flask import Blueprint, render_template, request,redirect , url_for, jsonify, flash
from flask import current_app as app
from app.dao.referencial.estado.EstadoDao import EstadoDao
from app.dao.referencial.funcionario.FuncionarioDao import FuncionarioDao
from app.dao.referencial.prioridad.PrioridadDao import PrioridadDao
from app.dao.referencial.insumos.InsumoDao import InsumoDao
from app.dao.gestionar_compras.registrar_solicitud_de_compras.SolicitudComprasDao import SolicitudComprasDao,SolicitudCompraDetalledto,SolcitudCompradto



rpcmod = Blueprint('rpcmod',__name__, template_folder='templates')
#algunas instancias 
estado = EstadoDao()
funci = FuncionarioDao()
prio = PrioridadDao()
insumo = InsumoDao()
solicitud_dao = SolicitudComprasDao()



@rpcmod.route('/index-registrar-solicitud-compras')
def index_registrar_solicitud_compras():
		url_modificar = '/gestionar-compras/registrar-solicitud-compras/formulario-modificar-solicitud-compras'
		lista_solicitudes = solicitud_dao.getSolcitudes()
		if len(lista_solicitudes) < 0:
			flash('No hay solicitudes registradas', 'warning')
		return render_template('index-registrar-solicitud-de-compras.html', lista_solicitudes = lista_solicitudes, url_modificar = url_modificar)

@rpcmod.route('/formulario-registrar-pedido-compras')
def formulario_registrar_solicitud_compras():
		return render_template('formulario-registrar-pedido-de-compras.html',estados = estado.getEsatdo(), \
								lista_funcionarios = funci.getFuncionario(), \
								lista_prioridades = prio.getPrioridades(), \
								lista_insumos = insumo.getInsumos())



@rpcmod.route('/formulario-modificar-solicitud-compras/<id_solicitud>')
def formulario_modificar_solicitud_compras(id_solicitud):
		
		return render_template('formulario-modificar-solicitud-de-compras.html',estados = [ { 'id':item['id'], 'descripcion': item['descripcion']} for item in estado.getEsatdo() if item['descripcion'] in ("PENDIENTE","UTILIZADO")] , \
                                solicitud = solicitud_dao.getSolcitudById(id_solicitud), \
								lista_funcionarios = funci.getFuncionario(), \
								lista_prioridades = prio.getPrioridades(), \
								lista_insumos = insumo.getInsumos())
	


# REST 

@rpcmod.route('/v1/get-funcionario-by-id/<id>')
def get_funcionario_by_id(id):
		funci = FuncionarioDao()
		return funci.getFuncionarioPorId(id), 200


@rpcmod.route('/v1/registrar-solicitud-compra', methods=['POST'])
def registrar_solicitud_compra():
		
		#recuperar informacion
		id_estado = request.json.get('id_estado')
		id_funcionario = request.json.get('id_funcionario')
		id_prioridad = request.json.get('id_prioridad')
		fecha_entrega = request.json.get('fecha_entrega')
		detalle_insumo = request.json.get('detalle_insumo')

		# Validar 
		if not id_estado or not id_funcionario or not id_prioridad or not fecha_entrega or not detalle_insumo or len(detalle_insumo) ==0:
				app.logger.error({'success': None, 'error':'Hay errores en el payload de POST, consulte al administrador' })
				return  {'success': None, 'error':'Hay errores en el payload de POST, consulte al administrador ' },400
		detalle_insumo_dto = [ SolicitudCompraDetalledto(None, item['id_insumo'], item['cantidad']) for item in detalle_insumo ]
		dto = SolcitudCompradto(None, None, id_estado, id_funcionario, id_prioridad, 1, fecha_entrega,detalle_insumo_dto)
		isSaved = solicitud_dao.insertSolicitud(dto)
		if isSaved:
			return {'success':'Insercion exitoso', 'error': None},200 
		else:
			return  {'success': None, 'error':'No se pudo registrar solicitud de compras, consulte al administrador' },500

@rpcmod.route('/v1/modificar-solicitud-compra', methods=['PUT'])
def modificar_solicitud_compra():
		
		#recuperar informacion
		id_solicitud = request.json.get('id_solicitud')
		id_estado = request.json.get('id_estado')
		id_funcionario = request.json.get('id_funcionario')
		id_prioridad = request.json.get('id_prioridad')
		fecha_entrega = request.json.get('fecha_entrega')
		detalle_insumo = request.json.get('detalle_insumo')

		# Validar 
		if not id_solicitud or not id_estado or not id_funcionario or not id_prioridad or not fecha_entrega or not detalle_insumo or len(detalle_insumo) ==0:
				app.logger.error({'success': None, 'error':'Hay errores en el payload de PUT, consulte al administrador' })
				return  {'success': None, 'error':'Hay errores en el payload de PUT, consulte al administrador ' },400
		detalle_insumo_dto = [ SolicitudCompraDetalledto(id_solicitud, item['id_insumo'], item['cantidad']) for item in detalle_insumo ]
		dto = SolcitudCompradto(id_solicitud, None, id_estado, id_funcionario, id_prioridad, 1, fecha_entrega,detalle_insumo_dto)
		isSaved = solicitud_dao.updateModificar(dto)
		if isSaved:
			return {'success':'Modificacion exitoso', 'error': None},200 
		else:
			return  {'success': None, 'error':'No se pudo modificar solicitud de compras, consulte al administrador' },500

@rpcmod.route('/v1/anular-solicitud-compra', methods=['PUT'])
def anular_solicitud_compra():
		
		#recuperar informacion
		id_solicitud = request.json.get('id_solicitud')
		# Validar 
		isProcessed = solicitud_dao.anularSolicitud(1, id_solicitud)
		if isProcessed:
			return {'success':'Anulacion exitoso', 'error': None},200 
		else:
			return  {'success': None, 'error':'No se pudo anular solicitud de compras, consulte al administrador' },500

			
		
		



