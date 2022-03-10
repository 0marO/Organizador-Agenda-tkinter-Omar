from tkinter import *
from tkinter import ttk
import tkinter as tk
from time import strftime
from datetime import date
import datetime
import os
import pandas as pd

from tabs import *
from constantes import *
from bindings import *
from func_guardado_tabs import existencia_de_archivos_tareas, mostrar_tareas_guardadas
from generador_clima import generar_imagen_clima
from clases import *
from relativo_al_calendario import *
from relativo_a_notas_texto import guardar_notas,mostrar_notas_guardadas,control_g
from relativo_a_HABITOS import *

def revertir_tamanio(panel_principal):
    #Al inicio del programa, setea las coordenadas del hover para ocultarlo.
    panel_principal.sash_place(0 , 1500 ,0)

def agrandar_habitos(e,bt1,img_hover_flecha_disminuir,raiz_general,panel_principal):
    #Si las coordenadas del sash son mayores a 610, las setea a ese valor para "mostrar" el hover.
    
    global pos_actual_hover_x,pos_actual_hover_y # variables para las actualizar las coordenadas del bt_hover
    
    coordenadas_del_sash = panel_principal.sash_coord(0)[0]
    if  coordenadas_del_sash > 610:
        #setea el sash
        panel_principal.sash_place(0 , 610 ,0)
        
        # setea el toplevel con bt_hover.
        x = raiz_general.winfo_x()
        y = raiz_general.winfo_y()
        lista_con_hover[0].geometry("35x35+%d+%d" % (x + 585, y +470)) # lista_con_hover contiene la ventana toplevel usada para el bt_hover
        pos_actual_hover_x,pos_actual_hover_y = 585,470

        # cambiamos imagen del bt_hover.
        bt1.config(image= img_hover_flecha_disminuir)
        bt1.img_hover_flecha_disminuir = img_hover_flecha_disminuir
    else:
        pass

def achicar_habitos(bt1,img_hover_flecha_aumentar,raiz_general,panel_principal,e):
    #Setea las coordenadas del hover y del toplevel con bt_hover para colapsarlos.

    global pos_actual_hover_x,pos_actual_hover_y # variables para las actualizar las coordenadas del bt_hover
    
    # seteamos el hover
    x = raiz_general.winfo_x()
    y = raiz_general.winfo_y()
    lista_con_hover[0].geometry("35x35+%d+%d" % (x + 836, y +470))  # lista_con_hover contiene la ventana toplevel usada para el bt_hover
    pos_actual_hover_x,pos_actual_hover_y = 836,470
    
    #seteamos el sash
    panel_principal.sash_place(0, 1500, 0)
    
    bt1.config(image = img_hover_flecha_aumentar)
    bt1.img_hover_flecha_aumentar = img_hover_flecha_aumentar

def hover_ampliar_cerrar(raiz_general,panel_principal):
    # pequeña ventana para el bt de ampliar/colapsar el hover.
    # se crea la ventana
    global pos_actual_hover_x,pos_actual_hover_y
    ventana_hover_cursor = Toplevel(raiz_general)
    lista_con_hover.append(ventana_hover_cursor)
    # resto de la configuración de la ventanita.
    ventana_hover_cursor.wm_attributes("-transparentcolor", "gray10") # fondo transparente

    ventana_hover_cursor.attributes('-topmost', 'true') #prioridad de atención.
    x = raiz_general.winfo_x()
    y = raiz_general.winfo_y()
    ventana_hover_cursor.geometry("35x35+%d+%d" % (x + 836, y +470)) 
    pos_actual_hover_x,pos_actual_hover_y = 836,470
    ventana_hover_cursor.overrideredirect(True)
    ventana_hover_cursor.config(bg= 'gray10')

    img_hover_flecha_aumentar = PhotoImage(file=CWD + 'imagenes_del_organizador\\circulo_flecha_aumentar.png')
    img_hover_flecha_diminuir = PhotoImage(file=CWD + 'imagenes_del_organizador\\circulo_flecha_disminuir.png')
    bt_hover = Button(ventana_hover_cursor,image = img_hover_flecha_aumentar,command= lambda: achicar_habitos(bt_hover,img_hover_flecha_aumentar,raiz_general,panel_principal,e = None,),
                borderwidth= 0,activebackground='gray10',bg='gray10')
    bt_hover.grid(row= 0, column= 0, )
    bt_hover.img_hover_flecha = img_hover_flecha_aumentar
    bt_hover.bind("<Enter>", lambda e: agrandar_habitos(e,bt_hover,img_hover_flecha_diminuir,raiz_general,panel_principal))

