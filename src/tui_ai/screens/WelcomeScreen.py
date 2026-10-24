from textual.app import App,ComposeResult
from textual.screen import Screen
from textual.widgets import Static,Input,RadioButton,RadioSet,Button,Label
from textual.containers import Container,Vertical,Horizontal,Center
from tui_ai.core.config import WELCOME_TCSS, ONBOARDING_DB
from tui_ai.screens.OnboardingScreen import OnboardingScreen
from tui_ai.screens.MainScreen import Main_screen
from tui_ai.util.file_handing import load_json
import pyfiglet
LOGO=pyfiglet.figlet_format("TUI   AI",font="big")
data=load_json(ONBOARDING_DB)
class WelcomeScreen(Screen):
    
    CSS_PATH= WELCOME_TCSS
    BINDINGS=[
        (
            "enter","next_screen","continue"
        ),
        (
            "q","quit_app","quit"
        ),
    ]
    def compose(self):
        with Container(id="welcome-outer"):
            yield Static("WELCOME TO TUI AI",id="welcome-title")
            yield Static("\u2500"*20+" \u2726 "+"\u2500"*20,id="divider")
            yield Static(
                "Developed by [bold magenta]ITZME 4[/]",
                id="dev-by",
                markup=True,
            )
            with Container(id="logo-box"):
                yield Static("[bold]\u2B24 \u2B24 \u2B24",id="dots")
                yield Static(LOGO,id="ascill-logo")
            with Container(id="desc-box"):
                yield Static(
                    "[bold magenta]\u25c6[/] TUI AI [bold magenta]\u25c6[/]"
                    "\nTextual User Interface AI[magenta]"
                    "\nOffline \u25c7 and \u25c7 online[dim]",
                    id="desc-text",
                    markup=True,
                )
            yield Static(
                "Press [bold cyan]ENTER[/] to continue "
                "Press [blue]ctrl+Q[/] to quit",
                id="footer-hint",
                markup=True,
            )
    def on_key(self,event):
        if event.key == "enter":
            if not data["setup"]:
                self.app.push_screen(OnboardingScreen())
            else:
                self.app.push_screen(Main_screen())