from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.metrics import dp

from View.Manager.info_manager import InfoManager
from Model.user_manager import user_manager


class Content(MDBoxLayout):
    spacing = dp(5)


class LoginScreenView(MDScreen):
    """
    Screen used for logging in game.
    """

    def login(self, name: str):
        """
        Logging in using user`s name. If name do not exist in database,
        creating user with that name.

        Args:
            name (str): String value representing player`s name.

        Returns:
            None.
        """
        if not name:
            info_manager = InfoManager()
            info_manager.login_info()
        else:
            with user_manager as manager:
                player = manager.get_or_create_player(name)
                self.manager.app.player = player
                self.manager.switch_screen('main')
