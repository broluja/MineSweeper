import random

from kivymd.uix.button import MDFlatButton
from kivy.metrics import dp

from Controller import settings
from View.Manager.info_manager import InfoManager
from Model.user_manager import user_manager


class Cell(object):
    """
    Cell class for creating base cell object containing mine, if decided by random function.
    """
    _instances = list()
    cell_count = settings.CELL_COUNT
    mine_count = settings.CELL_COUNT // settings.BEGINNER

    def __init__(self, x, y, is_mine=False):
        self.x, self.y = x, y
        self.is_mine = is_mine
        self.is_open = False
        self.cell_object = None
        Cell._instances.append(self)

    def __repr__(self):
        return f'{type(self).__name__}({self.x}, {self.y})'

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

    @classmethod
    def shuffle_mines(cls):
        """
        Called before start of new game to shuffle mines on table.
        Returns:
            None.
        """
        for instance in cls._instances:
            instance.is_mine = False
            instance.is_open = False
            instance.cell_object.text = ''
            instance.cell_object.disabled = False
        cls.cell_count = settings.CELL_COUNT
        cls.mine_count = settings.CELL_COUNT // settings.BEGINNER
        cls.randomize_mines()

    @classmethod
    def randomize_mines(cls):
        """
        Called to randomly select cells with mines.
        Returns:
            None.
        """
        for cell in random.sample(cls._instances, cls.mine_count):
            cell.is_mine = True

    def game_over(self, app):
        """
        Called when you step on mine.
        Args:
            app (MDApp): represents app object

        Returns:
            None: if no exceptions are raised inside context manager return None
        """
        InfoManager().game_over_info()
        with user_manager as manager:
            manager.record_loss(app.player)
        for cell in self._instances:
            cell.cell_object.disabled = True

    def create_button(self, position):
        """
        Instantiate button object and assign it to instance.cell_object.
        Args:
            position (tuple): position of the cell in grid layout.

        Returns:
            None
        """
        self.cell_object = MDFlatButton(pos=position,
                                        on_press=self.open_cell,
                                        on_release=self.refresh_label,
                                        line_color=(.5, .5, .5, .5),
                                        font_size=dp(16))

    def open_cell(self, widget):
        """
        Open cell object.
        Args:
            widget (MDFlatButton): represent button from which this function is triggered.

        Returns:
            None.
        """
        main_screen = widget.parent.parent.parent
        if main_screen.mine_flag:
            self.mark_mine(widget)
            main_screen.mine_flag = False
        elif self.is_mine:
            widget.text = 'MINE'
            self.game_over(main_screen.manager.app)
        else:
            if self.neighbour_mines == 0:
                for cell in self.neighbour_cells:
                    cell.show_cell()
            self.show_cell()

    def refresh_label(self, widget):
        """
        Refresh labels after opening cell.
        Args:
            widget (MDFlatButton): represent button from which this function is triggered.

        Returns:
            None.
        """
        main_screen = widget.parent.parent.parent
        cell_label = main_screen.ids.cell_counter
        cell_label.text = f'Cells left: {self.cell_count}'
        mine_label = main_screen.ids.mine_counter
        mine_label.text = f'Mines left: {self.mine_count}'
        if self.cell_count == settings.CELL_COUNT // settings.BEGINNER:
            InfoManager().win_info()
            with user_manager as manager:
                manager.record_win(main_screen.manager.app.player)

    def get_cell(self, x, y):
        """
        Function for retrieving a cell object based on it`s position.
        Args:
            x (int): represent x-axis in cell`s position
            y (int): represent y-axis in cell`s position

        Returns:
            Cell object.
        """
        for cell in self._instances:
            if cell.x == x and cell.y == y:
                return cell

    def show_cell(self):
        """
        Show cell info.
        Returns:
            None.
        """
        if not self.is_open:
            Cell.cell_count -= 1
            if self.cell_object.text == '*':
                Cell.mine_count += 1
            self.cell_object.text = str(self.neighbour_mines)
        self.is_open = True
        self.cell_object.disabled = True

    def mark_mine(self, widget):
        """
        Called when you want to mark a cell as a mine.
        Args:
            widget (MDFlatButton): represent button from which this function is triggered.

        Returns:
            None.
        """
        if not self.cell_object.text:
            Cell.mine_count -= 1
            self.cell_object.text = '*'
            widget.parent.parent.parent.mine_flag = False
