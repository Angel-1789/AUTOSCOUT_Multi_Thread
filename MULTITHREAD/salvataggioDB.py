import mysql.connector
from mysql.connector import Error
import pandas as pd

#---------------------------------------------------------------------------CONNESSIONE_AL_SERVER_MYSQL#
"""
Con questa funzione mi collego al server mysql. In questo progetto è localhost
"""
def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

#---------------------------------------------------------------------------Connessione_al_DB#
"""
Funzione per collegarsi al DB creato
"""
def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

#---------------------------------------------------------------------------Esecuzione_Query#
"""
Funzione per eseguire le query, passate come parametro in forma di stringa #Controllare  
"""
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

#---------------------------------------------------------------------------CREAZIONE_RELAZIONI_TRA_LE_TABELLE_Query#
"""
Funzione per eseguire le query, passate come parametro anche strutture dati #Controllare  
"""
def execute_list_query(connection, sql, val):
    cursor = connection.cursor()
    try:
        cursor.executemany(sql, val)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

