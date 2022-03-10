from tkinter import *
from constantes import*
from tkinter import ttk
import pandas as pd
from datetime import date


def al_cerrar_agregar_habitos(ventana):
    lista_con_agregar_entry.clear()
    ventana.destroy()
"""
def agregar_habitos(ventana_nueva_habitos):
    # abre una nueva ventana con un Entry y un botón para agregar su contenido a la tarjeta de habitos. 
    
    ventana_nueva_habitos.place(x= 240, y= 255)
    ventana_nueva_habitos.update()
    lista_con_agregar_entry.append(ventana_nueva_habitos) # para mantener la posicion relativa a la raiz.
    color_fondo = 'white'

    # ENTRY DE HABITOS!
    entrada_habito_frame = ttk.Frame(ventana_nueva_habitos ,style='Card.TFrame')
    entrada_habito_frame.place(x = 10, y = 11)
    
        # string var con maximo de caracteres
    var_entrada_habito = StringVar()
    var_entrada_habito.trace("w", lambda *args: limite_entry(var_entrada_habito, limite = 15))
    
    entrada_habito = Entry(entrada_habito_frame,textvariable = var_entrada_habito, font= ('Source Sans Pro light',10), 
                            borderwidth = 0, selectbackground = '#e0a8cd', selectforeground = 'Black',
                            width= 30)
    entrada_habito.pack(padx= 2, pady= 4)
    entrada_habito.bind("<KeyRelease>", lambda e: pasar_a_mayus(e, var_entrada_habito))

    # BOTON AGREGAR HABITO
    signo_mas_bb = PhotoImage(file= CWD + 'imagenes_del_organizador\\signo_mas.png')
    agregar_tarea = Button(
                    ventana_nueva_habitos,
                    command = lambda: agregar_un_habito_perro(var_entrada_habito,entrada_habito,frame_habitos_propio),
                    activebackground='#f9d6ec',
                    borderwidth = 0,
                    image = signo_mas_bb)
    agregar_tarea.signo_mas_bb = signo_mas_bb # para que no se borre la imagen por el garbage collector
    agregar_tarea.place(x = 170, y = 13)

    # BOTON cerrar ventana

    cerrar_ventana = Button(
                    ventana_nueva_habitos,
                    command = lambda: al_cerrar_agregar_habitos(ventana_nueva_habitos),
                    activebackground='#f9d6ec',
                    borderwidth = 0,
                    text = 'X')
    
    cerrar_ventana.place(x = 220, y = 13)

    entrada_habito.bind('<Return>', lambda e: bind_return_habitos(var_entrada_habito,entrada_habito))
"""
def agregar_un_habito_perro(var_entrada_habito,entrada_habito,circulo_tilddado,circulo_vacio,cruz_eliminar,marcador_de_distancia,frame_habitos_propio, inicio_programa = False,estado_tilde = 'destildado'):
    # Agrega un label con el habito y un circulo tildable en la tarjeta de habitos de la app.
    global fila_hab
    global ultima_fila
    global cantidad_de_habitos
    if not inicio_programa and cantidad_de_habitos < MAX_NRO_HABITOS:
        string_habito = var_entrada_habito.get()
        
        # evitar habitos repetidos:
        no_hay_igual = True
        archivo = open(CWD + 'archivos_de_almacenamiento\\archivo_habitos.txt','r')
        linea, fin_archivo = leer_linea_habitos(archivo)
        while not fin_archivo and no_hay_igual :
            if linea[POS_HABITO] == string_habito:
                no_hay_igual = False
            linea, fin_archivo = leer_linea_habitos(archivo)
        archivo.close()

        if no_hay_igual and string_habito != 'Habito ya ingre':
            guardar_linea_habitos(string_habito, estado_tilde = 'destildado')
    else:
        no_hay_igual = True # en el inicio al cargar no hay repetidos.
        string_habito = var_entrada_habito # la info sale de un csv
    

    if cantidad_de_habitos < MAX_NRO_HABITOS and no_hay_igual and string_habito != 'Habito ya ingre':
        variable_habito_actual = StringVar()
        habito_actual_label = Label(frame_habitos_propio,
                            text = string_habito,
                            font = ('Source Sans Pro black',11),
                            justify= LEFT,
                            )
        habito_actual_label.grid(column= 0, row= fila_hab, sticky = W)  

        boton2 = Button(frame_habitos_propio,image= circulo_vacio ,
                        command= lambda: tildar_habito(boton2,string_habito,habito_actual_label,variable_habito_actual,circulo_tilddado,circulo_vacio),
                        borderwidth=0,
                        activebackground= 'white')
        boton2.grid(column = 1, row = fila_hab, padx= 0 )
        boton2.circulo_vacio = circulo_vacio
             
        bt_eliminar_hab = Button(frame_habitos_propio,
                        image = cruz_eliminar,
                        command= lambda: eliminar_habito(boton2,bt_eliminar_hab,habito_actual_label,string_habito),
                        borderwidth=0)
        bt_eliminar_hab.grid(column = 2, row = fila_hab, padx= 20, pady= [2,0] )

        if estado_tilde == 'tildado': # solo puede ocurrir al inicio.
            tildar_habito_al_inicio(boton2,string_habito,habito_actual_label,variable_habito_actual,circulo_tilddado)  
        
        cantidad_de_habitos += 1
        fila_hab += 1
        ultima_fila += 1
        marcador_de_distancia.grid(column= 0, row = ultima_fila)

        try:
            var_entrada_habito.set('')
        except AttributeError:
            pass

    elif cantidad_de_habitos < MAX_NRO_HABITOS and (no_hay_igual == False or string_habito == 'Habito ya ingre'):
        var_entrada_habito.set('Habito ya ingresado!!')
    else:
        entrada_habito.config(fg = 'red')
        var_entrada_habito.set('Maximo de habitos alcanzado')

