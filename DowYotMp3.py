import os
from pytube import YouTube, Playlist
from tkinter import ttk, Tk, messagebox, filedialog, StringVar, BooleanVar
from moviepy.editor import AudioFileClip
from ttkbootstrap import Style


def mp4_to_mp3(mp4, mp3):
    audio_clip = AudioFileClip(mp4)
    audio_clip.write_audiofile(mp3)
    audio_clip.close()
    os.remove(mp4)


def dowload(url, path, ext, playlist):
    if ext == ".mp3":
        only_audio = True
    elif ext == ".mp4":
        only_audio = False
    else:
        only_audio = True
        ext = ".mp3"
    if playlist:
        playlist_generate = Playlist(url)
        nombre_lista = playlist_generate.title
        print(f"🚩 Descargando Lista: {nombre_lista}")
        total = len(playlist_generate.video_urls)
        ciclo = 0
        for video_url in playlist_generate.video_urls:
            ciclo += 1
            try:
                yt = YouTube(str(video_url))

                video = yt.streams.filter(
                    only_audio=only_audio, audio_codec='mp4a.40.2').first()
                nombre_archivo = video.default_filename[:-4]
                print(f"⌛ Iniciando Descarga: {nombre_archivo}")
                destino = path

                salida = video.download(output_path=destino)

                nombre, extension = os.path.splitext(salida)
                audio = nombre + ext
                if only_audio:
                    print("♫ Convirtiendo a mp3")
                    mp4_to_mp3(salida, audio)
                print(
                    f"✔️ Descarga Completada {nombre_archivo} ---> {ciclo}/{total}")
            except Exception as e:
                print(f"Error: {e}")
        print(f"🏁 {nombre_lista} ha sido descargado en {path}")
        messagebox.showinfo(title="Descarga de Lista Completada",
                            message=f"{nombre_lista} ha sido descargado en {path}")
    else:
        yt = YouTube(str(url))

        video = yt.streams.filter(
            only_audio=only_audio, audio_codec='mp4a.40.2').first()
        destino = path
        print("⌛ Iniciando Descarga")
        salida = video.download(output_path=destino)
        nombre_archivo = video.default_filename[:-4]
        print(
            f"✔️ Descarga Completada {nombre_archivo}")
        nombre, extension = os.path.splitext(salida)
        audio = nombre + ext
        if only_audio:
            print("♫ Convirtiendo a mp3")
            mp4_to_mp3(salida, audio)
        messagebox.showinfo(title=f"Descarga {ext} Completada",
                            message=f"{nombre_archivo} ha sido descargado en {path}")


def select_path(path_label):
    path = filedialog.askdirectory(title="Carpeta donde descargar...")
    path_label.insert(0, path)


def make_window():
    print("Programado por @emmanuelmmontesinos")
    window = Tk()
    window.title("DowYot")
    # window.config(background="LightGray")
    window.iconbitmap(default="icono.ico")
    window.geometry("430x125")
    window.resizable(False, False)
    style_all = Style(theme="litera")
    style_all.theme_use("litera")
    frame = ttk.Frame(window, border=5)
    frame_url = ttk.LabelFrame(
        frame, padding=6, text="URL")
    frame_path = ttk.LabelFrame(
        frame, padding=6, text="Carpeta")
    frame_dw = ttk.Label(frame, padding=6)
    url = ttk.Entry(frame_url)
    url.pack(side="left", expand=True)
    selected_ext = StringVar()
    mp3 = ttk.Radiobutton(frame_url, text="MP3", variable=selected_ext,
                          padding=2, value=(".mp3"))
    mp4 = ttk.Radiobutton(frame_url, text="MP4", variable=selected_ext,
                          padding=2, value=(".mp4"))

    mp3.pack(side="right")
    mp4.pack(side="right")
    frame_playlist = ttk.LabelFrame(
        frame, text="¿Es una Playlist?", padding=4, borderwidth=2)
    playlist = BooleanVar(window, value=False)
    ttk.Checkbutton(
        frame_playlist, text="Si, el link es una Playlist", variable=playlist).pack()
    path_label = ttk.Entry(frame_path)
    path_label.pack(side="left")
    ttk.Button(frame_path, text="Carpeta Destino",
               command=lambda: select_path(path_label), cursor="hand2").pack()
    dowloader = ttk.Button(frame_dw, text="Descargar", cursor="hand2", padding=(50, 15, 50, 15),
                           command=lambda: dowload(url.get(),
                                                   path=path_label.get(), ext=selected_ext.get(), playlist=playlist.get()))
    dowloader.grid(row=0, column=1)

    frame_url.grid(row=0, column=0)
    frame_path.grid(row=1, column=0, padx=2)
    frame_playlist.grid(row=0, column=1, padx=5)
    frame_dw.grid(row=1, column=1)
    frame.grid(row=0, column=0)
    window.mainloop()


make_window()


# print(f"{yt.title} ha sido descargado en MP3")
