
from tkinter import *
from tkinter import ttk
import tkinter as tk
from bindings import *
from constantes import *
from func_guardado_tabs import *

lista_de_colores = ('white','#f9e79f','#ffb74d','#82e0aa','#90caf9')
lista_ventana_colores=[]  # guarda el widget toplevel de elegir colores para poder modificar el focus si se minimiza la app.
lista_botones_colores_omar = []

def focusear_tab_del_dia(nombre_de_dia,notebook,tab1,tab2,tab3,tab4,tab5,tab6,tab7):
    dicc_dias_numero = { 'Monday': tab1,
                         'Tuesday': tab2,
                         'Wednesday':tab3,
                         'Thursday':tab4,
                         'Friday':tab5,
                         'Saturday':tab6,
                         'Sunday':tab7
                         }
    notebook.select(dicc_dias_numero[nombre_de_dia])
    
def copiar_en_portapapeles(caja_de_tareas):
    # recibe un widget caja de tareas activo, guarda en una lista global las strings de las tareas seleccionadas en esa caja.
    posiciones_tareas_selec = caja_de_tareas.curselection()
    if len(posiciones_tareas_selec) != 0:
        for pos in posiciones_tareas_selec:
            lista_portapapeles.append(caja_de_tareas.get(pos))

def pegar_tareas_en_listbox(caja_de_tareas,dia_str = None):
    # recibe una caja de tareas a la cual le inserta las strings presentes en la lista_portapapeles global
    # después de esto, vacía la lista portapapeles.
    if len(lista_portapapeles) != 0:
        for tarea_copiada in lista_portapapeles:
            caja_de_tareas.insert(END,tarea_copiada)
            guardar_tarea_ingresada(tarea_copiada,dia_elegido= dia_str)


    lista_portapapeles.clear()

def minimizar_colores(e):
    # Hide/Unvisible
    if lista_ventana_colores:
        lista_ventana_colores[0].withdraw()

def maximizar_colores(e):
    # Show/Visible
    if lista_ventana_colores:

        lista_ventana_colores[0].deiconify()

def identificar_dia(dia_actual):
    dias = ['Lunes','martes','miercoles','jueves','viernes','sabado','domingo']
    return dias[dia_actual]

def espaciar_str_dia(dia_actual_str):
    resultado = ''
    for c in dia_actual_str:
        resultado = resultado + c + '\n' 
    return resultado

def leer_linea(archivo):
    # lee lineas del archivo de tareas. Devuelve una lista de tareas y un bool de fin de archivo.
    registro = archivo.readline()
    fin_archivo = False
    if registro:
        registro = registro.rstrip('\n')  # aparecen saltos de línea por alguna razon
        linea = registro.split(',')
        if len(linea[0]) < 3 :
            del(linea[0]) # asi no queda el num. de dia en las tareas.

    else:
        fin_archivo = True
        linea = 0
    return linea, fin_archivo

def pasar_dia(caja_de_tareas, lista_de_cajas, dia_a_pasar,dia_str):

    seleccionado = caja_de_tareas.curselection()
    lista_tareas_guardadas = obtener_lista_tareas_guardadas(dia_str)

    tareas_a_pasar = [lista_tareas_guardadas[posicion] for posicion in seleccionado]
    
    # se insertan las tareas pasadas al dia deseado y se guardan en el archivo.
    mostrar_tareas_de_un_dia(lista_de_cajas[dia_a_pasar][POS_LISTBOX],tareas_a_pasar)
    guardar_pasado_de_dia(tareas_a_pasar,dia_a_pasar)

    # se eliminan tareas pasadas de la primera caja de tareas.
    seleccionado_al_reves = seleccionado[::-1]
    for pos in seleccionado_al_reves:
        caja_de_tareas.delete(pos)
    guardar_eliminado_tareas( seleccionado,dia_elegido = dia_str)

