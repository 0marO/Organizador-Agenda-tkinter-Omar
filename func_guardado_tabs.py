
from constantes import *
from tkinter import *

def existencia_de_archivos_tareas():

    try:
        archivo = open(CWD + 'archivos_de_almacenamiento\\archivo_tareas_dia0.csv','r')
        archivo.close()
    except FileNotFoundError:
        archivo = open(CWD + 'archivos_de_almacenamiento\\archivo_tareas_dia0.csv','w')
        archivo.close()

    try:
        archivo = open(CWD + 'archivos_de_almacenamiento\\archivo_tareas_dia1.csv','r')
        archivo.close()
    except FileNotFoundError:
        archivo = open(CWD + 'archivos_de_almacenamiento\\archivo_tareas_dia1.csv','w')
        archivo.close()

    try:
        archivo = open(CWD + 'archivos_de_almacenamiento\\archivo_tareas_dia2.csv','r')
        archivo.close()
    except FileNotFoundError:
        archivo = open(CWD + 'archivos_de_almacenamiento\\archivo_tareas_dia2.csv','w')
        archivo.close()

    try:
        archivo = open(CWD + 'archivos_de_almacenamiento\\archivo_tareas_dia3.csv','r')
        archivo.close()
    except FileNotFoundError:
        archivo = open(CWD + 'archivos_de_almacenamiento\\archivo_tareas_dia3.csv','w')
        archivo.close()

    try:
        archivo = open(CWD + 'archivos_de_almacenamiento\\archivo_tareas_dia4.csv','r')
        archivo.close()
    except FileNotFoundError:
        archivo = open(CWD + 'archivos_de_almacenamiento\\archivo_tareas_dia4.csv','w')
        archivo.close()

    try:
        archivo = open(CWD + 'archivos_de_almacenamiento\\archivo_tareas_dia5.csv','r')
        archivo.close()
    except FileNotFoundError:
        archivo = open(CWD + 'archivos_de_almacenamiento\\archivo_tareas_dia5.csv','w')
        archivo.close()

    try:
        archivo = open(CWD + 'archivos_de_almacenamiento\\archivo_tareas_dia6.csv','r')
        archivo.close()
    except FileNotFoundError:
        archivo = open(CWD + 'archivos_de_almacenamiento\\archivo_tareas_dia6.csv','w')
        archivo.close()

def leer_linea_tareas(archivo):
    # lee lineas del archivo de tareas. Devuelve una lista de tareas y un bool de fin de archivo.
    registro = archivo.readline()
    fin_archivo = False
    if registro:
        registro = registro.rstrip('\n')  # aparecen saltos de línea por alguna razon
        linea = registro.split(',')
    else:
        fin_archivo = True
        linea = 0
    return linea, fin_archivo

def guardar_tarea_ingresada(str_de_tarea, dia_elegido = 'Ninguno',color_elegido = 'white'):

    nombre_archivo_correspondiente = obtener_nombre_archivo(dia_elegido)
    archivo_correspondiente = open(CWD + f'archivos_de_almacenamiento\\{nombre_archivo_correspondiente}','a')
    archivo_correspondiente.write(f',{str_de_tarea}[{color_elegido}]')
    archivo_correspondiente.close()

def guardar_tachado_de_tarea(posicion,tachado = True,dia_elegido = 'Ninguno'):

    nombre_archivo_correspondiente = obtener_nombre_archivo(dia_elegido)
    archivo_correspondiente = open(CWD + f'archivos_de_almacenamiento\\{nombre_archivo_correspondiente}','r')

    # armamos la lista de tareas
    lista_de_tareas_archivadas, fin_archivo = leer_linea_tareas(archivo_correspondiente)
    del lista_de_tareas_archivadas[0]
    archivo_correspondiente.close()

    # agregamos o quitamos el indicador de tachado a la tarea correspondiente.
    tarea_elegida = lista_de_tareas_archivadas[posicion]
    if tachado:
        tarea_elegida = tarea_elegida + '[T]'
        lista_de_tareas_archivadas[posicion] = tarea_elegida
    else:
        tarea_elegida = tarea_elegida.replace('[T]','')
        lista_de_tareas_archivadas[posicion] = tarea_elegida

    # Volcamos todo nuevamente en el archivo.
    archivo_correspondiente = open(CWD + f'archivos_de_almacenamiento\\{nombre_archivo_correspondiente}','w')
    for tarea in lista_de_tareas_archivadas:
        archivo_correspondiente.write(f',{tarea}')
    archivo_correspondiente.close()

