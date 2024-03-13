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

        def getPaisesConCiudad(self):
              SQL = """
            SELECT id, p.paises as  descripcion FROM paises p 
            WHERE EXISTS(SELECT 1 FROM ciudades c WHERE c.id_pais = p.id);"""
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

