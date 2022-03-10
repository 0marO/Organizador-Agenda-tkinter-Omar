import os
from tkinter import *

# CURRENT WORKING DIRECTORY
CWD = os.getcwd() + '\\'

# CONSTANTES DE TABS
POS_LISTBOX = 1
DOMINGO = 6
LUNES = 0
LISTA_DE_COLORES = ('white','#f9e79f','#ffb74d','#82e0aa','#90caf9','#F34B4B')

# CONSTANTES DE BUSCAR REGISTROS MENSUALES 

global dicc_tareas_tooltip
dicc_tareas_tooltip = {}  # Almacena las id de eventos {fecha_selec : [[tarea1,id_evento],[tarea2,id_event2]]}
POS_AÑO = 0
POS_MES = 1
POS_DIA = 2


# CONSTANTES DE  POSICION DE TAREA- ID_EVENTO
POS_TAREA = 0
POS_EVENTO = 1


# CONSTANTES PARA LOS HABITOS 
ultima_fila = 1
cantidad_de_habitos = 0
fila_hab = 0  # para separar cada par habito-circulo_tick. 
MAX_NRO_HABITOS = 10
POS_HABITO = 0
POS_ESTADO_HABITO = 1

# DICCIONARIO PARA HACER TRACK DE LAS VENTANAS ABIERTAS DEL CALENDARIO (toplevels)

dicc_ventanas_calendario={}  # pares 'dd/mm/aaaa' : widget_toplevel


# LISTA "PORTAPAPELES" PARA CORTAR Y PEGAR TAREAS.

lista_portapapeles = []


#CONSTANTES DEL MAIN
POS_DIA_MENSUAL = 0
LISTA_DEL_MES = 0
MES = 1
lista_con_hover = []
lista_con_calendario = []
lista_con_agregar_entry = []
pos_actual_hover_x,pos_actual_hover_y = 0,0




