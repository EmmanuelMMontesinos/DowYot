import os
from pytube import YouTube, Playlist
from tkinter import ttk, Tk, messagebox, filedialog, StringVar, BooleanVar,Text, Scrollbar, END
from moviepy.editor import AudioFileClip
from ttkbootstrap import Style
import yt_dlp

def mp4_to_mp3(mp4: str, mp3: str):
    """
    Convierte un archivo MP4 a MP3 usando MoviePy.

    Args:
        mp4 (str): Ruta del archivo MP4 a convertir.
        mp3 (str): Ruta del archivo MP3 de salida.

    Returns: No retorna nada.
    """
    audio_clip = AudioFileClip(mp4)
    audio_clip.write_audiofile(mp3)
    audio_clip.close()
    os.remove(mp4)


def download(url: str, path: str, ext: str = ".mp4", playlist: bool = False):
    """
    Descarga un video o playlist de YouTube y lo convierte a MP3 si es necesario.
    Muestra el progreso de la descarga en la interfaz gráfica.


    Args:
        url (str): URL del video o playlist de YouTube.
        path (str): Ruta de la carpeta donde se descargará el archivo.
        ext (str): Extensión del archivo a descargar. Por defecto es ".mp4".
        playlist (bool): Indica si el link es una playlist. Por defecto es False.

    Returns: No retorna nada.
    """
    if not os.path.exists(path):
        os.makedirs(path)

    downloaded_file = {"filename": None}

    def progress_hook(d):
        if d["status"] == "finished":
            downloaded_file["filename"] = d["filename"]

    def log_message(message):
        text_widget.insert(END, message + "\n")
        text_widget.see(END)
        text_widget.update()

    root = Tk()
    root.title("Progreso de la descarga")

    text_widget = Text(root, wrap="word", height=20, width=60)
    text_widget.pack(side="left", fill="both", expand=True)

    scrollbar = Scrollbar(root, command=text_widget.yview)
    scrollbar.pack(side="right", fill="y")

    text_widget.configure(yscrollcommand=scrollbar.set)
    log_message("⌛ Preparando descarga...")

    ydl_opts = {
        "format": "bv+ba/best",
        "merge_output_format": "mp4",
        "outtmpl": os.path.join(path, "%(title)s.%(ext)s"),
        "quiet": True,
        "noplaylist": not playlist,
        "progress_hooks": [progress_hook],
        "postprocessors": [{
            "key": "FFmpegVideoConvertor",
            "preferedformat": "mp4",
        }],
        "ffmpeg_location": "./Assets/ffmpeg/bin/ffmpeg.exe",
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            log_message(f"⌛ Iniciando descarga desde: {url}")
            ydl.download([url])
            mp4_file = downloaded_file["filename"]
            mp4_file = os.path.splitext(mp4_file)[0][:-5] + ".mp4"
            if mp4_file is None:
                raise Exception("No se pudo obtener el archivo descargado.")
            if ext == ".mp3":
                mp3_file = os.path.splitext(mp4_file)[0] + ".mp3"
                log_message(f"♫ Convirtiendo {mp4_file} a MP3...")
                mp4_to_mp3(mp4_file, mp3_file)
                log_message(f"✔️ Conversión completada: {mp3_file}")
        if playlist:
            final_message = f"🏁 Lista de reproducción descargada en: {path}"
            log_message(final_message)
            messagebox.showinfo("Descarga completada", final_message)
        else:
            final_message = f"✔️ Video descargado en máxima calidad en: {path}"
            log_message(final_message)
            messagebox.showinfo("Descarga completada", final_message)
    except Exception as e:
        error_message = f"Error durante la descarga: {e}"
        log_message(error_message)
    root.mainloop()


def select_path(path_label):
    path = filedialog.askdirectory(title="Carpeta donde descargar...")
    path_label.insert(0, path)


def make_window():
    """
    Crea la ventana principal de la aplicación.
    """
    print("Programado por @emmanuelmmontesinos\nVisita mi Web: emmanuelmmontesinos.dev")
    window = Tk()
    window.title("DowYot")
    # window.config(background="LightGray")
    window.iconbitmap(default="icono.ico")
    window.geometry("430x125")
    window.resizable(False, False)
    style_all = Style(theme="superhero")
    style_all.theme_use("superhero")
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
                          padding=2, value=(".mp3") )
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
