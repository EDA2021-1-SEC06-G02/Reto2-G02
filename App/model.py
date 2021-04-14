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

def busquedaBinariaPaises(listaOrdenada, elemento):
    i, lon = 1, lt.size(listaOrdenada)
    elemento=elemento.lower()
    while i <= lon:
        m = (i + lon) // 2
        EM = lt.getElement(listaOrdenada,m)['country'].lower()
        if EM == elemento:
            return m
        elif elemento < EM:
            lon = m - 1
        else:
            i = m + 1
    return -1

def busquedaBinariaCategorias(listaOrdenada, elemento):
    i, lon = 1, lt.size(listaOrdenada)
    elemento=elemento.lower()
    while i <= lon:
        m = (i + lon) // 2
        EM = lt.getElement(listaOrdenada,m)['category_id'].lower()
        if EM == elemento:
            return m
        elif elemento < EM:
            lon = m - 1
        else:
            i = m + 1
    return -1

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

def busquedaBinariaCategoryID(listaOrdenada, elemento):
    i, lon = 1, lt.size(listaOrdenada)
    while i <= lon:
        m = (i + lon) // 2
        EM = lt.getElement(listaOrdenada,m)['category_id']
        if EM == elemento:
            return m
        elif elemento < EM:
            lon = m - 1
        else:
            i = m + 1
    return -1

def busquedaBinariaCategory_Name(listaOrdenada, elemento):
    elemento=elemento.lower()
    i, lon = 1, lt.size(listaOrdenada)
    while i <= lon:
        m = (i + lon) // 2
        EM = lt.getElement(listaOrdenada,m)['name'].lower()
        if EM == elemento:
            return m
        elif elemento < EM:
            lon = m - 1
        else:
            i = m + 1
    return -1

# Asignar Valores

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

# Sublistas

def subListaDeCategoria(listaOrdenada,index,elemento):
    elemento=elemento.lower()
    i=index-1
    l=index+1
    limIzq=0
    limDer=lt.size(listaOrdenada)
    VerIzq=True
    VerDer=True
    while i >= 0 and VerIzq:
        if not(lt.getElement(listaOrdenada,i)['category_id'].lower()==elemento):
            VerIzq=False
            if i==0:
                limIzq=i
            else:
                limIzq=i+1
        i-=1
    while l <= lt.size(listaOrdenada) and VerDer:
        if not(lt.getElement(listaOrdenada,l)['category_id'].lower()==elemento):
            VerDer=False
            if l==lt.size(listaOrdenada):
                limDer=l
            else:
                limDer=l-1
        l+=1
    sub_list = lt.subList(listaOrdenada, limIzq, limDer-limIzq)
    sub_list = sub_list.copy()
    return sub_list

def subListaDePais(listaOrdenada,index,elemento):
    elemento=elemento.lower()
    i=index-1
    l=index+1
    limIzq=0
    limDer=lt.size(listaOrdenada)
    VerIzq=True
    VerDer=True
    while i >= 0 and VerIzq:
        if not(lt.getElement(listaOrdenada,i)['country'].lower()==elemento):
            VerIzq=False
            if i==0:
                limIzq=i
            else:
                limIzq=i+1
        i-=1
    while l <= lt.size(listaOrdenada) and VerDer:
        if not(lt.getElement(listaOrdenada,l)['country'].lower()==elemento):
            VerDer=False
            if l==lt.size(listaOrdenada):
                limDer=l
            else:
                limDer=l-1
        l+=1
    sub_list = lt.subList(listaOrdenada, limIzq, limDer-limIzq)
    sub_list = sub_list.copy()
    return sub_list

