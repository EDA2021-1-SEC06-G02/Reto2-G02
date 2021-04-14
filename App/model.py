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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
import time
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.ADT import list as lt
from DISClib.Algorithms.Sorting import mergesort as Merge
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalog():
    catalog = {'video': None, 'category': None}
    catalog['video'] = lt.newList('ARRAY_LIST')

    catalog['country'] = mp.newMap(7,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction=compareMapCountry)

    catalog['category'] = mp.newMap(33,
                                    maptype='PROBING',
                                    loadfactor=0.5,
                                    comparefunction=CompareMapCategory)
    return catalog

def addCategory(catalog, category):
    cat = newCategory(category['id'], category['name'])
    mp.put(catalog['category'], cat['Category_id'], cat)

def newCategory(id, name):
    Category = {'Category_id': '', 'name': '','video':None}
    Category['Category_id'] = id
    Category['name'] = name.strip()
    Category['video'] = lt.newList('ARRAY_LIST', compareExistenceID)
    return Category

def newCountry(name):
    Country = {'name': "",
              "video": None}
    Country['name'] = name
    Country['video'] = lt.newList('ARRAY_LIST', compareExistenceID)
    return Country


# Funciones para agregar informacion al catalogo

def addVideoCountry(catalog, video):
    Countryname = video['country']
    existcountry = mp.contains(catalog['country'], Countryname)
    if existcountry:
        entry = mp.get(catalog['country'], Countryname)
        country = me.getValue(entry)
    else:
        country = newCountry(Countryname)
        mp.put(catalog['country'], Countryname, country)
    lt.addLast(country['video'], video)

def addVideoCategory(catalog,video):
    videoCategoryID = video['category_id']
    CategoryInfo = mp.get(catalog['category'],videoCategoryID)
    if CategoryInfo:
        listaVideos = me.getValue(CategoryInfo)['video']
        lt.addLast(listaVideos,video)

def addVideo(catalog, video):
    lt.addLast(catalog['video'], video)
    addVideoCountry(catalog,video)
    addVideoCategory(catalog,video)

# Funciones para creacion de datos

# Funciones de busqueda

#En uso
def busquedaBinariaID(listaOrdenada, elemento):
    i, lon = 1, lt.size(listaOrdenada)
    elemento=elemento.lower()
    while i <= lon:
        m = (i + lon) // 2
        EM = lt.getElement(listaOrdenada,m)['video_id'].lower()
        if EM == elemento:
            return m
        elif elemento < EM:
            lon = m - 1
        else:
            i = m + 1
    return -1

#En uso
def busquedaBinariaTITLE(listaOrdenada, elemento):
    i, lon = 1, lt.size(listaOrdenada)
    elemento=elemento.lower()
    while i <= lon:
        m = (i + lon) // 2
        EM = lt.getElement(listaOrdenada,m)['title'].lower()
        if EM == elemento:
            return m
        elif elemento < EM:
            lon = m - 1
        else:
            i = m + 1
    return -1

# Asignar Valores

#En uso
def asignarNombreCategoryToID(catalog,elemento):
    elemento=elemento.lower()
    i=1
    Verifica=True
    category_id=0
    try:
        while i<=(lt.size(mp.keySet(catalog['category']))+1) and Verifica:
            Name=mp.get(catalog['category'],lt.getElement(mp.keySet(catalog['category']),i))
            Name = me.getValue(Name)['name']
            if Name.lower()==elemento:
                elemento
                category_id=lt.getElement(mp.keySet(catalog['category']),i)
                Verifica=False
            i+=1
        return category_id
    except: 
        return -1

#Requerimientos

#En uso
def VideoPaisConMasTendencia(catalog,paisInteres):
        Pais = mp.get(catalog['country'], paisInteres)
        if Pais:
            listaPais = me.getValue(Pais)['video']
            listaOrdenID = VideosByID(listaPais)
            videoTendenciaID,DiasEnTendencia=VideoConMasDiasEnTendencia(listaOrdenID)
            videoTendencia=lt.getElement(listaOrdenID,busquedaBinariaID(listaOrdenID,videoTendenciaID))
            return videoTendencia,DiasEnTendencia
        else:
            return -1,-1

