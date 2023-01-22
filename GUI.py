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

current_directory = os.path.dirname(os.path.realpath(__file__))



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

logo_path =  os.getcwd() + "/data/logo/logo.mp4"

splash_label = Label(splash_root)
splash_label.pack()

#Función para ver el vídeo:
def visualizar():
    global cap
    if cap is not None:
        ret, frame = cap.read()
        if ret == True:
            frame = imutils.resize(frame, width=640)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)
            splash_label.configure(image=img)
            splash_label.image = img
            splash_label.after(10, visualizar)

#Funciones del main:
def open():
    global actual_image, my_image_label, mainFrame, root
    
    mainFrame = LabelFrame(root,padx=50,pady=50).grid(row=0,column=0)

    root.filename = filedialog.askopenfilename(initialdir="/",title="Selecciona una imagen", filetypes=(("jpg files", "*.jpg"),("all files", "*.*")))
    actual_image = ImageTk.PhotoImage(Image.open(root.filename))
    my_image_label= Label(mainFrame,image=actual_image).grid()


#VENTANA PRINCIPAL:
def main_window():
     
    
    #Formato de ventana:
    splash_root.destroy()
    root = Tk()
    root.geometry("1000x700")
    root.title("Trabajo SI")
    root.iconbitmap(current_directory+ "\data\logo\Icono.ico")

    frame = LabelFrame(root, padx=410,pady=250)
    frame.pack()

    botonSelección = Button(frame, text ="Selecciona una imagen")
    botonSelección.pack()

    textoInferior = Label(root, text="Selecciona una imagen en formato .png", font=("Arial", 20))
    textoInferior.pack()

    botonPredecir = Button(text="Predecir", width=50)
    botonPredecir.pack()
    
    

#LLamada a la ventana SPLASH

cap = cv2.VideoCapture(logo_path)
visualizar()

progress_label = Label(splash_root, text="", font=("Times New Roman",13,"bold"), fg="#FFFFFF", bg="#2F6C60")
progress_label.place(x=100,y=100)

progress = ttk.Style()
progress.theme_use("clam") #el theme se puede cambiar esto es una prueba
progress.configure("red.Horizontal.TProgressbar", background = "#108cff")

progress = Progressbar(splash_root,orient=HORIZONTAL, length=400, mode = "determinate" , style ="red.Horizontal.TProgressbar")
progress.place(x=125,y=225)

i = 0
def load():

    global i, tf,keras, hub

    if i==2:
        import tensorflow as tf
        txt = (str(10*i)+'%')
        progress_label.config(text=txt)
        progress_label.after(100,load)
        progress["value"] = 10*i
        i+=2
    elif i == 6:
        import tensorflow_hub as hub
        model = tf.keras.models.load_model((current_directory + "\Model\model.h5"),  custom_objects={'KerasLayer':hub.KerasLayer})
        txt = (str(10*i)+'%')
        progress_label.config(text=txt)
        progress_label.after(200,load)
        progress["value"] = 10*i
        i+=1
    elif i == 8:
        from tensorflow import keras
        txt = (str(10*i)+'%')
        progress_label.config(text=txt)
        progress_label.after(200,load)
        progress["value"] = 10*i
        i+=1
    elif i<=10:
        txt = (str(10*i)+'%')
        progress_label.config(text=txt)
        progress_label.after(600,load)
        progress["value"] = 10*i
        i+= 1
    else : splash_root.after(100,main_window)   


load()
mainloop()
