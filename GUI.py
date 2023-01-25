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
#from ttkthemes import ThemedTk
import numpy as np
import threading
import random
from PIL import ImageSequence


current_directory = os.getcwd()

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

themepath = current_directory +  '\data\\theme\Azure-ttk-theme-gif-based\\azure.tcl'
splash_style = ttk.Style(splash_root)
splash_root.tk.call("source", themepath)
splash_root.tk.call("set_theme", "dark")

splash_root.update()


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

    global height
    width, height = dummy.size
    if width >800:
        dummy = dummy.resize((800,height))
        width=800
    if height > 400:
        dummy = dummy.resize((width,399))
        height = 399
    return dummy

#Abrir la foto que quieras para predecir
def open():
    global actual_image, my_image_label #mainFrame

    root.filename = filedialog.askopenfilename(initialdir=current_directory + "/Test",title="Selecciona una imagen", filetypes=(("jpg files", "*.jpg"),("all files", "*.*")))
    dummy = Image.open(root.filename)
    dummy = reescalarsi(dummy)
    actual_image = ImageTk.PhotoImage(dummy)
    botonSeleccion.grid_forget()
    my_image_label= ttk.Label(frame,image=actual_image,width=800)
    my_image_label.pack(pady=200-(height/2))

    botonPredecir.config(state=NORMAL,style="Accent.TButton")

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
           
        frame = ttk.LabelFrame(root, text="")
        
        botonSeleccion = ttk.Button(frame, text ="Selecciona una imagen",style="Accent.TButton", command=open,width=40)
        textoInferior = ttk.Label(root, text="Selecciona una imagen en formato .jpg", font=("ComicSans", 20))
        botonPredecir = ttk.Button(root, text="Predecir", width=30,state=DISABLED, command=confirmacion)
        botonOtraPrediccion = ttk.Button(root,style="Accent.TButton", text="Elegir otra imagen para predecir", command=inicio)

        


#Creacción de botones de la ventana final y ocultación de botones de la ventana principal
def botonesFinal():
    global textoFinal,botonInicio,botonSi,botonNo


    if comparar(textoInferior):
        textoInferior.place_forget()
        botonOtraPrediccion.place_forget()
        botonPredecir.place_forget()    
        textoFinal= ttk.Label(root, text="Es tu personaje "+ nombrePj + "?", font=("ComicSans", 20))

        botonSi = ttk.Button(root, text="Si",style="Accent.TButton",command=lambda: memes(1))

        botonNo = ttk.Button(root, text="No",style="Accent.TButton", command=lambda: memes(0))

        botonInicio = ttk.Button(root,text="Volver a predecir otra imagen",style="Accent.TButton", command=inicio)

#Te lleva de vuelta a la ventana inicial
def inicio():
    try: 
        my_image_label.destroy()
        botonPredecir.configure(state=DISABLED,style ="TButton")
        otraVentana()
    except NameError:
        botonPredecir.configure(state=DISABLED,style ="TButton")
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

    #Como el formato es el siguiente (None,224,224,1) <- (1, 224, 224):

    image = np.expand_dims(image, axis=0)  #(1, 224, 224)
    image = np.expand_dims(image, axis=-1) #(1, 224, 224, 1)
    print(image.shape)

    #HAY QUE HACER EL MISMO PREPROCESAMIENTO O SI NO NO FUNCIONA
    normalization_layer = tf.keras.layers.Rescaling(1./255)
    image = normalization_layer(image) 


    predicted_batch = model.predict(image) # FUNCIÓN PARA PREDECIR LA IMAGEN

    predicted_id = tf.math.argmax(predicted_batch, axis=-1)
    predicted_id = predicted_id.numpy() #Se pasa a numpy porque el formato es raro (tuple)

    #Esta es la lista para convertir el número predicho en su correspondiente label
    class_names = ["Alfredo Linguini de Ratatoui","Boo de Monstruos S.A","Capitan B. McCrea de Wall-E","Carl Fredricksen de Up","Charles Muntz de Up","Chick Hicks de cars","Dash de los increibles","Doc Huston de cars","Dori de Buscando a Nemo","Edna de los increibles","Elastic girl de los increibles","Eva de Wall-E","Flo de cars","Frozono de los increibles","Gill de Buscando a Nemo","Guido de cars","Henry J. Waternoose III de Monstruos S.A","Jessie de Toy Story 3","Lightyear de Toy Story 3","Lotso de Toy Story 3","Luigi de cars","Marlin de Buscando a Nemo","Mate de cars","Mike Wazowski de Monstruos S.A","Mr. Increible de los increibles","Ramon de cars","Rayo de cars","Remy de Ratatoui","Rex de Toy Story 3","Russell de Up","Sally de cars","Sindrome de los increibles","Skinner de Ratatoui","Sr. Potato de Toy Story 3","Strip 'The King' Weathers de cars","Sully de Monstruos S.A","Violeta de los increibles","Wall-E de Wall-E","Woody de Toy Story 3","Nemo de Buscando a Nemo","Randall Boggs de Monstruos S.A"]

    #print(class_names[predicted_id[0]]) # Este es el valor que predice

    #Llamamos a la ventana final que pone el personaje y la predicción
    nombrePj = class_names[predicted_id[0]]
    ventanaFinal()

#Pregunta si quiere predecir
def confirmacion():
    respuesta = messagebox.askquestion("Mensaje de confirmación", "¿Quieres predecir esa imagen?")
    if respuesta == "yes":
        predecir()

    else: 
        inicio() 


