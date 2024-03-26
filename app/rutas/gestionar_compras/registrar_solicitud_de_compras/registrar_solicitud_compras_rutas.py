from flask import Blueprint, render_template, request,redirect , url_for, jsonify, flash
from flask import current_app as app
from app.dao.referencial.estado.EstadoDao import EstadoDao
from app.dao.referencial.funcionario.FuncionarioDao import FuncionarioDao
from app.dao.referencial.prioridad.PrioridadDao import PrioridadDao
from app.dao.referencial.insumos.InsumoDao import InsumoDao



rscmod = Blueprint('rscmod',__name__, template_folder='templates')

@rscmod.route('/index-registrar-solicitud-compras')
def index_registrar_solicitud_compras():
        pass

@rscmod.route('/formulario-registrar-solicitud-compras')
def formulario_registrar_solicitud_compras():
        estado = EstadoDao()
        funci = FuncionarioDao()
        prio = PrioridadDao()
        insumo = InsumoDao()


        return render_template('formulario-registrar-solicitud-de-compras.html',estados = estado.getEsatdo(), \
                                lista_funcionarios = funci.getFuncionario(), \
                                lista_prioridades = prio.getPrioridades(), \
                                lista_insumos = insumo.getInsumos())


# REST 

@rscmod.route('/v1/get-funcionario-by-id/<id>')
def get_funcionario_by_id(id):
        funci = FuncionarioDao()
        return funci.getFuncionarioPorId(id), 200