def bind_return_habitos(var_entrada_habito,entrada_habito,circulo_tilddado,circulo_vacio,cruz_eliminar,marcador_de_distancia,frame_habitos_propio):
    agregar_un_habito_perro(var_entrada_habito,entrada_habito,circulo_tilddado,circulo_vacio,cruz_eliminar,marcador_de_distancia,frame_habitos_propio)
    
def limite_entry(entry_text, limite = 5):
    # setea una cantidad maxima de caracteres en un entry, por defecto es 5
    # se usa como comando en junto al metodo .trace de una stringvar.
    if len(entry_text.get()) > 0:
        entry_text.set(entry_text.get()[:limite])

def pasar_a_mayus(event, var_entrada_habito):
    # Convierte todas las letras ingresadas en el entry de habitos a mayusculas.
    var_entrada_habito.set(var_entrada_habito.get().upper())

def tildar_habito(boton2,string_habito,habito_actual_label,variable_habito_actual,circulo_tilddado,circulo_vacio):
    # tilda o destilda la checkbox, tacha y cambia de color el label del habito (o lo revierte)
    resultado = ''
    contenido_variable = variable_habito_actual.get() 
    if '\u0336' not in contenido_variable: # si el habito NO está tachado.
        for c in string_habito:
            resultado = resultado + c + '\u0336'# agregar tachado

        boton2.config(image= circulo_tilddado) # cambio de imagen acorde
        boton2.circulo_tilddado = circulo_tilddado
        habito_actual_label.config( text = resultado, fg ='Green' )
        actualizar_habito(string_habito,tildado = True)
    else:
        string_encode = variable_habito_actual.get().encode("ascii", "ignore")  #sacar tachado.
        resultado = string_encode.decode()
        boton2.config(image = circulo_vacio) # cambio de imagen acorde
        boton2.circulo_vacio = circulo_vacio
        habito_actual_label.config( text = resultado, fg= 'black')
        actualizar_habito(string_habito)

    variable_habito_actual.set(resultado) # almacenar el nuevo estado del  label habito

def tildar_habito_al_inicio(boton2,string_habito,habito_actual_label,variable_habito_actual,circulo_tilddado):
    resultado = ''
    for c in string_habito:
        resultado = resultado + c + '\u0336'# agregar tachado

    boton2.config(image= circulo_tilddado) # cambio de imagen acorde
    boton2.circulo_tilddado = circulo_tilddado
    habito_actual_label.config( text = resultado, fg ='Green' )
    variable_habito_actual.set(resultado) # almacenar el nuevo estado del  label habito

def agregar_habitos_guardados(frame_habitos_propio,marcador_de_distancia,circulo_vacio,cruz_eliminar,circulo_tilddado):
    archivo = open(CWD + 'archivos_de_almacenamiento\\archivo_habitos.txt','r')  # abre el archivo
    linea, fin_archivo = leer_linea_habitos(archivo)

    if linea == ['']:  # por si aparecen \n no deseados al principio
        linea, fin_archivo = leer_linea_habitos(archivo)
    
    # si cambia de día se resetean los habitos.
    hoy = date.today()  
    fecha_hoy = hoy.strftime("%Y-%m-%d")

    try:
        importamos_el_csv = pd.read_csv(CWD + 'archivos_de_almacenamiento\\data_habitos.csv')
        importamos_el_csv = importamos_el_csv.transpose(copy=False)
        ultima_fecha_registrada = list(importamos_el_csv.columns)[-1]
        importamos_el_csv = importamos_el_csv.transpose(copy=False)
    except FileNotFoundError:
        ultima_fecha_registrada = 'No existe'

    if fecha_hoy != ultima_fecha_registrada:

        archivo_temporal = open(CWD + 'archivos_de_almacenamiento\\archivo_habitosTEMP.txt','w') # Para almacenar todos los habitos, destildados.
        archivo_temporal.close()
        while not fin_archivo:
            if linea:
                agregar_un_habito_perro(linea[POS_HABITO],None,circulo_tilddado,circulo_vacio,cruz_eliminar,marcador_de_distancia,frame_habitos_propio, inicio_programa = True, estado_tilde= 'destildado')
            guardar_linea_habitos(linea[POS_HABITO],nuevo_dia= True)
            linea, fin_archivo = leer_linea_habitos(archivo)
        
        archivo.close() # cierra el archivo
        os.remove(CWD + 'archivos_de_almacenamiento\\archivo_habitos.txt')
        os.rename(CWD + 'archivos_de_almacenamiento\\archivo_habitosTEMP.txt', CWD + 'archivos_de_almacenamiento\\archivo_habitos.txt')
    else:
        while not fin_archivo:
            if linea:
                agregar_un_habito_perro(linea[POS_HABITO],None ,circulo_tilddado,circulo_vacio,cruz_eliminar,marcador_de_distancia,frame_habitos_propio, inicio_programa = True, estado_tilde= linea[POS_ESTADO_HABITO])
            linea, fin_archivo = leer_linea_habitos(archivo)
        
        archivo.close() # cierra el archivo
    
