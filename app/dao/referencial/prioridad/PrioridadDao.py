from flask import current_app as app
from app.conexion.Conexion import Conexion

class PrioridadDao:
    def getPrioridades(self):
            querySQL = """SELECT id, descripcion
						FROM public.prioridades;"""
            conexion = Conexion()
            con = conexion.getConexion()
            cur = con.cursor()
            try:    
                cur.execute(querySQL)
                lista = cur.fetchall()
                return [{
                     'id': item[0],
                     'descripcion': item[1]
                } for item in lista ] if lista else []
            except con.Error as e:
                 app.logger.info(f"pgcode = {e.pgcode} , mensaje = {e.pgerror}")
            finally:
                 cur.close()
                 con.close()
