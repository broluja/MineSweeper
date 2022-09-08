import random

from kivymd.uix.button import MDFlatButton
from kivy.metrics import dp

from Controller.settings import CELL_COUNT, NUMBER_OF_MINES
from View.Manager.info_manager import InfoManager


info_manager = InfoManager()


class Cell(object):
    """Base cell object containing mine, if decided by random function."""
    _instances = []
    cell_count = CELL_COUNT
    mine_count = NUMBER_OF_MINES

    def __init__(self, x, y, is_mine=False):
        self.x, self.y = x, y
        self.is_mine = is_mine
        self.is_open = False
        self.cell_object = None
        Cell._instances.append(self)
        self.info_manager = info_manager

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

    def create_button(self, position):
        btn = MDFlatButton(pos=position, on_press=self.open_cell,
                           on_release=self.refresh_label, line_color=(.5, .5, .5, .5), font_size=dp(16))
        self.cell_object = btn

    def open_cell(self, widget):
        if widget.parent.parent.parent.mine_flag:
            self.mark_mine(widget)
        elif self.is_mine:
            widget.text = 'MINE'
            self.game_over()
        else:
            if self.neighbour_mines == 0:
                for cell in self.neighbour_cells:
                    cell.show_cell()
            self.show_cell()

    def refresh_label(self, widget):
        cell_label = widget.parent.parent.parent.ids.cell_counter
        cell_label.text = f'Cells left: {self.cell_count}'
        mine_label = widget.parent.parent.parent.ids.mine_counter
        mine_label.text = f'Mines left: {self.mine_count}'
        if Cell.cell_count == NUMBER_OF_MINES:
            self.info_manager.win_info()

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

    def game_over(self):
        self.info_manager.game_over_info()
