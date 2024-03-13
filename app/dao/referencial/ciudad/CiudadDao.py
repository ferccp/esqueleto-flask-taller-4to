from app.conexion.Conexion import Conexion
class CiudadDao:
    
    def getCiudades(self):
        
        ciudadSQL = """
            SELECT id, descripcion
            FROM ciudades
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:    
            cur.execute(ciudadSQL)
            lista_ciudades = cur.fetchall()
            return lista_ciudades
        except con.Error as e:
            print(f"pgcode = {e.pgcode} , mensaje = {e.pgerror}")            

        finally:
            cur.close()
            con.close()
            
    def getCiudadById(self, id):
        
        ciudadSQL = """
            SELECT id, descripcion
            FROM ciudades WHERE id = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:    
            cur.execute(ciudadSQL, (id,))
            ciudad = cur.fetchone()
            if ciudad:
                return { 'id': ciudad[0], 'descripcion': ciudad[1]}
            return None
        except con.Error as e:
            print(f"pgcode = {e.pgcode} , mensaje = {e.pgerror}")            

        finally:
            cur.close()
            con.close()
            
    def insertCiudad(self, descripcion):
        
        insertSQL = """
            INSERT INTO ciudades(descripcion) VALUES(%s)
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:    
            cur.execute(insertSQL, (descripcion,))
            con.commit()
            return True
        except con.Error as e:
            print(f"pgcode = {e.pgcode} , mensaje = {e.pgerror}")            

        finally:
            cur.close()
            con.close()
        return False
    
    def updateCiudad(self, id, descripcion):
        
        updateSQL = """
            UPDATE ciudades SET descripcion = %s WHERE id = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:    
            cur.execute(updateSQL, (descripcion, id,))
            con.commit()
            return True
        except con.Error as e:
            print(f"pgcode = {e.pgcode} , mensaje = {e.pgerror}")            

        finally:
            cur.close()
            con.close()
        return False
    
    def deleteCiudad(self, id):
        
        deleteSQL = """
            DELETE FROM ciudades WHERE id = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:    
            cur.execute(deleteSQL, (id,))
            con.commit()
            return True
        except con.Error as e:
            print(f"pgcode = {e.pgcode} , mensaje = {e.pgerror}")            

        finally:
            cur.close()
            con.close()
        return False
    
    def getCiudadByIdPais(self, id):
        
        querySQL = """
            SELECT id, descripcion
            FROM ciudades WHERE id_pais = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:    
            cur.execute(querySQL, (id,))
            lista = cur.fetchall()
            return [{'id': item[0], 'descripcion': item[1]} for item in lista] if lista else []  ##
        except con.Error as e:
            print(f"pgcode = {e.pgcode} , mensaje = {e.pgerror}")            

        finally:
            cur.close()
            con.close()
            