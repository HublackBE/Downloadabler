# Downloadabler is a personal project of mine(Hublack) that helps download and convert videos from YouTube
# Copyright (C) 2024  Hublack

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import tkinter.ttk as ttk
from pytube import YouTube
import os
from threading import Thread

def main():
    #Root tkinter
    root = tk.Tk()
    root.iconbitmap(f'{os.path.dirname(os.path.realpath(__file__))}/icon.ico')
    root.title('Downloadabler')
    root.geometry("600x700")

    #Frame tkinter
    frame = ttk.Frame(root, padding=25)
    frame.pack()

    url = tk.StringVar()
    name = tk.StringVar()
    author = tk.StringVar()
    format = tk.StringVar()

    def ChooseImage():
        global imagePath
        imagePath = filedialog.askopenfilename(initialdir='/Downloads', title='Choose Image', filetypes=(("Image file",".png .jpg .jpeg"),("All files",".*")))

    #Download function
    def download(url, name, author, format):
        progress['value'] = 0
        progress.start(500)
        path = filedialog.askdirectory(initialdir='/Downloads', title='Choose Location')
        if path == "":
            return
        progress['value'] = 25  #progressValue()
        #YouTube(url).bypass_age_gate()
        if name == "Name":
            try: name = YouTube(url).title
            except: errorBox()
        bad_char = ["<", ">", ":", "\"", "/", "\\", "|", "?", "*"]
        for i in bad_char:
            name = name.replace(i, '')
        if author == "Author":
            try: author = YouTube(url).author
            except: errorBox()
        if format == 'audio only (mp3)' or format == 'audio only (ogg)' or format == 'audio only (wav)':
            try: YouTube(url).streams.filter(only_audio=True).order_by('abr').desc().first().download(filename = f'audio.webm', output_path = f'{path}')
            except: errorBox()
            progress['value'] = 75
            try: os.system(f'ffmpeg -i "{path}/audio.webm" -i "{imagePath}" -map 0:a -map 1 -id3v2_version 3 -metadata title="{name}" -metadata artist="{author}" -metadata album="{name}" "{path}/{name}.{format[-4:-1]}"')
            except: os.system(f'ffmpeg -i "{path}/audio.webm" -map 0:a -metadata title="{name}" -metadata artist="{author}" -metadata album="{name}" "{path}/{name}.{format[-4:-1]}"')
            os.remove(f'{path}/audio.webm')
        if format == 'audio only (webm)':
            try: YouTube(url).streams.filter(only_audio=True).order_by('abr').desc().first().download(filename = f'audio.webm', output_path = f'{path}')
            except: errorBox()
            progress['value'] = 75
            try: 
                os.system(f'ffmpeg -i "{path}/audio.webm" -map 0:a -metadata title="{name}" -metadata artist="{author}" -metadata album="{name}" "{path}/{name}.webm"')
                os.remove(f'{path}/audio.webm')
            except: errorBox()
        if format == 'video only (mp4)' or format == 'video only (mkv)':
            try: YouTube(url).streams.filter(only_video=True).order_by('resolution').desc().first().download(filename = f'{name}.{format[-4:-1]}', output_path = f'{path}')
            except: errorBox()
        if format == 'video only (webm)':
            try: YouTube(url).streams.filter(only_video=True).order_by('resolution').desc().first().download(filename = f'{name}.{format[-5:-1]}', output_path = f'{path}')
            except: errorBox()
        if format == 'video + audio (mp4 + mp3)' or format == 'video + audio (mkv + mp3)':
            try: YouTube(url).streams.filter(only_audio=True).order_by('abr').desc().first().download(filename = f'audio.webm', output_path = f'{path}')
            except: errorBox()
            progress['value'] = 50
            try: YouTube(url).streams.filter(only_video=True).order_by('resolution').desc().first().download(filename = f'video.{format[-10:-7]}', output_path = f'{path}')
            except: errorBox()
            progress['value'] = 75
            try: os.system(f'ffmpeg -i "{path}/video.{format[-10:-7]}" -i "{path}/audio.webm" -c copy -map 0:v:0 -map 1:a "{path}/{name}.{format[-10:-7]}"')
            except: errorBox()
            os.remove(f'{path}/video.{format[-10:-7]}')
            os.remove(f'{path}/audio.webm')
        if format == 'video + audio (webm + mp3)':
            try: YouTube(url).streams.filter(only_audio=True).order_by('abr').desc().first().download(filename = f'audio.webm', output_path = f'{path}')
            except: errorBox()
            progress['value'] = 50
            try: YouTube(url).streams.filter(only_video=True).order_by('resolution').desc().first().download(filename = f'video.{format[-11:-7]}', output_path = f'{path}')
            except: errorBox()
            progress['value'] = 75
            try: os.system(f'ffmpeg -i "{path}/video.{format[-11:-7]}" -i "{path}/audio.webm" -c copy -map 0:v:0 -map 1:a "{path}/{name}.{format[-11:-7]}"')
            except: errorBox()
            os.remove(f'{path}/video.{format[-11:-7]}')
            os.remove(f'{path}/audio.webm')
        progress.stop()
        progress['value'] = 100

    def In(event):
        global changed
        global saved_text
        if 'changed' not in globals():
            changed = {}
        if 'saved_text' not in globals():
            saved_text = {}
        try: changed[event.widget]
        except KeyError: changed[event.widget] = False
        if changed[event.widget] is False:
            saved_text[event.widget] = event.widget.get()
            event.widget.delete(0,"end")
            event.widget.configure(style="TEntry")
    
    def Out(event):
        global changed
        if event.widget.get() == "":
            event.widget.configure(style="Grey.TEntry")
            event.widget.insert(0, saved_text[event.widget])
            changed[event.widget] = False
        else:
            event.widget.configure(style="TEntry")
            changed[event.widget] = True

    def Choice(event):
        if format.get() == 'audio only (mp3)':
            imageButton.configure(state='normal')
        else:
            imageButton.configure(state='disabled')

    def errorBox():
        messagebox.showerror("Unexpected Error", "An Unexpected Error occured.")
        raise Exception("An Unexpected Error occured")
    
    
    #URL label
    l1 = ttk.Label(frame, text='URL')
    l1.pack()
    url_entry = ttk.Entry(frame, textvariable=url, width=100)
    url_entry.insert(0,"URL")
    url_entry.configure(style="Grey.TEntry")
    url_entry.pack()

    #Name label
    l2 = ttk.Label(frame, text='Name')
    l2.pack()

    #Name text entry
    name_entry = ttk.Entry(frame, textvariable=name, width=75)
    name_entry.insert(0,"Name")
    name_entry.configure(style="Grey.TEntry")
    name_entry.pack()

    l3 = ttk.Label(frame, text="Author")
    l3.pack()

    author_entry = ttk.Entry(frame, textvariable=author, width=50)
    author_entry.insert(0,"Author")
    author_entry.configure(style="Grey.TEntry")
    author_entry.pack()
    
    l4 = ttk.Label(frame, text="Type")
    l4.pack()

    formats = ['video + audio (mp4 + mp3)', 'video + audio (mkv + mp3)', 'video + audio (webm + mp3)', 'video only (mp4)', 'video only (mkv)', 'video only (webm)', 'audio only (mp3)', 'audio only (ogg)', 'audio only (wav)', 'audio only (webm)']

    menu = ttk.Combobox(frame, state = 'readonly', textvariable=format, values = formats, width=25)
    menu.bind('<<ComboboxSelected>>', Choice)
    menu.current(0)
    menu.pack()

    l5 = ttk.Label(frame, text="Cover Art")
    l5.pack(pady= (5, 0))

    imageButton = ttk.Button(frame, text = "Choose Image", width=15, state='disabled', command = lambda: Thread(ChooseImage()))
    imageButton.pack()

    downloadButton = ttk.Button(frame, text = "Download", command = lambda: Thread(target = download, args=(url.get(), name.get(), author.get(), format.get())).start())
    downloadButton.pack(pady= (25, 0))

    progress = ttk.Progressbar(frame, length = 600, mode='determinate')
    progress.pack(pady = 25)
    root.bind_class("TEntry", "<FocusIn>", In)
    root.bind_class("TEntry", "<FocusOut>", Out)

    style = ttk.Style()
    style.configure("Grey.TEntry", foreground="grey")

    root.mainloop()


if __name__ == "__main__":
    Thread(main())
