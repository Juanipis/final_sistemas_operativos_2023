from typing import Dict, List
from uuid import UUID
from pydantic_settings import BaseSettings
import psycopg2
from logzero import logger

class RDSCredentiasl(BaseSettings):
    rds_host: str
    rds_port: int
    rds_user: str
    rds_password: str
    rds_region: str = 'us-east-1'
    drop_table: bool = False
    rds_db_name: str

class RDSController:
    def __init__(self, rds_credentials=RDSCredentiasl()):
        self.credentials = rds_credentials
        self.conn = psycopg2.connect(
            host=self.credentials.rds_host,
            port=self.credentials.rds_port,
            user=self.credentials.rds_user,
            password=self.credentials.rds_password,
            dbname=self.credentials.rds_db_name
        )
        
    
    def get_information(self, db_table:str):
        #El siguiente metodo se encarga de obtener la informacion de la tabla de la base de datos
        #db_table: nombre de la tabla de la base de datos
        self.cursor = self.conn.cursor()
        #Se obtiene la informacion de la tabla,
        #para ello se ejecuta la siguiente consulta
        self.cursor.execute("SELECT * FROM {}".format(db_table))
        #Se crea un diccionario con la informacion de la tabla, para ello se utiliza el metodo fetchall()
        #el cual devuelve una lista de tuplas, donde cada tupla representa una fila de la tabla
        self.data = self.cursor.fetchall()
        self.data_dict = {}
        for i in range(len(self.data)):
            self.data_dict[i] = self.data[i]
        return self.data_dict
    

rds_controller = RDSController()