def leer_linea_habitos(archivo):
    registro = archivo.readline()
    fin_archivo = False
    linea = None
    if registro:
        registro = registro.rstrip('\n')
        linea = registro.split(',')
    else:
        fin_archivo = True
        
    return linea, fin_archivo

def guardar_linea_habitos(string_habito, estado_tilde = 'destildado',nuevo_dia = False):
    
    if nuevo_dia:
        archivo = open(CWD + 'archivos_de_almacenamiento\\archivo_habitosTEMP.txt','a')
        archivo.write(f'\n{string_habito},{estado_tilde}')
        archivo.close()
    else:
        archivo = open(CWD + 'archivos_de_almacenamiento\\archivo_habitos.txt','a')
        archivo.write(f'\n{string_habito},{estado_tilde}')
        archivo.close()

def eliminar_habito(boton2,bt_eliminar_hab,habito_actual_label, string_habito):
    # busca los habitos guardados en un archivo, como son maximo 10, los pone en una lista,
    # y los vuelve a escribir en el archivo evitando el que se desea eliminar.
    global cantidad_de_habitos
    archivo = open(CWD + 'archivos_de_almacenamiento\\archivo_habitos.txt','r')
    lista_de_habitos = []
    linea, fin_archivo = leer_linea_habitos(archivo)
    while not fin_archivo and linea:
        if linea[POS_HABITO] != string_habito:
            lista_de_habitos.append(linea)
        linea, fin_archivo = leer_linea_habitos(archivo)
    archivo.close()

    if lista_de_habitos and lista_de_habitos[0] == ['']: # por alguna razon queda un espacio en blanco al principio después de eliminar todos los habitos.
        del (lista_de_habitos[0])
    principio = True
    archivo = open(CWD + 'archivos_de_almacenamiento\\archivo_habitos.txt','w')
    for habito,estado in lista_de_habitos:
        if principio:
            archivo.write(f'{habito},{estado}')
            principio = False
        else:
            archivo.write(f'\n{habito},{estado}')
    archivo.close()
    boton2.destroy()
    habito_actual_label.destroy()
    bt_eliminar_hab.destroy()

    cantidad_de_habitos -= 1

def actualizar_habito(string_habito,tildado = False):
    # abre el registro de habitos, almacena en una lista todos los habitos y su estado,
    # cierra el archivo y lo abre para sobreescribirlo con la actualizacion del tildado.
    archivo = open(CWD + 'archivos_de_almacenamiento\\archivo_habitos.txt','r')
    lista_de_habitos = []
    linea, fin_archivo = leer_linea_habitos(archivo)

    while not fin_archivo:
        if tildado and linea[POS_HABITO] == string_habito :
            linea[POS_ESTADO_HABITO] = 'tildado'
            lista_de_habitos.append(linea)
        elif (not tildado) and linea[POS_HABITO] == string_habito:
            linea[POS_ESTADO_HABITO] = 'destildado'
            lista_de_habitos.append(linea)
        else:
            lista_de_habitos.append(linea)
        linea, fin_archivo = leer_linea_habitos(archivo)
    archivo.close()
    if lista_de_habitos[0] == ['']:
        del (lista_de_habitos[0])
    if lista_de_habitos:
        principio = True
        archivo = open(CWD + 'archivos_de_almacenamiento\\archivo_habitos.txt','w')
        for habito,estado in lista_de_habitos:
            if principio:
                archivo.write(f'{habito},{estado}')
                principio = False
            else:
                archivo.write(f'\n{habito},{estado}')
        archivo.close()

def cheat_data_habitos():
    archivo = open(CWD + 'archivos_de_almacenamiento\\data_habitos.csv','r')
    archivo_temporal = open(CWD + 'archivos_de_almacenamiento\\data_habitosTEMP.csv','w',newline='')
    linea = archivo.readline()
    linea = linea.rstrip().split(',')
    del(linea[0])
    linea = ','.join(linea) # string de la primera linea sin la coma inicial.
    archivo_temporal.write(f'{linea}')
    linea = archivo.readline().rstrip()
    while linea: # DUMP
        archivo_temporal.write(f'\n{linea}')
        linea = archivo.readline().rstrip()

    archivo.close()
    archivo_temporal.close()
    os.remove(CWD + 'archivos_de_almacenamiento\\data_habitos.csv')
    os.rename(CWD + 'archivos_de_almacenamiento\\data_habitosTEMP.csv', CWD + 'archivos_de_almacenamiento\\data_habitos.csv')
