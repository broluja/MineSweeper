from kivymd.uix.screen import MDScreen

from View.Manager.info_manager import InfoManager


class LoginScreenView(MDScreen):
    def __init__(self, **kwargs):
        super(LoginScreenView, self).__init__(**kwargs)
        self.info_manager = InfoManager()

    def login(self, name):
        if not name:
            self.info_manager.login_info()
        else:
            self.manager.app.player = name
            self.manager.switch_screen('main')

    def on_leave(self, *args):
        self.ids.name_field.text = ''
