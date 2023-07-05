import tkinter as tk
from tkinter import filedialog
import tkinter.ttk as ttk
from pytube import YouTube
import os

def main():
    #Root tkinter
    root = tk.Tk()
    root.iconbitmap(f'{os.path.dirname(os.path.realpath(__file__))}/icon.ico')
    root.title('Downloader')
    root.geometry("600x700")

    #Frame tkinter
    frame = ttk.Frame(root, padding=25)
    frame.pack()

    url = tk.StringVar()
    name = tk.StringVar()
    format = tk.StringVar()

    #Download function
    def download(url, name, format):
        progress['value'] = 0
        path = filedialog.askdirectory(initialdir='/Downloads', title='Choose Location')
        if path == "":
            return
        #progressValue()
        progress['value'] = 25
        YouTube(url).bypass_age_gate()
        if name == "":
            name = YouTube(url).title
        if format == 'audio only (mp3)':
            YouTube(url).streams.filter(only_audio=True).order_by('abr').desc().first().download(filename = f'audio.webm', output_path = f'{path}')
            author = YouTube(url).author
            progress['value'] = 75
            os.system(f'ffmpeg -i "{path}/audio.webm" -map 0:a -metadata title="{name}" -metadata artist="{author}" -metadata album="{name}" "{path}/{name}.mp3"')
            os.remove(f'{path}/audio.webm')
        if format == 'audio only (ogg)':
            YouTube(url).streams.filter(only_audio=True).order_by('abr').desc().first().download(filename = f'audio.webm', output_path = f'{path}')
            author = YouTube(url).author
            progress['value'] = 75
            os.system(f'ffmpeg -i "{path}/audio.webm" -map 0:a -metadata title="{name}" -metadata artist="{author}" -metadata album="{name}" "{path}/{name}.ogg"')
            os.remove(f'{path}/audio.webm')
        if format == 'video only (mp4)':
            YouTube(url).streams.filter(only_video=True).order_by('resolution').desc().first().download(filename = f'{name}.mp4', output_path = f'{path}')
        if format == 'video + audio (mp4 + mp3)':
            YouTube(url).streams.filter(only_audio=True).order_by('abr').desc().first().download(filename = f'audio.webm', output_path = f'{path}')
            author = YouTube(url).author
            progress['value'] = 50
            YouTube(url).streams.filter(only_video=True).order_by('resolution').desc().first().download(filename = f'video.mp4', output_path = f'{path}')
            progress['value'] = 75
            os.system(f'ffmpeg -i "{path}/video.mp4" -i "{path}/audio.webm" -c copy -map 0:v:0 -map 1:a "{path}/{name}.mp4"')
            os.remove(f'{path}/video.mp4')
            os.remove(f'{path}/audio.webm')
        progress['value'] = 100


    #Name label
    l1 = ttk.Label(frame, text='Name')
    l1.pack()

    #Name text entry
    name_entry = ttk.Entry(frame, textvariable=name, width=75)
    name_entry.pack()

    l2 = ttk.Label(frame, text='URL')
    l2.pack()

    url_entry = ttk.Entry(frame, textvariable=url, width=100)
    url_entry.pack()
    
    formats = ['video + audio (mp4 + mp3)', 'video only (mp4)', 'audio only (mp3)', 'audio only (ogg)']

    menu = ttk.Combobox(frame, state = 'readonly', textvariable=format, values = formats, width=25)
    menu.current(0)
    menu.pack()

    button = ttk.Button(frame, text = "Download", command = lambda: download(url.get(), name.get(), format.get()))
    button.pack()

    progress = ttk.Progressbar(frame, length = 600)
    progress.pack(pady = 25)


    root.mainloop()


if __name__ == "__main__":
    main()