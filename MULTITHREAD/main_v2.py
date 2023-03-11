from typing import List

import \
    bs4  # Beautiful Soup v4 -> libreria di websraping, ci permette di estrarre i dati dalle pagine HTML, pesino dati nascosti
import requests  # libreria standard di Python per accedere ai siti web, tramitte richieste HTTP
from queue import Queue
from multi_job import usa_threads, ThreadsMacro
from salvataggioDB import create_db_connection, execute_list_query
import csv
from datetime import datetime
import json

pre_lnk = 'https://www.autoscout24.it/'
anno_inizio = 2010

# --------------------------------------------------------------------------------------------CARICA_FILE_META#
"""
Carico le classi deI vari div della pagina html da elaborare
"""
with open('../dati/meta_pagina_html.txt', 'r') as f:
    pg = json.loads(f.read())

# --------------------------------------------------------------------------------------------CREA_LINK_MACRO#
"""
Questa funzione serve a creare 'MACRO link'. Servono a esplorare un po' il sito che andremmo a trattare.
I link creati sono suddivisi per anno, fascia di prezzo e tipo di carburante, in questo ordine.
i link sono poi salvati in un oggetto di tipo coda.
"""


def crea_links_macro(pre_link, from_year):
    pre_website_queue = Queue()  # coda per i siti web
    year = int(datetime.today().strftime("%Y"))
    carburante = ['B', 'L', 'E', '2']
    price = [(lambda x: x * 1000)(x) for x in range(0, 60, 1)]

    posti = 'lst?seatsfrom=' + str(4) + '&seatsto=' + str(11)
    portiere = '&doorfrom=' + str(4) + '&doorto=' + str(5)
    km = '&kmfrom=' + str(1) + '&kmto=' + str(200000)

    a = '&sort=standard&desc=0&cy=I&zipr=400&zip=Milano&lon=9.18812&lat=45.46362&atype=C&ustate=N%2CU'
    b = '&powertype=hp&custtype=D'
    c = '&search_id=1zflu6brpqb'

    for y in range(from_year, year):
        anno = '&fregfrom=' + str(y) + '&fregto=' + str(y)
        for pr in range(0, len(price) - 1 ):
            prezzo = '&pricefrom=' + str(int(price[pr]) + 1) + '&priceto=' + str(price[pr + 1])
            for f in carburante:
                fuel = '&fuel=' + str(f)
                pre_website_queue.put([pre_link + posti + portiere + anno + km + a + fuel + b + prezzo + c,
                                       (anno, fuel, int(price[pr]) + 1, price[pr + 1])])
    return pre_website_queue


pre_website_queue = crea_links_macro(pre_link=pre_lnk, from_year=anno_inizio)

lista_link_macro = ThreadsMacro(N_THREADS=4, coda=pre_website_queue, pg=pg, pre_lnk=pre_lnk)

# --------------------------------------------------------------------------------------------CREA_LINK#
# def crea_link(pre_lnk):
#     posto = 'lst?seatsfrom=' + str(4) + '&seatsto=' + str(11)
#     portiere = '&doorfrom=' + str(4) + '&doorto=' + str(5)
#     anno = '&fregfrom=' + str(2011) + '&fregto=' + str(2022)
#     km = '&kmfrom=' + str(1) + '&kmto=' + str(200000)
#     prezzo = '&pricefrom=' + str(10) + '&priceto=' + str(50000)
#     fuel = '&fuel=B%2CL%2CE'
#
#     a = '&sort=standard&desc=0&cy=I&zipr=200&zip=Milano&lon=9.18812&lat=45.46362&atype=C&ustate=N%2CU'
#     b = '&powertype=hp&custtype=D'
#     c = '&search_id=1zflu6brpqb'
#
#     return pre_lnk + posto + portiere + anno + km + a + fuel + b + prezzo + c
#
#
# link = crea_link(pre_lnk)
# print(link)
#
# # --------------------------------------------------------------------------------------------Chiamata_pagina_da_elaborare#
# response = requests.get(link)
# response.raise_for_status()  # genera un'eccezione se la risposta è in stato di errore
# # Estraiamo il testo dalla risposta. Il testo è in formato html e lo salviamo in una variabile soup
# soup = bs4.BeautifulSoup(response.text, 'html.parser')
# tot_pages = int(
#     soup.find("div", {"class": pg['div_pagine']}).find_all('li', {"class": pg['lista_pagine']})[0].text.split('/')[1])
#
# """
# creo delle code per trattare gli elementi letti dalle pagine.
# """
# website_queue = Queue()  # coda per i siti web
#
# # --------------------------------------------------------------------------------------------Avvio_Threads#
# """
# Usiamo i thread per scaricare in parallelo le pagine individuate dalla prima chiamata.
# """
# for i in range(0, tot_pages):
#     website_queue.put(link + '&page=' + str(i + 1))
#
# auto = usa_threads(N_THREADS=3, website_queue=website_queue, tot_pages=tot_pages, pg=pg)
#
# # --------------------------------------------------------------------------------------------SALVA_dati_in_un_file_CSV#
# fields = list((auto['page=1'])[1].keys())
# righe = []
# for page in auto:
#     for dati_auto in auto[page]:
#         righe.append(list(dati_auto.values()))
# with open('../dati/dati_auto_' + str(datetime.now().strftime("%Y%m%d_%H%M%H")) + '.csv', 'w', newline='') as f:
#     w = csv.writer(f)
#     w.writerow(fields)
#     w.writerows(righe)
#
# # -------------------------------------------------------------------------------------------SALVA_DATI_NEL_DB
# pw = 'test'
# db = 'auto'
# connection = create_db_connection("localhost", "root", pw, db)
#
# sql = '''
#     INSERT INTO teacher (teacher_id, first_name, last_name, language_1, language_2, dob, tax_id, phone_no)
#     VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#     '''
#
# val = [
#     (7, 'Hank', 'Dodson', 'ENG', None, '1991-12-23', 11111, '+491772345678'),
#     (8, 'Sue', 'Perkins', 'MAN', 'ENG', '1976-02-02', 22222, '+491443456432')
# ]