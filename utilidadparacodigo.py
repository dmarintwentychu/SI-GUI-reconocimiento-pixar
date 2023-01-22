import os
import tensorflow as tf
from tensorflow import keras
import tensorflow_hub as hub

print(tf.__version__)
tf.keras.backend.clear_session()  # Para restablecer fácilmente el estado del portátil. No necesario o si ni idea jiji

import PIL

import numpy as np
current_directory = os.path.dirname(os.path.realpath(__file__))
model = tf.keras.models.load_model((current_directory + "\Model\model.h5"),  custom_objects={'KerasLayer':hub.KerasLayer})

model.summary()


image = PIL.Image.open(r"C:\Users\danim\OneDrive\Escritorio\SI_GUI\SI\Test\1.jpg")

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

print(predicted_id) #Número correspondiente al personaje predicho

#Esta es la lista para convertir el número predicho en su correspondiente label
class_names = ["Alfredo Linguini de Ratatoui","Boo de Monstruos S.A","Capitan B. McCrea de Wall-E","Carl Fredricksen de Up","Charles Muntz de Up","Chick Hicks de cars","Dash de los increibles","Doc Huston de cars","Dori de Buscando a Nemo","Edna de los increibles","Elastic girl de los increibles","Eva de Wall-E","Flo de cars","Frozono de los increibles","Gill de Buscando a Nemo","Guido de cars","Henry J. Waternoose III de Monstruos S.A","Jessie de Toy Story 3","Lightyear de Toy Story 3","Lotso de Toy Story 3","Luigi de cars","Marlin de Buscando a Nemo","Mate de cars","Mike Wazowski de Monstruos S.A","Mr. Increible de los increibles","Ramon de cars","Rayo de cars","Remy de Ratatoui","Rex de Toy Story 3","Russell de Up","Sally de cars","Sindrome de los increibles","Skinner de Ratatoui","Sr. Potato de Toy Story 3","Strip 'The King' Weathers de cars","Sully de Monstruos S.A","Violeta de los increibles","Wall-E de Wall-E","Woody de Toy Story 3","Nemo de Buscando a Nemo","Randall Boggs de Monstruos S.A"]

print(class_names[predicted_id[0]]) # Este es el valor que predice
