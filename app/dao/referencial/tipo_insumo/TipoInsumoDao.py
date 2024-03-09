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
		

		def getTipoInsumoById(self, id):
			tipoInsumoSQL = """
            SELECT id, descripcion
			FROM public.tipo_insumos WHERE id = %s """
			conexion = Conexion()
			con = conexion.getConexion()
			cur = con.cursor()
			try:    
				cur.execute(tipoInsumoSQL, (id,))
				tipoinsumo = cur.fetchone()
				if tipoinsumo:
					return { 'id': tipoinsumo[0], 'descripcion': tipoinsumo[1]}
			except con.Error as e:
					print(f"pgcode = {e.pgcode} , mensaje = {e.pgerror}")
			finally:
				cur.close()
				con.close()
			return None



		
		def updateTipoInsumo(self, id, descripcion):
				updateSQL = """
				update tipo_insumos set descripcion = %s where id = %s
				"""
				conexion = Conexion()
				conn = conexion.getConexion()
				cur = conn.cursor()
				try:
					cur.execute(updateSQL, (descripcion,id,))
					conn.commit()
					return True
				except conn.Error as e:
					print(f"pgcode = {e.pgcode} , mensaje = {e.pgerror}")
				finally:
					cur.close()
					conn.close()
				return False
		
  
		def deleteTipoInsumo(self, id):
				deleteSQL = """
				delete from tipo_insumos  where id = %s
				"""
				conexion = Conexion()
				conn = conexion.getConexion()
				cur = conn.cursor()
				try:
					cur.execute(deleteSQL, (id,))
					conn.commit()
					return True
				except conn.Error as e:
					print(f"pgcode = {e.pgcode} , mensaje = {e.pgerror}")
				finally:
					cur.close()
					conn.close()
				return False
		
  




