from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkcalendar import Calendar
from datetime import date

from constantes import *
from tabs import leer_linea, copiar_en_portapapeles

def buscar_registro_del_dia (fecha_selec):
    # recibe un objeto de date.date, busca un registro de tareas para el día seleccionado del calendario
    # devuelve una lista de las tareas(vacía o no) segun las tareas guardadas en ese día.
    
    archivo = open(CWD + 'archivos_de_almacenamiento\\archivo_notas_mensuales.txt', 'r')
    linea, fin_archivo = leer_linea(archivo)
    registro_encontrado = False # condicion de corte
    fecha_seleccionada = fecha_selec.get()
    while (not fin_archivo) and (registro_encontrado == False):
        if fecha_seleccionada == linea[0]: # la primera pos de linea tiene el str de la fecha.
            registro_encontrado = True
        else:
            linea, fin_archivo = leer_linea(archivo)
    
    archivo.close()

    return linea

def bt_eliminar_tareas_mensual(caja_de_tareas_mensual,calendario,str_fecha_del_toplevel):
    # recibe la caja de tareas de algún dia del mes seleccionado y el widget calendario.
    # Elimina la aparicion de la/s tareas seleccionadas de ambos.
    seleccionado = caja_de_tareas_mensual.curselection() # tupla de posiciones seleccionadas.
    fecha_selec = str_fecha_del_toplevel
    
    # el dicc tiene clave de fecha y como valor una lista de listas. 'dd-mm-aa' : [[POS_TAREA,POS_EVENTO], [POS_TAREA,POS_EVENTO]]
    tareas_de_fecha = dicc_tareas_tooltip[fecha_selec] 
    
    for selec in seleccionado[::-1]: # itera sobre posiciones seleccionadas por el usuario
        
        # Primero obtenemos el nombre de la tarea
        nombre_tarea = caja_de_tareas_mensual.get(selec)

        # le sacamos el formato para buscar en el dicc.
        string_encode = nombre_tarea.encode("ascii", "ignore") 
        resultado = string_encode.decode()
        resultado = resultado.lstrip(' ')

        # iteramos sobre la tarea para obtener las buscadas
        finalizado,pos_actual, pos_max = False, 0 , len(tareas_de_fecha) - 1 
        id_tarea_a_borrar = None
        while not finalizado and pos_actual <= pos_max:
            if tareas_de_fecha[pos_actual][POS_TAREA] == resultado:
                id_tarea_a_borrar = tareas_de_fecha[pos_actual][POS_EVENTO]
                del (tareas_de_fecha[pos_actual]) # Sacamos la tarea de la lista para no iterarla denuevo.
                finalizado = True
            else:
                pos_actual += 1

        # Se elimina la tarea del tooltip usando su id
        calendario.calevent_remove(id_tarea_a_borrar, tag = 'recordatorio')

        # Se elimina la tarea de la listbox
        caja_de_tareas_mensual.delete(selec)

def al_cerrar_notas_mensuales(ventana,str_fecha_seleccionada):
    del dicc_ventanas_calendario[str_fecha_seleccionada]
    ventana.destroy()

