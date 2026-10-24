from textual.app import App,ComposeResult
from textual.containers import Container, Vertical, Horizontal,VerticalScroll
from textual.widgets import Input,Static,Tree,ContentSwitcher
from textual.screen import Screen
from tui_ai.AI.routing import routing
import psutil
from tui_ai.core.config import ONBOARDING_DB,MAIN_TCSS
from tui_ai.util.file_handing import dump_json,load_json
from tui_ai.util.greeting import greeting
from datetime import datetime
from tui_ai.util.check_internet import check_internet_connection
data=load_json(ONBOARDING_DB)
user_name=data["user_name"]
ai_name=data["ai_name"]
time_format=int(data["time_format"])
space=" "*40
class StatusBar(Static):
    def on_mount(self):
        self.set_interval(3,self.update_stats)
        self.update_stats()
    def update_stats(self):
        cpu=psutil.cpu_percent(interval=None)
        ram=psutil.virtual_memory()
        ram=ram.used/(1024**3)
        battery=psutil.sensors_battery()
        battery=int(battery.percent) if battery is not None else 0
        time=datetime.now()
        if time_format == 12:
            time=time.strftime("%I:%M %p")
        else:
            time=time.strftime("%H:%M %P")
        date=datetime.now()
        date=date.strftime("%d/%m/%Y")
        self.update(
            f"[#00ff88]TUI RBA[/]"
            f"{" "*27}[bold white]Cpu: {cpu}%[/]"
            f" | [bold white]Ram: {ram:.1f}[/]"
            f" | [bold white]Battery: {battery}%[/]"
            f"{space}[bold white]Time: {time}[/]"
            f" | [bold white]Date: {date}[/]"
        ) 
class QuickAccess(Static):
    def compose(self):
        with VerticalScroll():
            apps=Tree("APPS")
            apps.show_root=True
            apps.show_guides=True
            apps.root.expand()
            apps.can_focus=False
            apps.root.add_leaf("TODO",data="app:todo")
            apps.root.add_leaf("Web Search")
            apps.root.add_leaf("Weather")
            apps.root.add_leaf("Open Apps")
            yield apps
            tools=Tree("TOOLS")
            tools.show_root=True
            tools.show_guides=True
            tools.can_focus=False
            tools.root.add_leaf("Btop")
            tools.root.add_leaf("Cmatrix")
            yield tools
            files=Tree("FILES")
            files.show_root=True
            files.show_guides=True
            files.root.add_leaf("System Files")
            yield files
            commands=Tree("Commands")
            commands.show_root=True
            commands.show_guides=True
            commands.root.add_leaf("Exit")
            commands.root.add_leaf("Shutdown")
            commands.root.add_leaf("Reboot")
            yield commands
            user_info=Tree("User Info")
            user_info.show_root=True
            user_info.show_guides=True
            yield user_info
class ChatPanel(VerticalScroll):
    def on_mount(self):
        if check_internet_connection():
            self.show_output(greeting())
        else:
            self.show_output("No internet connection. Please check your network settings.")
    def show_input(self,text:str):
        input_msg=Static(f"[bold green]{user_name}[/]: {text}",classes="input-msg")
        self.mount(input_msg)
        input_msg.scroll_visible()
    def show_output(self,text):
        output_msg=Static(f"[bold cyan]{ai_name}[/]: {text}",classes="output-msg")
        self.mount(output_msg)
        output_msg.scroll_visible()
        
class Main_screen(Screen):
    CSS_PATH=MAIN_TCSS
    def compose(self):
        with Container(id="outer-box"):
            yield StatusBar()
            with Horizontal(id="main-layout"):
                with Vertical(id="left-box"):
                    yield Static("\u2500"+" [bold cyan]QUICK ACCESS [/]"+"\u2500",classes="center-text")
                    yield QuickAccess()
                with Vertical(id="right-box"):
                    yield Static("TUI RBA",id="header")
                    yield ChatPanel()
            with Horizontal(id="input-box"):
                yield Input(placeholder="Terminal Input",id="terminal-input")
                yield Input(placeholder="Input chat",id="chat-input")
    def on_key(self,event):
        if event.key=="enter":
            user_input=self.query_one("#chat-input",Input)
            chat_panel=self.query_one(ChatPanel)
            user_text=user_input.value.lower().strip()
            user_input.clear()
            chat_panel.show_input(user_text)
            response=routing(user_input=user_text)
            chat_panel.show_output(response)