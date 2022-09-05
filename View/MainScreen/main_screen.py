import itertools

from kivymd.uix.screen import MDScreen
from kivy.utils import get_hex_from_color

from Controller.settings import GRID_SIZE
from Controller.cell import Cell


class MainScreenView(MDScreen):
    """Main Game Screen"""
    def on_enter(self, *args):
        for x, y in itertools.product(range(GRID_SIZE), range(GRID_SIZE)):
            c = Cell(x*10, y*10)
            c.create_button((x*10, y*20))
            self.ids.main_layout.add_widget(c.cell_object)
        Cell.randomize_mines()
        self.ids.welcome.text = f"""
        Welcome[color={get_hex_from_color(self.manager.app.theme_cls.primary_color)}]{self.manager.app.player}[/color]
        """

    def on_leave(self, *args):
        self.ids.main_layout.clear_widgets(self.ids.main_layout.children)