def guardar_eliminado_tareas( posiciones_seleccionadas,dia_elegido = 'Ninguno'):

    nombre_archivo_correspondiente = obtener_nombre_archivo(dia_elegido)
    archivo_correspondiente = open(CWD + f'archivos_de_almacenamiento\\{nombre_archivo_correspondiente}','r')
    
    # armamos la lista de tareas
    lista_de_tareas_archivadas, fin_archivo = leer_linea_tareas(archivo_correspondiente)
    del lista_de_tareas_archivadas[0]
    archivo_correspondiente.close()

    # eliminamos las tareas de las posiciones indicadas. 
    posiciones_seleccionadas_al_reves = posiciones_seleccionadas[::-1]
    for selec in posiciones_seleccionadas_al_reves:
        del lista_de_tareas_archivadas[selec]

    # Volcamos todo nuevamente en el archivo.
    archivo_correspondiente = open(CWD + f'archivos_de_almacenamiento\\{nombre_archivo_correspondiente}','w')
    for tarea in lista_de_tareas_archivadas:
        archivo_correspondiente.write(f',{tarea}')
    archivo_correspondiente.close()

def guardar_reposicionamiento_tareas(dia_elegido,lista_de_tareas_archivadas):
    nombre_archivo_correspondiente = obtener_nombre_archivo(dia_elegido)

    # Volcamos todo nuevamente en el archivo.
    archivo_correspondiente = open(CWD + f'archivos_de_almacenamiento\\{nombre_archivo_correspondiente}','w')
    for tarea in lista_de_tareas_archivadas:
        archivo_correspondiente.write(f',{tarea}')

    archivo_correspondiente.close()

def obtener_nombre_archivo(dia):
    dicc_dias_archivos = {'Lunes': 'archivo_tareas_dia0.csv' ,
                        'martes': 'archivo_tareas_dia1.csv',
                        'miercoles': 'archivo_tareas_dia2.csv',
                        'jueves': 'archivo_tareas_dia3.csv',
                        'viernes': 'archivo_tareas_dia4.csv',
                        'sabado': 'archivo_tareas_dia5.csv',
                        'domingo': 'archivo_tareas_dia6.csv'}

    return dicc_dias_archivos[dia]

def mostrar_tareas_guardadas(lista_de_cajas):
    pos_dia = 0
    lista_de_archivos = ['archivo_tareas_dia0.csv',
                        'archivo_tareas_dia1.csv',
                        'archivo_tareas_dia2.csv',
                        'archivo_tareas_dia3.csv',
                        'archivo_tareas_dia4.csv',
                        'archivo_tareas_dia5.csv',
                        'archivo_tareas_dia6.csv']
    
    for archivo in lista_de_archivos:
        caja_de_tareas = lista_de_cajas[pos_dia][POS_LISTBOX] # widget listbox.

        archivo_actual = open(CWD + f'archivos_de_almacenamiento\\{archivo}','r')
        lista_de_tareas_archivadas,fin_archivo = leer_linea_tareas(archivo_actual)
        archivo_actual.close()
        
        if type(lista_de_tareas_archivadas) != int and len(lista_de_tareas_archivadas) != 0: # Si no hay tareas en ese día evita lo siguiente.
            del lista_de_tareas_archivadas[0]
            mostrar_tareas_de_un_dia(caja_de_tareas,lista_de_tareas_archivadas)

        pos_dia += 1 

def mostrar_tareas_de_un_dia(caja_de_tareas,lista_de_tareas_archivadas):
    # recibe widget caja de tareas y una lista de tareas correspondiente, con marcas de formato.
    # identifica las marcas de formato de tachado y color de fondo para mostrar la tarea correctamente.
    for tarea in lista_de_tareas_archivadas:
            color_encontrado = ''
            for color in LISTA_DE_COLORES :   # configuración de subrayado.
                if f'[{color}]' in tarea:
                    color_encontrado = color
                    tarea = tarea.replace(f'[{color}]','')

            if '[T]' in tarea: # se tacha la tarea
                tarea = tarea.replace('[T]','')
                resultado = ''
                for c in tarea:
                    resultado = resultado + c + '\u0336'
                caja_de_tareas.insert(END,resultado)
                caja_de_tareas.itemconfigure(END, fg ='#585858', bg = color_encontrado)
            else:
                caja_de_tareas.insert(END,tarea)
                caja_de_tareas.itemconfigure(END, bg = color_encontrado)
                
def obtener_lista_tareas_guardadas(dia):

    nombre_archivo = obtener_nombre_archivo(dia)
    archivo = open(CWD + f'archivos_de_almacenamiento\\{nombre_archivo}', 'r')
    lista_tareas, fin_archivo = leer_linea_tareas(archivo)
    del lista_tareas[0]
    archivo.close()
    return lista_tareas

def guardar_pasado_de_dia(tareas_a_pasar,dia_a_pasar):
    dia_a_pasar = str(dia_a_pasar)
    dicc_dias_archivos = {'0': 'archivo_tareas_dia0.csv' ,
                        '1': 'archivo_tareas_dia1.csv',
                        '2': 'archivo_tareas_dia2.csv',
                        '3': 'archivo_tareas_dia3.csv',
                        '4': 'archivo_tareas_dia4.csv',
                        '5': 'archivo_tareas_dia5.csv',
                        '6': 'archivo_tareas_dia6.csv'}
    
    archivo = open(CWD + f'archivos_de_almacenamiento\\{dicc_dias_archivos[dia_a_pasar]}','a')
    for tarea in tareas_a_pasar:
        archivo.write(f',{tarea}')
    archivo.close()