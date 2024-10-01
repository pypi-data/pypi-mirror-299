# SPDX-FileCopyrightText: 2024-present U.N. Owen <void@some.where>
#
# SPDX-License-Identifier: MIT


from textual.app import App, ComposeResult
from textual.widgets import Static, Button, Placeholder, Input, Label, TextArea, Header, Footer
from textual.screen import Screen, ModalScreen
from textual.containers import Container, Horizontal, VerticalScroll, Grid
from .confmscn import Confirm_Screen  # Assuming this is in the same directory
from textual import events, on, work
import pandas as pd
from .revertpaxmodule import *  # Assuming this is in the same directory
from .DFTable import DataFrameTable
from .ti_labels_iccid import create_pdf

from .scan_qr import Scan_qr
from .scan_serials import Scan_serials
from .functionsScreen import FunctionsScreen
from .TI_Input import Select_QR_or_Barcode

class Input_app(App):

    def on_mount(self) -> None:
         self.push_screen(Select_QR_or_Barcode())
         

if __name__ == "__main__":
    app = Input_app()
    app.run()