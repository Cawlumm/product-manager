# main.py
import sys
from PyQt5.QtWidgets import QApplication
from gui import MyGUI

# Main Function
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyGUI()
    window.show()
    sys.exit(app.exec_())
