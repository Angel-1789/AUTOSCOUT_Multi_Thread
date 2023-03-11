import pandas as pd
from salvataggioDB import create_db_connection, execute_list_query
import json

df = pd.read_csv('../dati/dati_auto_20221116_194619.csv', delimiter=';')


def vis_data(data):
    count = 0
    for i in data:
        count += 1
        print(count, "\t", i, "\n")

vis_data(df)
print(df)

#-------------------------------------------------------------------------------------------SALVA_DATI_NEL_DB
pw = 'test'
db = 'auto'
#connection = create_db_connection("localhost", "root", pw, db)

#sql = "INSERT INTO annuncio "+str() VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

#val = [    (7, 'Hank', 'Dodson', 'ENG', None, '1991-12-23', 11111, '+491772345678'),(8, 'Sue', 'Perkins', 'MAN', 'ENG', '1976-02-02', 22222, '+491443456432')]
