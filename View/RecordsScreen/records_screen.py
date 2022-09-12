from kivy.properties import StringProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.metrics import dp

from Model.user_manager import UserManager


class RecordsScreenView(MDScreen):
    """Records Screen"""

    def __init__(self, **kwargs):
        super(RecordsScreenView, self).__init__(**kwargs)
        self.user_manager = UserManager()
        self.data = None

    def on_enter(self, *args):
        if not self.data:
            with self.user_manager as manager:
                data = manager.get_records()
            self.data = data
            dict_comprehension = [
                {'primary_data': f'{player[0]}: Games played: {player[1]}, Games Won: {player[2]}'} for player in data
            ]
            self.recycleView.viewclass.data = self.data
            self.recycleView.data = dict_comprehension


class RecordsWidget(MDBoxLayout):
    orientation = 'vertical'
    primary_data = StringProperty("")
