from flask import current_app as app
from app.conexion.Conexion import Conexion

class FuncionarioDao:
    def getFuncionario(self):
            querySQL = """
               select 
				f.id, p.ci,  p.nombres, p.apellidos 
				from 
				funcionarios f 
				left join personas p on p.id = f.id_persona;
        """
            conexion = Conexion()
            con = conexion.getConexion()
            cur = con.cursor()
            try:    
                cur.execute(querySQL)
                lista = cur.fetchall()
                return [{
                     'id': item[0],
                     'ci': item[1],
                     'nombres': item[2],
                     'apellidos': item[3],
                    
                } for item in lista ] if lista else []
            except con.Error as e:
                 app.logger.info(f"pgcode = {e.pgcode} , mensaje = {e.pgerror}")
            finally:
                 cur.close()
                 con.close()

    def getFuncionarioPorId(self,id):
            querySQL = """select 
	            f.id, p.ci,  p.nombres, p.apellidos, c.descripcion as cargo, d.descripcion as departamento
                from 
                funcionarios f 
                left join personas p on p.id = f.id_persona  
                left join cargos c on c.id = f.id_cargo 
                left join departamento d  on d.id = f.id_departamento  
                where f.id = %s"""
            conexion = Conexion()
            con = conexion.getConexion()
            cur = con.cursor()
            try:    
                cur.execute(querySQL,(id,))
                item = cur.fetchone()
                return {
                     'id': item[0],
                     'ci': item[1],
                     'nombres': item[2],
                      'apellidos': item[3],
                     'cargo': item[4],
                     'departamento': item[5],                   
                }  if item else {}
            except con.Error as e:
                 app.logger.info(f"pgcode = {e.pgcode} , mensaje = {e.pgerror}")
            finally:
                 cur.close()
                 con.close()