def dar_formato_fecha(hoy):
    # recibe una string de fecha dd-mm-aa, devuelve una lista con dia, mes(de dicc meses) y año
    # me olvidé de .split en este momento.
    fecha = ['','','']
    indice = 0
    meses ={'01':'Ene 01', '02':'Feb 02', '03':'Mar 03', '04':'Abr 04', '05':'May 05',
            '06':'Jun 06', '07':'Jul 07', '08':'Ago 08' , '09':'Sep 09',
                '10':'Oct 10', '11':'Nov 11', '12':'Dic 12'}
    for c in hoy:
        if c == '-':
            indice += 1
        else:
            fecha[indice] += c

    fecha[MES] = meses[fecha[MES]]

    return fecha 

def reloj():
    cadena = strftime('%H:%M:%S')
    lbl.config(text = cadena)
    lbl.after(1000, reloj)

def al_cerrar_app(hoy):

    fecha_hoy = hoy.strftime("%Y-%m-%d")

    # como no sé sacar info con pandas, saco la info de habitos a lo picapiedra
    d_hab_dia_actual = {}
    archivo_dia_habitos = open(CWD + 'archivos_de_almacenamiento\\archivo_habitos.txt','r') # abre el archivo
    linea, fin_archivo = leer_linea_habitos(archivo_dia_habitos)
    if linea == '': # por si aparecen saltos de linea no deseados al principio.
        linea, fin_archivo = leer_linea_habitos(archivo_dia_habitos)
    while not fin_archivo:
        d_hab_dia_actual[linea[POS_HABITO]] = linea[POS_ESTADO_HABITO]
        linea, fin_archivo = leer_linea_habitos(archivo_dia_habitos)
    archivo_dia_habitos.close() # cierra el archivo

# a continuación se guarda el estado de los habitos
    try:
        # SI EXISTEN HABITOS NUEVOS AGREGARLOS AL CSV CORRECTAMENTE (ya debe existir el csv de data previamente)
        importamos_el_csv = pd.read_csv(CWD + 'archivos_de_almacenamiento\\data_habitos.csv')
        importamos_el_csv = importamos_el_csv.transpose(copy=False)
        ultima_fecha_registrada = list(importamos_el_csv.columns)[-1]

        importamos_el_csv = importamos_el_csv.transpose(copy=False)
        habitos_en_csv = list(importamos_el_csv.columns)

        for habito,estado in d_hab_dia_actual.items():
            if habito not in habitos_en_csv:  # si aparecen habitos nuevos se crea una nueva columna. 
                importamos_el_csv[f'{habito}'] = 'destildado'
        habitos_en_csv = list(importamos_el_csv.columns)
        importamos_el_csv.to_csv(CWD + 'archivos_de_almacenamiento\\data_habitos.csv') 
        # aca empieza el cheat de noob hasta que aprenda mas pandas.
        cheat_data_habitos()
        # si el dia es diferente registra los nuevos estados de habitos.

        if fecha_hoy != ultima_fecha_registrada: 
            archivo_data_habitos = open(CWD + 'archivos_de_almacenamiento\\data_habitos.csv','a') # abre el archivo para append
            archivo_data_habitos.write(f'\n{hoy}')
            for habito in habitos_en_csv:
                if habito not in d_hab_dia_actual: # si es un habito viejo, se asigna destildado.
                    archivo_data_habitos.write(',destildado')
                else:    
                    # si el orden de los habitos cambia en la app, NO genera un problema al guardarlo, se guarda
                    # siempre en la misma posición por que se usa un diccionario para los habitos del dia. 
                    archivo_data_habitos.write(f',{d_hab_dia_actual[habito]}') #de lo contrario se asigna su estado.
            archivo_data_habitos.close() # cierra el archivo
        else: # si el día es igual reescribe lo viejo, actualizado.

            importamos_el_csv = importamos_el_csv.transpose(copy=False)
            d_csv_ultima_fecha = importamos_el_csv[f'{fecha_hoy}']
            d_csv_ultima_fecha = dict(d_csv_ultima_fecha)

            for habito, estado in d_hab_dia_actual.items():
                if habito in d_csv_ultima_fecha:
                    d_csv_ultima_fecha[habito] = estado
            importamos_el_csv[f'{fecha_hoy}'] = d_csv_ultima_fecha.values()
            importamos_el_csv = importamos_el_csv.transpose(copy=False)
            importamos_el_csv.to_csv(CWD + 'archivos_de_almacenamiento\\data_habitos.csv')
            
            # aca empieza el cheat de noob hasta que aprenda mas pandas.
            cheat_data_habitos()


    except FileNotFoundError: # se crea el archivo con formato correcto.
        if len(d_hab_dia_actual) > 0:
            archivo_data_habitos = open(CWD + 'archivos_de_almacenamiento\\data_habitos.csv','w',newline= '')

            primero = True
            for habito, estado in d_hab_dia_actual.items():
                if primero:
                    archivo_data_habitos.write(f'{habito}')
                    primero = False
                else:
                    archivo_data_habitos.write(f',{habito}')

            archivo_data_habitos.write(f'\n{hoy}')
            for habito, estado in d_hab_dia_actual.items():
                archivo_data_habitos.write(f',{estado}')    
            archivo_data_habitos.close()

    raiz_general.destroy()

