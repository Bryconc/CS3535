__author__ = 'Brycon'

import player_view


class Controller(object):
    def __init__(self, model):
        self.model = model
        self.view = player_view.View(self, model)

    def show(self):
        self.view.show()

    def start(self):
        self.model.on()
        self.view.enable_pause_button()
        self.view.disable_play_button()

    def stop(self):
        self.model.off()
        self.view.disable_pause_button()
        self.view.enable_play_button()

    def new_playlist(self, user_id, playlist_id, clear_playlist=True, clear_favorites=False):
        if clear_playlist:
            self.view.clear_playlist_box()
        if clear_favorites:
            self.view.clear_favorites_box()
        self.view.clear_detail_box()
        self.model.new_playlist(user_id, playlist_id)
        self.start()

    def unload_player(self, wait=True):
        self.model.unload_player(wait)

    def get_playlist_list(self):
        return self.model.get_playlist_list()

    def get_favorites_list(self):
        return self.model.get_favorites_list()

    def get_master_track_list(self):
        return self.model.get_master_track_list()

    def get_current_track(self):
        return self.model.get_current_track()

    def get_current_track_number(self):
        return self.model.get_current_track_number()

    def get_playlist_amount(self):
        return self.model.get_playlist_amount()

    def set_spotipy_information(self, username, playlist_id):
        self.model.set_spotipy_information(username, playlist_id)

