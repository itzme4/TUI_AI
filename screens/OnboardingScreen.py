from textual.app import App,ComposeResult
from textual.containers import Container,Horizontal,Vertical
from textual.widgets import Label, Static, Input,Header,Button,RadioButton,RadioSet,Footer
from textual.screen import Screen
from config import ONBOARDING_TCSS, ONBOARDING_DB
import json
with open(ONBOARDING_DB,"r") as file:
    data=json.load(file)
 
class Onboarding(Screen):
    CSS_PATH=ONBOARDING_TCSS
    TITLE="ONBOARDING"
    def compose(self):
        with Container(id="outer-box"):
            yield Header()
            yield Static("WELCOME TO TUI_RBA!",id="greeting")
            yield Static("Let's get setup",id="sub-title")
            yield Static(" ", classes="divider")
            with Container(id="form"):
                with Horizontal(classes="form-box"):
                    yield Label("AI name",classes="left-label")
                    yield Input(placeholder="Enter AI name",id="ai-name",classes="right-input")
                with Horizontal(classes="form-box"):
                    yield Label("Your Name ",classes="left-lable")
                    yield Input(placeholder="Enter your name",id="your-name",classes="right-input")
                with Horizontal(classes="form-box"):
                    yield Label("Location",classes="left-lable")
                    yield Input(placeholder="state",id="state-name",classes="right-input")
                    yield Input(placeholder="City",id="city-name",classes="right-input")
                with Horizontal(classes="form-box"):
                    yield Label("clock format",classes="left-label")
                    with RadioSet(id="clock-radio",classes="right-input"):
                        yield RadioButton("12 Hour",value=True,id="_12hr",classes="right-input")
                        yield RadioButton("24 Hour",id="_24hr",classes="right-input")
            with Container(id="footer"):
                yield Button("Continue",id="continue-btn",variant="primary")
    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id=="continue-btn":
            self._save_and_exit()
    def _save_and_exit(self):
        data["ai_name"]=self.query_one("#ai-name",Input).value
        data["user_name"]=self.query_one("#your-name",Input).value
        data["state"]=self.query_one("#state-name",Input).value
        data["city"]=self.query_one("#city-name",Input).value
        choice=self.query_one("#clock-radio",RadioSet)
        choice=choice.pressed_index
        if choice==0:
            data["time_format"]="12"
        elif choice==1:
            data["time_format"]="24"
        else:
            data["time_format"]="12"
        data["setup"]=True
        with open(ONBOARDING_DB,"w") as f:
            json.dump(data,f,indent=4)
        self.app.exit(data)