def bt_pasar_de_dia_adelante(caja_de_tareas, lista_de_cajas, dia_actual,dia_str):
    if dia_actual != DOMINGO:
        dia_a_pasar = dia_actual + 1
    else:
        dia_a_pasar = LUNES
    pasar_dia(caja_de_tareas, lista_de_cajas, dia_a_pasar,dia_str)

def bt_pasar_de_dia_atras(caja_de_tareas, lista_de_cajas, dia_actual,dia_str):
    if dia_actual != LUNES:
        dia_a_pasar = dia_actual -1
    else:
        dia_a_pasar = DOMINGO
    pasar_dia(caja_de_tareas, lista_de_cajas, dia_a_pasar,dia_str)

def bt_agregar_tarea(caja_de_tareas , var_entrada,entrada_nombre, lista_de_cajas, dia_str):
    # funcion que agrega una string a una listbox. es usada para las tabs y para el almanaque
    # lista_de_cajas es una lista con las cajas de tareas de las tabs, en cambio lista_de_cajas = False cuando se usa en el almanaque.
    str_de_tarea = var_entrada.get()
    if str_de_tarea != '': # asi no hay tareas vacías.
        caja_de_tareas.insert(END , "• " + str_de_tarea) #  Con bullet point.
        entrada_nombre.delete(0, 'end')

    if lista_de_cajas and str_de_tarea != '':
        global color_elegido
        caja_de_tareas.itemconfig(END, {'bg':f'{color_elegido}'})
        guardar_tarea_ingresada(str_de_tarea, dia_elegido = dia_str ,color_elegido = color_elegido)

def bt_eliminar_tareas(caja_de_tareas,lista_de_cajas, dia_str):
    seleccionado = caja_de_tareas.curselection() # tupla de posiciones seleccionadas.
    for selec in seleccionado[::-1]:
        caja_de_tareas.delete(selec)
    guardar_eliminado_tareas( seleccionado,dia_elegido = dia_str)

def tachar_tarea(caja_de_tareas,lista_de_cajas,dia_str):
    seleccionado = caja_de_tareas.curselection() # tupla de posiciones seleccionadas.
    tareas = [(caja_de_tareas.get(pos_tarea),pos_tarea) for pos_tarea in seleccionado] # tarea es un int de posicion
    resultado = ''
    for tarea, pos_tarea in tareas:
        if '\u0336' not in tarea: # caracter de tachado es  '\u0336'
            for c in tarea:
                resultado = resultado + c + '\u0336'
            caja_de_tareas.insert(pos_tarea,resultado)
            caja_de_tareas.itemconfigure(pos_tarea, fg ='#585858')
            guardar_tachado_de_tarea(pos_tarea,tachado = True,dia_elegido = dia_str)
        else:
            string_encode = tarea.encode("ascii", "ignore")
            resultado = string_encode.decode()
            caja_de_tareas.insert(pos_tarea, "•" + resultado)  # con bullet point
            caja_de_tareas.itemconfigure(pos_tarea, fg ='black')
            guardar_tachado_de_tarea(pos_tarea,tachado = False,dia_elegido = dia_str)
        
        caja_de_tareas.delete(pos_tarea+1)  # El original se corre 1 pos.
        resultado = ''

def doble_click_tareas(e,caja_de_tareas, var_caja_tareas,lista_de_cajas, dia_str):
    tachar_tarea(caja_de_tareas,lista_de_cajas,dia_str)

def control_a(e,caja_de_tareas,var_entrada,entrada_nombre, lista_de_cajas, dia_str):
    bt_agregar_tarea(caja_de_tareas , var_entrada,entrada_nombre, lista_de_cajas, dia_str)

def suprimir(e,caja_de_tareas,lista_de_cajas, dia_str):
    bt_eliminar_tareas(caja_de_tareas,lista_de_cajas, dia_str)

def tach_abrir(e,boton_tacho, tacho_abierto):
    boton_tacho.config(image = tacho_abierto)
