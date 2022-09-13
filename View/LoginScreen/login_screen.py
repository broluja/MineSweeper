from kivymd.uix.screen import MDScreen

from View.Manager.info_manager import InfoManager
from Model.user_manager import user_manager


class LoginScreenView(MDScreen):
    """Login Screen"""

    def login(self, name):
        if not name:
            info_manager = InfoManager()
            info_manager.login_info()
        else:
            with user_manager as manager:
                player = manager.get_or_create_player(name)
                self.manager.app.player = player
                self.manager.switch_screen('main')

    def on_leave(self, *args):
        self.ids.name_field.text = ''
