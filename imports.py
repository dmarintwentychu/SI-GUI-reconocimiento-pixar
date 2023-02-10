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
install("sounddevice")
install("scipy")
install("tensorflow")
install("playsound")

#parece ser que han actualizado algo y 