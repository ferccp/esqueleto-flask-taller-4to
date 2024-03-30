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
    def getSolcitudes(self):
        querySQL = """
        SELECT id_solicitud,
		nro_solicitud, 
	    sc.id_estado,
		e.descripcion as estado,
		sc.id_prioridad,p.descripcion as prioridad,
		sc.fecha_entrega,
		f.id_departamento,
		d.descripcion as departamento,
		f.id_cargo,
		c.descripcion  as cargo
FROM public.solicitud_de_compra sc
left join estados e on e.id = sc.id_estado
left join funcionarios f on f.id = sc.id_funcionario  
left join cargos c on c.id = f.id_cargo 
left join departamento d on d.id = f.id_departamento 
left join prioridades p on p.id = sc.id_prioridad 
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(querySQL)
            lista = cur.fetchall()
            return  [{ 
                'id_solicitud': item[0]
                ,'nro_solicitud': item[1]
                ,'id_estado': item[2]
                ,'estado': item[3]
                ,'id_prioridad': item[4]
                ,'prioridad': item[5]
                ,'fecha_entrega': item[6]
                ,'id_departamento': item[7]
                ,'departamento': item[8]
                ,'id_cargo': item[9]
                ,'cargo': item[10]
            }for item in lista] if lista else []
        except con.Error as e:
            app.logger.error(e)
        finally:
            cur.close()
            con.close()
        return []
    
    def getSolcitudById(self, id_solicitud):
        querySQLcabecera = """
            SELECT id_solicitud,
		nro_solicitud, 
		id_funcionario,
	    id_estado,
		id_prioridad,
		fecha_entrega::TEXT
        FROM public.solicitud_de_compra 
        where id_solicitud = %s
        """
        querySQLdetalle = """
        select 
        ds.id_solicitud, 
        ds.id_insumo, i.descripcion insumo, um.descripcion  unidad_medida,
        ds.cantidad
        from detalle_solicitud ds
        left join insumos i on i.id = ds.id_insumo 
        left join unidad_medida um on um.id = i.id_unidad_medida 
        where id_solicitud = %s
        """


        conexion = Conexion()
        con = conexion.getConexion()
        cursor_solicitud = con.cursor()
        cursor_detalle = con.cursor()
        try:
            cursor_solicitud.execute(querySQLcabecera, (id_solicitud,))
            cursor_detalle.execute(querySQLdetalle, (id_solicitud,))
            solcitud_cabecera = cursor_solicitud.fetchone()
            solicitud_detalle = cursor_detalle.fetchall()
            return { 
                'id_solicitud': solcitud_cabecera[0]
                ,'nro_solicitud': solcitud_cabecera[1]
                ,'id_funcionario': solcitud_cabecera[2]
                ,'id_estado': solcitud_cabecera[3]
                ,'id_prioridad': solcitud_cabecera[4]
                ,'fecha_entrega': solcitud_cabecera[5]
                ,'detalle_insumo':[{
                    'id_solicitud': item[0]
                    ,'id_insumo':item[1]
                    ,'insumo':item[2]
                    ,'unidad_medida':item[3]
                    ,'cantidad':item[4]} for item in solicitud_detalle]
            }
        except con.Error as e:
            app.logger.error(e)
        finally:
            cursor_solicitud.close()
            cursor_detalle.close()
            con.close()
        return {}



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
    
    def updateModificar(self, dto: SolcitudCompradto):

        updateSQLcabecera = """
            update public.solicitud_de_compra set  id_estado =%s, id_funcionario =%s, id_prioridad =%s, fecha_entrega =%s,
           modificacion_usuario =%s,modificacion_fecha =CURRENT_DATE, modificacion_hora = CURRENT_TIME(0)
           where id_solicitud =%s
        """

        deleteSQLdetalle = """
                DELETE FROM public.detalle_solicitud where id_solicitud = %s
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
            cur.execute(updateSQLcabecera, (dto.id_estado,dto.id_funcionario,dto.id_prioridad,dto.fecha_entrega, dto.current_user, dto.id_solicitud,))

            cur.execute(deleteSQLdetalle,(dto.id_solicitud,))

            for item in dto.detalle_solicitud:
                cur.execute(insertSQLdetalle, (dto.id_solicitud, item.id_insumo, item.cantidad,))

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