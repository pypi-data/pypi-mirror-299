from __future__ import annotations
from PySide6.QtWidgets import QVBoxLayout, QMainWindow
from som_gui.icons import get_icon
from som_gui import tool


class ModelcheckExternalWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(get_icon())
        self.vertical_layout = QVBoxLayout(self)
        self.resize(1139, 720)
        self.setLayout(self.vertical_layout)
        self.setWindowTitle(f"Modellprüfung exportieren | {tool.Util.get_status_text()}")
