from app.conexion.Conexion import Conexion
class ProveedorDto:
      def __init__(self, id, ruc , identificador_ruc , razon , apellido , direccion , email , telefono  , id_ciudad, usuario_actual):
              self.id = id  
              self.ruc = ruc
              self.identificador_ruc = identificador_ruc
              self.razon = razon
              self.apellido = apellido
              self.direccion = direccion
              self.email = email
              self.telefono = telefono
              self.id_ciudad = id_ciudad
              self.usuario_actual = usuario_actual



class ProveedorDao:
        
        def insertProveedor(self, dto:ProveedorDto):
            insertSQL = """
              INSERT INTO public.proveedores
              (ruc, ruc_nro_identificador, razon_social, apellido, direccion, email, telefono, id_ciudad, creacion_usuario, creacion_fecha, creacion_hora)
              VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_DATE,  CURRENT_TIME(0));
              """
            conexion = Conexion()
            con = conexion.getConexion()
            cur = con.cursor()
            try:    
                cur.execute(insertSQL, (dto.ruc,dto.identificador_ruc,dto.razon,dto.apellido,dto.direccion,dto.email,dto.telefono,dto.id_ciudad,dto.usuario_actual,))
                con.commit()
                return True
            except con.Error as e:
                print(f"pgcode = {e.pgcode} , mensaje = {e.pgerror}")            
            finally:
                cur.close()
                con.close()
            return False