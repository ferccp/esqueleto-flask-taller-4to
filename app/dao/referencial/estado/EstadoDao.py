from app.conexion.Conexion import  Conexion

class EstadoDao:
        def getEsatdo(self):
                sql = "select id, descripcion from estados"
                conexion = Conexion()
                conn = conexion.getConexion()
                cur = conn.cursor()
                try:
                        cur.execute(sql) 
                        tuplas = cur.fetchall()
                        return [{ 'id':item[0], 'descripcion': item[1] } for item in tuplas] if tuplas else []
                except conn.Error as e:
                        print( f'pgcode = { e.pgcode }, mensaje = {e.pgerror}' )
                finally:
                        cur.close()
                        conn.close()
                return None

        def inserEstado(self,descripcion):
                insertSQL = """
                INSERT INTO estados(descripcion) VALUES(%s)
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
                estadoSQL = """
                SELECT id, descripcion
	        FROM public.estados WHERE id = %s """
                conexion = Conexion()
                con = conexion.getConexion()
                cur = con.cursor()
                try:
                        cur.execute(estadoSQL, (id,))
                        estado = cur.fetchone()
                        if estado:
                                return { 'id': estado[0], 'descripcion': estado[1]}
                except con.Error as e:
                        print(f"pgcode = {e.pgcode} , mensaje = {e.pgerror}")
                finally:
                        cur.close()
                        con.close()
                return None
        
        def updateEstado(self, id, descripcion):
                updateSQL = """
		update estados set descripcion = %s where id = %s"""
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
        def deleteEstado(self, id):
                deleteSQL = """delete from estados  where id = %s"""
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
