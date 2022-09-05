from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton


class InfoManager(MDDialog):
    """Information delivering manager (Pop-Up messages)"""
    title = 'Info Manager'
    type = 'simple'

    def __init__(self, **kwargs):
        super(InfoManager, self).__init__(**kwargs)
        self.buttons = [MDRaisedButton(text='OK'), MDRaisedButton(text='Cancel')]
   