from flask import current_app as app
from app.conexion.Conexion import Conexion

class InsumoDao:
	def getInsumos(self):
		querySQL = """
			select
				i.id,
				i.descripcion, 
				i.costo, 
				i.referencia_interna, 
				i.codigo_de_barras, 
				i.stock_minimo, 
				i.stock_maximo, 
				i.fecha_vecimiento, 
				i.id_tipo_insumo,ti.descripcion  as tipo_insumo, 
				i.id_unidad_medida,um.descripcion  as unidad_medida,
				i.id_impuesto,imp.descripcion as impuesto ,
				i.id_categoria,cat.descripcion as categorias,
				i.id_marca,m.descripcion as marca,
				i.id_estado,e.descripcion as estado
			from
				public.insumos i
			left join impuestos imp on imp.id = i.id_impuesto 
			left join unidad_medida um on um.id = i.id_unidad_medida 
			left join tipo_insumo ti on ti.id = i.id_tipo_insumo 
			left join categorias cat on cat.id = i.id_categoria 
			left join marcas m on m.id = i.id_marca 
			left join estados e on e.id = i.id_estado;
		"""
		conexion = Conexion()
		con = conexion.getConexion()
		cur = con.cursor()
		try:    
			cur.execute(querySQL)
			lista = cur.fetchall()
			return [{
				'id': item[0],
				'descripcion': item[1],
				'costo': item[2],
				'referencia_interna': item[3],
				'codigo_de_barras': item[4],
				'stock_minimo': item[5],
				'stock_minimo': item[6],
				'fecha_vecimiento': item[7],
				'id_tipo_insumo': item[8],
				'tipo_insumo': item[9],
				'id_unidad_medida': item[10],
				'unidad_medida': item[11],
				'id_impuesto': item[12],
				'impuesto': item[13],
				'id_categoria': item[14],
				'categorias': item[15],
				'id_marca': item[16],
				'marca': item[17],
				'id_estado': item[18],
				'estado': item[19]
				} for item in lista ] if lista else []
		except con.Error as e:
			app.logger.info(f"pgcode = {e.pgcode} , mensaje = {e.pgerror}")
		finally:
			cur.close()
			con.close()      