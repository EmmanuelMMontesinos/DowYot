@echo off

echo Borrando archivos...

del DowYot.bat
del DowYotMp3.py
del icono.ico
del install.bat
del Pipfile
del Pipfile.lock
del README.MD
del image.png


pip uninstall -r requirements.txt -y

echo Desistalado, puede cerrar el terminal y borrar la carpeta.

REM Pausa para que el usuario tenga la oportunidad de leer el mensaje antes de cerrar la ventana
pause