from app.conexion.Conexion import Conexion

class CargoDao:
        def getCargo(self):
                cargoSQL = """ select * from cargos """
                conexion = Conexion()
                con = conexion.getConexion()
                cur = con.cursor()
                try:
                    cur.execute(cargoSQL)
                    lista = cur.fetchall()
                    return lista
                except con.Error as e:
                      print(f"pgcode = {e.pgcode} , mensaje = {e.pgerror}")
                finally:
                       cur.close()
                       con.close()

        def getCargoById(self, id):
               cargoSQL =""" select * from cargos where id = %s """
               conexion = Conexion()
               con = conexion.getConexion()
               cur = con.cursor()
               try:
                      cur.execute(cargoSQL, (id),)
                      cargo = cur.fetchone()
                      if cargo:
                              return { 'id': cargo[0], 'descripcion': cargo[1]}
                      return None
               except con.Error as e:
                       print(f"pgcode = {e.pgcode} , mensaje = {e.pgerror}")            
               finally:
                       cur.close()
                       con.close()   

               
               
            
                      
                        
                        
                        
                    