def tach_cerrar(e,boton_tacho, tacho_cerrado):
    boton_tacho.config(image = tacho_cerrado)

def bt_guardar_tareas(lista_de_cajas, nombre_archivo, caja_con_subrrallado = None, dia_elegido = 'Lunes'):

    archivo = open(CWD + f'archivos_de_almacenamiento\\{nombre_archivo}', mode= 'w')
    nro_dia = LUNES
    for var_caja, caja_de_tareas in lista_de_cajas:
        archivo.write(f'{nro_dia}')
        tareas_existentes = caja_de_tareas.get(0,END) # tupla con strings de las tareas ingr. por el usuario

        pos_tarea_actual, long_tareas_ex  = 0, len(tareas_existentes) , 

        while long_tareas_ex != 0 and pos_tarea_actual <= (long_tareas_ex -1):  #no ciclar si no hay tareas.
            tarea = tareas_existentes[pos_tarea_actual]

            if '\u0336' not in tarea: # Pasan cosas raras al escribir las tachadas
                archivo.write(f',{tarea}')
            else:
                string_encode = tarea.encode("ascii", "ignore")
                resultado = string_encode.decode()
                archivo.write(f',{resultado}[T]') # [T] es el identificador de tarea tachada.

            # se guarda el color de subrrallado elegido si la tarea es nueva. (va estar en la ultima posición.)
            if caja_con_subrrallado and (caja_con_subrrallado == caja_de_tareas) and pos_tarea_actual == (long_tareas_ex -1): # 
                archivo.write(f'[{color_elegido}]')
            
            pos_tarea_actual += 1

        if nro_dia != DOMINGO: # Sin salto de linea al final.
            archivo.write(f' \n')
        nro_dia += 1

    archivo.close()

