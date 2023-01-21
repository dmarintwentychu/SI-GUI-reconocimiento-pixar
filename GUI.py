from tkinter import *
from PIL import ImageTk,Image
import time
from tkinter import filedialog
import cv2
import imutils
import os

#IMPORTANTE: ESTO TARDA 5s en funcionar + PUEDE DAR ERRORES AL HACER EL PIP INSTALL🤬🖕 (Solucionarlo es fácil al menos en windows, en mac ni idea)
#import tensorflow as tf
#from tensorflow import keras

current_directory = os.path.dirname(os.path.realpath(__file__))

#model = tf.keras.models.load_model(current_directory + "\Model\EfficienNetB0") 

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

logo_path =  current_directory + "\data\logo\Logo.mp4"

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
    root.title("Fary")
    #root.iconbitmap() #Si queremos poner un icono
    
    

#LLamada a la ventana SPLASH

cap = cv2.VideoCapture(logo_path)
visualizar()

splash_root.after(4000,main_window)   


mainloop()