def sincronizar_hover_ampliar_cerrar(e,raiz):
    
    if lista_con_hover:
        x = raiz.winfo_x() 
        y = raiz.winfo_y()
        lista_con_hover[0].geometry("+%d+%d" % (x + pos_actual_hover_x , y + pos_actual_hover_y))

def minimizar_hover(e):
    # Hide/Unvisible
    if lista_con_hover:
        lista_con_hover[0].withdraw()

def maximizar_hover(e):
    # Show/Visible
    if lista_con_hover:
        lista_con_hover[0].deiconify()

def minimizar_agregar_habitos(e):
    # Hide/Unvisible
    if lista_con_agregar_entry:
        lista_con_agregar_entry[0].withdraw()

def maximizar_agregar_habitos(e):
    # Show/Visible
    if lista_con_agregar_entry:
        lista_con_agregar_entry[0].deiconify()

def actualizar_clima():
    global lbl_fondo_clima
    global tkimage
    lbl_fondo_clima.destroy()
    generar_imagen_clima()
    algo = PhotoImage(file = CWD + 'imagenes_del_organizador\\nn_R.png')
    tkimage = PhotoImage(file = CWD + 'imagenes_del_organizador\\NewImg.png')
    lbl_fondo_clima = Label(frame_tabs,image = algo)
    lbl_fondo_clima.config(image= tkimage)
    lbl_fondo_clima.place(x= 465, y= 340)

    lbl_fondo_clima.tkimage = tkimage

# generamos imagen del clima con la info escrita arriba (tkinter es malisismo para poner texto arriba de imagenes.)
generar_imagen_clima() 

####################################################################################################################################################
########################################################################## Empieza la GUI ##########################################################
####################################################################################################################################################
raiz_general = tk.Tk()
raiz_general.title('Organizador')
raiz_general.iconbitmap(CWD + 'imagenes_del_organizador\\icono_agenda.ico')
raiz_general.geometry('879x480')
raiz_general.protocol("WM_DELETE_WINDOW", lambda : al_cerrar_app(hoy))
raiz_general.resizable(0,0)

# Simply set the theme
raiz_general.tk.call("source", CWD + "temas de tkinter\\Azure-ttk-theme-main\\azure.tcl")
raiz_general.tk.call("set_theme", "light")

estilo = ttk.Style()
estilo.configure('Notebook.tab',tabposition='wn')



############################## PANEL PRINCIPAL ##############################

panel_principal = PanedWindow( raiz_general, bg='#e0a8cd', sashpad = 2 ,opaqueresize = False)
panel_principal.config(borderwidth = 0, cursor= '')
panel_principal.pack(fill= BOTH, expand= True)

