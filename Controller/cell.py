import random

from kivymd.uix.button import MDFlatButton
from kivy.metrics import dp

from Controller.settings import CELL_COUNT, NUMBER_OF_MINES
from View.Manager.info_manager import InfoManager
from Model.user_manager import user_manager


class Cell(object):
    """Cell class for creating base cell object containing mine, if decided by random function."""
    _instances = []
    cell_count = CELL_COUNT
    mine_count = NUMBER_OF_MINES

    def __init__(self, x, y, is_mine=False):
        self.x, self.y = x, y
        self.is_mine = is_mine
        self.is_open = False
        self.cell_object = None
        Cell._instances.append(self)

    def __repr__(self):
        return f'Cell({self.x}, {self.y})'

    def __bool__(self):
        return self.is_mine

    @property
    def neighbour_mines(self):
        return sum(bool(cell) for cell in self.neighbour_cells)

    @property
    def neighbour_cells(self):
        surrounded_cells = [
            self.get_cell(self.x - 10, self.y - 10),
            self.get_cell(self.x - 10, self.y),
            self.get_cell(self.x - 10, self.y + 10),
            self.get_cell(self.x, self.y - 10),
            self.get_cell(self.x, self.y + 10),
            self.get_cell(self.x + 10, self.y - 10),
            self.get_cell(self.x + 10, self.y),
            self.get_cell(self.x + 10, self.y + 10),
        ]
        return [cell for cell in surrounded_cells if cell is not None]

    @staticmethod
    def randomize_mines():
        for cell in random.sample(Cell._instances, NUMBER_OF_MINES):
            cell.is_mine = True

    @classmethod
    def shuffle_mines(cls):
        for instance in cls._instances:
            instance.is_mine = False
            instance.is_open = False
            instance.cell_object.text = ''
            instance.cell_object.disabled = False
        cls.randomize_mines()

    def create_button(self, position):
        btn = MDFlatButton(pos=position, on_press=self.open_cell,
                           on_release=self.refresh_label, line_color=(.5, .5, .5, .5), font_size=dp(16))
        self.cell_object = btn

    def open_cell(self, widget):
        main_screen = widget.parent.parent.parent
        if main_screen.mine_flag:
            self.mark_mine(widget)
        elif self.is_mine:
            widget.text = 'MINE'
            self.game_over(main_screen.manager.app)
        else:
            if self.neighbour_mines == 0:
                for cell in self.neighbour_cells:
                    cell.show_cell()
            self.show_cell()

    def refresh_label(self, widget):
        main_screen = widget.parent.parent.parent
        cell_label = main_screen.ids.cell_counter
        cell_label.text = f'Cells left: {self.cell_count}'
        mine_label = main_screen.ids.mine_counter
        mine_label.text = f'Mines left: {self.mine_count}'
        if Cell.cell_count == NUMBER_OF_MINES:
            InfoManager().win_info()
            with user_manager as manager:
                manager.record_win(main_screen.manager.app.player)

    def get_cell(self, x, y):
        for cell in self._instances:
            if cell.x == x and cell.y == y:
                return cell

    def show_cell(self):
        if not self.is_open:
            Cell.cell_count -= 1
            self.cell_object.text = str(self.neighbour_mines)
        self.is_open = True
        self.cell_object.disabled = True

    def mark_mine(self, widget):
        if not self.cell_object.text:
            Cell.mine_count -= 1
            self.cell_object.text = '*'
            widget.parent.parent.parent.mine_flag = False

    def game_over(self, app):
        info_manager = InfoManager()
        info_manager.game_over_info()
        with user_manager as manager:
            manager.record_loss(app.player)