def notas_mensuales(e,fecha_selec, calendario, raiz_general):
    # Crea los widgets para la lista de tareas mensual, en una nueva ventana, similar a la lista de tareas semanal.
    
    if fecha_selec.get() not in dicc_ventanas_calendario: # evita abrirla si la ventana de la fecha ya se creó
        registro_dia  = buscar_registro_del_dia (fecha_selec)
        fecha_de_hoy = fecha_selec
        fecha_str_lista = [f'{fecha_selec.get()}'] # cochinada para poder mandarla como una string


        ventana_nueva = Toplevel(raiz_general)
        ventana_nueva.protocol("WM_DELETE_WINDOW",lambda: al_cerrar_notas_mensuales(ventana_nueva,fecha_str_lista[0]) )
        ventana_nueva.attributes('-topmost', 'true')
        ventana_nueva.resizable(0,0)
        x = raiz_general.winfo_x()
        y = raiz_general.winfo_y()
        ventana_nueva.geometry("230x340+%d+%d" % (x + 375, y + 30))
        ventana_nueva.title(fecha_str_lista[0])
        color_fondo = 'white'

        # ENTRY DE TAREAS
        entrada_nombre_frame = ttk.Frame(ventana_nueva ,style='Card.TFrame')
        entrada_nombre_frame.place(x = 10, y = 11)
        var_entrada = StringVar()
        entrada_nombre = Entry(entrada_nombre_frame,textvariable = var_entrada, font= ('Source Sans Pro Light',10), 
                                borderwidth = 0, selectbackground = '#e0a8cd', selectforeground = 'Black')
        entrada_nombre.pack(padx= 2, pady= 4)


        # BOTON AGREGAR TAREAS
        signo_mas_bb = PhotoImage(file= CWD + 'imagenes_del_organizador\\signo_mas.png')
        agregar_tarea = Button(
                        ventana_nueva,
                        command= lambda: [poner_en_tooltip(calendario,fecha_str_lista[0],var_entrada), bt_agregar_tarea_mensual(caja_de_tareas_mensual , var_entrada,entrada_nombre), guardar_tareas_mensuales(fecha_str_lista[0],caja_de_tareas_mensual)],
                        activebackground='#f9d6ec',
                        borderwidth = 0,
                        image = signo_mas_bb)
        agregar_tarea.signo_mas_bb = signo_mas_bb # para que no se borre la imagen por el garbage collector
        agregar_tarea.place(x = 140, y = 13)

        # BOTON COPIAR SELECCIONADAS TAREAS
        imagen_copiar = PhotoImage(file= CWD + 'imagenes_del_organizador\\icono_copiar_R.png')
        copiar_tareas = Button(
                        ventana_nueva,
                        command= lambda: copiar_en_portapapeles(caja_de_tareas_mensual),
                        activebackground='#f9d6ec',
                        borderwidth = 0,
                        image= imagen_copiar)
        copiar_tareas.imagen_copiar = imagen_copiar # para que no se borre la imagen por el garbage collector
        copiar_tareas.place(x = 165, y = 13)

        # BOTON PEGAR tareas en portapapeles.
        imagen_pegar = PhotoImage(file= CWD + 'imagenes_del_organizador\\icono_pegado_R.png')
        pegar_tareas_notas = Button(
                        ventana_nueva,
                        command= lambda: [pegar_tareas_portapapeles_mensual(calendario,fecha_str_lista[0],caja_de_tareas_mensual), guardar_tareas_mensuales(fecha_str_lista[0],caja_de_tareas_mensual)],
                        activebackground='#f9d6ec',
                        borderwidth = 0,
                        image = imagen_pegar)
        pegar_tareas_notas.imagen_pegar = imagen_pegar # para que no se borre la imagen por el garbage collector
        pegar_tareas_notas.place(x = 185, y = 13)

        # LISTBOX DE TAREAS
        var_caja_tareas = StringVar()
        fuente_utilizada =('Source Sans Pro Light', 15)
        caja_de_tareas_mensual = Listbox(ventana_nueva,
                            justify= LEFT,
                            height= 8,
                            width= 19,
                            bd=0 ,
                            bg= color_fondo,
                            highlightthickness = 0,
                            selectbackground=color_fondo,
                            selectforeground = '#e0a8cd',
                            activestyle = 'none',
                            font = fuente_utilizada,
                            selectmode=tk.EXTENDED,
                            listvariable= var_caja_tareas
                            )
        caja_de_tareas_mensual.place(x = 10, y= 60)


        if registro_dia != 0: # mostrar las tareas guardadas al abrir.
            insertar_tareas_en_listbox(caja_de_tareas_mensual, registro_dia[1:])


        # SCROLLBAR listbox VERTICAL
        scroll_vertical = ttk.Scrollbar(ventana_nueva, orient= 'vertical')
        scroll_vertical.place(x=215, y = 49, height= 200, width= 10)
        caja_de_tareas_mensual.config(yscrollcommand= scroll_vertical.set)
        scroll_vertical.config(command= caja_de_tareas_mensual.yview)

        # SCROLLBAR listbox HORIZONTAL
        scroll_horizontal= ttk.Scrollbar(ventana_nueva, orient= 'horizontal')
        scroll_horizontal.place(x= 70, y = 320,  height= 10, width = 100)
        caja_de_tareas_mensual.config(xscrollcommand= scroll_horizontal.set)
        scroll_horizontal.config(command= caja_de_tareas_mensual.xview)

        # BOTÓN BORRAR TAREAS
        tacho_cerrado = PhotoImage(file = CWD + 'imagenes_del_organizador\\tachito_rosa_cerrado.png')
        tacho_abierto = PhotoImage(file = CWD + 'imagenes_del_organizador\\tachito_rosa_abierto.png')
        eliminar_tildadas = Button(ventana_nueva, text='-' ,
                                    command= lambda: [bt_eliminar_tareas_mensual(caja_de_tareas_mensual,calendario,fecha_str_lista[0]),guardar_tareas_mensuales(fecha_str_lista[0],caja_de_tareas_mensual)],
                                    borderwidth = 0 , image = tacho_cerrado , activebackground= '#f9d6ec' )
        eliminar_tildadas.place(x = 0, y = 300)
        eliminar_tildadas.tacho_cerrado = tacho_cerrado

        # guardado del toplevel en diccionario para trackearlo y evitar multiples fechas iguales abiertas.
        dicc_ventanas_calendario[fecha_str_lista[0]] = ventana_nueva
        
        # binds del toplevel de tareas mensuales
        entrada_nombre.bind('<Return>', lambda e: bind_intro_mensual(e,calendario,fecha_str_lista[0],var_entrada,caja_de_tareas_mensual, entrada_nombre,fecha_str_lista[0])) # agregar tareas
        caja_de_tareas_mensual.bind('<Delete>', lambda e: bind_suprimir_mensual(e,caja_de_tareas_mensual,calendario,fecha_str_lista[0])) # eliminar tareas

