"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
assert cf
import time

#default_limit = 1000
#sys.setrecursionlimit(default_limit*10)

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Requerimiento 1")
    print("3- Requerimiento 2")
    print("4- Requerimiento 3")
    print("5- Requerimiento 4")
    print("Escriba cualquier otro número para detener la ejecución del programa")

catalog = {}
cataOrdenPaises = {}
cataOrdenCategorias = {}

def initCatalog ():
    return controller.initCatalog()

def loadData(catalog):
    controller.loadData(catalog)

def printResultVideosByViews(listaOrdenada, paisInteres,sample=10):
    size = lt.size(listaOrdenada)
    if size <= sample:
        print("No se pueden imprimir los videos que se están buscando debido a que exceden el número de muestras disponibles para alguno de los parámetros ingresados.")
        print("Los primeros ", size, " videos con más likes del pais ", paisInteres," son:")        
    else:
        print("Los primeros ", sample, " videos con más likes del pais ", paisInteres," son:")        
    i=1
    while i<= sample:
        video = lt.getElement(listaOrdenada,i)
        print(i,'- Fecha de tendencia: ',video['trending_date'],'; Titulo: '+ video['title'],'; Nombre del Canal: ', video['channel_title'], '; Fecha de publicación', video['publish_time'],'; Visitas del Video: ', video['views'],'; Likes del Video: ',video['likes'],'; Dislikes del Video: ',video['dislikes'])
        i+=1

def printResultVideosByLikes(listaOrdenada, paisInteres, TagInteres, sample):
    size = lt.size(listaOrdenada)
    if size <= sample:
        print("No se pueden imprimir los videos que se están buscando debido a que exceden el número de muestras disponibles para alguno de los parámetros ingresados.")
        print("Los primeros ", size, " videos con más likes del pais ", paisInteres," son para el tag ",TagInteres," son:")        
    else:
        print("Los primeros ", sample, " videos con más likes del pais ", paisInteres," son para el tag ",TagInteres," son:")        
    i=1
    while i<= sample:
        video = lt.getElement(listaOrdenada,i)
        print(i,'- Titulo: '+ video['title'],'; Nombre del Canal: ', video['channel_title'], '; Fecha de publicación', video['publish_time'],'; Visitas del Video: ', video['views'],'; Likes del Video: ',video['likes'],'; Dislikes del Video: ',video['dislikes'],'; tags del Video: ',video['tags'])
        i+=1

def VideoPaisConMasTendencia(catalog,paisInteres):
    return controller.VideoPaisConMasTendencia(catalog,paisInteres)

def printTodasLasCategorias(catalog):
    i=1
    while i<=lt.size(catalog['category']):
        print(i,'-ID: ',lt.getElement(catalog['category'],i)['Category_id'],'; Name: ',lt.getElement(catalog['category'],i)['name'])
        i+=1

def VideoCategoriaConMasTendencia(catalog, catalogOrdenado,categoria):
    return controller.VideoCategoriaConMasTendencia(catalog,catalogOrdenado,categoria)

