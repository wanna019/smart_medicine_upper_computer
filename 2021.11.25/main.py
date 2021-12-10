
import sys
from PyQt5 import QtWidgets
from ui import *
from BLE import *

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    # main_ui = uic.loadUi('2021.7.1_MainWindow_matplotlib.ui')
    # MainWindow(main_ui)
    # BLE_CTL()

    # main_ui.show()
    app.exec_()