from app.conexion.Conexion import Conexion #app.conexion(paquete) .Conexion(Modulo) import Conexion(clase)

class TipoInsumoDao:
		def getTipoInsumo(self):
				sql = "select * from tipo_insumos"
				conexion = Conexion()
				conn = conexion.getConexion()
				cur = conn.cursor()
				try:
						cur.execute(sql)
						return cur.fetchall()
				except conn.Error as e:
						print( f'pgcode = { e.pgcode }, mensaje = {e.pgerror}' )
				finally:
						cur.close()
						conn.close()
				return None
		

		def insertTipoInsumo(self, descripcion):
				insertSQL = """
				INSERT INTO tipo_insumos(descripcion) VALUES(%s)
				"""
				conexion = Conexion()
				conn = conexion.getConexion()
				cur = conn.cursor()
				try:
					cur.execute(insertSQL, (descripcion,))
					conn.commit()
					return True
				except conn.Error as e:
					print(f"pgcode = {e.pgcode} , mensaje = {e.pgerror}")
				finally:
					cur.close()
					conn.close()
				return False

		
		            