def bt_colores(raiz_general,bt_cambiar_color):
    # pequeña ventana con botones de colores para cambiar el color de subrayado de listbox.

    # se crea la ventana
    ventana_colores = Toplevel(raiz_general)
    lista_ventana_colores.append(ventana_colores)
    # resto de la configuración de la ventanita.
    ventana_colores.wm_attributes("-transparentcolor", "gray10")

    ventana_colores.attributes('-topmost', 'true')
    x = raiz_general.winfo_x()
    y = raiz_general.winfo_y()
    ventana_colores.geometry("260x35+%d+%d" % (x + 150, y +120))
    ventana_colores.overrideredirect(True)
    ventana_colores.config(bg= 'gray10')

    c_blanco = PhotoImage(file=CWD + 'imagenes_del_organizador\\circulo_colores_blanco_chico.png')
    bt1 = Button(ventana_colores,image = c_blanco, command= lambda: cambiar_color_fondo('white',ventana_colores,bt_cambiar_color,c_blanco,raiz_general),
                borderwidth= 0,activebackground='gray10',bg='gray10')
    bt1.grid(row= 0, column= 0, )
    bt1.c_blanco = c_blanco

    c_amarillo = PhotoImage(file=CWD + 'imagenes_del_organizador\\circulo_colores_amarillo_chico.png')
    bt2 = Button(ventana_colores,image = c_amarillo, command= lambda: cambiar_color_fondo('#f9e79f',ventana_colores,bt_cambiar_color,c_amarillo,raiz_general),
                borderwidth = 0, activebackground='gray10',bg='gray10')
    bt2.grid(row= 0, column= 1,)
    bt2.c_amarillo = c_amarillo

    c_naranja = PhotoImage(file=CWD + 'imagenes_del_organizador\\circulo_colores_naranja_chico.png')
    bt3 = Button(ventana_colores,image = c_naranja, command=  lambda: cambiar_color_fondo('#ffb74d',ventana_colores,bt_cambiar_color,c_naranja,raiz_general),
                borderwidth= 0, activebackground='gray10',bg='gray10')
    bt3.grid(row= 0, column= 2,)
    bt3.c_naranja = c_naranja

    c_verde = PhotoImage(file=CWD + 'imagenes_del_organizador\\circulo_colores_verde_chico.png')
    bt4 = Button(ventana_colores,image = c_verde, command= lambda: cambiar_color_fondo('#82e0aa',ventana_colores,bt_cambiar_color,c_verde,raiz_general),
                borderwidth= 0, activebackground='gray10',bg='gray10')
    bt4.grid(row= 0, column= 3, )
    bt4.c_verde = c_verde

    c_azul = PhotoImage(file=CWD + 'imagenes_del_organizador\\circulo_colores_azul_chico.png')
    bt5 = Button(ventana_colores,image = c_azul, command= lambda: cambiar_color_fondo('#90caf9',ventana_colores,bt_cambiar_color,c_azul,raiz_general),
                borderwidth= 0, activebackground='gray10',bg='gray10')
    bt5.grid(row= 0, column= 4, )
    bt5.c_azul = c_azul

    c_rojo = PhotoImage(file=CWD + 'imagenes_del_organizador\\circulo_colores_rojo_chico.png')
    bt5 = Button(ventana_colores,image = c_rojo, command= lambda: cambiar_color_fondo('#F34B4B',ventana_colores,bt_cambiar_color,c_rojo,raiz_general),
                borderwidth= 0, activebackground='gray10',bg='gray10')
    bt5.grid(row= 0, column= 5, )
    bt5.c_rojo = c_rojo


    # Cambio de comando del bt_cambiar_color para poder cerrar todo apretandolo nuevamente.
    dicc_colores_imagenes = {'white':c_blanco,'#f9e79f':c_amarillo,
                             '#ffb74d':c_naranja,'#82e0aa':c_verde,
                             '#90caf9':c_azul,'#F34B4B':c_rojo}
    global color_elegido
    bt_cambiar_color.config(command= lambda: cambiar_color_fondo(color_elegido,ventana_colores,bt_cambiar_color,dicc_colores_imagenes[color_elegido],raiz_general) )


    # Desabilitar el resto de los botones de color de las otras tabs.
    for boton in lista_botones_colores_omar:
        if boton != bt_cambiar_color:
            boton.config(state = DISABLED)

def cambiar_color_fondo(color_seleccionado,ventana_colores,bt_cambiar_color,imagen,raiz_general):
    # cambia la variable color_elegido que se usa cada vez que se ingresa una tarea. Esto cambia el color de fondo de la tarea en la listbox.
    # Cambia la imagen del seleccionador de colores para que sea acorde al color elegido.
    global color_elegido
    color_elegido = color_seleccionado
    bt_cambiar_color.config(image = imagen, command= lambda : bt_colores(raiz_general,bt_cambiar_color))
    bt_cambiar_color.imagen = imagen
    ventana_colores.destroy()
    del lista_ventana_colores[0]

    # se habilitan todos los botones nuevamente

    for boton in lista_botones_colores_omar:
        boton.config(state = ACTIVE)

def subir_tarea(caja_de_tareas,dia_str):
    seleccionado = caja_de_tareas.curselection() # tupla de posiciones seleccionadas.
    lista_tareas_guardadas = obtener_lista_tareas_guardadas(dia_str)

    if len(seleccionado) == 1:
        indice_tarea_actualizado = seleccionado[0]
        pos_tarea_a_subir = seleccionado[0] # unica tarea seleccionada.
        tarea_a_subir = lista_tareas_guardadas[pos_tarea_a_subir]
        del lista_tareas_guardadas[pos_tarea_a_subir]
        
        if pos_tarea_a_subir != 0:
            lista_tareas_guardadas.insert(pos_tarea_a_subir - 1 , tarea_a_subir)
            indice_tarea_actualizado -= 1
        else:
            lista_tareas_guardadas.append(tarea_a_subir)
            indice_tarea_actualizado =  len(lista_tareas_guardadas) - 1 # indice de ultima posicion, -1 no funciona
            
        caja_de_tareas.delete(0,END)
        mostrar_tareas_de_un_dia(caja_de_tareas,lista_tareas_guardadas)
        guardar_reposicionamiento_tareas(dia_str,lista_tareas_guardadas)
        caja_de_tareas.update()
        select_de_tarea_automatico(caja_de_tareas,indice_tarea_actualizado)

