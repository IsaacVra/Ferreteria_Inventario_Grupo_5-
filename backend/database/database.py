import mysql.connector
from mysql.connector import Error
from config import Config

class Database:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.connection = None
            cls._instance.connect()
        return cls._instance
    
    def connect(self):
        """Establece la conexión a la base de datos."""
        try:
            self.connection = mysql.connector.connect(**Config.DB_CONFIG)
            if self.connection.is_connected():
                print("Conexión exitosa a la base de datos MySQL")
        except Error as e:
            print(f"Error al conectar a MySQL: {e}")
            raise
    
    def disconnect(self):
        """Cierra la conexión a la base de datos."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Conexión a MySQL cerrada")
    
    def execute_query(self, query, params=None, fetch=True, commit=False):
        """
        Ejecuta una consulta SQL.
        
        Args:
            query (str): Consulta SQL a ejecutar
            params (tuple, optional): Parámetros para la consulta. Defaults to None.
            fetch (bool, optional): Si es True, devuelve los resultados. Defaults to True.
            commit (bool, optional): Si es True, hace commit de la transacción. Defaults to False.
            
        Returns:
            list/dict: Resultados de la consulta o información de la operación
        """
        cursor = None
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)
            
            if commit:
                self.connection.commit()
            
            if fetch and query.strip().upper().startswith('SELECT'):
                return cursor.fetchall()
            elif not fetch and (query.strip().upper().startswith(('INSERT', 'UPDATE', 'DELETE'))):
                return {
                    'affected_rows': cursor.rowcount,
                    'lastrowid': cursor.lastrowid
                }
            
            return None
            
        except Error as e:
            if self.connection:
                self.connection.rollback()
            print(f"Error en la consulta: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
    
    def get_connection(self):
        """Obtiene la conexión actual a la base de datos."""
        if not self.connection or not self.connection.is_connected():
            self.connect()
        return self.connection

# Instancia global de la base de datos
db = Database()
