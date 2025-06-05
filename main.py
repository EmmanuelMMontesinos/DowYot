import flet as ft
import pyperclip
import os
import datetime
from pathlib import Path
from moviepy.editor import AudioFileClip
import zipfile
import yt_dlp
from Package_Update.Update import UpdateApp

# Actualización
name_app = "DowYot"
version_app = "2.0.1"
url_repository = "https://github.com/EmmanuelMMontesinos/DowYot"

update_app = UpdateApp(name_app, version_app, url_repository)


current_dir = os.getcwd()
ffmpeg_path = current_dir + "\\assets\\ffmpeg\\bin\\ffmpeg.exe"
os.environ["IMAGEIO_FFMPEG_EXE"] = ffmpeg_path
os.environ['PATH'] += ';' + ffmpeg_path


def main(page: ft.Page):
    def close_dialog(dialog):
        dialog.open = False
        page.update()
    def check_and_prompt_update():
        try:
            if update_app.check_update():
                dialog = ft.AlertDialog(
                    title=ft.Text("Actualización disponible"),
                    content=ft.Text("Hay una nueva versión disponible. ¿Deseas actualizar?"),
                    actions=[
                        ft.TextButton("Sí", on_click=lambda _: perform_update(dialog)),
                        ft.TextButton("No", on_click=lambda _: close_dialog(dialog)),
                    ],
                    actions_alignment="center",
                )
                page.dialog = dialog
                dialog.open = True
                page.update()
        except Exception as e:
            print(f"Error al verificar la actualización: {e}")

    # Función para realizar la actualización
    def perform_update(dialog):
        try:
            update_app.update()
            close_dialog(dialog)
            ft.AlertDialog(
                title=ft.Text("Actualización completada"),
                content=ft.Text("La aplicación se ha actualizado correctamente."),
                actions=[ft.TextButton("Aceptar", on_click=lambda _: dialog.close())],
            ).open = True
            page.update()
        except Exception as e:
            ft.AlertDialog(
                title=ft.Text("Error"),
                content=ft.Text(f"Error al actualizar: {e}"),
                actions=[ft.TextButton("Aceptar", on_click=lambda _: dialog.close())],
            ).open = True
            page.update()
    def copy_ffmpeg():
        zip_file = current_dir + "\\Assets\\ffmpeg.zip"
        outpt = current_dir + "\\Assets\\"
        with zipfile.ZipFile(zip_file, "r") as zip:
            zip.extractall(outpt)

    def paste(e: ft.Control):
        url_input.value = pyperclip.paste()
        url_input.update()

    def set_directory(e):
        path_input.value = e.path if e.path else ""
        path_input.update()

    def mp4_to_mp3(mp4, mp3):
        audio_clip = AudioFileClip(mp4)
        audio_clip.write_audiofile(mp3)
        audio_clip.close()
        os.remove(mp4)

    def download(url, path, ext, playlist):
        if not os.path.exists(ffmpeg_path):
            copy_ffmpeg()

        def test_1(e):
            field_output.controls.append(
                ft.Text(
                    value=f"{e}",
                    text_align=ft.MainAxisAlignment.CENTER
                )
            )
            field_output.update()
            page.update()

        if ext:
            ext = ".mp3"
        else:
            ext = ".mp4"

        def log_message(message, size=8, is_error=False):
            text_part = ft.Text(message, size=size, color="red" if is_error else None)
            field_output.controls.append(text_part)
            field_output.update()
            page.update()

        def update_progress_bar(progress):
            progres_bar.value = progress
            field_output.update()
            page.update()

        ydl_opts = {
            "format": "bestaudio/best" if ext == ".mp3" else "bv+ba/best",
            "merge_output_format": "mp4",
            "outtmpl": os.path.join(path, "%(title)s.%(ext)s"),
            "quiet": True,
            # "progress_hooks": [lambda d: update_progress_bar(d["_percent_str"])],
            "postprocessors": [{
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mp3" if ext == ".mp3" else "mp4",
            }],
            "ffmpeg_location": ffmpeg_path,
        }

        try:
            progres_bar = ft.ProgressBar(color="green400", width=450, expand=True)
            field_output.controls.append(progres_bar)
            field_output.update()

            if playlist:
                start = datetime.datetime.now()
                log_message("⌛ Procesando lista de reproducción...")
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                end = datetime.datetime.now()
                log_message(f"🏁 Descarga completada en {end - start}.")
            else:
                log_message(f"⌛ Iniciando descarga de {url}...")
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                log_message("✅ Video descargado correctamente.")

            field_output.controls.remove(progres_bar)
            field_output.update()
        except Exception as e:
            log_message(f"⛔ Error: {e}", is_error=True)
            field_output.update()
    # Actualización
    check_and_prompt_update()
    # UI
    layout = ft.Column(alignment=ft.MainAxisAlignment.CENTER, wrap=False)
    field_url = ft.Row(alignment=ft.MainAxisAlignment.END, wrap=False)
    url_input = ft.TextField("URL YOUTUBE", expand=True)
    url_button = ft.OutlinedButton(
        text="Pegar",
        icon=ft.icons.PASTE,
        icon_color="white",
        on_click=paste,
        expand=True)

    field_path = ft.Row(alignment=ft.MainAxisAlignment.END)
    path_input = ft.TextField(expand=True)
    picked = ft.FilePicker(on_result=set_directory)
    path_button = ft.OutlinedButton(
        text="Destino",
        icon=ft.icons.DRIVE_FILE_MOVE_RTL,
        icon_color="yellow900",
        on_click=lambda _: picked.get_directory_path(),
        expand=True
    )

    field_options = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
    format_option = ft.Switch(label="Solo Audio", value=True)
    playlist_option = ft.Switch(label="Es una Playlist", value=False)

    field_dowload = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
    button_dowload = ft.OutlinedButton(
        text="Descargar",
        icon=ft.icons.DOWNLOAD,
        icon_color="red900",
        expand=True,
        on_click=lambda _: download(
            url=url_input.value,
            path=path_input.value,
            ext=format_option.value,
            playlist=playlist_option.value
        )
    )
    field_output = ft.ListView(
        expand=True,
        auto_scroll=True)

    field_dowload.controls.append(button_dowload)
    field_options.controls.append(format_option)
    field_options.controls.append(playlist_option)
    field_url.controls.append(url_input)
    field_url.controls.append(url_button)
    field_path.controls.append(path_input)
    field_path.controls.append(picked)
    field_path.controls.append(path_button)

    layout.controls.append(field_url)
    layout.controls.append(field_path)
    layout.controls.append(field_options)
    layout.controls.append(field_dowload)

    page.add(layout)
    page.add(field_output)
    
    page.title = "DowYot V2"
    icono = os.path.join("assets", "icono.ico")
    # page.window_icon = icono
    page.window_height = 400
    page.window_width = 525
    page.window_resizable = False
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER

    page.update()


ft.app(target=main, assets_dir="assets")
