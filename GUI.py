from tkinter import *
import PIL
from PIL import ImageTk,Image
import time
from tkinter import filedialog
import cv2
import imutils
import os
from tkinter import font
from tkinter import ttk
from tkinter.ttk import Progressbar
from tkinter import messagebox
from ttkthemes import ThemedTk
import numpy as np
import threading
from io import BytesIO

current_directory = os.getcwd()



#IMPORTANTE: ESTO TARDA 5s en funcionar + PUEDE DAR ERRORES AL HACER EL PIP INSTALL🤬🖕 (Solucionarlo es fácil al menos en windows, en mac ni idea)

#PANTALLA SPLASH:

#Formato de la pantalla de splash y vídeo:

splash_root = Tk()
width_of_window = 640
height_of_window = 300
screen_width = splash_root.winfo_screenwidth()
screen_height = splash_root.winfo_screenheight()
x_coordinate = (screen_width/2)-(width_of_window/2)
y_coordinate = (screen_height/2)-(height_of_window/2)
splash_root.geometry("%dx%d+%d+%d" %(width_of_window,height_of_window,x_coordinate,y_coordinate))
splash_root.title("Fary")

splash_root.overrideredirect(1)

logo_path =  current_directory + "/data/logo/logo.mp4"

style = ttk.Style(splash_root)

themepath = current_directory + "/data//theme/Azure-ttk-theme-main//azure dark 2//azure dark 3.tcl"
print(themepath)
splash_root.tk.call("source", themepath)
style.theme_use('azure')


splash_label = Label(splash_root, width=140, height=130)
splash_label.place(x=240,y=30)

#Función para ver el vídeo:
def visualizar():
    global cap,fin
    if fin == False:
        if cap is not None:
            ret, frame = cap.read()
            if ret == True:
                frame = imutils.resize(frame, width=640)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (260, 130)) 
                nrows = 130
                ncols = 260
                row, col = np.ogrid[:nrows, :ncols]
                cnt_row, cnt_col = nrows / 2, ncols / 2
                outer_disk_mask = ((row - cnt_row)**2 + (col - cnt_col)**2 > (nrows / 2)**2)
                frame[outer_disk_mask] = 51
                im = Image.fromarray(frame)
                img = ImageTk.PhotoImage(image=im)

                splash_label.configure(image=img)
                splash_label.image = img
                splash_label.after(10,visualizar)

#Funciones del main:

def reescalarsi(dummy):

    width, height = dummy.size
    if width >800:
        dummy = dummy.resize((800,height))
    if height > 400:
        dummy = dummy.resize((height,400))
    return dummy

#Abrir la foto que quieras para predecir
def open():
    global actual_image, my_image_label #mainFrame
    
    #mainFrame = LabelFrame(root,padx=50,pady=50).grid(row=0,column=0)

    root.filename = filedialog.askopenfilename(initialdir=current_directory + "/Test",title="Selecciona una imagen", filetypes=(("jpg files", "*.jpg"),("all files", "*.*")))
    dummy = Image.open(root.filename)
    dummy = reescalarsi(dummy)
    actual_image = ImageTk.PhotoImage(dummy)
    botonSeleccion.grid_forget()
    my_image_label= Label(frame,image=actual_image,width=800,height=400)
    my_image_label.pack()

    botonPredecir.config(state=NORMAL)

#Creacción de botones de la ventana principal y ocultación de botones de la ventana final             
def botonesPrincipal():
    global frame, botonOtraPrediccion, botonPredecir, botonSeleccion,textoInferior

    try:
        if comparar(textoFinal):
            textoFinal.place_forget()
            botonSi.place_forget()
            botonNo.place_forget()
            botonInicio.place_forget()

    except NameError:
           
        frame = LabelFrame(root,padx=10,pady=10)
        
        botonSeleccion = Button(frame, text ="Selecciona una imagen", command=open,width=40,height=10)
        textoInferior = Label(root, text="Selecciona una imagen en formato .jpg", font=("ComicSans", 20))
        botonPredecir = Button(root, text="Predecir", width=30,state=DISABLED, command=confirmacion, pady=20)
        botonOtraPrediccion = Button(root, text="Elegir otra imagen para predecir", command=inicio,pady=20,padx=13)
a

        


#Creacción de botones de la ventana final y ocultación de botones de la ventana principal
def botonesFinal():
    global textoFinal,botonInicio,botonSi,botonNo

    if comparar(textoInferior):
        textoInferior.place_forget()
        botonOtraPrediccion.place_forget()
        botonPredecir.place_forget()    
        textoFinal= Label(root, text="Es tu personaje "+ nombrePj + "?", font=("ComicSans", 20))

        botonSi = Button(root, text="Si", padx = 30, pady = 20, command=memes)

        botonNo = Button(root, text="No", padx = 30, pady = 20, command=memes)

        botonInicio = Button(root,text="Volver a predecir otra imagen", padx=20,command=inicio,pady=20)

#Te lleva de vuelta a la ventana inicial
def inicio():
    try: 
        my_image_label.destroy()
        botonPredecir.configure(state=DISABLED)
        otraVentana()
    except NameError:
        botonPredecir.configure(state=DISABLED)
        otraVentana()

#Revisa que el objeto que le pases por parámetro existe
def comparar(objeto):
    vivo = False
    for obj in root.winfo_children():
        if isinstance(obj, type(objeto)):
            vivo = True

    return vivo

