from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHeaderView
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class ResultsWindow(QDialog):
    def __init__(self, item_details):
        super().__init__()
        print(item_details)
        self.setWindowTitle("Results")
        self.setGeometry(100, 100, 800, 600)

        self.item_details = item_details

        self.layout = QVBoxLayout()

        self.table_widget = QTableWidget()
        self.table_widget.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #ccc;
            }
            QTableWidget QHeaderView {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
            }
            QTableWidget QHeaderView::section {
                font-weight: bold;
                padding: 5px;
            }
            QTableWidget::item {
                padding: 5px;
            }
        """)
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(
            ["Title", "Price", "Sold", "Price Change"])
        # Set width of the title column (index 0) to stretch and take available space
        self.table_widget.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Stretch)
        self.populate_table()

        self.layout.addWidget(self.table_widget)

        self.canvas = FigureCanvas(Figure(figsize=(5, 4)))
        self.plot_graph()

        self.layout.addWidget(self.canvas)

        self.setLayout(self.layout)

    def populate_table(self):

        self.table_widget.setRowCount(len(self.item_details['results']))
        for row, result in enumerate(self.item_details['results']):
            title_item = QTableWidgetItem(result['title'])
            price_item = QTableWidgetItem(result['price'])
            sold_item = QTableWidgetItem(result['sold'])
            # Default to an empty list if 'price_change' key is not present
            price_change_list = result.get('price_change', [])
            if price_change_list:
                # Get the first price change dictionary, if available
                first_price_change = price_change_list[0]
                # Get the 'change' value, default to empty string if key not present
                change = first_price_change.get('change', 'NONE')
                # Get the 'amount' value, default to 0.0 if key not present
                amount = first_price_change.get('amount', 0.0)
            else:
                change = 'NONE'
                amount = 0.0

            # Create a QTableWidgetItem for the 'change' value
            change_item = QTableWidgetItem(
                str(change))  # Convert change to string

            self.table_widget.setItem(row, 0, title_item)
            self.table_widget.setItem(row, 1, price_item)
            self.table_widget.setItem(row, 2, sold_item)
            # Set the QTableWidgetItem for 'change'
            self.table_widget.setItem(row, 3, change_item)

    def plot_graph(self):
        ax = self.canvas.figure.add_subplot(111)
        prices = [result['price'] for result in self.item_details['results']]
        ax.plot(prices)
        ax.set_xlabel('Time')
        ax.set_ylabel('Price')
        ax.set_title('Price History')
        self.canvas.draw()