#En uso
def VideoCategoriaConMasTendencia(catalog,categoria,tipo_comparacion):
    IdCategoria = asignarNombreCategoryToID(catalog,categoria)
    if(IdCategoria==-1):
        return -1,0
    elif(tipo_comparacion!='1' and tipo_comparacion!='2'):
        return -2,0
    else:
        listaSoloCategoria=me.getValue(mp.get(catalog["category"],IdCategoria))["video"]
        if (tipo_comparacion =='1'):
            listaOrdenID=VideoConMasTendencia(listaSoloCategoria)
            videoTendenciaID,DiasEnTendencia=VideoConMasDiasEnTendenciaCategoria(listaOrdenID)
            videoTendencia=lt.getElement(listaOrdenID,busquedaBinariaID(listaOrdenID,videoTendenciaID))
        else:
            listaOrdenTITLE=VideoConMasTendenciaTITLE(listaSoloCategoria)
            videoTendenciaTITLE,DiasEnTendencia=VideoConMasDiasEnTendenciaCategoria(listaOrdenTITLE)
            videoTendencia=lt.getElement(listaOrdenTITLE,busquedaBinariaTITLE(listaOrdenTITLE,videoTendenciaTITLE))
    return videoTendencia,DiasEnTendencia

#En uso
def VideoConMasDiasEnTendencia(listaOrdenID):
    contador=0
    Mayor=0
    MayorID=''
    i=0
    elementoComparado=lt.getElement(listaOrdenID,i)['video_id'].lower()
    while i<=lt.size(listaOrdenID):
        if elementoComparado==lt.getElement(listaOrdenID,i)['video_id'].lower():
            contador+=1
        else:
            if contador>Mayor:
                Mayor=contador
                MayorID=elementoComparado
            elementoComparado=lt.getElement(listaOrdenID,i)['video_id'].lower()
            contador=1
        i+=1
    return MayorID,Mayor

#En uso
def VideoConMasDiasEnTendenciaCategoria(listaOrdenID):
    Mayor=0
    MayorID=''
    i=2
    elementoComparado=lt.getElement(listaOrdenID,1)
    listaNueva=lt.newList('ARRAY_LIST',cmpfunction=cmpIgualdadFechas)
    lt.addLast(listaNueva,elementoComparado)
    contador=1
    while i<=lt.size(listaOrdenID):
        if elementoComparado['title'].lower()==lt.getElement(listaOrdenID,i)['title'].lower():
            posF=lt.isPresent(listaNueva,lt.getElement(listaOrdenID,i)['trending_date'])
            if not(posF>0):
                lt.addLast(listaNueva,lt.getElement(listaOrdenID,i))
                contador+=1
        else:
            if contador>Mayor:
                Mayor=contador
                MayorID=elementoComparado['title'].lower()
            listaNueva=lt.newList('ARRAY_LIST',cmpfunction=cmpIgualdadFechas)
            elementoComparado=lt.getElement(listaOrdenID,i)
            lt.addLast(listaNueva,elementoComparado)
            contador=1
        i+=1
    return MayorID,Mayor

#En uso
def VideoConMasTendencia(listaOrdenada):
    return VideosByID(listaOrdenada)

#En uso
def VideoConMasTendenciaTITLE(listaOrdenada):
    return VideosByTITLE(listaOrdenada) 
    
#En uso
def VideosPaisMasLikes(catalog,idCategoria,numeroElementos,paisInteres):
    idCategoria = mp.get(catalog['category'], idCategoria)
    Pais = mp.get(catalog['country'], paisInteres)
    listaPaisViews=lt.newList('ARRAY_LIST',cmpfunction=compareExistenceID)
    if idCategoria and Pais:
        listaViews = me.getValue(idCategoria)['video']
        listaPais = me.getValue(Pais)['video']
        listaViews = VideosByViews(listaViews)
        i=1
        verifica=True
        while i<=lt.size(listaViews) and verifica:
            elemento=lt.getElement(listaViews,i)
            if elemento['country']==paisInteres and lt.isPresent(listaPais,elemento['video_id']):
                lt.addLast(listaPaisViews,elemento)
            if lt.size(listaPaisViews)==numeroElementos:
                verifica=False
            i+=1
        return listaPaisViews
    return None