def bind_intro_mensual(e,calendario,fecha_selec,var_entrada,caja_de_tareas_mensual, entrada_nombre,fecha_de_hoy):
    poner_en_tooltip(calendario,fecha_selec,var_entrada)
    bt_agregar_tarea_mensual(caja_de_tareas_mensual , var_entrada,entrada_nombre)
    guardar_tareas_mensuales(fecha_de_hoy,caja_de_tareas_mensual)

def bind_suprimir_mensual(e,caja_de_tareas_mensual,calendario,fecha_de_hoy):
    bt_eliminar_tareas_mensual(caja_de_tareas_mensual,calendario,fecha_de_hoy)
    guardar_tareas_mensuales(fecha_de_hoy,caja_de_tareas_mensual)

def poner_en_tooltip(calendario,fecha_selec,var_entrada,es_inicio = False):
    # recibe el widget calendario, fecha seleccionada, la var que almacena la str de la tarea.
    # crea un evento en el calendario visualizado por el usuario cuando pasa el mouse sobre
    # el dia.


    if not es_inicio:
        lista_fecha = fecha_selec.split('/')
    else:
        lista_fecha = fecha_selec.split('/')  #no hace falta el get por que viene de un csv.
    nro_dia_selec , mes_seleccionado ,año_seleccionado  = lista_fecha
    nro_dia_selec , mes_seleccionado ,año_seleccionado  = int(nro_dia_selec ), int(mes_seleccionado) ,int(año_seleccionado) + 2000
    
    d = calendario.datetime(año_seleccionado,mes_seleccionado,nro_dia_selec)
    
    if not es_inicio: # asi no hay tareas vacías.
        if  var_entrada.get() != '':
            id_evento = calendario.calevent_create(d,var_entrada.get(), 'recordatorio')
            if fecha_selec not in dicc_tareas_tooltip:
                dicc_tareas_tooltip[fecha_selec] = [[var_entrada.get(),id_evento]]
            else:
                dicc_tareas_tooltip[fecha_selec].append([var_entrada.get(),id_evento])
    else:
        # si es el inicio de la app, las fechas ya son str, que salen de el csv archivo_tareas_mensuales.txt
        id_evento = calendario.calevent_create(d,var_entrada, 'recordatorio')   #no hace falta el get por que viene de un csv.
        
        if fecha_selec not in dicc_tareas_tooltip:
            dicc_tareas_tooltip[fecha_selec] = [[var_entrada,id_evento]]  
        else:
            dicc_tareas_tooltip[fecha_selec].append([var_entrada,id_evento])

def bt_agregar_tarea_mensual(caja_de_tareas , var_entrada,entrada_nombre):
    # funcion que agrega una string a una listbox. es usada para las tabs y para el almanaque
    # lista_de_cajas es una lista con las cajas de tareas de las tabs, en cambio lista_de_cajas = False cuando se usa en el almanaque.
    str_de_tarea = var_entrada.get()
    if str_de_tarea != '': # asi no hay tareas vacías.
        caja_de_tareas.insert(END , "• " + str_de_tarea) #  Con bullet point.
        entrada_nombre.delete(0, 'end')

