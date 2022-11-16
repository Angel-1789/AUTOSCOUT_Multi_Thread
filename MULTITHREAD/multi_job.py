import bs4  # Beautiful Soup v4 -> libreria di websraping, ci permette di estrarre i dati dalle pagine HTML, pesino dati nascosti
import requests  # libreria standard di Python per accedere ai siti web, tramitte richieste HTTP
from queue import Queue
from threading import Lock, Thread
from time import time
from time import sleep

data_queue = Queue()  # coda per i dati SCARICATI
file_lock = Lock()  # gestione PER IL salvataggio dati nel dict 'auto'. gestione più thread
ris = {}

# ----------------------------------------------------------------------------------------FUNZIONE_LEGGI_DATI#
"""
Funzione valida solo per il sito autoscout.it, perchè dipende dal file 'meta_pagina_html' contenente i class name
dei div della pagina.
Se si vuole trattare un'altra pagina, si deve modificare il file 'meta_pagina_html' e la funzione 'leggi'
"""


def leggi(elemsoup, lnk, pg):
    articoli = elemsoup.find_all("article", {"class": pg['article_class']})
    pre_lnk = lnk[0:(lnk.find('.it') + 4)]
    lista_auto = []

    for ann in articoli:
        dati_auto = {'KM': '', 'data_imm': '', 'potenza': '', 'condizone': '', 'proprietari': '', 'trasmissione': '',
                     'carburante': '', 'Consumo di carburante': '', 'Emissioni': ''}
        temp = list(dati_auto)
        z = 0
        an_tit = ann.find('div', {'class': pg['div_dati']}).find('div', {'class': pg['div_marca_modello']})
        an_ven = ann.find('div', {'class': pg['div_dati']}).find('div', {'class': pg['div_vendita']})
        an_vend = ann.find('div', {'class': pg['div_venditore']})

        dati_auto['marca_car'] = (an_tit.find('h2').text).replace('\xa0', '')
        dati_auto['model_car'] = an_tit.find('span').text
        dati_auto['lnk_auto'] = pre_lnk + an_tit.find('a')['href']
        dati_auto['prezzo'] = an_ven.find('div', {'class': pg['div_prezzo']}).find('div', {
            'class': pg['div_dato_prezzo']}).find('p').text
        dati_auto['nome_venditore'] = an_vend.find('span', {'class': pg['span_nome']}).text
        dati_auto['ind_venditore'] = an_vend.find('span', {'class': pg['span_ind']}).text
        dati_vendita = an_ven.find('div', {'class': pg['div_dati_vendita']}).find_all('span')

        for i in dati_vendita:
            dati_auto[temp[z]] = i.text
            z += 1
        lista_auto.append(dati_auto)
    return (lnk[lnk.find('&page=') + 1:len(lnk)], lista_auto)


# ----------------------------------------------------------------------------------------FUNZIONE_SCARICARE_DATI#
"""funzione per SCARICARE i dati. 
1) A ogni chiamata della funzione estrae un link dalla coda dei siti web. 
2) Poi esegue un controllo sull'elemento estratto dalla coda, se viene estratto un 
valore NULL significa che sono stati processati tutti i link e non c'è bisogno 
di andare avanti con l'elaborazione. 
3) dalla libreria 'urllib' viene fatta partire una richiesta per scaricarsi i 
metadati della pagina.
4) estraiamo i dati dalla richiesta
5) salviamo i dati nella CODA DEI DATI
"""


def download_data(website_queue):
    #print("\t\tDownload\twebsite_queue_len: ", website_queue.qsize(), "\tdata_queue_len: ", data_queue.qsize())
    while True:
        var = website_queue.get()
        if var is None:
            break
        response = requests.get(var)
        response.raise_for_status()  # genera un'eccezione se la risposta è in stato di errore
        soup = bs4.BeautifulSoup(response.text, 'html.parser')  # Estraiamo il testo dalla risposta. Il testo è in formato html e lo salviamo in una variabile soup
        t0 = time()
        sleep(3)
        data_queue.put((soup, var, t0))
        #print("download : ", var[var.find('&page=') + 1:len(var)], "\n\twebsite_queue.qsize():", website_queue.qsize(), "\n\tdata_queue.qsize():", data_queue.qsize())


# ----------------------------------------------------------------------------------------FUNZIONE_SALVA_DATI#
"""funzione per SALVARE i dati scaricati.
1) A ogni chiamata della funzione viene estrato il dato ottenuto dalla CODA DATI. 
2) Poi esegue un controllo sull'elemento estratto dalla coda, se viene estratto un 
valore NULL significa che sono stati processati tutti i dati scaricati e non c'è bisogno 
di andare avanti con l'elaborazione.
3) dalla libreria 'threading' usiamo la funzione LOCK, istanziata nella variabile
file_lock. Il ciclo controlla solo quale numero di file è disponibile. 
Dobbiamo usare un blocco qui perché c'è una modifica, due thread eseguono le 
stesse righe contemporaneamente e trovano che il file disponibile sia lo stesso.
4) Quando scriviamo sul file, non ci interessa il blocco, perché sappiamo che 
solo un thread scriverà su ogni file.
Ecco perché creiamo il file su una riga, mentre viene acquisito il blocco,
Ma scriviamo i dati su una riga separata, senza il blocco
"""


def save_data(pg):
    #print("\t\tsave_funzione\tpg_len: ", len(pg))
    while True:
        var = data_queue.get()
        if var is None:
            break
        dati = leggi(var[0], var[1], pg)
        with file_lock:
            ris[dati[0]] = dati[1]
        print(f'Elaborazione: {dati[0]}\t-> tempo trascorso {time() - var[2]:2.2f} sec')


"""
eseguiamo i thread per il download dei dati.
"""


def usa_threads(N_THREADS, website_queue, tot_pages, pg):
    threads_download = []
    threads_save = []

    for i in range(N_THREADS):
        t = Thread(target=download_data, args=(website_queue, ))
        t.start()
        threads_download.append(t)
        t2 = Thread(target=save_data, args=(pg, ))
        t2.start()
        threads_save.append(t2)

    for i in range(N_THREADS):
        website_queue.put(None)

    for t in threads_download:
        t.join()

    for i in range(N_THREADS):
        data_queue.put(None)

    for t in threads_save:
        t.join()

    print(f'Finished downloading {tot_pages} pagine del sito web')

    return ris