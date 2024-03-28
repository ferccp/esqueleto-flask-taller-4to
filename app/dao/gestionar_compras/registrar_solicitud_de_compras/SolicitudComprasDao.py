from flask import current_app as app
from app.conexion.Conexion import Conexion

class SolcitudCompradto:
    def __init__(self,id_solicitud: int\
                , nro_solicitud: str, id_estado: int, id_funcionario: int\
                , id_prioridad: int, current_user: int, fecha_entrega, detalle_solicitud: list) -> None:
        self.id_solicitud = id_solicitud
        self.nro_solicitud = nro_solicitud
        self.id_estado = id_estado
        self.id_funcionario = id_funcionario
        self.id_prioridad = id_prioridad
        self.current_user = current_user
        self.fecha_entrega = fecha_entrega
        self.detalle_solicitud = [] 
        
        for detalle in detalle_solicitud:
            if isinstance(detalle, SolicitudCompraDetalledto):
                self.detalle_solicitud.append(detalle)
            else:
                raise ValueError("Los elementos detalle_solicitud deben ser de tipo SolicitudCompraDetalledto")





class SolicitudCompraDetalledto:
    def __init__(self, id_solicitud: int, id_insumo: int, cantidad:int) -> None:
        self.id_solicitud = id_solicitud
        self.id_insumo = id_insumo
        self.cantidad = cantidad
    

class SolicitudComprasDao:
    def insertSolicitud(self, dto: SolcitudCompradto):

        insertSQLcabecera = """
            INSERT INTO public.solicitud_de_compra(nro_solicitud, id_estado, id_funcionario, id_prioridad, fecha_entrega,
           creacion_usuario,creacion_fecha, creacion_hora)
	        VALUES ((SELECT CONCAT('RSC',(COUNT(id_solicitud)+1)::TEXT) FROM solicitud_de_compra)
, %s, %s, %s, %s, %s, CURRENT_DATE, CURRENT_TIME(0))
            RETURNING id_solicitud
        """

        insertSQLdetalle = """
         INSERT INTO public.detalle_solicitud
            (id_solicitud, id_insumo, cantidad)
            VALUES(%s, %s, %s);
        """
        conexion = Conexion()
        con = conexion.getConexion()

        # desabilitar el autocomit
        con.autocommit = False

        cur = con.cursor()
        try:    ##dto.nro_solicitud,
            cur.execute("SET TIME ZONE GMT")
            cur.execute(insertSQLcabecera, ( dto.id_estado,dto.id_funcionario,dto.id_prioridad,dto.fecha_entrega, dto.current_user,))

            # recuperamos el id solicitud
            id_solicitud = cur.fetchone()[0]

            if not id_solicitud:
                raise Exception("No se pudo insertar en tabla solicitud_de_compra")
            
            for item in dto.detalle_solicitud:
                cur.execute(insertSQLdetalle, (id_solicitud, item.id_insumo, item.cantidad,))

            con.commit()
            return True
        except con.Error as e:
            con.rollback()
            app.logger.error(e)

        finally:
            con.autocommit = True
            cur.close()
            con.close()
        return False