def bajar_tarea(caja_de_tareas,dia_str):
    seleccionado = caja_de_tareas.curselection() # tupla de posiciones seleccionadas.
    lista_tareas_guardadas = obtener_lista_tareas_guardadas(dia_str)
    
    if len(seleccionado) == 1:
        indice_tarea_actualizado = seleccionado[0]
        pos_tarea_a_subir = seleccionado[0] # unica tarea seleccionada.
        tarea_a_subir = lista_tareas_guardadas[pos_tarea_a_subir]
        del lista_tareas_guardadas[pos_tarea_a_subir]
        
        ultima_posicion_lista =len(lista_tareas_guardadas) 
        if pos_tarea_a_subir != ultima_posicion_lista:
            lista_tareas_guardadas.insert(pos_tarea_a_subir + 1 , tarea_a_subir)
            indice_tarea_actualizado += 1
        else:
            lista_tareas_guardadas.insert(0, tarea_a_subir)
            indice_tarea_actualizado =  0
            
        caja_de_tareas.delete(0,END)
        mostrar_tareas_de_un_dia(caja_de_tareas,lista_tareas_guardadas)
        guardar_reposicionamiento_tareas(dia_str,lista_tareas_guardadas)
        caja_de_tareas.update()
        select_de_tarea_automatico(caja_de_tareas,indice_tarea_actualizado)

def select_de_tarea_automatico(caja_de_tareas, index):
    caja_de_tareas.select_clear(0, "end")
    caja_de_tareas.selection_set(index)
    caja_de_tareas.see(index)
    caja_de_tareas.activate(index)
    caja_de_tareas.selection_anchor(index)

def sincronizar_ventana_colores(e,raiz):
    
    if lista_ventana_colores:
        x = raiz.winfo_x() 
        y = raiz.winfo_y()
        lista_ventana_colores[0].geometry("+%d+%d" % (x + 150, y +120))