def subListaDeCategories(listaOrdenada,index,elemento):
    i=index-1
    l=index+1
    limIzq=0
    limDer=lt.size(listaOrdenada)
    VerIzq=True
    VerDer=True
    while i >= 0 and VerIzq:
        if not(lt.getElement(listaOrdenada,i)['category_id']==elemento):
            VerIzq=False
            if i==0:
                limIzq=i
            else:
                limIzq=i+1
        i-=1
    while l <= lt.size(listaOrdenada) and VerDer:
        if not(lt.getElement(listaOrdenada,l)['category_id']==elemento):
            VerDer=False
            if l==lt.size(listaOrdenada):
                limDer=l
            else:
                limDer=l-1
        l+=1
    sub_list = lt.subList(listaOrdenada, limIzq, limDer-limIzq)
    sub_list = sub_list.copy()
    return sub_list

#Requerimientos

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

def NombreAId (catalog,categoria):
    id = -1
    centi = True
    i = 0
    while (i < lt.size(catalog["category"]) and centi):
        if (lt.getElement(catalog['category'],i)["name"].lower() == categoria.lower()):
            centi = False
            id = lt.getElement(catalog['category'],i)["Category_id"]
        i += 1
    return id

def VideoCategoriaConMasTendencia(catalog,listaOrdenada,categoria):
    IdCategoria = NombreAId(catalog, categoria)
    if(IdCategoria==-1):
        return -1,0
    else:
        indexProvi=busquedaBinariaCategorias(listaOrdenada,IdCategoria)
        listaSoloCategoria=subListaDeCategoria(listaOrdenada,indexProvi,IdCategoria)
        listaOrdenID=VideoConMasTendencia(listaSoloCategoria)
        listaOrdenDate=VideosPorDate(listaOrdenID)
        videoTendenciaID,DiasEnTendencia=VideoConMasDiasEnTendenciaCategoria(listaOrdenDate)
        videoTendencia=lt.getElement(listaOrdenDate,busquedaBinariaID(listaOrdenDate,videoTendenciaID))
    return videoTendencia,DiasEnTendencia

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

def VideoConMasDiasEnTendenciaCategoria(listaOrdenID):
    Mayor=0
    MayorID=''
    i=2
    elementoComparado=lt.getElement(listaOrdenID,1)
    listaNueva=lt.newList('ARRAY_LIST',cmpfunction=cmpIgualdadFechas)
    lt.addLast(listaNueva,elementoComparado)
    contador=lt.size(listaNueva)
    while i<=lt.size(listaOrdenID):
        if elementoComparado['video_id'].lower()==lt.getElement(listaOrdenID,i)['video_id'].lower():
            posF=lt.isPresent(listaNueva,lt.getElement(listaOrdenID,i)['trending_date'])
            if not(posF>0):
                lt.addLast(listaNueva,lt.getElement(listaOrdenID,i))
                contador=lt.size(listaNueva)
        else:
            if contador>Mayor:
                Mayor=contador
                MayorID=elementoComparado['video_id'].lower()
            listaNueva=lt.newList('ARRAY_LIST',cmpfunction=cmpIgualdadFechas)
            elementoComparado=lt.getElement(listaOrdenID,i)
            lt.addLast(listaNueva,elementoComparado)
            contador=lt.size(listaNueva)
        i+=1
    return MayorID,Mayor

def VideoConMasTendencia(listaOrdenada):
    return VideosByID(listaOrdenada)

def VideosConMasViewsPorPais(listaOrdenada,paisInteres,idCategoria):
    indexProvi=busquedaBinariaPaises(listaOrdenada,paisInteres)
    if(indexProvi==-1):
        return -1
    else:
        listaSoloPaises=subListaDePais(listaOrdenada,indexProvi,paisInteres)
        listaOrdenadaCategoria=VideosByCategoryID(listaSoloPaises)
        indexCategory=busquedaBinariaCategoryID(listaOrdenadaCategoria,idCategoria)
        listaSoloCategoria=subListaDeCategories(listaOrdenadaCategoria,indexCategory,idCategoria)
        listaPaisViews=VideosByViews(listaSoloCategoria)
    return listaPaisViews

