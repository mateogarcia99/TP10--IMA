from tkinter import *
import customtkinter
from tkinter import filedialog
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import calculo

#Defino variables globales
data=None
fs=None
t_inicial=None
t_final=None

def load_ir():
    delete_old_plot()
    global data, fs
    
    filepath = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav;*.flac;*.ogg;*.mp3;*.m4a")])
    if filepath:
        data, fs = sf.read(filepath)
        ttotal = len(data) / fs
        tiempo = np.linspace(0, ttotal, len(data))

        fig, ax = plt.subplots()
        ax.plot(tiempo, data)
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Amplitud')
        ax.set_title('Impulse response')

        # Establecer tamaño de la figura en pulgadas
        fig.set_size_inches(6.5, 2)  # Ancho x Alto
        fig.tight_layout() 
        

        ir_plot = FigureCanvasTkAgg(fig, master=select_view_frame)
        ir_plot = ir_plot.get_tk_widget()
        ir_plot.pack()



        #Creo los slider temporales
        time_frame=customtkinter.CTkFrame(ir_tab)
        time_frame.pack()

        t_inicial_label= customtkinter.CTkLabel(time_frame, text="Initial time")
        t_inicial_label.pack()
        t_inicial_slider= customtkinter.CTkSlider(time_frame,from_= 0, to=len(tiempo),number_of_steps= len(tiempo),command=actualizar_t_inicial)
        t_inicial_slider.pack()
        t_final_label= customtkinter.CTkLabel(time_frame, text="Final time")
        t_final_label.pack()
        t_final_slider= customtkinter.CTkSlider(time_frame,from_= 0, to=len(tiempo),number_of_steps= len(tiempo),command=actualizar_t_final)
        t_final_slider.pack()

def load_ss():
    delete_old_plot()
    global data, fs
    
    filepath = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav;*.flac;*.ogg;*.mp3;*.m4a")])
    if filepath:
        data, fs = sf.read(filepath)
        ttotal = len(data) / fs
        tiempo = np.linspace(0, ttotal, len(data))

        fig, ax = plt.subplots()
        ax.plot(tiempo, data)
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Apmlitude')
        ax.set_title('Sine Sweep')

        # Establecer tamaño de la figura en pulgadas
        fig.set_size_inches(6.5, 2)  # Ancho x Alto
        fig.tight_layout() 
        

        ss_plot = FigureCanvasTkAgg(fig, master=select_view_frame)
        ss_plot = ss_plot.get_tk_widget()
        ss_plot.pack()

def actualizar_t_inicial(value):
    global t_inicial
    t_inicial = float(value)

def actualizar_t_final(value):
    global t_final
    t_final = float(value)

def recortar_ir():
    delete_old_plot()
    global t_inicial, t_final, data, fs
    
    data_recortada=data[int(t_inicial):int(t_final)]
    ttotal = len(data_recortada) / fs
    tiempo = np.linspace(0, ttotal, len(data_recortada))

    fig, ax = plt.subplots()
    ax.plot(tiempo, data_recortada)
    ax.set_xlabel('Tiempo (s)')
    ax.set_ylabel('Amplitud')
    ax.set_title('Respuesta al Impulso')

    # Establecer tamaño de la figura en pulgadas
    fig.set_size_inches(6.5,2)  # Ancho x Alto
    fig.tight_layout()


    ir_plot = FigureCanvasTkAgg(fig, select_view_frame)
    ir_plot = ir_plot.get_tk_widget()
    ir_plot.pack()

def delete_old_plot():
    for widget in select_view_frame.winfo_children():
        widget.destroy()


# Crear ctk window
root = customtkinter.CTk()
root.title("Acoustical Parameters calculator")

# Definir el tamaño de la ventana
root.geometry("1000x600")

#Tab view para selecionar entre Ir o SS
selection_tab=customtkinter.CTkTabview(master=root,width=300)
selection_tab.grid(row=0,column=0,padx=10,pady=10,rowspan=2)

# Creo las dos tabs
ss_tab = selection_tab.add("Sine Sweep")
ir_tab = selection_tab.add("Impulse Response")

#Creamos el frame que contiene el archivo cargado
title_font=customtkinter.CTkFont(weight="bold",size=12)
select_view_label=customtkinter.CTkLabel(root,text="Selected file view",width=650,font=title_font)
select_view_label.grid(row=0,column=1,columnspan=2)

select_view_frame=customtkinter.CTkFrame(root,width=650)
select_view_frame.grid(row=1,column=1,columnspan=2)


#Agrego boton para cargar Ir en una tab
load_ir = customtkinter.CTkButton(ir_tab,
                                 width=200,
                                 height=32,
                                 border_width=0,
                                 corner_radius=8,
                                 text="Select IR",
                                 command=load_ir,
                                 font=title_font)