#En uso
def VideosConMasLikesPorPaisTag(catalog,paisInteres,TagInteres,numeroElementos,opcion):
    Pais = mp.get(catalog['country'], paisInteres)
    if Pais:
        listaPais = me.getValue(Pais)['video']
        listaPais = VideosBylikes(listaPais)
        i=1
        verifica = True
        listaPaisLikesTags=lt.newList('ARRAY_LIST',cmpfunction=compareExistenceID)
        if opcion==2:
            while ((i<=lt.size(listaPais)) and verifica):
                if TagInteres in lt.getElement(listaPais,i)['tags']:
                    posElemento = lt.isPresent(listaPaisLikesTags,lt.getElement(listaPais,i)['video_id'])
                    if not(posElemento>0):
                        lt.addLast(listaPaisLikesTags,lt.getElement(listaPais,i))
                        if lt.size(listaPaisLikesTags)==numeroElementos:
                            verifica=False
                i+=1
        elif opcion==1:
            while ((i<=lt.size(listaPais)) and verifica):
                if TagInteres in lt.getElement(listaPais,i)['tags']:
                    lt.addLast(listaPaisLikesTags,lt.getElement(listaPais,i))
                    if lt.size(listaPaisLikesTags)==numeroElementos:
                        verifica=False
                i+=1
    return listaPaisLikesTags

# Funciones utilizadas para comparar elementos dentro de una lista

def cmpVideosByViews(video1, video2):
    return (float(video1['views']) > float(video2['views']))

def cmpVideosBylikes(video1, video2):
    return (float(video1['likes']) > float(video2['likes']))

def cmpByID(video1, video2):
    return ((video1['video_id']).lower() < (video2['video_id']).lower())

def cmpByTITLE(video1, video2):
    return ((video1['title']).lower() < (video2['title']).lower())

def cmpIgualdadFechas(fecha, Lista):
    if (fecha in Lista['trending_date']):
        return 0
    return -1

def compareExistenceID(ID,Lista):
    if (ID.lower() in Lista['video_id'].lower()):
        return 0
    return -1

# Funciones de ordenamiento

def VideosByViews(listaOrdenada):
    sub_list = lt.subList(listaOrdenada, 1, lt.size(listaOrdenada))
    sub_list = sub_list.copy()
    sorted_list = sa.sort(sub_list, cmpVideosByViews)
    return sorted_list

def VideosBylikes(listaOrdenada):
    sub_list = lt.subList(listaOrdenada, 1, lt.size(listaOrdenada))
    sub_list = sub_list.copy()
    sorted_list = sa.sort(sub_list, cmpVideosBylikes)
    return sorted_list

def VideosByID(listaOrdenada):
    sub_list = lt.subList(listaOrdenada, 0, lt.size(listaOrdenada))
    sub_list = sub_list.copy()
    sorted_list = sa.sort(sub_list, cmpByID)
    return sorted_list

def VideosByTITLE(listaOrdenada):
    sub_list = lt.subList(listaOrdenada, 0, lt.size(listaOrdenada))
    sub_list = sub_list.copy()
    sorted_list = sa.sort(sub_list, cmpByTITLE)
    return sorted_list
    
def CompareMapCategory(id,Category):
    Categoryentry = me.getKey(Category)
    if (id == Categoryentry):
        return 0
    elif (id > Categoryentry):
        return 1
    else:
        return 0

def compareMapCountry(name,Country):
    Countryentry = me.getKey(Country)
    if (name == Countryentry):
        return 0
    elif (name > Countryentry):
        return 1
    else:
        return -1