def guardar_tareas_mensuales(fecha_de_hoy,caja_de_tareas_mensual):
    # actualiza las tareas mensuales en los archivos, tanto si hay que guardar nuevas como si hay que sacar borradas.
    fecha_actual = str(fecha_de_hoy)
    tareas_existentes = caja_de_tareas_mensual.get(0,END)
    
    dicc_temporal = {} # dicc de pares "[2022,1,20] : [2022,1,20,tarea1,tarea2.....]" 
    archivo = open(CWD + 'archivos_de_almacenamiento\\archivo_notas_mensuales.txt','r')
    linea, fin_archivo = leer_linea_mensual(archivo)
    while not fin_archivo:
        fecha = linea[0] # de formato dd/mm/aa
        if fecha not in dicc_temporal:
            dicc_temporal[fecha] = linea
        else:
            dicc_temporal[fecha] = dicc_temporal[fecha] + linea[1:] # por las dudas que se repita la fecha en el archivo.
        linea, fin_archivo = leer_linea_mensual(archivo)

    # si está repetida la fecha se guarda lo nuevo, si es una fecha nueva se agrega.

    
    lista_tareas_existentes = list(tareas_existentes)
    lista_tareas_existentes.insert(0,fecha_actual)
    dicc_temporal[fecha_actual] = lista_tareas_existentes

    archivo.close()
    
    archivo = open(CWD + 'archivos_de_almacenamiento\\archivo_notas_mensuales.txt','w')  # Ahora lo sobreescribimos
    for clave, registro in dicc_temporal.items():
        if len(registro) > 1:
            archivo.write(f'{registro[0]}')
            reg_sin_fecha = registro[1:] 

            for valor in reg_sin_fecha:
                string_encode = valor.encode("ascii", "ignore")
                resultado = string_encode.decode()
                resultado = resultado.lstrip(' ')
                archivo.write(f',{resultado}')
            archivo.write('\n')  #salto de linea para el siguiente registro.
    archivo.close()

def pegar_tareas_portapapeles_mensual(calendario,fecha_selec,caja_de_tareas):
    if len(lista_portapapeles) != 0:
        for tarea_copiada in lista_portapapeles:

            string_encode = tarea_copiada.encode("ascii", "ignore")
            resultado = string_encode.decode()
            resultado = resultado.lstrip(' ')
            poner_en_tooltip(calendario,fecha_selec,resultado,es_inicio = True)
            caja_de_tareas.insert(END,tarea_copiada)

    lista_portapapeles.clear()

def insertar_tareas_en_listbox(caja_de_tareas, tareas_guardadas):
    # itera la lista de tareas (str), por cada el. de la lista lo inserta en la caja de tareas.
    for tarea in tareas_guardadas:
        caja_de_tareas.insert(END, tarea)

def leer_linea_mensual(archivo):
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

def poner_en_tooltip_al_inicio(calendario):
    archivo = open(CWD + 'archivos_de_almacenamiento\\archivo_notas_mensuales.txt','r')
    linea, fin_archivo = leer_linea_mensual(archivo)

    while not fin_archivo:
        tareas_sin_fecha = linea[1:]
        fecha_actual = linea[0]
        for tarea in tareas_sin_fecha:
            poner_en_tooltip(calendario,fecha_actual,tarea, es_inicio = True)
        linea, fin_archivo = leer_linea_mensual(archivo)

    archivo.close()

def crear_grid_mensual(grid_mensual, raiz_general):
    fecha_selec = StringVar()
    calendario = Calendar(grid_mensual, borderwidth = 0,
                        showweeknumbers = False,locale = 'es_ES',
                        textvariable = fecha_selec, 
                        selectmode = 'day',
                        background = '#c38db0', # color de la barra de mes y año.
                        bordercolor = '#e0a8cd', # color del grid delineador.
                        headersbackground = '#e0a8cd', #color de bg del indicador de dias.
                        selectbackground = '#e0a8cd', # bg de fecha seleccionada.
                        tooltipalpha = 0.8, # opacidad del tooltip .
                        tooltipdelay = 0, # tiempo que tarda en mostrarse el tool.
                        tooltipforeground = 'blue', # color de letra tooltip.
                        tooltipbackground = '#c38db0', # color de fondo del tooltip.
                        showothermonthdays = False, # no mostrar los dias del otro mes.
                        weekendforeground = 'red' )  # color de letra de sab y domingo
    calendario.tag_config('recordatorio', background='#c38db0', foreground='blue')
    calendario.pack()
    lista_con_calendario.append(calendario)
    poner_en_tooltip_al_inicio(calendario)
    calendario.bind('<<CalendarSelected>>',lambda e: notas_mensuales(e,fecha_selec,calendario, raiz_general))

