from flask import Flask

app = Flask(__name__)
app.secret_key = b'123'

##inicio principal
from app.rutas.inicio.inicio_rutas import iniciomod


# referenciales
from app.rutas.referencial.modulo_1.ciudad.ciudad_rutas import ciumod
from app.rutas.referencial.modulo_1.tipo_insumo.tipo_insumo_rutas import tipoinsumomod
from app.rutas.referencial.modulo_1.estado.estado_rutas import estadomod
from app.rutas.referencial.modulo_1.proveedor.proveedor_rutas import proveedormod 

#gestionar compras

from app.rutas.gestionar_compras.registrar_solicitud_de_compras.registrar_solicitud_compras_rutas import rscmod
from app.rutas.gestionar_compras.registrar_pedido_de_compra.registrar_pedido_compra_rutas import rpcmod



#inicio 
app.register_blueprint(iniciomod, url_prefix=f'/')



modulo0 = '/referencial'
app.register_blueprint(ciumod, url_prefix=f'{modulo0}/ciudad')
app.register_blueprint(tipoinsumomod, url_prefix=f'{modulo0}/tipo-insumo')
app.register_blueprint(estadomod,url_prefix=f'{modulo0}/estado')
app.register_blueprint(proveedormod,url_prefix=f'{modulo0}/proveedor')

modulo1 = '/gestionar-compras'
app.register_blueprint(rscmod, url_prefix=f'{modulo1}/registrar-solicitud-compras')
app.register_blueprint(rpcmod, url_prefix=f'{modulo1}/registrar-pedido-compras')

#