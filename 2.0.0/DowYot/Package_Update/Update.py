import requests
import os
from tqdm import tqdm
from dataclasses import dataclass
import zipfile


@dataclass(slots=True)
class UpdateApp:
    name_app: str
    version_app: str
    url_repository: str
    latest_version: str = None

    def check_update(self) -> bool:
        """
        Verifica si hay una nueva versión disponible en el repositorio.
        """
        url_latest = f"{self.url_repository}/releases/latest"
        response = requests.get(url_latest, allow_redirects=True)
        if response.status_code == 200:
            latest_version = response.url.split("/")[-1]  # Extrae la versión de la URL
            print(f"Última versión disponible: {latest_version}")
            self.latest_version = latest_version
            return latest_version != self.version_app
        else:
            print(f"Error al obtener la última versión: {response.status_code}")
            return False

    def update(self):
        """
        Realiza el proceso de actualización si es necesario.
        """
        print(f"Buscando actualizaciones para {self.name_app}...")
        if self.check_update():
            print(f"Actualización disponible para {self.name_app}. Descargando...\n")
            path_new_version = self.download_latest()
            if path_new_version != None:
                self.install(path_new_version)
        else:
            print(f"{self.name_app} ya está actualizado.")
    def install(self,path_new_version):
        """
        Instala la nueva versión descargada.
        """
        path = os.path.dirname(path_new_version)  # Obtiene el directorio donde se descomprimirá
        print(f"Instalando {self.name_app}...")

        with zipfile.ZipFile(path_new_version, 'r') as zip_ref:
            # Lista de archivos dentro del ZIP
            archivos = zip_ref.namelist()
            total_archivos = len(archivos)

            # Barra de progreso para la extracción
            with tqdm(total=total_archivos, desc="Extrayendo archivos", unit="archivo") as barra:
                for archivo in archivos:
                    zip_ref.extract(archivo, path)  # Extrae archivo individualmente
                    barra.update(1)  # Actualiza la barra por cada archivo extraído

        print(f"{self.name_app} instalado correctamente.\n")
        os.remove(path_new_version)
        print(f"Archivo {path_new_version} eliminado.\n")
        print(f"Actualizando 'repo_config.txt'...")
        with open("repo_config.txt", "w") as file:
            file.write(f"name_app-{self.name_app}\n")
            file.write(f"version_app-{self.latest_version}\n")
            file.write(f"url_repository-{self.url_repository}\n")

        print(f"Configuración actualizada en 'repo_config.txt'.")

    def download_latest(self):
        """
        Descarga la última versión disponible de los assets del repositorio.
        """
        owner, app = self.url_repository.split("/")[3:5]
        url_latest = f"https://api.github.com/repos/{owner}/{app}/releases/latest"
        response = requests.get(url_latest)
        if response.status_code == 200:
            release_data = response.json()
            download_url = release_data["assets"][0]["browser_download_url"]
            latest_version = release_data["tag_name"]
            print(f"Descargando {self.name_app} versión {latest_version} desde {download_url}")

            # Directorio destino
            path = os.getcwd().replace("\\", "/")
            file_name = download_url.split("/")[-1]
            file_path = os.path.join(path, file_name)

            # Descargar el archivo con barra de progreso
            with requests.get(download_url, stream=True) as r:
                r.raise_for_status()
                total_size = int(r.headers.get("content-length", 0))
                block_size = 1024  # Tamaño del bloque para la barra de progreso

                with open(file_path, "wb") as file, tqdm(
                    desc=f"Descargando {self.name_app}",
                    total=total_size,
                    unit="B",
                    unit_scale=True,
                    unit_divisor=1024,
                ) as barra:
                    for chunk in r.iter_content(chunk_size=block_size):
                        file.write(chunk)
                        barra.update(len(chunk))

            print(f"Archivo descargado en: {file_path}\n")
            return file_path
        else:
            print(f"Error al obtener información de la release: {response.status_code}\n")
            return None

def cli():
    """
    Script de consola para actualizar una aplicación desde un repositorio GitHub.
    Es necesario un archivo llamado 'repo_config.txt' en la ruta raiz del proyecto con la siguiente estructura:

    name_app-Nombre de la aplicación
    version_app-Versión actual de la aplicación
    url_repository-URL del repositorio de GitHub
    """
    with open("repo_config.txt", "r") as f:
        config = f.read().splitlines()

    name_app = config[0].split("-")[1].strip()
    version_app = config[1].split("-")[1].strip()
    url_repository = config[2].split("-")[1].strip()
    update_app = UpdateApp(name_app, version_app, url_repository)
    update_app.update()

# CLI para usarlo como script en lugar de clase integrada en tu codigo
if __name__ == "__main__":

    try:
        cli()
    except Exception as e:
        print(f"Revise el archivo 'repo_config.txt' y el repositorio.\nError: {e}")