"""
Function:UI界面操作
Author:HZH
Date:2021.11.25
"""
import sys
from PyQt5.QtCore import QTimer, QDateTime
from PyQt5 import uic



class MainWindow:
    def __init__(self):
        self.function_connect()
        # self.main_ui =main_ui

    def function_connect(self):
        """UI界面各块功能绑定"""
        self.connect_to_device()

    def connect_to_device(self):
        """连接到设备"""
        self.main_ui.connectButton.clicked.connect(connect_to_device_func)  # 点击连接按钮，connect





def connect_to_device_func():
    """
    Function:connect_to_device具体功能实现
    """
    main_ui.label_confim.setText("连接中")  # 设置label_tip的文本，用于确认
    print("连接中")
    QtWidgets.qApp.processEvents() #可以一边执行耗时程序，一边刷新界面的功能
    com_label = main_ui.comboBox.currentText()  # 读取下拉菜单此时显示的字符串
    addr_index = list_ble['name'].index(com_label)
    addr = list_ble["addr"][addr_index]
    connect_thread = Thread(target=self.ble.connect_device(addr))
    connect_thread.start()


# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#
#     main_ui = uic.loadUi('2021.7.1_MainWindow_matplotlib.ui')  # 动态读取ui文件
#     MainWindow()
#
#
#
#
#
#
#     main_ui.show()
#     app.exec_()