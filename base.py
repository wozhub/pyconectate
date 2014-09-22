#!/usr/bin/python
# -*- coding: utf -*-

from sqlalchemy import create_engine, MetaData, select, and_
from sqlalchemy import Table, Column, Integer, String, \
    ForeignKey, UniqueConstraint
from sqlalchemy.orm import scoped_session, sessionmaker


class Biblioteca():
    def __init__(self, echo=False):

        self.db = create_engine('sqlite:///biblioteca.sqlite', echo=echo)
        # encoding defaults to utf8
        self.metadata = MetaData(bind=self.db)
        self.session = scoped_session(sessionmaker(self.db, autoflush=True,
                                                   autocommit=True))

        try:
            self.programas = Table('programas', self.metadata, autoload=True)
        except:
            self.programas = Table('programas', self.metadata,
                                   Column('id', Integer, primary_key=True),
                                   # sqlalchemy lo hace autoincrement de por si
                                   Column('titulo', String(64)),
                                   Column('descripcion', String(512)),
                                   Column('sitio', String(12)),
                                   UniqueConstraint('id', 'titulo'))
            self.programas.create()

        try:
            self.temporadas = Table('temporadas', self.metadata, autoload=True)
        except:
            self.temporadas = Table('temporadas', self.metadata,
                                    Column('id', Integer, primary_key=True),
                                    Column('numero', Integer),
                                    Column('anio', Integer),
                                    Column('sinopsis', String(64)),
                                    Column('programa_id', Integer,
                                           ForeignKey('programas.id')),
                                    Column('titulo', String(64)),
                                    UniqueConstraint('programa_id', 'titulo'))

            self.temporadas.create()

        try:
            self.capitulos = Table('capitulos', self.metadata, autoload=True)
        except:
            self.capitulos = Table('capitulos', self.metadata,
                                   Column('id', Integer, primary_key=True),
                                   Column('programa_id', Integer,
                                          ForeignKey('programas.id')),
                                   Column('temporada_id', Integer,
                                          ForeignKey('temporadas.id')),
                                   Column('nombre', String(64)),
                                   Column('link', String(64)),
                                   )
            self.capitulos.create()

    def agregarCapitulo(self, capitulo):
        id = self.session.execute(select([self.capitulos.c.id]).
                                  where(self.capitulos.c.id == capitulo['id'])).first()
        if id is None:
            print "Capitulos: '%s' No existe en la db" % capitulo['nombre']
            id = self.capitulos.insert().execute(capitulo).inserted_primary_key
        return int(id[0])

    def agregarPrograma(self, programa):
        id = self.session.execute(select([self.programas.c.id]).
                                  where(self.programas.c.id == programa['id'])).first()
        if id is None:
            print "Programas: '%s' No existe en la db" % programa['titulo']
            id = self.programas.insert().execute(programa).inserted_primary_key
        return int(id[0])

    def agregarTemporada(self, temporada):
        id = self.session.execute(select([self.temporadas.c.id]).
                                  where(and_(self.temporadas.c.programa_id == temporada['programa_id'],
                                             self.temporadas.c.titulo == temporada['titulo']))).first()
        if id is None:
            print "Temporadas: '%s' No existe en la db" % temporada['titulo']
            id = self.temporadas.insert().execute(temporada).inserted_primary_key
        return int(id[0])

    def cuantosProgramas(self):
        return self.temporadas.count().execute().first()[0]

    def paginarProgramas(self, pagina, limite):
        programas = []
        for p in self.programas.select().limit(limite).offset((pagina - 1) * limite).execute():
            programas.append(p)
        return programas

    def obtenerPrograma(self, id):
        p = self.session.execute(select([self.programas]).where(self.programas.c.id == id)).first()
        return p

    def verCapitulos(self, programa_id):
        capitulos = []
        sql = self.capitulos.select(self.capitulos.c.programa_id == programa_id)
        for c in self.session.execute(sql):
            capitulos.append(c)
        return capitulos

    def verTemporadas(self, programa_id):
        temporadas = []
        sql = self.temporadas.select(self.temporadas.c.programa_id == programa_id)
        for c in self.session.execute(sql):
            temporadas.append(c)
        return temporadas

    def verProgramas(self):
        programas = []
        for p in self.session.execute(select([self.programas])):
            programas.append(p)
        return programas

    def buscarTemporada(self, programa_id, nombre):
        temporadas = []
        for t in self.session.execute(select([self.temporadas.c.id]).
                                      where(and_(self.temporadas.c.programa_id == programa_id,
                                                 self.temporadas.c.titulo == titulo))):
            temporadas.append(t)
        return temporadas
