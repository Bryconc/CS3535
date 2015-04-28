__author__ = 'Brycon'

import Tkinter as tk
import ttk

DEFAULT_CSV_EXPORT_FILE = "export"


class PlaylistPrompt(tk.Toplevel):
    def __init__(self, parent, controller, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.__init_prompt()
        self.parent = parent
        self.controller = controller

        self.parent.wm_attributes("-disabled", 1)
        self.wm_attributes("-topmost", 1)
        self.focus()
        self.transient(parent)
        self.protocol("WM_DELETE_WINDOW", self.__close_handler)

    def __close_handler(self):
        self.parent.wm_attributes("-disabled", 0)
        self.destroy()

    def __init_prompt(self):
        self.__init_prompt_label()
        # self.__init_user_frame()
        # self.__init_playlist_frame()
        # self.__init_or_frame()
        self.__init_url_frame()
        self.__init_clear_frame()
        self.__init_submit_button()

    def __init_prompt_label(self):
        self.prompt_label = tk.Label(self, text="Please enter the Spotify URL below: ")
        self.prompt_label.pack(pady=10)

    def __init_user_frame(self):
        self.user_frame = tk.Frame(self)
        self.user_label = tk.Label(self.user_frame, text="User ID:     ")
        self.user_entry = tk.Entry(self.user_frame, bd=5)
        self.user_label.pack(side=tk.LEFT)
        self.user_entry.pack(side=tk.RIGHT)
        self.user_frame.pack()

    def __init_playlist_frame(self):
        self.playlist_frame = tk.Frame(self)
        self.playlist_label = tk.Label(self.playlist_frame, text="Playlist ID: ")
        self.playlist_entry = tk.Entry(self.playlist_frame, bd=5)
        self.playlist_label.pack(side=tk.LEFT)
        self.playlist_entry.pack(side=tk.RIGHT)
        self.playlist_frame.pack()

    def __init_clear_frame(self):
        self.clear_frame = tk.Frame(self)

        self.clear_playlist = tk.IntVar()
        self.clear_favorites = tk.IntVar()
        self.clear_playlist.set(1)
        self.clear_favorites.set(1)
        self.clear_playlist_checkbox = tk.Checkbutton(self.clear_frame, text="Clear Playlist",
                                                      variable=self.clear_playlist)
        self.clear_favorites_checkbox = tk.Checkbutton(self.clear_frame, text="Clear Favorites",
                                                       variable=self.clear_favorites)

        self.clear_playlist_checkbox.pack(side=tk.LEFT)
        self.clear_favorites_checkbox.pack(side=tk.RIGHT)
        self.clear_frame.pack()

    def __init_or_frame(self):
        self.or_frame = tk.Frame(self, width=20)
        or_separator_top = ttk.Separator(self.or_frame, orient=tk.HORIZONTAL)
        or_label = tk.Label(self.or_frame, text="Or")
        or_separator_bottom = ttk.Separator(self.or_frame, orient=tk.HORIZONTAL)
        or_separator_top.pack(expand=True, fill=tk.X)
        or_label.pack()
        or_separator_bottom.pack(expand=True, fill=tk.X)
        self.or_frame.pack(expand=True)

    def __init_url_frame(self):
        self.url_frame = tk.Frame(self)
        self.url_label = tk.Label(self.url_frame, text="Spotify Url:")
        self.url_entry = tk.Entry(self.url_frame, bd=5)
        self.url_label.pack(side=tk.LEFT)
        self.url_entry.pack(side=tk.RIGHT)
        self.url_frame.pack()

    def __init_submit_button(self):
        self.submit_button = tk.Button(self, text="Sample", command=self.__validate_new_playlist)
        self.submit_button.pack(pady=(0, 10))

    def __validate_new_playlist(self):
        # if self.url_entry.get():
        user_id, playlist_id = self.__process_url()
        # else:
        # playlist_id = self.playlist_entry.get()
        # user_id = self.user_entry.get()
        clear_playlist = self.clear_playlist.get()
        clear_favorites = self.clear_favorites.get()
        self.controller.new_playlist(user_id, playlist_id, clear_playlist, clear_favorites)
        self.__close_handler()

    def __process_url(self):
        import re

        url = self.url_entry.get()
        regex = r'./user/(?P<user_id>[a-zA-z0-9]+)/playlist/(?P<playlist_id>[a-zA-z0-9]+)'
        regexp = re.compile(regex)
        result = regexp.search(url)
        return result.group('user_id'), result.group('playlist_id')


class ExportCSVPrompt(tk.Toplevel):
    def __init__(self, parent, controller, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.__init_prompt()
        self.parent = parent
        self.controller = controller

        self.parent.wm_attributes("-disabled", 1)
        self.wm_attributes("-topmost", 1)
        self.focus()
        self.transient(parent)
        self.protocol("WM_DELETE_WINDOW", self.__close_handler)

    def __close_handler(self):
        self.parent.wm_attributes("-disabled", 0)
        self.destroy()

    def __init_prompt(self):
        self.__init_export_label()
        self.__init_export_entry()
        self.__init_export_options()
        self.__init_export_button()

    def __init_export_label(self):
        self.export_frame = tk.Frame(self)
        self.export_label = tk.Label(self.export_frame, text="Enter the name for the output file below:",
                                     font="Verdana 10 bold")
        self.export_label.pack(pady=10, padx=10)
        self.export_frame.pack()

    def __init_export_entry(self):
        self.export_entry_frame = tk.Frame(self)
        self.export_entry = tk.Entry(self.export_entry_frame, bd=5)
        self.export_entry.insert(0, DEFAULT_CSV_EXPORT_FILE)
        self.export_entry.pack()
        self.export_entry_frame.pack()

    def __init_export_options(self):
        self.export_options_frame = tk.Frame(self)

        self.export_options_label = tk.Label(self.export_options_frame, text="Export CSV file should include: ",
                                             font="Verdana 10 bold")

        self.export_name = tk.IntVar()
        self.export_name.set(1)
        self.export_album = tk.IntVar()
        self.export_album.set(0)
        self.export_artists = tk.IntVar()
        self.export_artists.set(0)
        self.export_preview_url = tk.IntVar()
        self.export_preview_url.set(0)

        self.export_name_check = tk.Checkbutton(self.export_options_frame, text="Track Name", variable=self.export_name)
        self.export_album_check = tk.Checkbutton(self.export_options_frame, text="Album", variable=self.export_album)
        self.export_artists_check = tk.Checkbutton(self.export_options_frame, text="Artists",
                                                   variable=self.export_artists)
        self.export_preview_url_check = tk.Checkbutton(self.export_options_frame, text="Preview Url",
                                                       variable=self.export_preview_url)

        self.export_options_label.grid(row=0, columnspan=2, pady=10)
        self.export_name_check.grid(row=1, column=0)
        self.export_album_check.grid(row=1, column=1)
        self.export_artists_check.grid(row=2, column=0)
        self.export_preview_url_check.grid(row=2, column=1)

        self.export_options_frame.pack()

    def __init_export_button(self):
        self.export_button_frame = tk.Frame(self)
        self.export_button = tk.Button(self.export_button_frame, text="Export", command=self.__validate_export)
        self.export_button.pack()
        self.export_button_frame.pack(pady=(0, 10))

    def __validate_export(self):
        if self.export_entry.get():
            if self.export_name.get() or self.export_artists.get() or self.export_album.get() or self.export_preview_url.get():
                self.__export()

    def __export(self):
        information = []

        if self.export_name.get():
            information.append('name')

        if self.export_artists.get():
            information.append('artists')

        if self.export_album.get():
            information.append('album')

        if self.export_preview_url.get():
            information.append('preview_url')

        file_name = self.export_entry.get()

        self.controller.export_favorites('csv', file_name=file_name, information=information)
        self.__close_handler()


class ExportExistingPlaylistPrompt(tk.Toplevel):
    def __init__(self, parent, controller, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.__init_prompt()
        self.parent = parent
        self.controller = controller

        self.parent.wm_attributes("-disabled", 1)
        self.wm_attributes("-topmost", 1)
        self.focus()
        self.transient(parent)
        self.protocol("WM_DELETE_WINDOW", self.__close_handler)

    def __close_handler(self):
        self.parent.wm_attributes("-disabled", 0)
        self.destroy()

    def __init_prompt(self):
        self.__init_export_label()
        self.__init_export_entry()
        self.__init_export_button()

    def __init_export_label(self):
        self.export_frame = tk.Frame(self)
        self.export_label = tk.Label(self.export_frame, text="Enter the url of your playlist to extend:",
                                     font="Verdana 10 bold")
        self.export_label.pack(pady=10, padx=10)
        self.export_frame.pack()

    def __init_export_entry(self):
        self.export_entry_frame = tk.Frame(self)
        self.export_entry = tk.Entry(self.export_entry_frame, bd=5)
        self.export_entry.pack()
        self.export_entry_frame.pack()

    def __init_export_button(self):
        self.export_button_frame = tk.Frame(self)
        self.export_button = tk.Button(self.export_button_frame, text="Export", command=self.__validate_export)
        self.export_button.pack()
        self.export_button_frame.pack(pady=(10, 10))

    def __validate_export(self):
        if self.export_entry.get():
            self.__export()

    def __parse_url(self):
        import re

        url = self.export_entry.get()
        regex = r'./user/(?P<user_id>[a-zA-z0-9]+)/playlist/(?P<playlist_id>[a-zA-z0-9]+)'
        regexp = re.compile(regex)
        result = regexp.search(url)
        return result.group('user_id'), result.group('playlist_id')

    def __export(self):
        user_id, playlist_id = self.__parse_url()
        self.controller.export_favorites('existing', playlist=playlist_id, user=user_id)
        self.__close_handler()