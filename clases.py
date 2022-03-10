
from tkinter import *
import tkinter as tk

from constantes import *


class ToggledFrame(tk.Frame):

    def __init__(self, parent, text="", *args, **options):
        tk.Frame.__init__(self, parent, *args, **options)

        self.show = tk.IntVar()
        self.show.set(0)
        self.title_frame = Frame(self,borderwidth=0)
        #self.title_frame.pack(fill="x", expand=1)
        self.title_frame.grid()
        Label(self.title_frame, text=text, font =('Source Sans Pro Black', 16,'bold' )).place(x = 39, y = -7)

        self.signo_mas_bb = PhotoImage(file= CWD + 'imagenes_del_organizador\\signo_mas.png')
        self.signo_cruz_bb = PhotoImage(file= CWD + 'imagenes_del_organizador\\cruz_hab_chica.png')
        self.toggle_button = Button(self.title_frame, image= self.signo_mas_bb, command=lambda : [self.set_variable(),self.toggle()]
                                    ,borderwidth=0, activebackground= 'white')
        #self.toggle_button.pack(side='left')
        self.toggle_button.grid(column=0, row= 0)

        self.sub_frame = tk.Frame(self, borderwidth=0)

    def set_variable(self):
        if self.show.get() == 0:
            self.show.set(1)
        else:
            self.show.set(0)
    
    def toggle(self):
        if self.show.get() == 1:
            #self.sub_frame.pack(fill="x", expand=1,anchor=S)
            self.sub_frame.grid(column=1 , row=0)
            self.toggle_button.config(image= self.signo_cruz_bb)
        else:
            self.sub_frame.grid_forget()
            self.toggle_button.config(image= self.signo_mas_bb)


# FUNCIONES PARA COLAPSAR / RESTITUR FRAME TARJETA CON HABITOS.

def colapsar_el_frame(e,frame_a_colapsar,colapsar_habitos,imagen_restituir,imagen_colapsar):
    frame_a_colapsar.place_forget()
    colapsar_habitos.config(image = imagen_restituir )
    colapsar_habitos.bind('<Button-1>', lambda e: restituir_el_frame(e,frame_a_colapsar,colapsar_habitos,imagen_restituir,imagen_colapsar))

def restituir_el_frame(e,frame_a_restituir,bt_apretado,imagen_restituir,imagen_colapsar):
    frame_a_restituir.place(x = 10, y= 245 - 35, width= 240, height= 265)
    bt_apretado.config(image = imagen_colapsar )
    bt_apretado.bind('<Button-1>', lambda e: colapsar_el_frame(e,frame_a_restituir,bt_apretado,imagen_restituir,imagen_colapsar))

