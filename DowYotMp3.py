import os
from pytube import YouTube, Playlist
from tkinter import ttk, Tk, messagebox, filedialog, StringVar, BooleanVar
from moviepy.editor import AudioFileClip
from ttkbootstrap import Style
import yt_dlp

def mp4_to_mp3(mp4, mp3):
    audio_clip = AudioFileClip(mp4)
    audio_clip.write_audiofile(mp3)
    audio_clip.close()
    os.remove(mp4)


def download(url, path, ext, playlist):
    """
    Descarga un video o lista de reproducción desde YouTube usando yt-dlp.

    Args:
        url (str): URL del video o lista de reproducción.
        path (str): Ruta de destino para guardar los archivos.
        ext (str): Extensión deseada ('.mp3' o '.mp4').
        playlist (bool): Indica si es una lista de reproducción.
    """
    only_audio = ext == ".mp3"

    ydl_opts = {
        "format": "bestaudio/best" if only_audio else "best", 
        "outtmpl": os.path.join(path, "%(title)s.%(ext)s"),
        "quiet": False,
        "noplaylist": not playlist,
    }


    if only_audio:
        ydl_opts.update({
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
            "ffmpeg_location": "./Assets/ffmpeg/bin/ffmpeg.exe",
        })

    try:
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"⌛ Iniciando descarga desde: {url}")
            ydl.download([url])

        if playlist:
            print(f"🏁 Lista de reproducción descargada en: {path}")
            messagebox.showinfo(
                title="Descarga de Lista Completada",
                message=f"La lista de reproducción ha sido descargada en {path}",
            )
        else:
            print(f"✔️ Video descargado en: {path}")
            messagebox.showinfo(
                title=f"Descarga {ext} Completada",
                message=f"El video ha sido descargado en {path}",
            )
    except Exception as e:
        print(f"Error durante la descarga: {e}")
        messagebox.showerror(
            title="Error de Descarga",
            message=f"Hubo un error durante la descarga: {e}",)


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
                           command=lambda: download(url.get(),
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
