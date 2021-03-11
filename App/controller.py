"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Funciones para la carga de datos

def initCatalog():
    return model.newCatalog()

def loadData(catalog):
    loadVideos(catalog)
    loadCategories(catalog)

def loadVideos(catalog):
    videofile = cf.data_dir + 'Videos/videos-large.csv'
    input_file = csv.DictReader(open(videofile, encoding='utf-8'))
    for video in input_file:
        model.addVideo(catalog, video)

def loadCategories(catalog):
    categoriesfile = cf.data_dir + 'category-id.csv'
    input_file = csv.DictReader(open(categoriesfile, encoding='utf-8'), delimiter='\t')
    for category in input_file:
        model.addCategory(catalog, category)

# Funciones de ordenamiento

def OrdenCatalogoPaises(catalog):
    return model.VideosByCountry(catalog)

def OrdenCatalogoCategorias(catalog):
    return model.VideosByCategory(catalog)

def VideoPaisConMasTendencia(catalog,paisInteres):
    return model.VideoPaisConMasTendencia(catalog, paisInteres)

def VideosConMasViewsPorPais(catalog,paisInteres,idCategoria):
    return model.VideosConMasViewsPorPais(catalog,paisInteres,idCategoria)

def VideoCategoriaConMasTendencia(catalog,catalogOrdenado,categoria):
    return model.VideoCategoriaConMasTendencia(catalog, catalogOrdenado, categoria)

def VideosConMasLikesPorPaisTag(listaOrdenada,paisInteres,TagInteres,numeroElementos,opcion):
    return model.VideosConMasLikesPorPaisTag(listaOrdenada,paisInteres,TagInteres,numeroElementos,opcion)

# Funciones de consulta sobre el catálogo

def asignarNombreCategoryToID(catalog,elemento):
    return model.asignarNombreCategoryToID(catalog,elemento)