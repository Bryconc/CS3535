__author__ = 'Brycon'

import Tkinter as tk
import threading
import urllib
import tkMessageBox
import os

from PIL import Image, ImageTk


FRAME_WIDTH = 50
FRAME_HEIGHT = 20
BACKGROUND_COLOR = "#383b38"
TEXT_COLOR = "#FFF"

WINDOW_WIDTH = 670
WINDOW_HEIGHT = 500


class PlayerGUI(object):
    def __init__(self, player, title="Player"):
        self.player = player

        self.root = tk.Tk()
        self.root.title(title)
        self.root.maxsize(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.root.minsize(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.root.resizable(height=False, width=False)
        self.root.config(bg=BACKGROUND_COLOR)

        self.thr = None
        self.current_track = None
        self.timer = TimerThread(self, threading.Event())
        self.current_track_time = 0

        self.__init_frames()
        self.root.protocol("WM_DELETE_WINDOW", self.__close_handler)

    def __init_frames(self):
        self.__init_menu()
        self.__init_playlist_frame()
        self.__init_mid_playlist_buttons()
        self.__init_favorite_frame()
        self.__init_player_frame()
        self.__init_album_frame()

    def __close_handler(self):
        if tkMessageBox.askokcancel("Quit?", "Are you sure you want to quit?"):
            self.root.quit()
            os._exit(-1)

    def __init_menu(self):
        self.menu_bar = tk.Menu(self.root)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.__close_handler)

        self.export_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.export_menu.add_command(label="Export to existing playlist")
        self.export_menu.add_command(label="Export to new playlist")

        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.menu_bar.add_cascade(label="Export", menu=self.export_menu)
        self.root.config(menu=self.menu_bar)

    def __init_playlist_frame(self):
        self.playlist_frame = tk.Frame(self.root, width=FRAME_WIDTH, height=FRAME_HEIGHT, bg=BACKGROUND_COLOR)

        playlist_label = tk.Label(self.playlist_frame, text="Played Songs:", fg=TEXT_COLOR, bg=BACKGROUND_COLOR, pady=5)
        playlist_label.pack()

        self.playlist_list = tk.Listbox(self.playlist_frame, width=40, height=13, highlightbackground=BACKGROUND_COLOR)
        self.playlist_list.pack()

        self.playlist_frame.grid(row=1, column=0, padx=20)

    def __init_mid_playlist_buttons(self):
        self.button_frame = tk.Frame(self.root, width=10, height=20, bg=BACKGROUND_COLOR)

        to_playlist_btn = tk.Button(self.button_frame, text="<<", width=4, command=self._moveto_playlist,
                                    bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
        to_favorite_btn = tk.Button(self.button_frame, text=">>", width=4, command=self._moveto_favorite,
                                    bg=BACKGROUND_COLOR, fg=TEXT_COLOR)

        to_playlist_btn.pack(pady=10)
        to_favorite_btn.pack()

        self.button_frame.grid(row=1, column=1)

    def __init_favorite_frame(self):
        self.favorite_frame = tk.Frame(self.root, width=FRAME_WIDTH, height=FRAME_HEIGHT, bg=BACKGROUND_COLOR)

        favorite_label = tk.Label(self.favorite_frame, text="Favorite Songs:", fg=TEXT_COLOR, bg=BACKGROUND_COLOR,
                                  pady=5)
        favorite_label.pack()

        self.favorite_list = tk.Listbox(self.favorite_frame, width=40, height=13, highlightbackground=BACKGROUND_COLOR)
        self.favorite_list.pack()
        self.favorite_frame.grid(row=1, column=2, padx=20)

    def __init_player_frame(self):
        BACKGROUND_COLOR = "black"
        self.player_frame = tk.Frame(self.root, width=FRAME_WIDTH, height=FRAME_HEIGHT, bg=BACKGROUND_COLOR)
        self.track_name_label = tk.Label(self.player_frame, text="No song name", width=40, bg=BACKGROUND_COLOR,
                                         fg=TEXT_COLOR)
        self.track_name_label.pack()
        self.timer_label = tk.Label(self.player_frame, text="0/30", bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
        self.timer_label.pack()

        btn_frame = tk.Frame(self.player_frame, bg=BACKGROUND_COLOR)
        self.play_button = tk.Button(btn_frame, text="PLAY", bg="red", fg=TEXT_COLOR, command=self._resume_player)
        self.pause_button = tk.Button(btn_frame, text="PAUSE", bg="green", fg=TEXT_COLOR, command=self._pause_player)
        self.play_button.pack(side=tk.LEFT, padx=5)
        self.pause_button.pack(side=tk.LEFT, padx=5)
        btn_frame.pack(pady=10)

        self.player_frame.grid(row=2, column=0, padx=20)

    def __init_album_frame(self):
        self.album_frame = tk.Frame(self.root, width=FRAME_WIDTH, height=FRAME_HEIGHT, bg=BACKGROUND_COLOR)
        self.album_image = tk.Label(self.album_frame, bg=BACKGROUND_COLOR)
        self.album_image.pack()
        self.album_frame.grid(row=2, column=2, pady=10)

    def show(self):
        if not self.thr:
            self.thr = threading.Thread(target=self.root.mainloop)
            self.thr.start()
        else:
            print("Already running.")

    def update_track(self, track):
        self.current_track = track
        self._update_track_name()
        self._update_album_art()
        self._add_track_to_list()
        self.current_track_time = 0

    def start_timer(self):
        self.timer.start()

    def _add_track_to_list(self):
        self.playlist_list.insert(0, self.current_track['track']['name'])

    def _update_timer(self):
        time_string = str(self.current_track_time) + "/30"
        self.timer_label.config(text=time_string)
        self.current_track_time += 1

    def _update_track_name(self):
        self.track_name_label.config(text=self.current_track['track']['name'])

    def _update_album_art(self):
        if self.current_track:
            image_file, headers = urllib.urlretrieve(self.current_track['track']['album']['images'][0]['url'],
                                                     'Temp_Directory/temp_art.jpg')
            img = Image.open(image_file)
            maxsize = (240, 240)
            img.thumbnail(maxsize, Image.ANTIALIAS)
            pic = ImageTk.PhotoImage(img)
            self.album_image.config(image=pic)
            self.album_image.image = pic

    def _moveto_favorite(self):
        tracks = self.playlist_list.curselection()
        tracks = tracks[::-1]

        for track in tracks:
            t = self.playlist_list.get(track)
            self.favorite_list.insert(0, t)
            self.playlist_list.delete(track)

    def _moveto_playlist(self):
        tracks = self.favorite_list.curselection()
        tracks = tracks[::-1]

        for track in tracks:
            t = self.favorite_list.get(track)
            self.playlist_list.insert(0, t)
            self.favorite_list.delete(track)

    def _pause_player(self):
        if self.player.playing:
            self.player.pause()
            self.pause_button.config(bg='red')
            self.play_button.config(bg='green')

    def _resume_player(self):
        if not self.player.playing:
            self.player.play()
            self.pause_button.config(bg='green')
            self.play_button.config(bg='red')


class TimerThread(threading.Thread):
    def __init__(self, player, event):
        super(TimerThread, self).__init__()
        self.stopped = event
        self.player = player

    def run(self):
        while not self.stopped.wait(1):
            if self.player.player.playing or self.player.current_track_time < 30:
                self.player._update_timer()