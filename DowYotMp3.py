import os
from pytube import YouTube


yt = YouTube(str(input("Pegue el Link de Youtube: ")))
video = yt.streams.filter(only_audio=True,
                          progressive=False,
                          audio_codec="").first()
destino = "."

salida = video.download(output_path=destino)

nombre, extension = os.path.splitext(salida)
audio = nombre + ".mp4"
os.rename(salida, audio)

print(f"{yt.title} ha sido descargado en MP3")
