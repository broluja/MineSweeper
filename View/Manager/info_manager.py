from kivymd.uix.dialog import MDDialog


class InfoManager(MDDialog):
    """Information delivering manager (Pop-Up messages)"""
    title = 'Info Manager'
    type = 'custom'

    def __init__(self, **kwargs):
        super(InfoManager, self).__init__(**kwargs)

    def login_info(self):
        self.text = 'Please, enter your name.'
        self.open()

    def game_over_info(self):
        self.text = 'You stepped on mine. Game Over!'
        self.open()

# TODO Implement MDDialog on GameOver and on WinnGame situations
