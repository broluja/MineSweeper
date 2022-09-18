from kivy.properties import NumericProperty
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.app import MDApp


class InfoManager(MDDialog):
    """
    Information delivering manager (Pop-Up messages).
    """
    title = 'Info'
    type = 'custom'
    _scroll_height = NumericProperty("100dp")
    _spacer_top = NumericProperty("50dp")

    def __init__(self, **kwargs):
        super(InfoManager, self).__init__(**kwargs)
        self.buttons = [
            MDFlatButton(text='New Game', font_size='25dp', on_press=self.new_game),
            MDFlatButton(text='Exit', on_press=self.exit, font_size='25dp')
        ]

    def login_info(self):
        """
        Information provided if player tries to log in without username.
        Returns:
            None.
        """
        self.text = 'Please, enter your name.'
        self.open()

    def game_over_info(self):
        """
        Information on game over, triggered when player step on mine.
        Returns:
            None.
        """
        self.create_buttons()
        self.text = 'You stepped on mine. Game Over!'
        self.open()

    def win_info(self):
        """
        Information on game win, triggered when player finishes game.
        Returns:
            None.
        """
        self.create_buttons()
        self.text = 'You won the game. Congratulations!'
        self.open()

    def exit(self, widget):
        """
        Leaving MainScreen.
        Args:
            widget (MDFlatButton): Representing button that triggered this function.

        Returns:
            None.
        """
        app = MDApp.get_running_app()
        manager = app.manager_screen
        manager.switch_screen('login')
        self.dismiss()

    def new_game(self, widget):
        """
        Triggered when player starts new game.
        Args:
            widget (MDFlatButton): Representing button that triggered this function.

        Returns:
            None.
        """
        app = MDApp.get_running_app()
        main_screen = app.manager_screen.get_screen('main')
        main_screen.shuffle_table()
        self.dismiss()
