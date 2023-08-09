# gui.py
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextBrowser, QPushButton, QCheckBox, QLabel, QScrollArea
from PyQt5.QtCore import Qt
import functools
from asyncio import Event
from custom import CustomButton
from favorites_handler import save_favorites_to_file, grab_favorites_from_file, search_ebay_items

# GUI Class


class MyGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set up the main window
        self.setWindowTitle("Product Manager")
        self.setGeometry(100, 100, 900, 400)

        # Create the central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create the layout for the central widget
        layout = QVBoxLayout()

        # Add the search bar at the top
        search_layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setStyleSheet("""
            QLineEdit {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
                font-size: 14px;
            }
        """)
        search_layout.addWidget(self.search_bar)

        # Add checkboxes in the middle
        # self.favorites_title = QLabel()
        # self.favorites_title.setText('Favorite Products:')

        self.favorites = grab_favorites_from_file()
        self.checkbox_layout = QVBoxLayout()
        # Apply a common stylesheet to all checkboxes
        self.widget_style = (
            "QCheckBox, QPushButton {"
            "    padding: 5px;"
            "    spacing: 10px;"
            "}"
            "QCheckBox::indicator {"
            "    width: 20px;"
            "    height: 20px;"
            "}"
            "QCheckBox::indicator:checked {"
            "    image: url(tick.png);"
            "}"
        )
        # self.checkbox_layout.addWidget(self.favorites_title)

        # Add the textarea with scroll bars
        self.scroll_area = QScrollArea()
        # Add styles to the QLabels and QScrollArea
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: #F0F0F0;
                border: 1px solid #CCCCCC;
            }
            QScrollArea QLabel {
                font-size: 14px;
                color: #333333;
            }
        """)
        self.content_widget = QWidget()
        self.scroll_area_content = QVBoxLayout()
        self.content_widget.setLayout(self.scroll_area_content)

        # Add the run and cancel buttons at the bottom
        button_layout = QHBoxLayout()
        self.run_button = QPushButton("Run")
        self.cancel_button = QPushButton("Clear")
        self.run_button.setStyleSheet("""
            QPushButton {
                padding: 10px;
                background-color: #4CAF50;
                border: none;
                color: white;
                font-size: 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.cancel_button.setStyleSheet("""
            QPushButton {
                padding: 10px;
                background-color: #f44336;
                border: none;
                color: white;
                font-size: 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        button_layout.addWidget(self.run_button)
        button_layout.addWidget(self.cancel_button)

        # Add all the layouts to the main layout
        layout.addLayout(search_layout)
        layout.addLayout(self.checkbox_layout)
        layout.addWidget(self.scroll_area)
        layout.addLayout(button_layout)

        # Set the main layout for the central widget
        central_widget.setLayout(layout)

        # Load inital saved checkboxes into GUI
        self.add_favorites_to_chkboxes(self.favorites)

        # Connect buttons to their functions
        self.run_button.clicked.connect(self.on_run_button_clicked)
        self.cancel_button.clicked.connect(self.on_cancel_button_clicked)

    # Function to clear widgets from layotus
    def remove_all_widgets(self):
        # Clear the scroll area conten
        for i in reversed(range(self.scroll_area_content.count())):
            widget = self.scroll_area_content.takeAt(i).widget()
            if widget:
                widget.deleteLater()

    def is_checkbox_in_layout(self, checkbox_layout, checkbox_to_find):
        # For each widget_layout in checkbox_layout
        for index in range(checkbox_layout.count()):
            widget_layout = checkbox_layout.itemAt(index)  # Grab the chkbox

            # Varifying the layout has two objects
            if widget_layout and widget_layout.count() == 2:
                chkbox = widget_layout.itemAt(0).widget()

                # If the chkboxes have the same text it is in layout
                if chkbox.text() == checkbox_to_find.text():
                    return True
        return False

    # Function to remove item from favorites
    def remove_favorite(self, text):
        # Go through each item in favorites
        for index in reversed(range(self.checkbox_layout.count())):
            widget_layout = self.checkbox_layout.itemAt(index)
            # Check if there are more than one object inside of this layout
            if widget_layout and widget_layout.count() == 2:
                chkbox = widget_layout.itemAt(0).widget()
                text = text.strip()
                chkbox_text = chkbox.text().strip()
                # Check if the current text matches the given text from the event
                if chkbox and chkbox_text == text:
                    popped = self.favorites.pop(index)
                    print(popped)
                    widget_layout.itemAt(0).widget().deleteLater()
                    widget_layout.itemAt(1).widget().deleteLater()
                    self.checkbox_layout.removeItem(widget_layout)

    # Function to handle when a checkbox's state changes
    def checkbox_state_changed_handler(self, state, item_to_update):
        # Find the index of the dictionary with the matching 'item'
        index_to_update = next((index for index, favorite in enumerate(
            self.favorites) if favorite['item'] == item_to_update), None)

        if index_to_update is not None:
            # Update the checked state
            self.favorites[index_to_update]['checked'] = state
            print("Checked state updated:", item_to_update)
        else:
            print("Item not found:", item_to_update)

    # Function to add checkboxes for each item in the favorites list
    def add_favorites_to_chkboxes(self, array):
        """Add items to the favorites list"""
        # Loop over each item in the array
        for dic in array:
            # Create horizontal layout for chkbox and remove button
            item = dic['item']
            checked = dic['checked']
            widget_layout = QHBoxLayout()

            # Create and add chkbox to layout
            checkbox = QCheckBox(item)
            checkbox.setChecked(checked)
            checkbox.setStyleSheet(self.widget_style)
            widget_layout.addWidget(checkbox)

            # Move the "Remove" button to the left
            widget_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
            # Create the "Remove" button with the 'remove.png' icon image
            remove_button = CustomButton()

            # Use functools.partial to capture the value of 'item'
            print(item)
            remove_button.clicked.connect(
                functools.partial(self.remove_favorite, item))
            checkbox.clicked.connect(
                lambda state, item_to_update=item: self.checkbox_state_changed_handler(state, item_to_update))
            widget_layout.addWidget(remove_button)
            self.checkbox_layout.addLayout(widget_layout)

    def add_favorite_to_ckhboxes(self, data):
        # Favorites: List of Dictonaries containtaining item: data, checked: True/False
        # Varifying the data is not already in the lust
        if data not in [favorite['item'] for favorite in self.favorites]:
            # Append Dictonary to the Favorites List
            self.favorites.append({'item': data, 'checked': False})
            # For each item in the tracker array: all the data sections from each dictonary
            for item in [favorite['item'] for favorite in self.favorites]:
                # Create horizontal layout for chkbox and remove button
                widget_layout = QHBoxLayout()

                # Create and add chkbox to layout
                checkbox = QCheckBox(item)
                checkbox.setChecked(False)
                checkbox.setStyleSheet(self.widget_style)
                widget_layout.addWidget(checkbox)

                # Move the "Remove" button to the left
                widget_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

                # Use of bool function to handle logic
                if not self.is_checkbox_in_layout(self.checkbox_layout, checkbox):
                    # If it isn't it can be added to the checkbox layout
                    # Create the "Remove" button with the 'remove.png' icon image
                    remove_button = CustomButton()
                    remove_button.setFixedSize(15, 15)

                    # Use functools.partial to capture the value of 'item'
                    remove_button.clicked.connect(
                        functools.partial(self.remove_favorite, data))
                    checkbox.clicked.connect(
                        lambda state, item_to_update=data: self.checkbox_state_changed_handler(state, item_to_update))
                    widget_layout.addWidget(remove_button)
                    self.checkbox_layout.addLayout(widget_layout)

    # Helper function for the label event click
    def label_click_handler(self, text):
        self.add_favorite_to_ckhboxes(text)

    class DataLabel(QLabel):
        # Override for mousehover event, give the cursor a pointer look
        def enterEvent(self, a0: Event) -> None:
            self.setCursor(Qt.CursorShape.PointingHandCursor)

    def on_run_button_clicked(self):
        # Function to run when the "Run" button is clicked
        print("Run button clicked")

        # Clear text area when button runs
        self.remove_all_widgets()

        # Collect Items
        soup = search_ebay_items(self.search_bar.text())

        # Extract the item titles
        item_titles = [item.get_text()
                       for item in soup.select(".s-item__title")]

        # Extract the item prices
        item_prices = [item.get_text()
                       for item in soup.select(".s-item__price")]

        # Extract the item quantity sold
        item_sold = [item.get_text()
                     for item in soup.select(".s-item__quantitySold")]

        # Print the extracted data
        for title, price, sold in zip(item_titles, item_prices, item_sold):

            # Instanciate new dataLabel
            label = self.DataLabel(f"Title: {title} | Price: {price} | {sold}")

            # Use the current text of the label as an argument for the click handler to use
            label.mousePressEvent = lambda event, text=label.text(): self.label_click_handler(text)

            # Add widget to content widget
            self.scroll_area_content.addWidget(label)

        # Set the content widget layout and update the scroll area
        self.scroll_area.setWidget(self.content_widget)

        # Set the vertical stretch factor for the layout to 1 (default is 0)
        # Optional: Set layout margins for spacing
        self.scroll_area.setContentsMargins(10, 10, 10, 10)
        self.scroll_area.setWidgetResizable(True)

    def on_cancel_button_clicked(self):
        # Function to run when the "Cancel" button is clicked
        print("Cancel button clicked")
        self.remove_all_widgets()

        # Save favorites array when closing the program
    def closeEvent(self, event):
        save_favorites_to_file(self.favorites)
        super().closeEvent(event)