#predicción con tensorflow
def predecir():

    global nombrePj
    

    tf.keras.backend.clear_session()  # Para restablecer fácilmente el estado del portátil. No necesario o si ni idea jiji

    image = PIL.Image.open(root.filename)

    #PREPROCESAMIENTO (mismo que en el colab):

    #se ajusta la altura y anchura a la misma:
    baseheight = 224
    width = 224
    image = np.array(image.resize((width, baseheight)))
    print(image.shape)

    #Como el formato es el siguiente (None,224,224,1) -> (1, 224, 224, 1):

    image = np.expand_dims(image, axis=0) # To make the shape as (1, 224, 224)
    image = np.expand_dims(image, axis=-1) # To make the shape as (1, 224, 224, 1)
    print(image.shape)

    #HAY QUE HACER EL MISMO PREPROCESAMIENTO O SI NO NO FUNCIONA .|.
    normalization_layer = tf.keras.layers.Rescaling(1./255)
    image = normalization_layer(image) 


    predicted_batch = model.predict(image) # FUNCIÓN PARA PREDECIR LA IMAGEN

    predicted_id = tf.math.argmax(predicted_batch, axis=-1)
    predicted_id = predicted_id.numpy() #Sepasa a numpy porque el formato es raro (tuple)

    #print(predicted_id) #Número correspondiente al personaje predicho

    #Esta es la lista para convertir el número predicho en su correspondiente label
    class_names = ["Alfredo Linguini de Ratatoui","Boo de Monstruos S.A","Capitan B. McCrea de Wall-E","Carl Fredricksen de Up","Charles Muntz de Up","Chick Hicks de cars","Dash de los increibles","Doc Huston de cars","Dori de Buscando a Nemo","Edna de los increibles","Elastic girl de los increibles","Eva de Wall-E","Flo de cars","Frozono de los increibles","Gill de Buscando a Nemo","Guido de cars","Henry J. Waternoose III de Monstruos S.A","Jessie de Toy Story 3","Lightyear de Toy Story 3","Lotso de Toy Story 3","Luigi de cars","Marlin de Buscando a Nemo","Mate de cars","Mike Wazowski de Monstruos S.A","Mr. Increible de los increibles","Ramon de cars","Rayo de cars","Remy de Ratatoui","Rex de Toy Story 3","Russell de Up","Sally de cars","Sindrome de los increibles","Skinner de Ratatoui","Sr. Potato de Toy Story 3","Strip 'The King' Weathers de cars","Sully de Monstruos S.A","Violeta de los increibles","Wall-E de Wall-E","Woody de Toy Story 3","Nemo de Buscando a Nemo","Randall Boggs de Monstruos S.A"]

    #print(class_names[predicted_id[0]]) # Este es el valor que predice
    #Llamamos a la ventana final que pone el personaje y la predicción
    nombrePj = class_names[predicted_id[0]]
    ventanaFinal()

#Pregunta de si quiere predecir
def confirmacion():
    respuesta = messagebox.askquestion("Mensaje de confirmación", "¿Quieres predecir esa imagen?")
    if respuesta == "yes":
        predecir()

    else: 
        inicio() 


#Ventana mostrando el pj y preguntando si ha acertado
def ventanaFinal():
    
    botonesFinal()

    textoFinal.place(x=270, y=450)

    botonSi.place(x=400, y=500)

    botonNo.place(x=519, y=500)

    botonInicio.place(x=400, y=563)

    
#Creacción de botones para las distintas ventanas
def otraVentana():

    botonesPrincipal()

    
    frame.place(x=50,y=15,width=900, height=425)
    frame.pack_propagate(0)

    botonSeleccion.grid(row=2, column=2,padx=300,pady=130)

    textoInferior.place(x=270, y=450)
  
    botonPredecir.place(x=500, y=500)

    botonOtraPrediccion.place(x=300, y=500)

#Generador de memesfelices o tristes cuando clicke en si o en No
def memes():
    print("MEMEs")



#VENTANA PRINCIPAL:
def main_window():
     
    global root
    #Formato de ventana:
    #fin = True
    #t1.join()
    splash_root.destroy()
    root = Tk()
    root.geometry("1000x700")
    root.title("Trabajo SI")
    root.iconbitmap(current_directory+ "/data/logo/Icono.ico")
    root.resizable(False, False) 



    otraVentana()
    
    

#LLamada a la ventana SPLASH

progress_label = Label(splash_root, text="", font=("Times New Roman",13,"bold"), fg="#FFFFFF")
progress_label.place(x=300,y=190)


progress = Progressbar(splash_root,orient=HORIZONTAL, length=400, mode = "determinate")
progress.place(x=125,y=225)


i = 0
def load():

    global i, tf,keras, hub,model,fin

    if i==2:
        import tensorflow as tf
        txt = (str(10*i)+'%')
        progress_label.config(text=txt)
        progress_label.after(600,load)
        progress["value"] = 10*i
        i+=2
    elif i == 6:
        from tensorflow import keras
        import tensorflow_hub as hub
        txt = (str(10*i)+'%')
        progress_label.config(text=txt)
        progress_label.after(600,load)
        progress["value"] = 10*i
        i+=1
    elif i == 8:
        model = tf.keras.models.load_model((current_directory + "/Model/model.h5"),  custom_objects={'KerasLayer':hub.KerasLayer})
        txt = (str(10*i)+'%')
        progress_label.config(text=txt)
        progress_label.after(600,load)
        progress["value"] = 10*i
        i+=1
    elif i<=10:
        txt = (str(10*i)+'%')
        progress_label.config(text=txt)
        progress_label.after(400,load)
        progress["value"] = 10*i
        i+= 1
        
    else : 
        fin = True
        splash_root.after(600,main_window)   


cap = cv2.VideoCapture(logo_path)
fin = False
t1 = threading.Thread(target = visualizar)
t1.start()
load()


mainloop()