# Creamos el hover para ampliar/ disminuir el segundo panel
hover_ampliar_cerrar(raiz_general,panel_principal)
############################## PRIMER panel hijo.##############################
panel1 = PanedWindow( panel_principal, bg='Black', orient= VERTICAL)
panel1.config(borderwidth= 0)
panel_principal.add(panel1,minsize = 70)

## frame para las tabs, para que no se agrande automaticamente por paned window...
frame_tabs = Frame(panel1)
frame_tabs.config(cursor='')
panel1.add(frame_tabs)

# notebook con tabs.
existencia_de_archivos_tareas()
tab_control = ttk.Notebook(frame_tabs,style='lefttab.TNotebook')
tab_control.place(x= 10, y = 15)

tab1 = ttk.Frame(tab_control,width = 320 , height = 420)
tab2 = ttk.Frame(tab_control,width = 320 , height = 420)
tab3 = ttk.Frame(tab_control,width = 320 , height = 420)
tab4 = ttk.Frame(tab_control,width = 320 , height = 420)
tab5 = ttk.Frame(tab_control,width = 320 , height = 420)
tab6 = ttk.Frame(tab_control,width = 320 , height = 420)
tab7 = ttk.Frame(tab_control,width = 320 , height = 420)

tab_control.add(tab1, text='Lu',sticky=W)
tab_control.add(tab2, text='Ma',sticky=W)
tab_control.add(tab3, text='Mie',sticky=W)
tab_control.add(tab4, text='Ju',sticky=W)
tab_control.add(tab5, text='Vi',sticky=W)
tab_control.add(tab6, text='Sa',sticky=W)
tab_control.add(tab7, text='Do',sticky=W)

lista_de_cajas = []


crear_contenido_tab(tab1, lista_de_cajas, raiz_general ,dia_actual = 0)
crear_contenido_tab(tab2, lista_de_cajas, raiz_general ,dia_actual = 1)
crear_contenido_tab(tab3, lista_de_cajas, raiz_general ,dia_actual = 2)
crear_contenido_tab(tab4, lista_de_cajas, raiz_general ,dia_actual = 3)
crear_contenido_tab(tab5, lista_de_cajas, raiz_general ,dia_actual = 4)
crear_contenido_tab(tab6, lista_de_cajas, raiz_general ,dia_actual = 5)
crear_contenido_tab(tab7, lista_de_cajas, raiz_general ,dia_actual = 6)

mostrar_tareas_guardadas(lista_de_cajas)  ###  AL iniciar muestra lo guardado.



now = datetime.datetime.now()
focusear_tab_del_dia(now.strftime("%A"),tab_control,tab1,tab2,tab3,tab4,tab5,tab6,tab7)



# marco para notas.
posicionamiento_general_y = 25
carta_notas = ttk.Frame(frame_tabs, style='Card.TFrame', padding=(5, 6, 7, 8))
carta_notas.place(x = 350, y= 16 +posicionamiento_general_y, width= 500)

label_notas = Label(carta_notas, text = 'Notas', font= ('Source Sans Pro Black', 16,'bold' ))
label_notas.pack(anchor= W)
notas = Text(carta_notas, height= 10, width= 42, borderwidth=0, font= ('Source Sans Pro Light', 15,),
            selectbackground= '#e0a8cd' ,selectforeground= 'black', wrap= WORD)
notas.pack(anchor= W)
mostrar_notas_guardadas(notas) ###  AL iniciar muestra lo guardado.

# Boton para guardar notas 
img_g_notas = PhotoImage(file=CWD + 'imagenes_del_organizador\\guardar_notas.png')
b_g_notas = Button(carta_notas, command= lambda: guardar_notas(notas), image= img_g_notas, borderwidth = 0,
        activebackground = '#e0a8cd')
b_g_notas.place(x= 70 , y= 5 )

# scrollbar NOTAS
scroll_vertical = ttk.Scrollbar(carta_notas, orient= 'vertical')
scroll_vertical.place(x= 469, y= 10, height= 269, width= 10)
notas.config(yscrollcommand= scroll_vertical.set)
scroll_vertical.config(command= notas.yview)

