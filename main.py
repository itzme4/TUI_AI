from screens.WelcomeScreen import WelcomeScreen
from textual.app import App
class TUIAI(App):
    def on_mount(self):
        self.push_screen(WelcomeScreen())

if __name__ == "__main__":
    TUIAI().run()