#Ventana mostrando el pj y preguntando si ha acertado
def ventanaFinal():
    
    botonesFinal()

    textoFinal.place(x=root.winfo_width()/2, y=480, anchor="center")

    botonSi.place(x=400, y=530)

    botonNo.place(x=506, y=530)

    botonInicio.place(x=400, y=570)

    
#Creacción de botones para las distintas ventanas
def otraVentana():

    botonesPrincipal()

    
    frame.place(x=50,y=15,width=900, height=425)
    frame.pack_propagate(0)

    botonSeleccion.grid(row=2, column=2,padx=300,pady=180)

    textoInferior.place(x=root.winfo_width()/2, y=480, anchor="center")
    botonPredecir.place(x=495, y=530)

    botonOtraPrediccion.place(x=275, y=530)

#Generador de memes felices o tristes cuando clicke en si o en No
def memes(respuesta):
    global top,topLabelIF,imagenF,imagenT,framesCnt,frames,canvas,path

    top=Toplevel()    
    top.geometry("500x350")

    width_of_window = 500
    height_of_window = 350
    screen_width = top.winfo_screenwidth()
    screen_height = top.winfo_screenheight()
    x_coordinate = (screen_width/2)-(width_of_window/2)
    y_coordinate = (screen_height/2)-(height_of_window/2)
    top.geometry("%dx%d+%d+%d" %(width_of_window,height_of_window,x_coordinate,y_coordinate))

    imgGif = random.randint(1,2)
    botonSi.config(state=DISABLED,style ="TButton")
    botonNo.config(state=DISABLED,style ="TButton")
    top.overrideredirect(1)

    if respuesta==1:
        top.title("😃😃😃😃😃😃😃😃😃😃😃😃")
        if imgGif == 1:
            print("Meme en Imagen")
            listaArchivos = os.listdir(current_directory+"/data/memesImgFelices")
            meme = random.randint(1,len(listaArchivos))
            dummy = Image.open(current_directory+"/data/memesImgFelices/"+ str(meme)+".jpg")
            dummy = dummy.resize((500,350))
            imagenF = ImageTk.PhotoImage(dummy)
            topLabelIF= ttk.Label(top,image=imagenF).pack()
            top.after(2000, habilitarBtn)
        else :
            print("Meme en Gif")
            
            listaArchivos = os.listdir(current_directory+"/data/memesGifFelices")
            meme = random.randint(1,len(listaArchivos))
            print(meme)
            path = current_directory+"/data/memesGifFelices/"+ str(meme)+".gif"
            dummy = Image.open(path)
            framesCnt = dummy.n_frames
            threading.Thread(play_gif())
            top.after((framesCnt), habilitarBtn)
    

    else :

        top.title("💀💀💀💀💀💀💀💀💀💀💀💀💀")
        if imgGif == 1:
            print("Meme en Imagen")
            listaArchivos = os.listdir(current_directory+"/data/memesImgTristes")
            meme = random.randint(1,len(listaArchivos))
            dummy = Image.open(current_directory+"/data/memesImgTristes/"+ str(meme)+".jpg")
            dummy = dummy.resize((500,350))
            imagenT = ImageTk.PhotoImage(dummy)
            topLabelIF= ttk.Label(top,image=imagenT).pack()
            top.after(2000, habilitarBtn)

        else :
            
            print("Meme en Gif")
            
            listaArchivos = os.listdir(current_directory+"/data/memesGifTristes")
            meme = random.randint(2,len(listaArchivos))
            print(meme)
            path = current_directory+"/data/memesGifTristes/"+ str(meme)+".gif"
            dummy = Image.open(path)
            framesCnt = dummy.n_frames
            threading.Thread(play_gif())
            top.after((framesCnt), habilitarBtn)


def play_gif():
    global path,top

    img = Image.open(path)

    canvas = Canvas(top, width=500, height=350) # Modificar segun el tamaño de la imagen
    canvas.pack()
    for img in ImageSequence.Iterator(img):
        
        img = img.resize((500,350))
        img = ImageTk.PhotoImage(img)
        
        canvas.create_image(0, 0, image=img, anchor=NW)
        top.update()
        time.sleep(0.02)
    


#Funcion para visualizar gifs
def visualizarGif(ind):
    global canvas

    frame = frames[ind]
    ind += 1
    if ind == framesCnt:
        ind = 0
    canvas.create_image(0, 0, image=frame, anchor=NW)
    top.after(20, visualizarGif, ind)




#Cerrar ventana y habilitar botones :)
def habilitarBtn():
    top.destroy()
    botonSi.config(state=NORMAL,style="Accent.TButton")
    botonNo.config(state=NORMAL,style="Accent.TButton")

#VENTANA PRINCIPAL:
def main_window():
     
    global root
    #Formato de ventana:

    splash_root.destroy()
    root = Tk()
    root.geometry("1000x700")
    root.title("Trabajo SI")
    root.iconbitmap(current_directory + "/data/logo/Pixar.ico")


    root.resizable(False, False) 

    root.tk.call("source", themepath)
    root.tk.call("set_theme", "dark")


    otraVentana()

#LLamada a la ventana SPLASH

splash_label = Label(splash_root, width=140, height=130)
splash_label.place(x=243,y=33)

progress_label = Label(splash_root, text="", font=("Times New Roman",13,"bold"), fg="#FFFFFF")
progress_label.place(x=300,y=190)


progress = ttk.Progressbar(splash_root,orient=HORIZONTAL, length=400, mode = "determinate")
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