# imagen calendario
posicionamiento_x, posicionamiento_y  = 350, 337

imagen_agenda = PhotoImage(file = CWD + 'imagenes_del_organizador\\agenda_t_chico.png')
label_agenda = Label(frame_tabs,image= imagen_agenda)
label_agenda.place(x= posicionamiento_x , y = 20  + posicionamiento_y + posicionamiento_general_y)


# labels fecha
hoy = date.today()
año,mes,dia = dar_formato_fecha(str(hoy))
label_fecha = Label(frame_tabs, text = año , font= ('Arial Rounded MT Bold', 5) ,fg= '#585858',bg='#e0a8cd' )
label_fecha.place(x= 29  +posicionamiento_x, y= 35 + posicionamiento_y + posicionamiento_general_y)
label_mes = Label(frame_tabs, text = mes, font= ('Source Sans Pro Black', 12) ,fg= '#585858')
label_mes.place(x= 12 +posicionamiento_x, y= 55 + posicionamiento_y + posicionamiento_general_y)
label_dia = Label(frame_tabs, text = dia, font= ('Source Sans Pro Black', 14) , fg= '#585858')
label_dia.place(x= 27 +posicionamiento_x, y= 75 + posicionamiento_y + posicionamiento_general_y)


# label RELOJ
frm_reloj = ttk.Frame(frame_tabs ,style='Card.TFrame' )
lbl = Label(frm_reloj, font = ('Arial Rounded MT Bold', 15, 'bold'),
            bg = 'white',
            fg = '#e0a8cd', width = 5,padx= 16)
lbl['foreground'] = '#585858'
frm_reloj.place(x= 350, y= 320 + posicionamiento_general_y, height= 33, width= 110)
lbl.place(x= 1, y= 1)
reloj()


# Mostramos la imagen DEL CLIMA
tkimage = PhotoImage(file = CWD + 'imagenes_del_organizador\\NewImg.png')
lbl_fondo_clima = Label(frame_tabs,image = tkimage)
lbl_fondo_clima.place(x= 465, y= 340)
lbl_fondo_clima.tkimage = tkimage

# actualizar IMAGEN CLIMA
icono_actualizar = PhotoImage(file=CWD + 'imagenes_del_organizador\\icono_actualizar.png')
bt_actualizar_clima = Button(frame_tabs, image= icono_actualizar, borderwidth = 0, command= lambda: actualizar_clima(),
        activebackground = 'white')
bt_actualizar_clima.place(x= 438 , y= 395 )

############################## SEGUNDO PANEL HIJO ##############################

# segundo panel hijo.
panel2 = PanedWindow( panel_principal, bg='#ffffff', borderwidth= 0, orient= VERTICAL)
panel_principal.add(panel2,minsize = 10 )

# colocando el sash al iniciar la app
panel_principal.update()
revertir_tamanio(panel_principal)

# frame del panel.
frame_habitos = Frame(panel2)
panel2.add(frame_habitos)

#----------------------- widgets dentro del -frame- panel 2.-----------------------

# marco para grid mensual.
grid_mensual = ttk.Frame(frame_habitos, style='Card.TFrame', padding=(5, 5, 5, 5))
grid_mensual.place(x = 10, y= 2, width= 240, height= 170)

# poblamos el grid.
crear_grid_mensual(grid_mensual, raiz_general)

subir_estructura = 35
# Label "Habitos"
lbl_habitos = Label(frame_habitos,text= 'Habitos', font =('Source Sans Pro Black', 16,'bold' ))
lbl_habitos.place(x = 50, y = 210 - subir_estructura )

# Label fecha del dia
lbl_fecha_del_dia = Label(frame_habitos,text= hoy.strftime("%d/%m"), font =('Source Sans Pro Black', 16,'bold' ))
lbl_fecha_del_dia.place(x = 170, y = 210 - subir_estructura  )


# Frame tarjeta para los habitos
frame_habitos_propio = ttk.Frame(frame_habitos, style='Card.TFrame', padding=(5, 5, 5, 5))
frame_habitos_propio.place(x = 10, y= 245 - subir_estructura, width= 240, height= 265)

