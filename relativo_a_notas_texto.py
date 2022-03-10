from constantes import *
from tkinter import *


def guardar_notas(notas):
    # guarda el contenido de el textbox de notas.
    archivo = open(CWD + 'archivos_de_almacenamiento\\archivo_notas.txt', mode= 'w')
    archivo.write(notas.get(1.0,END))
    archivo.close()

def mostrar_notas_guardadas(notas):
    # inserta el contenido del archivo en la textbox de noteas
    registro = open(CWD + 'archivos_de_almacenamiento\\archivo_notas.txt', mode= 'r')
    texto = registro.read()
    registro.close()
    notas.insert(END, texto)

def control_g(e, notas):
    guardar_notas(notas)
