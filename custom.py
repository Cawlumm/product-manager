# custom_button.py
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize
from asyncio import Event

# Globle styles
widget_style = (
    "QCheckBox, QPushButton {"
    "    padding: 5px;"
    "    spacing: 10px;"
    "}"
)

# Custom button class


class CustomButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setFixedSize(15, 15)
        self.setStyleSheet(widget_style)

        pixmap = QPixmap("remove.png")
        icon_size = QSize(24, 24)
        scaled_pixmap = pixmap.scaled(icon_size)
        icon = QIcon(scaled_pixmap)
        self.setIcon(icon)
        self.setIconSize(icon_size)
    # Overide hover event

    def enterEvent(self, a0: Event) -> None:
        self.setCursor(Qt.CursorShape.PointingHandCursor)
