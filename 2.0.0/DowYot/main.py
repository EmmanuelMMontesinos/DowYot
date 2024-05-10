import flet as ft
import pyperclip
import os
from pytube import YouTube, Playlist, helpers
import datetime
from pathlib import Path

current_dir = os.getcwd()
ffmpeg_path = current_dir + "\\assets\\ffmpeg\\bin\\ffmpeg.exe"
os.environ["IMAGEIO_FFMPEG_EXE"] = ffmpeg_path
os.environ['PATH'] += ';'+ffmpeg_path
from moviepy.editor import AudioFileClip
from pydub import AudioSegment
import zipfile 

def main(page: ft.Page):
    def copy_ffmpeg():
        zip_file = current_dir + "\\assets\\ffmpeg.zip"
        outpt = current_dir + "\\assets\\"
        with zipfile.ZipFile(zip_file,"r") as zip:
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


    def dowload(url, path, ext, playlist):
        if not os.path.exists(ffmpeg_path):
            copy_ffmpeg()
        def test_1(e):
            field_output.controls.append(
            ft.Text(
                value=f"{e}",
                text_align= ft.MainAxisAlignment.CENTER
                )
            )
            field_output.update()
            page.update()
        if ext:
            only_audio = True
            ext = ".mp3"
        else:
            only_audio = False
            ext = ".mp4"
        if playlist:
            try:
                start = datetime.datetime.now()
                playlist_generate = Playlist(url)
                nombre_lista = playlist_generate.title
                total = len(playlist_generate.video_urls)
                ciclo = 0
                field_progres = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
                progres_bar = ft.ProgressBar(
                    width=450,
                    expand=True,
                    value=ciclo
                    )
                field_progres.controls.append(progres_bar)
                layout.controls.append(field_progres)
                layout.update()
                page.update()
                for video_url in playlist_generate.video_urls:
                    ciclo += 1
                    try:
                        yt = YouTube(video_url)

                        video = yt.streams.get_highest_resolution()
                        nombre_archivo = video.default_filename[:-4]
                        destino = path
                        salida = video.download(output_path=destino)

                        nombre, extension = os.path.splitext(salida)
                        audio = nombre + ext
                        if only_audio:
                            mp4_to_mp3(salida, audio)
                        text_part = ft.Text(f"✅ Descarga Completada {nombre_archivo} ---> {ciclo}/{total}",
                                            size=8)
                        field_output.controls.append(text_part)
                        field_output.update()
                        total_p = 100 / len(playlist_generate.video_urls)
                        progres_bar.value += total_p / 100
                        field_output.update()
                        page.update()
                    except Exception as e:
                        text_part = ft.Text(f"⛔ Descarga Fallida {url} ---> {ciclo}/{total}",
                                            size=8)
                        test_1(f"{e}")
                        print(e)
                        field_output.controls.append(text_part)
                        field_output.update()
                        total_p = 100 / len(playlist_generate.video_urls)
                        progres_bar.value += total_p / 100
                        page.update()
                # mensaje fin descarga lista
                end = datetime.datetime.now()
                text_end = ft.Text(value=f"🏁 {nombre_lista} ha sido descargado en {end - start}",size=17)
                field_output.controls.append(text_end)
                field_output.update()
                page.update()
            except Exception as e:
                field_output.controls.append(
                    ft.Text(
                        value=f"{e}",
                        text_align= ft.MainAxisAlignment.CENTER
                        )
                    )
                print(e)
                field_output.update()
                page.update()
        else:
            try:
                progres_bar = ft.ProgressBar(color="green400")
                field_output.controls.append(progres_bar)
                field_output.update()
                yt = YouTube(url)

                video = yt.streams.get_highest_resolution()
                nombre_archivo = video.default_filename[:-4]
                destino = path
                salida = video.download(output_path=destino)

                nombre, extension = os.path.splitext(salida)
                audio = nombre + ext
                if only_audio:
                    mp4_to_mp3(salida, audio)
                text_part = ft.Text(f"✅ Descarga Completada {nombre_archivo}",
                                    size=8)
                field_output.controls.append(text_part)
                field_output.controls.remove(progres_bar)
                field_output.update()
                page.update()
            except Exception as e:
                text_part = ft.Text(f"⛔ Descarga Fallida {url}",
                                            size=8)
                test_1(e)
                field_output.controls.append(text_part)
                field_output.controls.remove(progres_bar)
                print(e)
                field_output.update()
                page.update()

    # UI
    layout = ft.Column(alignment=ft.MainAxisAlignment.CENTER,
                       wrap=False)
    field_url = ft.Row(alignment=ft.MainAxisAlignment.END,
                       wrap= False)
    url_input = ft.TextField(
        "URL YOUTUBE",
        expand=True)
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
        on_click= lambda _: picked.get_directory_path(),
        expand=True
    )
    
    field_options = ft.Row(alignment= ft.MainAxisAlignment.CENTER)
    format_option = ft.Switch(label="Solo Audio",value=True)
    playlist_option = ft.Switch(label="Es una Playlist",value=False)
    
    field_dowload = ft.Row(alignment= ft.MainAxisAlignment.CENTER)
    button_dowload = ft.OutlinedButton(
        text="Descargar",
        icon=ft.icons.DOWNLOAD,
        icon_color="red900",
        expand=True,
        on_click= lambda _: dowload(
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
    page.window_height = 400
    page.window_width = 525
    page.window_resizable = False
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    
    page.update()


ft.app(main,assets_dir="assets")