def crear_contenido_tab(tab_actual, lista_de_cajas , raiz_general, dia_actual):

    
    dia_str = identificar_dia(dia_actual)
    dia_str_vertical = espaciar_str_dia(dia_str)
    ############################## PRIMER TAB LUNES ##############################
    color_fondo = 'white'
    # widgets adentro del tab actual
    label_lunes = Label(tab_actual,text = dia_str_vertical,font = ('Source Sans Pro Light', 20), anchor = N, bg= color_fondo)
    label_lunes.place(x = 3, y = 1)

    # ENTRY DE TAREAS
    entrada_nombre_frame = ttk.Frame(tab_actual ,style='Card.TFrame')
    entrada_nombre_frame.place(x = 42, y = 11)
    var_entrada = StringVar()
    entrada_nombre = Entry(entrada_nombre_frame,textvariable = var_entrada, font= ('Source Sans Pro Light',10), 
                            borderwidth = 0, selectbackground = '#e0a8cd', selectforeground = 'Black')
    entrada_nombre.pack(padx= 2, pady= 4)

    # BOTON COLOR 
    signo_mas_bb = PhotoImage(file= CWD + 'imagenes_del_organizador\\circulo_colores_vacio_chico.png')
    bt_cambiar_color = Button(
                    tab_actual,
                    command= lambda:[raiz_general.deiconify,bt_colores(raiz_general,bt_cambiar_color)],
                    activebackground='white',
                    borderwidth = 0,
                    image = signo_mas_bb)
    bt_cambiar_color.signo_mas_bb = signo_mas_bb # para que no se borre la imagen por el garbage collector
    bt_cambiar_color.place(x = 175, y = 14)
    lista_botones_colores_omar.append(bt_cambiar_color)
    


    # BOTON AGREGAR TAREAS 
    signo_mas_bb = PhotoImage(file= CWD + 'imagenes_del_organizador\\signo_mas.png')
    agregar_tarea = Button(
                    tab_actual,
                    command= lambda: bt_agregar_tarea(caja_de_tareas , var_entrada, entrada_nombre, lista_de_cajas, dia_str),
                    activebackground='#f9d6ec',
                    borderwidth = 0,
                    image = signo_mas_bb)
    agregar_tarea.signo_mas_bb = signo_mas_bb # para que no se borre la imagen por el garbage collector
    agregar_tarea.place(x = 200, y = 13)


    # LISTBOX DE TAREAS
    global color_elegido
    color_elegido = 'white'
    var_caja_tareas = StringVar()
    fuente_utilizada =('Source Sans Pro Light', 15)
    caja_de_tareas = Listbox(tab_actual,
                        justify= LEFT,
                        height= 13,
                        width= 24,
                        bd=0 ,
                        bg= color_fondo,
                        highlightthickness = 0,
                        selectbackground='#E8DAEF',
                        selectforeground = '#e0a8cd',
                        activestyle = 'none',
                        font = fuente_utilizada,
                        selectmode=tk.EXTENDED,
                        listvariable= var_caja_tareas
                        )
    

    caja_de_tareas.place(x = 40, y= 60)
    lista_de_cajas.append([var_caja_tareas,caja_de_tareas])
   
   

    # BOTON SUBIR TAREAS 
    triangulo_arriba = PhotoImage(file= CWD + 'imagenes_del_organizador\\triangulo_chico_arriba.png')
    agregar_tarea = Button(
                    tab_actual,
                    command= lambda: subir_tarea(caja_de_tareas,dia_str) ,
                    activebackground='#f9d6ec',
                    borderwidth = 0,
                    image = triangulo_arriba)
    agregar_tarea.triangulo_arriba = triangulo_arriba # para que no se borre la imagen por el garbage collector
    agregar_tarea.place(x = 4, y = 320)
    
    
    # BOTON BAJAR TAREAS 
    triangulo_abajo = PhotoImage(file= CWD + 'imagenes_del_organizador\\triangulo_chico_abajo.png')
    agregar_tarea = Button(
                    tab_actual,
                    command= lambda: bajar_tarea(caja_de_tareas,dia_str) ,
                    activebackground='#f9d6ec',
                    borderwidth = 0,
                    image = triangulo_abajo)
    agregar_tarea.triangulo_abajo = triangulo_abajo # para que no se borre la imagen por el garbage collector
    agregar_tarea.place(x = 4, y = 350)



    # SCROLLBAR listbox VERTICAL
    scroll_vertical = ttk.Scrollbar(tab_actual, orient= 'vertical')
    scroll_vertical.place(x=310, y = 49, height= 340, width= 10)
    caja_de_tareas.config(yscrollcommand= scroll_vertical.set)
    scroll_vertical.config(command= caja_de_tareas.yview)

    # SCROLLBAR listbox HORIZONTAL
    scroll_horizontal= ttk.Scrollbar(tab_actual, orient= 'horizontal')
    scroll_horizontal.place(x=80, y = 403,  height= 10, width = 150)
    caja_de_tareas.config(xscrollcommand= scroll_horizontal.set)
    scroll_horizontal.config(command= caja_de_tareas.xview)

    # BOTÓN BORRAR TAREAS
    tacho_cerrado = PhotoImage(file = CWD + 'imagenes_del_organizador\\tachito_rosa_cerrado.png')
    tacho_abierto = PhotoImage(file = CWD + 'imagenes_del_organizador\\tachito_rosa_abierto.png')
    eliminar_tildadas = Button(tab_actual, text='-' ,
                                command= lambda: bt_eliminar_tareas(caja_de_tareas,lista_de_cajas, dia_str),
                                borderwidth = 0 , image = tacho_cerrado , activebackground= '#f9d6ec' )
    eliminar_tildadas.place(x = 0, y = 380)

    # BOTÓN TACHAR TAREAS
    letra_tachada = PhotoImage(file = CWD + 'imagenes_del_organizador\\letra_tachada.png')
    tachar = Button( tab_actual,
                     text = 't',
                     activebackground='#f9d6ec',
                     image = letra_tachada,
                     command= lambda: tachar_tarea(caja_de_tareas,lista_de_cajas,dia_str),
                     borderwidth = 0)
    tachar.place(x = 230, y = 15)
    tachar.letra_tachada = letra_tachada # para que no se borre la imagen por el garbage collector

    # BOTÓN PASAR TAREAS DIA SIGUIENTE
    adelante_lila_chico = PhotoImage(file=CWD + 'imagenes_del_organizador\\adelante_lila_chico.png')
    pasar_tareas_adelante = Button(tab_actual, text= '>>',activebackground='#E9F7EF',  bg = 'white',
                        image= adelante_lila_chico,
                        command = lambda: bt_pasar_de_dia_adelante(caja_de_tareas, lista_de_cajas, dia_actual,dia_str),
                        borderwidth = 0)
    pasar_tareas_adelante.place(x = 280, y = 400)
    pasar_tareas_adelante.adelante_lila_chico = adelante_lila_chico

    # BOTÓN PASAR TAREAS DIA ANTERIOR
    atras_lila_chico = PhotoImage(file=CWD + 'imagenes_del_organizador\\atras_lila_chico.png')
    pasar_tareas_atras = Button(tab_actual, text= '<<',activebackground='#E9F7EF', bg = 'white',
                        image= atras_lila_chico,
                        command = lambda: bt_pasar_de_dia_atras(caja_de_tareas, lista_de_cajas, dia_actual,dia_str),
                        borderwidth= 0)
    pasar_tareas_atras.place(x = 250, y = 400)
    pasar_tareas_atras.atras_lila_chico = atras_lila_chico


    # BOTÓN PEGAR TAREAS DEL PORTAPAPELES    
    icono_pegado = PhotoImage(file = CWD + 'imagenes_del_organizador\\icono_pegado_R.png')
    pegar_tareas = Button(tab_actual, bg= '#E9F7EF', text= 'G',
                        command = lambda: pegar_tareas_en_listbox(caja_de_tareas,dia_str),
                        image= icono_pegado,
                        borderwidth = 0,
                        activebackground = '#e0a8cd'
                        )
    pegar_tareas.place(x = 260, y = 15)
    pegar_tareas.icono_pegado = icono_pegado # para que no se borre la imagen por el garbage collector
    # --------------------------------- BINDINGS ---------------------------------
    
    # bindings de LISTBOX 
    eliminar_tildadas.bind('<Enter>',lambda e: tach_abrir(e,eliminar_tildadas, tacho_abierto)) # tacho abierto / cerrado
    eliminar_tildadas.bind('<Leave>',lambda e: tach_cerrar(e,eliminar_tildadas, tacho_cerrado))
    entrada_nombre.bind('<Return>', lambda e: control_a(e,caja_de_tareas,var_entrada,entrada_nombre, lista_de_cajas, dia_str)) # agregar tareas
    caja_de_tareas.bind('<Delete>', lambda e: suprimir(e,caja_de_tareas,lista_de_cajas,dia_str)) # eliminar tareas
    caja_de_tareas.bind('<Double-Button-1>',lambda e: doble_click_tareas(e,caja_de_tareas, var_caja_tareas,lista_de_cajas,dia_str) )

    pegar_tareas.bind('<Enter>',on_enter)
    pegar_tareas.bind('<Leave>',on_leave)

    