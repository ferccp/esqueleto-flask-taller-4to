from flask import current_app as app
from app.conexion.Conexion import Conexion

class DepostioDao:
    def getDeposito(self):
        sql = "SELECT id, descripcion, limite_fisico_insumo FROM public.depositos;"
        conexion = Conexion()
        conn = conexion.getConexion()
        cur = conn.cursor()
        try:
            cur.execute(sql)
            lista = cur.fetchall()
            return [{
                'id': item[0],
                'descripcion': item[1]
            } for item in lista ] if lista else []
        except conn.Error as e:
            app.logger.info(f"pgcode = {e.pgcode} , mensaje = {e.pgerror}")
        finally:
            cur.close()
            conn.close()
            
	