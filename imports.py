#Esto es para que cuando abras el programa en cualquier ordenador no tenga que hacer pip install y lo haga solo.
import subprocess
import sys
import os


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install("pillow")
install("opencv-python")
install("imutils")
subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade","tensorflow"]) #si no os funciona me avisais

