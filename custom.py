# custom_button.py
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize
from asyncio import Event

# styles
widget_style = ("""
    QPushButton {
        padding: 0px;
        spacing: 10px;
        border: none;  
    }
""")


search_button = ("""
        QPushButton {
            border: none;  /* Remove button border */
            padding: 0;    /* Remove padding */
        }
    """)

# Custom button class


class XButton(QPushButton):
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


class SearchButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setFixedSize(20, 20)
        self.setStyleSheet(search_button)

        pixmap = QPixmap("16px-Magnifying_glass_icon.svg.png")
        icon_size = QSize(20, 20)
        scaled_pixmap = pixmap.scaled(icon_size)
        icon = QIcon(scaled_pixmap)
        self.setIcon(icon)
        self.setIconSize(icon_size)
    # Overide hover event

    def enterEvent(self, a0: Event) -> None:
        self.setCursor(Qt.CursorShape.PointingHandCursor)
