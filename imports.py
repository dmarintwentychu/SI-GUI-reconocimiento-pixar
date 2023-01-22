#Esto es para que cuando abras el programa en cualquier ordenador no tenga que hacer pip install y lo haga solo.
import subprocess
import sys
import os


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install("pillow")
install("opencv-python")
install("imutils")
install("tensorflow_hub")
install("pyyaml")
install("h5py")
install("ttkthemes")
#subprocess.check_call([sys.executable, "-m", "pip", "install","tensorflow","==","2.9.2"]) 
#si no os funciona me avisais || Tiene que ser esta versión o si no no es compatible (creo ni idea me quiero pegar un tiro en el escroto)
