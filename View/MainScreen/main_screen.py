import itertools

from kivymd.uix.screen import MDScreen
from kivy.utils import get_hex_from_color

from Controller.settings import GRID_SIZE
from Controller.cell import Cell


class MainScreenView(MDScreen):
    """Main Game Screen"""
    mine_flag = False
    table_created = False

    def on_enter(self, *args):
        """
        Creating game table if not created, calling create_table method.
        In other case just shuffle the mines positions.

        Args:
            *args: optional arguments

        Returns:
            None.
        """
        if not self.table_created:
            self.create_table()
        else:
            self.shuffle_table()
        self.ids.cell_counter.text = f'Cells left: {Cell.cell_count}'
        self.ids.mine_counter.text = f'Mines left: {Cell.mine_count}'

    def shuffle_table(self):
        """
        Shuffling mines positions.
        Returns:
            None.
        """
        Cell.shuffle_mines()
        self.ids.welcome.text = f"""
                Welcome[color={get_hex_from_color(self.manager.app.theme_cls.primary_color)}]{self.manager.app.player}[/color]
                            """

    def flag(self):
        """
        Turning on flag. Used to mark the cell as mine cell.
        Returns:
            None.
        """
        self.mine_flag = True

    def create_table(self):
        """
        Creating table method.
        Returns:
            None.
        """
        for x, y in itertools.product(range(GRID_SIZE), range(GRID_SIZE)):
            c = Cell(x * 10, y * 10)
            c.create_button((x * 10, y * 10))
            self.ids.main_layout.add_widget(c.cell_object)
        self.table_created = True
        Cell.randomize_mines()
        self.ids.welcome.text = f"""
        Welcome[color={get_hex_from_color(self.manager.app.theme_cls.primary_color)}]{self.manager.app.player}[/color]
        """

    def clear_table(self):
        """
        Clear cells on MainScreen leave.
        Returns:
            None.
        """
        for widget in self.ids.main_layout.children:
            widget.text = ''
