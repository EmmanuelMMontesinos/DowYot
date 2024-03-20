@echo off



REM Verificar si Python ya está instalado

REM Descargar e instalar Python desde la página oficial
echo Descargando e instalando Python...
curl -o python-installer.exe https://www.python.org/ftp/python/3.9.7/python-3.9.7-amd64.exe || call :Error "Error al descargar Python"
python-installer.exe /quiet TargetDir=C:\Python || call :Error "Error al instalar Python"
del python-installer.exe

pip install pipenv
REM Instalar dependencias usando Pipenv
echo Instalando dependencias con Pipenv...
pipenv install || call :Error "Error al instalar dependencias con Pipenv"
pip install pytube
echo Pytube instalado
REM Notificar al usuario que la instalación ha terminado
echo Instalacion completa.

REM Pausa para que el usuario tenga la oportunidad de leer el mensaje antes de cerrar la ventana
pause