def VideosConMasLikes2(catalog,idCategoria):
    idCategoria = mp.get(catalog['category'], idCategoria)
    if idCategoria:
        listaPaisViews = me.getValue(idCategoria)['video']
        listaPaisViews = VideosBylikes(listaPaisViews)
        return listaPaisViews
    return 
    
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

def VideosPorDate(listaOrdenada):
    return VideosByTDate(listaOrdenada)

# Funciones utilizadas para comparar elementos dentro de una lista

def cmpVideosByViews(video1, video2):
    return (float(video1['views']) > float(video2['views']))

def cmpVideosBylikes(video1, video2):
    return (float(video1['likes']) > float(video2['likes']))

def cmpByCountry(video1, video2):
    return ((video1['country']).lower() < (video2['country']).lower())

def cmpByCategory(video1, video2):
    return ((video1['category_id']).lower() < (video2['category_id']).lower())

def cmpByID(video1, video2):
    return ((video1['video_id']).lower() < (video2['video_id']).lower())

def cmpByCategoryID(video1, video2):
    return ((video1['category_id']).lower() < (video2['category_id']).lower())

def cmpCategoryByName(categoria1, categoria2):
    return ((categoria1['name']).lower() < (categoria2['name']).lower())

def cmpByTDate(video1, video2):
    FechaVideo1 = video1['trending_date'].strip().split(".")
    FechaVideo2 = video2['trending_date'].strip().split(".")
    Fecha1Dias = FechaVideo1[0]*365 + FechaVideo1[2]*31 + FechaVideo1[1]
    Fecha2Dias = FechaVideo2[0]*365 + FechaVideo2[2]*31 + FechaVideo2[1]
    return (Fecha1Dias<Fecha2Dias)

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

def VideosByCountry(catalog):
    sub_list = lt.subList(catalog['video'], 1, lt.size(catalog['video']))
    sub_list = sub_list.copy()
    sorted_list = Merge.sort(sub_list, cmpByCountry)
    return sorted_list

def VideosByCategory(catalog):
    sub_list = lt.subList(catalog['video'], 0, lt.size(catalog['video']))
    sub_list = sub_list.copy()
    start_time = time.process_time()
    sorted_list = Merge.sort(sub_list, cmpByCategory)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    return elapsed_time_mseg, sorted_list

def VideosByID(listaOrdenada):
    sub_list = lt.subList(listaOrdenada, 0, lt.size(listaOrdenada))
    sub_list = sub_list.copy()
    sorted_list = sa.sort(sub_list, cmpByID)
    return sorted_list

def VideosByCategoryID(listaOrdenada):
    sub_list = lt.subList(listaOrdenada, 0, lt.size(listaOrdenada))
    sub_list = sub_list.copy()
    sorted_list = Merge.sort(sub_list, cmpByCategoryID)
    return sorted_list

def CategoryByName(catalog):
    sub_list = lt.subList(catalog['category'], 0, lt.size(catalog['category']))
    sub_list = sub_list.copy()
    sorted_list = Merge.sort(sub_list, cmpCategoryByName)
    return sorted_list

def VideosByTDate(listaOrdenada):
    ListaOrdenaDates = lt.newList("ARRAY_LIST")
    inicio = 1
    fin = 1
    i = 2
    ID = lt.getElement(listaOrdenada,1)["video_id"]
    while i <= lt.size(listaOrdenada):
        if (lt.getElement(listaOrdenada,i)["video_id"] == ID):
            fin += 1
        else:
            sub_list = lt.subList(listaOrdenada, inicio-1, fin-inicio) #Revisar
            sub_list = sub_list.copy()
            sorted_list = Merge.sort(sub_list, cmpByTDate)
            j = 1
            while j <= lt.size(sorted_list):
                lt.addLast(ListaOrdenaDates,lt.getElement(sorted_list,j))
                j += 1
            inicio = fin
            ID = lt.getElement(listaOrdenada,i)["video_id"]
        i += 1
    return ListaOrdenaDates

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

