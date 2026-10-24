from textual.app import App,ComposeResult
from textual.containers import Container,Horizontal,Vertical
from textual.widgets import Label, Static, Input,Header,Button,RadioButton,RadioSet,Footer,ContentSwitcher
from textual.screen import Screen
from tui_ai.core.config import ONBOARDING_TCSS, ONBOARDING_DB, CONFIG_DB
from tui_ai.screens.MainScreen import Main_screen
from tui_ai.services.save_api_key import save_api_key
from tui_ai.util.file_handing import dump_json, load_json
data=load_json(ONBOARDING_DB)
config_data=load_json(CONFIG_DB)
class OnboardingScreen(Screen):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.mode = None
    CSS_PATH=ONBOARDING_TCSS
    TITLE="ONBOARDING"
    def compose(self):
        with Container(id="outer-box"):
            yield Header()
            yield Static("WELCOME TO TUI_RBA!",id="greeting")
            yield Static("Let's get setup",id="sub-title")
            yield Static(" ", classes="divider")
            with ContentSwitcher(initial="step1",id="form"):
                with Container(id="step1"):
                    with Horizontal(classes="form-box"):
                        yield Label("AI name",classes="left-label")
                        yield Input(placeholder="Enter AI name",id="ai-name",classes="right-input")
                    with Horizontal(classes="form-box"):
                        yield Label("Your Name ",classes="left-label")
                        yield Input(placeholder="Enter your name",id="your-name",classes="right-input")
                    with Horizontal(classes="form-box"):
                        yield Label("Location",classes="left-label")
                        yield Input(placeholder="Country",id="country",classes="right-input")
                        yield Input(placeholder="state",id="state-name",classes="right-input")
                        yield Input(placeholder="City",id="city-name",classes="right-input")
                    with Horizontal(classes="form-box"):
                        yield Label("clock format",classes="left-label")
                        with RadioSet(id="clock-radio",classes="right-input"):
                            yield RadioButton("12 Hour",value=True,id="_12hr",classes="right-input")
                            yield RadioButton("24 Hour",id="_24hr",classes="right-input")
                with Container(id="step2"):
                    yield Label("[magenta]Select below options[/]")
                    with RadioSet(id="mode",classes="right-input"):
                        yield RadioButton("Online",id="online",classes="right-input")
                        yield RadioButton("Offline",id="Offline",classes="right-input")
                        yield RadioButton("Both online and offline",id="both",classes="right-input")
                with Container(id="step3"):
                    yield Label("Online Configuration")
                    with Horizontal():
                        yield Label("Select AI provider")
                        with RadioSet(id="provider",classes="right-input"):
                            yield RadioButton("Gemini",id="gemini",classes="right-input")
                            yield RadioButton("Groq",id="groq",classes="right-input")
                    yield Label("Model name")
                    yield Input(placeholder="Enter model name Ex: (gemini-3.8,openai/gpt-oss-120b)"
                                ,id="online-model"
                                ,classes="right-input")
                    yield Label("API KEY")
                    yield Input(placeholder="Enter API KEY",id="api-key",classes="right-input")
                with Container(id="step4"):
                    yield Label("Offline Configuration")
                    with Horizontal():
                        yield Label("Select Ollama model")
                        yield Input(placeholder="Enter model name",id="ollama_model",classes="right-input")

            yield Button("Continue",id="continue-btn",variant="primary")
            yield Static("[bold cyan]TAB[/][white] to navigate between fields[/], [blue]continue[/blue][white] to next step[/], [green][ctrl+Q][/green] [white]to quit[/]",id="footer-hint")
    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id=="continue-btn":
            self._next_step()

    def _next_step(self):
        switcher=self.query_one("#form",ContentSwitcher)
        current=switcher.current
        if current == "step1":
            switcher.current="step2"
        elif current == "step2":
            pressed=self.query_one("#mode",RadioSet).pressed_button
            btn_id=pressed.id if pressed else None
            if pressed is None:
                self.notify("select any option",severity="warning")
                return
            elif btn_id in ["Offline","both"]:
                self.notify("Offline mode is not supported yet",severity="warning")
                return
            self.mode=pressed.id
            switcher.current="step4" if self.mode == "offline" else "step3"
        elif current == "step3":
            if self.mode == "both":
                switcher.current="step4"
            else:
                self._save_and_exit()
                self.app.push_screen(Main_screen())
        elif current == "step4":
            self._save_and_exit()
            self.app.push_screen(Main_screen())
    def _save_and_exit(self):
        def radio_id(selector):
            btn=self.query_one(selector,RadioSet).pressed_button
            return btn.id if btn else None
        data["ai_name"]=self.query_one("#ai-name",Input).value
        data["user_name"]=self.query_one("#your-name",Input).value
        data["country"]=self.query_one("#country",Input).value
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
        config_data["mode"]=self.mode
        config_data["provider"]=radio_id("#provider")
        provider=config_data["provider"]
        api_key=self.query_one("#api-key",Input).value
        save_api_key(provider,api_key)
        config_data["ollama_model"]=self.query_one("#ollama_model",Input).value
        dump_json(ONBOARDING_DB,data)
        dump_json(CONFIG_DB,config_data)
        self.app.exit(data)
        self.app.exit(config_data)