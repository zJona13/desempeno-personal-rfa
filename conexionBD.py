import mysql.connector
from config import Config

class Conexion:
    def __init__(self):
        self.dblink = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME,
            port=Config.DB_PORT
        )

    @property
    def open(self):
        return self.dblink
