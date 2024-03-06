import psycopg2

class Conexion:
    
    def __init__(self):
        """Metodo constructor de la conexion
        
        Se retorna una instancia de la base de datos
        """
        self.__con = psycopg2.connect("dbname=pruebita user=postgres host=localhost password=urbana1992")
        
    def getConexion(self):
        return self.__con    