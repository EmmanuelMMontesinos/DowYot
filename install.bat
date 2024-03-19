@echo off

REM Función para mostrar mensaje de error y pausar antes de salir
:Error
echo ERROR: %1
pause
exit /b 1

REM Verificar si Python ya está instalado
python --version 2>NUL
IF %ERRORLEVEL% EQU 0 (
    echo Python ya está instalado.
) ELSE (
    REM Descargar e instalar Python desde la página oficial
    echo Descargando e instalando Python...
    curl -o python-installer.exe https://www.python.org/ftp/python/3.9.7/python-3.9.7-amd64.exe || call :Error "Error al descargar Python"
    python-installer.exe /quiet TargetDir=C:\Python || call :Error "Error al instalar Python"
    del python-installer.exe
)

REM Instalar dependencias usando Pipenv
echo Instalando dependencias con Pipenv...
pipenv install || call :Error "Error al instalar dependencias con Pipenv"

REM Notificar al usuario que la instalación ha terminado
echo Instalación completa.

REM Pausa para que el usuario tenga la oportunidad de leer el mensaje antes de cerrar la ventana
pause
