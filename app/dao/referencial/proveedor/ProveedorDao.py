from flask import current_app as app
from app.conexion.Conexion import Conexion
class ProveedorDto:
      def __init__(self, id, ruc , identificador_ruc , razon , apellido , direccion , email , telefono  , id_ciudad, usuario_actual,id_pais):
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
              self.id_pais = id_pais



class ProveedorDao:
        def getProveedores(self):
            querySQL = """
                SELECT p.id, ruc, ruc_nro_identificador, razon_social, apellido, direccion, email, telefono, 
           id_ciudad, c.descripcion  as nombre_ciudad,c.id_pais
           FROM public.proveedores p LEFT JOIN ciudades c on c.id=p.id_ciudad;
        """
            conexion = Conexion()
            con = conexion.getConexion()
            cur = con.cursor()
            try:    
                cur.execute(querySQL)
                lista = cur.fetchall()
                return [{
                     'id': item[0],
                     'ruc': item[1],
                     'ruc_nro_identificador': item[2],
                     'razon_social': item[3],
                     'apellido': item[4],
                     'direccion': item[5],
                     'email': item[6],
                     'telefono': item[7],
                     'id_ciudad': item[8],
                     'nombre_ciudad': item[9],
                     'id_pais':item[10]
                } for item in lista ] if lista else []
            except con.Error as e:
                 app.logger.info(f"pgcode = {e.pgcode} , mensaje = {e.pgerror}")
            finally:
                 cur.close()
                 con.close()
        
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
                app.logger.info(f"pgcode = {e.pgcode} , mensaje = {e.pgerror}")            
            finally:
                cur.close()
                con.close()
            return False
        
        def deleteProveedor(self, id):
            deleteSQL = """
              delete from public.proveedores where id = %s;
              """
            conexion = Conexion()
            con = conexion.getConexion()
            cur = con.cursor()
            try:    
                cur.execute(deleteSQL, (id,))
                con.commit()
                return True
            except con.Error as e:
                app.logger.info(f"pgcode = {e.pgcode} , mensaje = {e.pgerror}")            
            finally:
                cur.close()
                con.close()
            return False

        def updateProveedor(self, dto:ProveedorDto):
            updateSQL = """
              update public.proveedores SET
              ruc=%s, ruc_nro_identificador=%s, razon_social=%s, apellido=%s, direccion=%s,
              email=%s, telefono=%s, id_ciudad=%s, modificacion_usuario=%s, modificacion_fecha=CURRENT_DATE, modificacion_hora=CURRENT_TIME(0)   
              where id=%s;"""
            conexion = Conexion()
            con = conexion.getConexion()
            cur = con.cursor()
            try:    
                cur.execute(updateSQL, (dto.ruc,dto.identificador_ruc,dto.razon,dto.apellido,dto.direccion,dto.email,dto.telefono,dto.id_ciudad,dto.usuario_actual,dto.id,))
                con.commit()
                return True
            except con.Error as e:
                app.logger.info(f"pgcode = {e.pgcode} , mensaje = {e.pgerror}")            
            finally:
                cur.close()
                con.close()
            return False
        

        def getProveedoresByIdProveedor(self, id_proveedor) -> ProveedorDto:
            querySQL = """
                SELECT p.id, ruc, ruc_nro_identificador, razon_social, apellido, direccion, email, telefono, 
           id_ciudad,c.id_pais
           FROM public.proveedores p LEFT JOIN ciudades c on c.id=p.id_ciudad
           where p.id = %s;
        """
            conexion = Conexion()
            con = conexion.getConexion()
            cur = con.cursor()
            try:    
                cur.execute(querySQL, (id_proveedor,))
                item = cur.fetchone()
                return  ProveedorDto(item[0], item[1],item[2],item[3],item[4],item[5], item[6],item[7],item[8],None,item[9]) if item else None
            except con.Error as e:
                 app.logger.info(f"pgcode = {e.pgcode} , mensaje = {e.pgerror}")
            finally:
                 cur.close()
                 con.close()        