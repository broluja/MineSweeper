from kivymd.uix.screen import MDScreen


class LoginScreenView(MDScreen):

    def login(self, name):
        self.manager.app.player = name
        self.manager.switch_screen('main')

    def on_leave(self, *args):
        self.ids.name_field.text = ''
