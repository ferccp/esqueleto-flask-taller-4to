from flask import current_app as app
from app.conexion.Conexion import Conexion


class PedidoDeCompraDao:

    def registrarPedidos(self, pedidos):
        #inserta y recupera el id generado
        insertSQLFormularioPedidoCompras = """ INSERT INTO public.formulario_pedido_compras
        (id_establecimiento, id_solicitud, fecha_entrega_plazo_pedido, creacion_usuario, creacion_fecha, creacion_hora)
        VALUES( %s, %s, %s, %s ,CURRENT_DATE, CURRENT_TIME(0)) RETURNING id_formulario_pedido_compras
        """
        insertarPedidoComprasProveedor = """
        INSERT INTO 
        public.pedidos_de_compras_proveedor(id_formulario_pedido_compras, id_proveedor, id_estado, creacion_usuario, creacion_fecha, creacion_hora)
        VALUES(%s, %s, %s, %s ,CURRENT_DATE, CURRENT_TIME(0))"""

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



