from flask import Blueprint, render_template, request,redirect , url_for, jsonify, flash
from flask import current_app as app
from app.dao.referencial.estado.EstadoDao import EstadoDao
from app.dao.referencial.funcionario.FuncionarioDao import FuncionarioDao
from app.dao.referencial.prioridad.PrioridadDao import PrioridadDao
from app.dao.referencial.insumos.InsumoDao import InsumoDao
from app.dao.gestionar_compras.registrar_solicitud_de_compras.SolicitudComprasDao import SolicitudComprasDao,SolicitudCompraDetalledto,SolcitudCompradto
from app.dao.referencial.proveedor.ProveedorDao import ProveedorDao
from app.dao.referencial.deposito.DepositoDao import DepostioDao
from app.dao.gestionar_compras.registrar_pedido_compra.PedidoDeCompraDao import PedidoDeCompraDao 
from flask_weasyprint import HTML, render_pdf

rpcmod = Blueprint('rpcmod',__name__, template_folder='templates')
#algunas instancias 
estado = EstadoDao()
funci = FuncionarioDao()
prio = PrioridadDao()
insumo = InsumoDao()
solicitud_dao = SolicitudComprasDao()
proveedor_dao = ProveedorDao()
depostio_dao = DepostioDao()
pedidoDao = PedidoDeCompraDao()

##Pedido externo

@rpcmod.route('/index-listar-pedido-de-compra')
def index_listar_pedido_de_compra():
		url_ver_pedido = '/gestionar-compras/registrar-pedido-compras/formulario-ver-pedido-compra'
		
		pedidoDao = PedidoDeCompraDao()
		lista = pedidoDao.getPedidosdeCompras()
		if len(lista) < 0:
			flash('No hay solicitudes registradas', 'warning')
		return render_template('index-listar-pedido-de-compra.html', lista_pedidos = lista, lista_proveedores = proveedor_dao.getProveedores() ,
						  url_ver_pedido = url_ver_pedido)

@rpcmod.route('/formulario-registrar-pedido-compras')
def formulario_registrar_solicitud_compras():
	lista_solicitudes_pendientes = solicitud_dao.getSolcitudesPendientes()
	
	return render_template('formulario-registrar-pedido-de-compras.html',estados = estado.getEsatdo(), \
								lista_funcionarios = funci.getFuncionario(), \
								lista_prioridades = prio.getPrioridades(), \
								lista_insumos = insumo.getInsumos(), \
							    lista_proveedor = proveedor_dao.getProveedores() , \
								listar_deposito = depostio_dao.getDeposito() , \
								listado_solicitudes_pendientes = lista_solicitudes_pendientes , \
								habilitarBtnRegistra = {'btnBotonPedidoRegistrar':False})

#Visualizar pedido
@rpcmod.route('/formulario-ver-pedido-compra')
@rpcmod.route('/formulario-ver-pedido-compra/<nro_pedido>')
def formulario_ver_pedido_compra(nro_pedido):
	lista_pedido_compra = pedidoDao.getPedidosDeCompraByNroPedido(nro_pedido)
	return render_template('formulario-ver-pedido-compra.html',estados = estado.getEsatdo(), \
								lista_funcionarios = funci.getFuncionario(), \
								lista_prioridades = prio.getPrioridades(), \
								lista_insumos = insumo.getInsumos(), \
							    lista_proveedor = proveedor_dao.getProveedores() , \
								listar_deposito = depostio_dao.getDeposito() , \
								listado_solicitudes_pendientes = [] , \
								habilitarBtnRegistra = {'btnBotonPedidoRegistrar':False} , \
								pedido = lista_pedido_compra
								)


@rpcmod.route('/formulario-modificar-solicitud-compras/<id_solicitud>')
def formulario_modificar_solicitud_compras(id_solicitud):
		
		return render_template('formulario-modificar-solicitud-de-compras.html',estados = [ { 'id':item['id'], 'descripcion': item['descripcion']} for item in estado.getEsatdo() if item['descripcion'] in ("PENDIENTE","UTILIZADO")] , \
                                solicitud = solicitud_dao.getSolcitudById(id_solicitud), \
								lista_funcionarios = funci.getFuncionario(), \
								lista_prioridades = prio.getPrioridades(), \
								lista_insumos = insumo.getInsumos())
	


# REST 
# Obtener solicitud de Compra
@rpcmod.route('/v1/get-solicitud-by-id/<id>')
def get_solicitudo_by_id(id):
		return solicitud_dao.getSolcitudById(id), 200

#PDF
@rpcmod.route('/generar-pedido-compra-por-proveedor', methods=['POST'])
def generar_pedido_compra_por_proveedor():
	nro_pedido=request.form['nro_pedido']
	lista_pedido_compra = pedidoDao.getPedidosDeCompraByNroPedido(nro_pedido)
	html = render_template('generar-pedido-compra.html',nro_pedido = nro_pedido ,pedido = lista_pedido_compra )
	return render_pdf(HTML(string=html))



@rpcmod.route('/v1/get-funcionario-by-id/<id>')
def get_funcionario_by_id(id):
		funci = FuncionarioDao()
		return funci.getFuncionarioPorId(id), 200


@rpcmod.route('/v1/registrar_pedido_compra', methods=['POST'])
def registrar_pedido_compra():
	print(request.json)
	pedidos = {}
	pedidos['current_user'] = 1
	pedidos['id_establecimiento'] = 1 #obtener desde de la sesion
	pedidos['id_solicitud'] = request.json.get('id_solicitud')
	pedidos['fecha_entrega_plazo_pedido'] = request.json.get('fecha_entrega_plazo_pedido')
	pedidos['pedidos_de_compras_proveedor'] = request.json.get('pedidos_de_compras_proveedor')
	isSaved = pedidoDao.registrarPedidos(pedidos)
	if isSaved:
		return {'success':' exitoso', 'error': None},200 
	else:
		return  {'success': None, 'error':'No se pudo registrar pedido de compras, consulte al administrador' },500



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
		

@rpcmod.route('/v1/actualizar-proveedor-por-pedido-compra', methods=['PUT'])
def actualizar_proveedor_por_pedido_compra():
	pedido = {}
	pedido['new_id_proveedor'] = request.json.get('new_id_proveedor')
	pedido['old_id_proveedor'] = request.json.get('old_id_proveedor')
	pedido['id_formulario_pedido_compra'] = request.json.get('id_formulario_pedido_compra')
	isProcessed = pedidoDao.actualizarProveedorPorPedido(pedido)
	if isProcessed:
		return {'success':'Cambio exitoso', 'error': None},200 
	else:
		return  {'success': None, 'error':'No se pudo anular solicitud de compras, consulte al administrador' },500
			
		
		



