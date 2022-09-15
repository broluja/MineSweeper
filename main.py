import os
from pathlib import Path

from Controller import settings
from kivy.config import Config

Config.set("graphics", "width", f"{settings.WIDTH}")
Config.set("graphics", "height", f"{settings.HEIGHT}")

from kivymd.app import MDApp

from View.Manager.manager_screen import ManagerScreen

os.environ['MINESWEEPER'] = str(Path(__file__).parent)


class MinesweeperApp(MDApp):
    """MineSweeper Game"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'DeepOrange'
        self.manager_screen = ManagerScreen()

    def build(self):
        self.manager_screen.add_widget(self.manager_screen.create_screen('login'))
        return self.manager_screen


MinesweeperApp().run()
# TODO: Implement game levels
