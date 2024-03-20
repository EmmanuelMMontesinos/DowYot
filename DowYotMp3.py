import os
from pytube import YouTube, Playlist
from tkinter import ttk, Tk, messagebox, filedialog, StringVar, BooleanVar


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
            yt = YouTube(str(video_url))

            video = yt.streams.filter(only_audio=only_audio,
                                      audio_codec="").first()
            nombre_archivo = video.default_filename[:-4]
            print(f"⌛ Iniciando Descarga: {nombre_archivo}")
            destino = path

            salida = video.download(output_path=destino)

            nombre, extension = os.path.splitext(salida)
            audio = nombre + ext
            os.rename(salida, audio)
            print(
                f"✔️ Descarga Completada {nombre_archivo} ---> {ciclo}/{total}")
        print(f"🏁 {nombre_lista} ha sido descargado en {path}")
        messagebox.showinfo(title="Descarga de Lista Completada",
                            message=f"{nombre_lista} ha sido descargado en {path}")
    else:
        yt = YouTube(str(url))

        video = yt.streams.filter(only_audio=only_audio,
                                  audio_codec="").first()
        destino = path
        print(f"⌛ Iniciando Descarga")
        salida = video.download(output_path=destino)
        nombre_archivo = video.default_filename[:-4]
        print(
            f"✔️ Descarga Completada {nombre_archivo}")
        nombre, extension = os.path.splitext(salida)
        audio = nombre + ext
        os.rename(salida, audio)
        messagebox.showinfo(title=f"Descarga {ext} Completada",
                            message=f"{nombre_archivo} ha sido descargado en {path}")


def select_path(path_label):
    path = filedialog.askdirectory(title="Carpeta donde descargar...")
    path_label.insert(0, path)


def make_window():
    print("Programado por @emmanuelmmontesinos")
    window = Tk()
    window.title("DowYot")
    window.config(background="red")
    window.iconbitmap(default="icono.ico")
    window.geometry("300x165")
    window.resizable(False, False)
    frame_url = ttk.LabelFrame(window, padding=2, text="URL",)
    frame_path = ttk.LabelFrame(window, padding=2, text="Carpeta")
    frame_dw = ttk.Label(window, padding=2, style="TLabel")
    style_labelFrame = ttk.Style(window)
    style_labelFrame.configure("TLabel", background="blue")
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
        window, text="¿Es una Playlist?", padding=2)
    playlist = BooleanVar(window, value=False)
    ttk.Checkbutton(
        frame_playlist, text="Si, el link es una Playlist", variable=playlist).pack(side="right")
    path_label = ttk.Entry(frame_path)
    path_label.pack(side="left")
    style = ttk.Style(window)
    style.configure(window, background="red")
    ttk.Button(frame_path, text="Carpeta Destino",
               command=lambda: select_path(path_label)).pack(side="right")
    dowloader = ttk.Button(frame_dw, text="Descargar",
                           command=lambda: dowload(url.get(),
                                                   path=path_label.get(), ext=selected_ext.get(), playlist=playlist.get()), padding=2)

    style_dw = ttk.Style(dowloader)
    style_dw.configure(dowloader, background="red")
    dowloader.pack()

    frame_url.pack(expand=True)
    frame_playlist.pack()
    frame_path.pack(expand=True)
    frame_dw.pack(expand=True)
    window.mainloop()


make_window()


# print(f"{yt.title} ha sido descargado en MP3")