"""
Menu principal
"""
while True:
    printMenu()
    inputs = int(input('Seleccione una opción para continuar\n'))
    if inputs == 1:
        print("Cargando información de los archivos ....")
        t1 = time.process_time()
        catalog = initCatalog()
        loadData(catalog)
        t2 = time.process_time()
        time_mseg = (t2 - t1)*1000
        print('Videos cargados exitósamente: ' + str(lt.size(catalog['video'])))
        video=lt.getElement(catalog['video'],1)
        print('1- Titulo: '+ video['title'],'; Nombre del Canal: ', video['channel_title'], 'Fecha de tendencia: ',video['trending_date'],'; Visitas del Video: ', video['views'],'; Likes del Video: ',video['likes'],'; Dislikes del Video: ',video['dislikes'])
        printTodasLasCategorias(catalog)
        print ("Tiempo de ejecucion: ",time_mseg," milisegundos.")

    elif inputs == 2:
        if len(catalog)==0:
            print("No se han cargado datos al catálogo, por favor realize la opción 1 antes de proseguir.")
        else:
            numeroElementos= int(input("¿Cuantos videos con más views desea conocer?:\t"))
            while numeroElementos>lt.size(catalog['video']) or numeroElementos<=0 :
                print("Está tratando de comparar más o menos elementos de los que cuenta el catálogo de videos. El máximo de videos que se pueden comprar son: ",lt.size(catalog['video']), ". El mínimo es 1.")
                numeroElementos= int(input("¿Cuantos elementos quiere comparar?:\t"))
            if len(cataOrdenPaises)==0:
                start_time = time.process_time()
                print("Estamos ordenando la lista por orden de paises esto puede tardar unos cuantos segundos")
                cataOrdenPaises=controller.OrdenCatalogoPaises(catalog)
                stop_time = time.process_time()
                tiempoO = (stop_time - start_time)*1000
                print("El tiempo de ejecución del ordenamiento es: ",tiempoO)
            start_time = time.process_time()
            categoriaInteres=input("Ingrese el nombre de la categoría de interes:\t")
            idCategoria=controller.asignarNombreCategoryToID(catalog,categoriaInteres)
            if idCategoria==-1:
                print("La categoría consultada no existe intente nuevamente")
            else:
                paisInteres = input("Ingrese el nombre del país del cual quiere conocer los videos con más views por categoría:\t")
                listaVideoViesPais=controller.VideosConMasViewsPorPais(cataOrdenPaises,paisInteres,idCategoria)
                stop_time = time.process_time()
                elapsed_time_mseg = (stop_time - start_time)*1000
                if listaVideoViesPais==-1:
                    print("El país ingresado no se encuentra en el arreglo, intente con otro país.")
                else:
                    printResultVideosByViews(listaVideoViesPais,paisInteres,numeroElementos)
                print("El tiempo de ejecución de la consulta es: ",elapsed_time_mseg)

    elif inputs == 3:
        if len(catalog)==0:
            print("No se han cargado datos al catálogo, por favor realize la opción 1 antes de proseguir.")
        else:
            if len(cataOrdenPaises)==0:
                start_time = time.process_time()
                print("Estamos ordenando la lista por orden de paises esto puede tardar unos cuantos segundos")
                cataOrdenPaises=controller.OrdenCatalogoPaises(catalog)
                stop_time = time.process_time()
                tiempoO = (stop_time - start_time)*1000
                print("El tiempo de ejecución del ordenamiento es: ",tiempoO)
            start_time = time.process_time()
            paisInteres = input("Ingrese el nombre del país del cual quiere conocer el video que más días a sido tendencia:\t")
            result,DiasEnTendencia=VideoPaisConMasTendencia(cataOrdenPaises,paisInteres)
            stop_time = time.process_time()
            elapsed_time_mseg = (stop_time - start_time)*1000
            if result==-1:
                print("El país ingresado no se encuentra en el arreglo, intente con otro país.")
            else:
                print("El título del video es: ",result['title'],"; el nombre del canal es: ",result['channel_title'],"; el país en el que es tendencia: ",result['country']," sus días siendo tendencia son: ",DiasEnTendencia)
            print("El tiempo de ejecución de la consulta es: ",elapsed_time_mseg)

    elif inputs == 4:
        if len(catalog)==0:
            print("No se han cargado datos al catálogo, por favor realize la opción 1 antes de proseguir.")
        else:
            if len(cataOrdenCategorias)==0:
                print("Estamos ordenando la lista por orden de categorias, esto puede tardar unos cuantos segundos")
                tiempoO,cataOrdenCategorias=controller.OrdenCatalogoCategorias(catalog)
                print("El tiempo de ejecución del ordenamiento es: ",tiempoO)
            categoria = input("Ingrese el nombre de la categoria de la cual quiere conocer el video que más días a sido tendencia:\t")
            start_time = time.process_time()
            result,DiasEnTendencia=VideoCategoriaConMasTendencia(catalog,cataOrdenCategorias,categoria)
            stop_time = time.process_time()
            elapsed_time_mseg = (stop_time - start_time)*1000
            if result==-1:
                print("La categoria ingresada no se encuentra en el arreglo, intente con otra categoria.")
            else:
                print("El título del video es: ",result['title'],"; el nombre del canal es: ",result['channel_title'],"; el id de la categoria es: ",result['category_id'],"; sus días siendo tendencia son: ",DiasEnTendencia)
            print("El tiempo de ejecución de la consulta es: ",elapsed_time_mseg)

    elif inputs == 5:
        if len(catalog)==0:
            print("No se han cargado datos al catálogo, por favor realize la opción 1 antes de proseguir.")
        else:
            numeroElementos= int(input("¿Cuantos videos con más likes desea conocer?:\t"))
            while numeroElementos>lt.size(catalog['video']) or numeroElementos<=0 :
                print("Está tratando de comparar más o menos elementos de los que cuenta el catálogo de videos. El máximo de videos que se pueden comprar son: ",lt.size(catalog['video']), ". El mínimo es 1.")
                numeroElementos= int(input("¿Cuantos elementos quiere comparar?:\t"))
            if len(cataOrdenPaises)==0:
                start_time = time.process_time()
                print("Estamos ordenando la lista por orden de paises esto puede tardar unos cuantos segundos")
                cataOrdenPaises=controller.OrdenCatalogoPaises(catalog)
                stop_time = time.process_time()
                tiempoO = (stop_time - start_time)*1000
                print("El tiempo de ejecución del ordenamiento es: ",tiempoO)
            start_time = time.process_time()
            TagInteres=input("Ingrese el nombre del tag que desea consultar:\t")
            paisInteres = input("Ingrese el nombre del país del cual quiere conocer los videos con más likes en el tag de interés:\t")
            print("Estamos realizando su consulta re reogamos que tenga un poco de paciencia")
            print("Desea conocer los resultados con videos repetidos?")
            print("1- Si")
            print("2- No")
            opcion=int(input("Ingrese su selección opción:\t"))
            while not(opcion<=2 and opcion>=1):
                print("Opción invalida intente nuevamente")
                print("Desea conocer los resultados con videos repetidos?")
                print("1- Si")
                print("2- No")
                opcion=int(input("Ingrese su selección opción:\t"))
            listaVideoLikesTag=controller.VideosConMasLikesPorPaisTag(cataOrdenPaises,paisInteres,TagInteres,numeroElementos,opcion)
            stop_time = time.process_time()
            elapsed_time_mseg = (stop_time - start_time)*1000
            if listaVideoLikesTag==-1:
                print("El pais ingresado no existe en la lista intente nuevamente")
            else:
                printResultVideosByLikes(listaVideoLikesTag,paisInteres,TagInteres,numeroElementos)
                print("El tiempo de ejecución de la consulta es: ",elapsed_time_mseg)
    else:
        sys.exit(0)
sys.exit(0)