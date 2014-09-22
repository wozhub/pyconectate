#!/usr/bin/python
# -*- coding: utf -*-

from base import Biblioteca
b = Biblioteca()

from urllib3 import connection_from_url
from bs4 import BeautifulSoup
from operator import itemgetter

from selenium import webdriver
wd = webdriver.Firefox()
base_url = 'http://www.conectate.gob.ar/'

http = connection_from_url('http://www.conectate.gob.ar/', maxsize=8)
sitios = ['educar', 'encuentro', 'deportv', 'pakapaka', 'conectar']


def parsearPrograma(url):
    pagina = http.request('GET', url)
    soup = BeautifulSoup(pagina.data)
    pagina.release_conn()

    script = soup.find_all('script')[1].text

    j = wd.execute_script(script + 'return recurso')

    campos = ['descripcion', 'titulo']
    programa = dict(zip(campos, itemgetter(*campos)(j)))
    programa['id'] = j['rec_id']
    b.agregarPrograma(programa)

    campos = ['id', 'numero', 'titulo', 'sinopsis']
    for t in j['tipo_funcional']['data']['temporadas']:
        temporada = dict(zip(campos, itemgetter(*campos)(t)))
        temporada['programa_id'] = programa['id']
        b.agregarTemporada(temporada)