marcador_de_distancia = Label(frame_habitos_propio,
                              text = '                                                       ',
                              font =('Source Sans Pro Black', 11,'bold')
                               )

marcador_de_distancia.grid(column= 0, row = ultima_fila)

# '                                                       '
# boton para COLAPSAR HABITOS
imagen_colapsar = PhotoImage(file=CWD + 'imagenes_del_organizador\\colapsar_algo.png')
imagen_restituir = PhotoImage(file=CWD + 'imagenes_del_organizador\\restituir_algo.png')
colapsar_habitos = Button(frame_habitos, image= imagen_colapsar, borderwidth= 0,activebackground='white')
colapsar_habitos.place(x = 230, y= 180)
colapsar_habitos.bind('<Button-1>', lambda e: colapsar_el_frame(e,frame_habitos_propio,colapsar_habitos,imagen_restituir,imagen_colapsar))


# Se crea un frame colapsable.
# imagenes de la gui
circulo_vacio = PhotoImage(file = CWD + 'imagenes_del_organizador\\circulo_vacio_chico.png')
circulo_tilddado = PhotoImage(file = CWD + 'imagenes_del_organizador\\circulo_con_tilde2_chico.png')
cruz_eliminar = PhotoImage(file = CWD + 'imagenes_del_organizador\\cruz_hab_chica.png')

frame_colapsable = ToggledFrame(frame_habitos, text='Habitos', relief="raised", borderwidth=0)
frame_colapsable.place( x= 10, y = 216- subir_estructura)

# una tarjeta redondeada para el entry, como un subframe del frame colapsable.
entrada_habito_frame = ttk.Frame(frame_colapsable.sub_frame,style='Card.TFrame')
entrada_habito_frame.pack()

# string var con maximo de caracteres
var_entrada_habito = StringVar()
var_entrada_habito.trace("w", lambda *args: limite_entry(var_entrada_habito, limite = 15))
entrada_habito = Entry(entrada_habito_frame,textvariable = var_entrada_habito, font= ('Source Sans Pro light',10), 
                        borderwidth = 0, selectbackground = '#e0a8cd', selectforeground = 'Black',
                        width= 30)
entrada_habito.pack(padx= 2, pady= 4)
entrada_habito.bind("<KeyRelease>", lambda e: pasar_a_mayus(e, var_entrada_habito))
entrada_habito.bind('<Return>', lambda e: bind_return_habitos(var_entrada_habito,entrada_habito,circulo_tilddado,circulo_vacio,cruz_eliminar,marcador_de_distancia,frame_habitos_propio))

agregar_habitos_guardados(frame_habitos_propio,marcador_de_distancia,circulo_vacio,cruz_eliminar,circulo_tilddado)


# Botón para eliminar tareas mensuales hasta el dia de hoy. 
bt_el_hasta_hoy = ttk.Button(
                frame_habitos,
                command= lambda : eliminar_tareas_mensuales_hasta_hoy(lista_con_calendario[0]),
                text= 'Eliminar recordatorios\nhasta hoy.')
bt_el_hasta_hoy.place(x = 270, y = 5)


# IMAGEN TOSTADITOS RICOS BB

imagen_tostados = PhotoImage(file= CWD + 'imagenes_del_organizador\\tostado_rico_RR.png')
label_tostados = Label(frame_habitos, image= imagen_tostados)
label_tostados.place(x= 420, y= 69)

############################# binds #############################

b_g_notas.bind('<Enter>',on_enter)
b_g_notas.bind('<Leave>',on_leave)
notas.bind('<Control-g>',lambda e: control_g(e, notas))

# bindings para movimiento toplevel colores y HOVER 
raiz_general.bind('<Configure>',lambda e: [sincronizar_ventana_colores(e,raiz_general),sincronizar_hover_ampliar_cerrar(e,raiz_general)])
raiz_general.bind('<FocusOut>', lambda e: [minimizar_colores(e), minimizar_hover(e),minimizar_agregar_habitos(e)])
raiz_general.bind('<FocusIn>',lambda e:  [maximizar_colores(e), maximizar_hover(e),])
# maximizar_agregar_habitos(e)
raiz_general.mainloop()