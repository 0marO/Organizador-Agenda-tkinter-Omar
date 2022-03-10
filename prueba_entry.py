
from tkinter import *
from tkinter import ttk
import tkinter as tk
from constantes import *
class ToggledFrame(tk.Frame):

    def __init__(self, parent, text="", *args, **options):
        tk.Frame.__init__(self, parent, *args, **options)

        self.show = tk.IntVar()
        self.show.set(0)

        self.title_frame = ttk.Frame(self)
        self.title_frame.pack(fill="x", expand=1)

        ttk.Label(self.title_frame, text=text).place(x = 1, y = 1)
        self.signo_mas_bb = PhotoImage(file= CWD + 'imagenes_del_organizador\\signo_mas.png')
        self.toggle_button = ttk.Checkbutton(self.title_frame, width=2, image= self.signo_mas_bb, command=self.toggle,
                                            variable=self.show, style='Toolbutton')
        self.toggle_button.pack(side="left")

        self.sub_frame = tk.Frame(self, borderwidth=1)

    def toggle(self):
        if bool(self.show.get()):
            self.sub_frame.pack(fill="x", expand=1)
            self.toggle_button.configure(text='-')
        else:
            self.sub_frame.forget()
            self.toggle_button.configure(text='+')



if __name__ == "__main__":
    root = tk.Tk()


    frame_colapsable = ToggledFrame(root, text='', relief="raised", borderwidth=1)
    frame_colapsable.place( x= 200, y = 200)

    # ENTRY DE HABITOS! 
    entrada_habito_frame = ttk.Frame(frame_colapsable.sub_frame,style='Card.TFrame')
    entrada_habito_frame.pack()
    
    # string var con maximo de caracteres
    var_entrada_habito = StringVar()
    entrada_habito = Entry(entrada_habito_frame,textvariable = var_entrada_habito, font= ('Source Sans Pro light',10), 
                            borderwidth = 0, selectbackground = '#e0a8cd', selectforeground = 'Black',
                            width= 30)
    entrada_habito.pack(padx= 2, pady= 4)


    root.mainloop()
