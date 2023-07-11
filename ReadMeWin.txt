1º: Tener descargada la versión 3.9 o superiores de python. Si no funciona en python 3.10 en adelante, desinstalar y probar con la versión 3.9.

2º: Ejecute el programa imports.py, que son los imports necesarios para la correcta ejecución del programa.

3º: Descargar tensorflow 2.9.2 con el siguiente comando: "pip install tensorflow==2.9.2" 
3.1º: Si da error al ejecutar el anterior comando, tendrá que realizar los siguientes pasos:
3.1.1º: Busque en la barra de windows "Editor del registro"
3.1.2º: Dentro de editor del registro entre en "HKEY_LOCAL_MACHINE", dentro de esta en "SYSTEM" y dentro de "SYSTEM" en "CurrentControlSet", luego en "Control" y por último en
"FileSystem" ("\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem")
3.1.3º Dentro de FileSystem, haga doble click en "LongPathsEnabled" y cambie la información del valor de 0 a 1 (A nosotros nos aparece "LongPathsEnabled" en la 4ª posición)
3.2º: Vuelva a intentar instalar tensorflow con el comando de "3º"

4º: Ejecutar launch-win.bat

