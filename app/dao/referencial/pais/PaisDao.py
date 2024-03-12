from app.conexion.Conexion import Conexion

class PaisDao:
        
        def getPaises(self):
              SQL = """
            SELECT id, paises
            FROM public.paises;"""
              conexion = Conexion()
              con = conexion.getConexion()
              cur = con.cursor()
              try:    
                   cur.execute(SQL)
                   lista_pais = cur.fetchall()
                   return lista_pais
              except con.Error as e:
                   print(f"pgcode = {e.pgcode} , mensaje = {e.pgerror}")
              finally:
                   cur.close()
                   con.close()

