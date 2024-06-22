from flask import current_app as app
from app.conexion.Conexion import Conexion


class PedidoDeCompraDao:
    def getPedidosDeCompraByNroPedido(self, nro_pedido):
        querySQLcabecera = """select b.id_formulario_pedido_compras,
                b.id_proveedor ,
                concat('( ', p.ruc,'-',p.ruc_nro_identificador,' ) ', p.razon_social) as ruc_iden,
                b.id_estado ,
                e.descripcion as estado_pedido,
                sdc.id_solicitud,
                sdc.nro_solicitud,
                b.nro_solicitud_compra,
                b.creacion_fecha,
                a.fecha_entrega_plazo_pedido
                from public.formulario_pedido_compras a
                join solicitud_de_compra sdc on sdc.id_solicitud = a.id_solicitud
                join pedidos_de_compras_proveedor b on 
                a.id_formulario_pedido_compras = b.id_formulario_pedido_compras 
                join proveedores p on p.id = b.id_proveedor 
                join estados e on e.id = b.id_estado
                 where b.nro_solicitud_compra = %s order by b.nro_solicitud_compra  desc;"""
        
        querySQLdetalle = """select  concat('( ',i.id,' ) ', trim(i.descripcion)) as insumos,
          um.descripcion as unidad_medida,
                    dpdc.cantidad ,d.descripcion  as deposito
                    from pedidos_de_compras_proveedor  pdcp
                    join proveedores p2 on p2.id = pdcp.id_proveedor 
                    join detalle_pedido_de_compras dpdc  
                    on dpdc.id_proveedor = pdcp.id_proveedor 
                    and p2.id = dpdc.id_proveedor 
                    join insumos i on i.id = dpdc.id_insumo
                    join unidad_medida um on um.id = i.id_unidad_medida 
                    join depositos d on d.id = dpdc.id_deposito 
                    join estados e on e.id = pdcp.id_estado 
                    where pdcp.nro_solicitud_compra = %s"""
        conexion = Conexion()
        con = conexion.getConexion()
        cursor_solcitud = con.cursor()
        cursor_detalle = con.cursor()
        try:
            cursor_solcitud.execute(querySQLcabecera, (nro_pedido,))
            cursor_detalle.execute(querySQLdetalle, (nro_pedido,) )
            pedido_solicitud = cursor_solcitud.fetchone()
            pedido_detalle = cursor_detalle.fetchall()
            return {
                'id_formulario_pedido_compras': pedido_solicitud[0]
                ,'id_proveedor': pedido_solicitud[1]
                ,'ruc_iden': pedido_solicitud[2]
                ,'id_estado': pedido_solicitud[3]
                ,'estado_pedido': pedido_solicitud[4]
                ,'id_solicitud': pedido_solicitud[5]
                ,'nro_solicitud': pedido_solicitud[6]
                ,'nro_solicitud_compra': pedido_solicitud[7]
                ,'creacion_fecha': pedido_solicitud[8]
                ,'fecha_entrega_plazo_pedido': pedido_solicitud[9]
                ,'detalle_pedido':[{
                    'insumos':item[0]
                    ,'unidad_medida':item[1]
                    ,'cantidad':item[2]
                    ,'deposito':item[3]} for item in pedido_detalle]
            }
        except Exception as e:
            app.logger.error(e)
        finally:
            cursor_solcitud.close()
            cursor_detalle.close()
        return []
    
    def getPedidosdeCompras(self):
        querySQL = """select b.id_formulario_pedido_compras,
                b.id_proveedor ,
                concat('( ', p.ruc,'-',p.ruc_nro_identificador,' ) ', p.razon_social) as ruc_iden,
                b.id_estado ,
                e.descripcion as estado_pedido,
                sdc.id_solicitud,
                sdc.nro_solicitud,
                b.nro_solicitud_compra,
                b.creacion_fecha,
                a.fecha_entrega_plazo_pedido
                from public.formulario_pedido_compras a
                join solicitud_de_compra sdc on sdc.id_solicitud = a.id_solicitud
                join pedidos_de_compras_proveedor b on 
                a.id_formulario_pedido_compras = b.id_formulario_pedido_compras 
                join proveedores p on p.id = b.id_proveedor 
                join estados e on e.id = b.id_estado  order by b.nro_solicitud_compra  desc;"""
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(querySQL)
            lista = cur.fetchall()
            return [{
                'id_formulario_pedido_compras': item[0],
                'id_proveedor': item[1],
                'ruc_iden': item[2],
                'id_estado': item[3],
                'estado_pedido': item[4],
                'id_solicitud': item[5],
                'nro_solicitud': item[6],
                'nro_solicitud_compra': item[7],
                'creacion_fecha': item[8],
                'fecha_entrega_plazo_pedido': item[9],
            } for item in lista ] if lista else []
        except Exception as e:
            app.logger.error(e)
        finally:
            cur.close()
            con.close()
        return []
        
    



    def actualizarProveedorPorPedido(self, pedido):
             updatePedidoCompraProveedorSQL = """  UPDATE public.pedidos_de_compras_proveedor 
             SET id_proveedor = %s
             where id_formulario_pedido_compras = %s and id_proveedor = %s
             """
             conexion = Conexion()
             con = conexion.getConexion()
             cur = con.cursor()
             try:
                 cur.execute(updatePedidoCompraProveedorSQL,(pedido['new_id_proveedor'], pedido['id_formulario_pedido_compra'], pedido['old_id_proveedor'],))
                 con.commit()
                 return True
             except con.Error as e:
                app.logger.error(e)
             finally:
                cur.close()
                con.close()
             return False
                




    def registrarPedidos(self, pedidos):
        #inserta y recupera el id generado
        insertSQLFormularioPedidoCompras = """ INSERT INTO public.formulario_pedido_compras
        (id_establecimiento, id_solicitud, fecha_entrega_plazo_pedido, creacion_usuario, creacion_fecha, creacion_hora)
        VALUES( %s, %s, %s, %s ,CURRENT_DATE, CURRENT_TIME(0)) RETURNING id_formulario_pedido_compras
        """
        insertarPedidoComprasProveedor = """
        INSERT INTO 
        public.pedidos_de_compras_proveedor(id_formulario_pedido_compras, id_proveedor, id_estado, creacion_usuario, creacion_fecha, creacion_hora, nro_solicitud_compra)
        VALUES(%s, %s, %s, %s ,CURRENT_DATE, CURRENT_TIME(0), (SELECT CONCAT('RPC', LPAD((COUNT(id_formulario_pedido_compras) + 1)::TEXT, 6, '0'))
FROM public.pedidos_de_compras_proveedor pdcp))"""

        insertarDetallePedidosCompras = """
        INSERT INTO public.detalle_pedido_de_compras
            (id_formulario_pedido_compras, id_proveedor, id_insumo, id_deposito, cantidad)
            VALUES(%s, %s, %s, %s, %s)"""
        
        conexion = Conexion()
        con = conexion.getConexion()

        #deshabilitar el autocommit
        con.autocommit = False
        cur = con.cursor()
        try:
            creacion_usuario = pedidos['current_user']
            
            parametroFormularioPedidoCompras = (pedidos['id_establecimiento'],pedidos['id_solicitud'],pedidos['fecha_entrega_plazo_pedido'],creacion_usuario,)
            cur.execute(insertSQLFormularioPedidoCompras, parametroFormularioPedidoCompras)
            id_formulario_pedido_compras = cur.fetchone()[0]
            if not id_formulario_pedido_compras:
                raise Exception("no se pudo insertar en la tabla formulario pedido_compras")
            
            for pedido in pedidos['pedidos_de_compras_proveedor']:
                id_proveedor = pedido['id_proveedor']
                id_estado = pedido['id_estado']
                parametrosInsertarPedidodeComprasProveedor = [id_formulario_pedido_compras,id_proveedor,id_estado,creacion_usuario]
                cur.execute(insertarPedidoComprasProveedor,parametrosInsertarPedidodeComprasProveedor,)

                for detalle_pedido in pedido['detalle_pedido_de_compras']:
                    id_insumo = detalle_pedido['id_insumo']
                    id_deposito = detalle_pedido['id_deposito']
                    cantidad = detalle_pedido['cantidad']
                    parametrosInsertDetallePedidoDeCompras = (id_formulario_pedido_compras, id_proveedor, id_insumo, id_deposito, cantidad )
                    cur.execute(insertarDetallePedidosCompras,parametrosInsertDetallePedidoDeCompras)

            ##actualizar estado de la solicitud a utilizado

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



