from textual.screen import Screen
from textual.widgets import Static, Input
from textual import events, on, work
from textual.app import ComposeResult
from .confmscn import Confirm_Screen
from .revertpaxmodule import apiPaxFunctions
from .functionsScreen import FunctionsScreen

class Scan_qr(Screen):
    """QR SCANNER"""

    def compose(self) -> ComposeResult:
        yield Static("PlEASE SCAN QR CODE TO BEGIN", classes="question" )
        yield Input(placeholder=">>>>")
    
    @on(Input.Submitted)
    @work
    async def fix_qr(self) -> None:
        self.l = self.query_one(Input).value
        self.disabled = True
        self.serialList = eval(self.l)  # Assuming the QR code contains a list of serial numbers
        if await self.app.push_screen_wait(Confirm_Screen(f"Are these terminals you wish to activate\n{self.serialList}?")):
            self.notify("Activating>>>")

            apifun = apiPaxFunctions() 
            self.thing = await apifun.startPaxGroup(self.serialList)
            thing2 = await apifun.activateTerminals(apifun.idList)
            self.notify(str(thing2))
            self.app.push_screen(FunctionsScreen(self.thing))