@echo off

echo Descargando e instalando Python...
curl -o python-installer.exe https://www.python.org/ftp/python/3.9.7/python-3.9.7-amd64.exe || call :Error "Error al descargar Python"
python-installer.exe /quiet TargetDir=C:\Python InstallAllUsers=1 PrependPath=1 || call :Error "Error al instalar Python"
del python-installer.exe

echo -------------------------------------------
echo Instalando Pip
python -m ensurepip --upgrade
echo -------------------------------------------

echo Instalando dependencias: Pytube, moviepy
pip install pytube
pip install moviepy
pip install ttkbootstrap
echo -------------------------------------------
echo Pytube, movipy instalados

REM Notificar al usuario que la instalación ha terminado
echo Instalacion completa.
pause
