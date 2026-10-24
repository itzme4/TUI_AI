from tui_ai.screens.WelcomeScreen import WelcomeScreen
from textual.app import App
class TUIAI(App):
    def on_mount(self):
        self.push_screen(WelcomeScreen())