def eliminar_tareas_mensuales_hasta_hoy(calendario):
    # se encarga de eliminar del archivo y del tooltip todas las tareas del calendario previas al día de hoy.
    hoy = date.today()
    fecha_de_ahora = hoy.strftime("%Y-%m-%d")
    lista_de_fecha_ahora = fecha_de_ahora.split('-')
    lista_de_fecha_ahora[0] = int(lista_de_fecha_ahora[0]) - 2000 # castear a int para comparar fechas
    lista_de_fecha_ahora[1] = int(lista_de_fecha_ahora[1])
    lista_de_fecha_ahora[2] = int(lista_de_fecha_ahora[2])

    archivo = open(CWD + 'archivos_de_almacenamiento\\archivo_notas_mensuales.txt','r')
    archivo_temporal= open(CWD + 'archivos_de_almacenamiento\\archivo_notas_mensuales_TEMP.txt','w') # creado el archivo temporal.
    archivo_temporal.close()
    archivo_temporal= open(CWD + 'archivos_de_almacenamiento\\archivo_notas_mensuales_TEMP.txt','a')

    linea,fin_archivo = leer_linea_mensual(archivo)
    
    while not fin_archivo:
            if linea:
                fecha_s_parsear = linea[0] # posicion de la fecha en la linea leída.
                lista_de_fecha = fecha_s_parsear.split('/')  # dd/mm/aa
                lista_de_fecha[0] = int(lista_de_fecha[0]) 
                lista_de_fecha[1] = int(lista_de_fecha[1])
                lista_de_fecha[2] = int(lista_de_fecha[2])
                lista_de_fecha = lista_de_fecha[::-1]
                condicion_de_descarte1= lista_de_fecha[POS_AÑO] < lista_de_fecha_ahora[POS_AÑO]
                condicion_de_descarte2 = (lista_de_fecha[POS_AÑO] <= lista_de_fecha_ahora[POS_AÑO] and lista_de_fecha[POS_MES] < lista_de_fecha_ahora[POS_MES])
                condicion_de_descarte3 = (lista_de_fecha[POS_AÑO] <= lista_de_fecha_ahora[POS_AÑO] and lista_de_fecha[POS_MES] <= lista_de_fecha_ahora[POS_MES] and lista_de_fecha[POS_DIA] < lista_de_fecha_ahora[POS_DIA])
                if condicion_de_descarte1 or condicion_de_descarte2 or condicion_de_descarte3:
                    # Si el año es <= y el mes es <= y el día ES MENOR, no se escribe.
                    tareas_de_fecha = dicc_tareas_tooltip[fecha_s_parsear] # en este dicc se almacenan las id de todas las tareas del calendario.
                    for tarea, id_evento in tareas_de_fecha:
                        calendario.calevent_remove(id_evento, tag = 'recordatorio')
                else:
                    archivo_temporal.write(f'{linea[0]}') # sin coma
                    pos = 0
                    for tarea in linea:
                        if pos != 0:
                            archivo_temporal.write(f',{tarea}') # con coma.
                        pos += 1
                
            linea, fin_archivo = leer_linea_mensual(archivo)
            condicion_de_descarte1= lista_de_fecha[POS_AÑO] < lista_de_fecha_ahora[POS_AÑO]
            condicion_de_descarte2 = lista_de_fecha[POS_AÑO] <= lista_de_fecha_ahora[POS_AÑO] and lista_de_fecha[POS_MES] < lista_de_fecha_ahora[POS_MES]
            condicion_de_descarte3 = lista_de_fecha[POS_AÑO] <= lista_de_fecha_ahora[POS_AÑO] and lista_de_fecha[POS_MES] <= lista_de_fecha_ahora[POS_MES] and lista_de_fecha[POS_DIA] < lista_de_fecha_ahora[POS_DIA]
            if not fin_archivo and not (condicion_de_descarte1 or condicion_de_descarte2 or condicion_de_descarte3) :
                # si no es el fin de archivo y la proxima tarea NO se descarta, escribimos un salto de lines.
                archivo_temporal.write('\n')


    archivo_temporal.close()
    archivo.close()
    os.remove(CWD + 'archivos_de_almacenamiento\\archivo_notas_mensuales.txt')
    os.rename(CWD + 'archivos_de_almacenamiento\\archivo_notas_mensuales_TEMP.txt', CWD + 'archivos_de_almacenamiento\\archivo_notas_mensuales.txt')