load_ir.pack(padx=10,pady=20)

#recortar ir boton

recortar_button=customtkinter.CTkButton(master=ir_tab,
                                        width=200,
                                        height=32,
                                        border_width=0,
                                        corner_radius=8,
                                        text="Cut Impulse response",
                                        command=recortar_ir)

recortar_button.pack()

# Agrego boton para cargar SS en una tab
load_ss = customtkinter.CTkButton(ss_tab,
                                 width=200,
                                 height=32,
                                 border_width=0,
                                 corner_radius=8,
                                 text="Select SineSweep",
                                 command=load_ss,
                                 font=title_font)


fs = customtkinter.CTkEntry(ss_tab, placeholder_text="Sampling rate",width=200,)
fi = customtkinter.CTkEntry(ss_tab, placeholder_text="Initial frecuency",width=200)
ff = customtkinter.CTkEntry(ss_tab, placeholder_text="Final frecuency",width=200)
ttotal= customtkinter.CTkEntry(ss_tab, placeholder_text="Total duration",width=200)

load_ss.pack(padx=10,pady=20)
fs.pack(pady=1)
fi.pack(pady=1)
ff.pack(pady=1)
ttotal.pack(pady=1)


#Creamos el frame que contenga los datos para el fitrado
filter_frame= customtkinter.CTkFrame(root,width=300,height=110)
filter_frame.grid(row=3,column=0)

filter_label= customtkinter.CTkLabel(filter_frame,text="Filtering settings",width=300,font=title_font)
filter_label.place(rely=.05)

filter_subframe=customtkinter.CTkFrame(filter_frame,width=300,fg_color="transparent")
filter_subframe.place(rely=.3)

#Selector de bandas de filtrado
bands_selection=customtkinter.StringVar(value="octave")
oct_selection=customtkinter.CTkRadioButton(filter_subframe,text="Octave",value="octave",variable=bands_selection)
third_selection=customtkinter.CTkRadioButton(filter_subframe,text="Third",value="third",variable=bands_selection,height=40)

oct_selection.grid(row=0,column=0,padx=40)
third_selection.grid(row=0,column=1)

#Checkbox Reverse Ir

rev_check=customtkinter.CTkCheckBox(filter_subframe,text="Reversed Rir",checkbox_height=20,checkbox_width=20,onvalue="on",offvalue="off")
rev_check.grid(row=1,column=0,columnspan=2)


#Creamos el frame que contenga el suavizado
smoot_frame= customtkinter.CTkFrame(root,width=300,height=100)
smoot_frame.grid(row=4,column=0,pady=10)

smoot_label= customtkinter.CTkLabel(smoot_frame,text="Smoothing settings",width=300,font=title_font)
smoot_label.place(rely=.05)

smoot_subframe=customtkinter.CTkFrame(smoot_frame,width=300,fg_color="transparent")
smoot_subframe.place(rely=.3)

#Selector de tipo de suavizado
smoot_selec=customtkinter.StringVar(value="sch")
sch_selection=customtkinter.CTkRadioButton(smoot_subframe,text="Schroeder",value="sch",variable=smoot_selec,height=35)
mmf_selection=customtkinter.CTkRadioButton(smoot_subframe,text="Moving Median",value="mmf",variable=smoot_selec,height=35)
nsamples=customtkinter.CTkEntry(smoot_subframe,placeholder_text="Window Size",width=100)

sch_selection.grid(row=0,column=0,padx=35)
mmf_selection.grid(row=0,column=1)
nsamples.grid(row=1,column=1)



# Funcion q se ejecuta para el calculo
def calculate():
    
    global data,fs
    tiempo = np.linspace(0, len(data) / fs, len(data))

    #Verifica si Inverse Rir esta activo y de ser asi da vuelta el valor de data
    inv_rir= rev_check.get()

    if inv_rir == "on":
        data = data[::-1]
    
    #Verifica que tipo de filtrado esta seleccionado
    bands= bands_selection.get()

    data_filtrada=calculo.filtro(data,fs,bands)
    # convierte la lista en un array de arrays
    data_filtrada=np.stack(data_filtrada)

    #flipea el filtardo si esta actiado IRi
    if inv_rir == "on":
        data_filtrada=np.flip(data_filtrada,axis=1)

    smooting=smoot_selec.get()
    N=int(nsamples.get())
    smoot=smoot_selec.get()

    smoot_data=calculo.suaviazado(data,smoot,fs,N)






    




#Creamos el frame para el boton de calcular parametros
calculate_frame=customtkinter.CTkFrame(root,width=300,height=80)
calculate_frame.grid(row=5,column=0)

calculate_btn=customtkinter.CTkButton(calculate_frame,width=200,height=50,text="CALCULATE",font=title_font,command=calculate)
calculate_btn.place(rely=0.1,relx=.15)

root.mainloop()