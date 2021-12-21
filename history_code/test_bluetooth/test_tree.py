from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer, QDateTime
from PyQt5 import uic
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QBrush, QColor
from PyQt5.QtCore import Qt


class MainWindow:
    def __init__(self):

        self.ui = uic.loadUi('/home/book/Documents/plot_project/2021.7.2(2)/2021.7.1_MainWindow_matplotlib.ui')  # 动态读取ui文件

        self.ui.tableWidget.setHorizontalHeaderLabels(["ID", "时间", "温度", "心率"])
        self.ui.tableWidget.setColumnWidth(1, 150)  # 设置第2列宽度
        self.set_treeWidget()
    def set_treeWidget(self):
        self.tree=self.ui.treeWidget
        self.tree.setColumnCount(2)
        # 设置树形控件头部的标题
        self.tree.setHeaderLabels(['Key', 'Value'])

        root = QTreeWidgetItem(self.tree)
        root.setText(0, 'Root')

        brush_red = QBrush(Qt.red)
        root.setBackground(0, brush_red)
        brush_blue = QBrush(Qt.blue)
        root.setBackground(1, brush_blue)
        self.tree.setColumnWidth(0, 150)

        # 设置子节点1
        child1 = QTreeWidgetItem(root)
        child1.setText(0, 'child1')
        child1.setText(1, 'ios')

        child1.setCheckState(0, Qt.Checked)

        child2 = QTreeWidgetItem(root)
        child2.setText(0, 'child2')
        child2.setText(1, '')



        child3 = QTreeWidgetItem(child2)
        child3.setText(0, 'child3')
        child3.setText(1, 'android')

        # 加载根节点的所有属性与子控件
        self.tree.addTopLevelItem(root)

        self.tree.clicked.connect(self.onClicked)

        # 节点全部展开
        self.tree.expandAll()


    def onClicked(self, qmodeLindex):
        item = self.tree.currentItem()
        print('Key=%s,value=%s' % (item.text(0), item.text(1)))
        self.tree.clear() # 删除所有节点



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)


    main_window = MainWindow()





    main_window.ui.show()
    app.exec_()