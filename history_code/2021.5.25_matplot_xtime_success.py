import traceback

import serial
import serial.tools.list_ports

from threading import Thread

import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer, QDateTime
from PyQt5 import uic
from PyQt5.uic import loadUi

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import matplotlib.dates as mdate
import matplotlib.pyplot as plt


import pandas as pd

import numpy as np
import array
import sqlite3

import time

from PyQt5.QtWidgets import QTableWidgetItem

import gatt


plot_i = 0
ptr1 = 0
time_index_min = 0
time_index_max = 0

class COM:
    """读取端口信息，连接端口，关闭端口"""
    def __init__(self):
        self.serial_com = []  # 初始化端口列表
        self.ser = None  # 端口对象初始化

    def get_serial_com(self):
        """获取端口设备名，并添加到端口列表中"""
        port_list = list(serial.tools.list_ports.comports())

        if len(port_list) == 0:
            print('无可用串口')

        else:
            for i in range(0, len(port_list)):
                print(port_list[i])
                self.serial_com.append('%s' % (port_list[i]))

    def set_com(self, com_label):
        """将传入的端口名取COMx，并设置波特率，创建端口实例"""
        com = com_label[0:10]
        port = com
        print(port)
        bps = 115200
        timex = 1
        self.ser = serial.Serial("%s" % port, bps, timeout=timex)
        if self.ser.isOpen():
            print("open serial:%s success" % com)
        else:
            print("open serial:%s failed" % com)

    def close(self):
        """关闭端口"""
        if self.ser is not None and self.ser.isOpen():
            self.ser.close()
            if self.ser.isOpen():
                print("close serial failed")
            else:
                print("close serial success")


# class MatplotlibWidget(QMainWindow):
#
#     def __init__(self):
#         QMainWindow.__init__(self)
#         loadUi("qt_designer.ui", self)
#         self.setWindowTitle("PyQt5 & Matplotlib Example GUI")
#         self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))
#
#     def update_graph(self):
#         fs = 500
#         f = random.randint(1, 100)
#         ts = 1 / fs
#         length_of_signal = 100
#         t = np.linspace(0, 1, length_of_signal)
#
#         cosinus_signal = np.cos(2 * np.pi * f * t)
#         sinus_signal = np.sin(2 * np.pi * f * t)
#
#         self.MplWidget.canvas.axes1.clear()
#         self.MplWidget.canvas.axes1.plot(t, cosinus_signal)
#         self.MplWidget.canvas.axes1.plot(t, sinus_signal)
#         self.MplWidget.canvas.axes1.legend(('cosinus', 'sinus'), loc='upper right')
#         self.MplWidget.canvas.axes1.set_title(' Cosinus - Sinus Signal')
#         self.MplWidget.canvas.draw()

class MainWindow:
    def __init__(self):
        self.roll_i = 0
        self.insert_i = 0
        self.ui = uic.loadUi('2021.5.25_MainWindow_matplotlib.ui')  # 动态读取ui文件
        self.com = COM()  # 创建COM实例
        self.com.get_serial_com()  # 获取端口信息

        self.ui_init()

    def ui_init(self):
        self.ui.comboBox.addItems(self.com.serial_com)  # 将获得的端口信息添加到下拉菜单。
        self.ui.confirmButton.clicked.connect(self.init_serial)  # 点击确认按钮，绑定端口
        self.ui.sendTextEdit.textChanged.connect(self.send_func)  # 输入回车则发送数据
        self.ui.tabWidget.currentChanged.connect(self.show_table)
        # self.ui.tab_2.changeEvent(self.show_table())
        self.ui.tableWidget.setHorizontalHeaderLabels(["ID", "时间", "温度", "心率"])
        self.ui.tableWidget.setColumnWidth(1, 150)  # 设置第2列宽度

        self.init_plot()


    def init_serial(self):
        com_label = self.ui.comboBox.currentText()  # 读取下拉菜单此时显示的字符串
        self.ui.label_tip.setText(com_label)  # 设置label_tip的文本，用于确认
        self.com.set_com(com_label)  # 连接端口
        self.timer_start()

    def send_func(self):
        send_str = self.ui.sendTextEdit.toPlainText()
        if "\n" in send_str:
            self.com.ser.write(('%s' % send_str).encode('utf-8'))  # 如果有换行符，则发送数据
            self.ui.sendTextEdit.clear()  # 清空输入框

    def timer_start(self):
        self.timer = QTimer()
        self.timer.start(10)
        self.timer.timeout.connect(self.insert_data)

    def thread_get(self):
        conn = sqlite3.connect('recv_data.db')
        print("Opened database successfully")
        c = conn.cursor()
        try:
            c.execute('''CREATE TABLE  if not exists DATA
                    (ID INT PRIMARY KEY NOT NULL,
                    TIME TEXT NOT NULL,
                    TEMPERATURE FLOAT NOT NULL,
                    HEART_RATE INTEGER NOT NULL);''')
            print("Table created/opened successfully")
        except :
            print("Create/opened table failed")
            return False
        conn.commit()
        conn.close()
        self.show_table()

    def insert_data(self):
        cur_time = self.showTime()
        # self.show_table()
        if self.com.ser.in_waiting:
            try:
                result = self.com.ser.read(self.com.ser.in_waiting).decode('utf-8')  # 读取得到的数据
                temperature = result[0:5]
                heart_rate = result[5:7]
                conn = sqlite3.connect('recv_data.db')  # 打开数据库
                c = conn.cursor()  # 创建光标
                c.execute("SELECT COUNT(*) FROM DATA")  # 获取DATA表中的行数
                num = c.fetchall()  # 显示得到的结果，显示类似于[(x,)],所以读取时[0][0]
                # print(num[0][0])
                # print(self.i, self.showTime(), result)
                self.insert_i = num[0][0]
                c.execute("INSERT INTO DATA(ID,TIME,TEMPERATURE,HEART_RATE)\
                        VALUES(?,?,?,?)", (self.insert_i, cur_time, temperature, heart_rate))
                self.insert_i += 1
                conn.commit()
                conn.close()
                self.ui.recv_textBrowser.insertPlainText(cur_time + "    温度：%s" % temperature + "    心率：%s\n" % heart_rate)  # 显示数据到窗口
                self.ui.recv_textBrowser.ensureCursorVisible()  # 滚动屏幕到最新

                self.draw_plot(temperature_array, heart_rate_array, cur_time[-8:], temperature, heart_rate)
                # print(temperature_array)
            except Exception as e:
                print(traceback.print_exc())

    def showTime(self):
        # 获取系统当前时间
        current_time = QDateTime.currentDateTime()
        # 设置系统时间的显示格式
        timeDisplay = current_time.toString('yyyy-MM-dd hh:mm:ss')
        # 在标签上显示时间
        self.ui.label_tip.setText(timeDisplay)
        return timeDisplay

    def show_table(self):
        """从sqlite中读取数据，然后显示"""
        conn = sqlite3.connect('recv_data.db')
        c = conn.cursor()
        cursor = c.execute("SELECT id,time,temperature,heart_rate from DATA")

        for row in cursor:
            if (row[0] > self.roll_i) or (self.roll_i == 0 and row[0] == 0):
                table_id = row[0]
                table_time = row[1]
                table_temperature = row[2]
                table_heart_rate = row[3]
                self.insert_data_to_table(table_id, table_time, table_temperature, table_heart_rate)
                self.roll_i = table_id  # 令roll_i参数等于最新数据的id，跳出for循环后，roll_i为最大值，用于判断
                # print("ID = ", table_id)
                # print("TIME = ", table_time)
                # print("TEMPERATURE = ", table_temperature)
                # print("RATE = ", table_heart_rate)
        conn.close()

    def insert_data_to_table(self, row, table_time, table_temperature, table_heart_rate):
        """插入数据到ui的表格中"""
        self.ui.tableWidget.insertRow(row)
        self.ui.tableWidget.setItem(row, 0, QTableWidgetItem(str(row)))
        self.ui.tableWidget.setItem(row, 1, QTableWidgetItem(table_time))
        self.ui.tableWidget.setItem(row, 2, QTableWidgetItem(str(table_temperature)))
        self.ui.tableWidget.setItem(row, 3, QTableWidgetItem(str(table_heart_rate)))

    def init_plot(self):
        p = self.ui.mplwidget.canvas
        # p.showGrid(x=True, y=True)  # 把X和Y的表格打开
        # p.setRange(yRange=[34, 40], padding=0)
        # p.setLabel(axis='left', text='体温 / ℃')  # 靠左
        # p.setLabel(axis='bottom', text='时间')
        # p.setBackground('w')
        # p.setTitle('体温实时折线图', color='008080', size='12pt')  # 表格的名字
        p.axes1.set_title("体温/心率实时折线图", fontsize=12)

    def update_Data(self, array1, array2, cur_time, data1, data2):
        global plot_i, ptr1, time_index_min, time_index_max  # time_index用于横坐标
        ptr1 += 1
        if plot_i < historyLength:
            array1.append(float(data1))
            array2.append(float(data2))
            plot_i = plot_i + 1
            time_array.append(cur_time)

        else:
            array1.pop(0)
            array1.append(float(data1))
            array2.pop(0)
            array2.append(float(data2))
            time_array.pop(0)
            time_array.append(cur_time)


    def draw_plot(self, plot_array1, plot_array2, cur_time, data1, data2):
        """绘制曲线"""
        p = self.ui.mplwidget.canvas  # 画布
        self.update_Data(plot_array1, plot_array2, cur_time, data1, data2)
        self.draw_canvas(p.axes1, plot_array1, "体温", "时间", "温度", 35, 40)
        self.draw_canvas(p.axes2, plot_array2, "心率", "时间", "心率", 0, 200)

        p.draw()




    def draw_canvas(self, axes, plot_array, title, x_label, y_label, y_lim_min, y_lim_max):
        axes.clear()
        # nozero_plot_array = plot_array.ravel()[np.flatnonzero(plot_array)]  # 提取出非零元素
        axes.plot(time_array,plot_array, ":ob", label=title)  # pg.mkPen线条颜色
        axes.legend(loc="upper right")  # 标签位置
        axes.set_title(title + "实时折线图", fontsize=12)
        axes.set_xlabel(x_label, fontsize=10)
        axes.set_ylabel(y_label, fontsize=10)
        axes.set_ylim(y_lim_min, y_lim_max)  # 设置y轴范围
        axes.set_xlim(0, 20)
        axes.set_adjustable('box')
        # axes.set_autoscale_on('b')  # 设置自动缩放
        # axes.set_adjustable()  # 边框调整
        # axes.xaxis.set_major_formatter(mdate.DateFormatter('%H:%M:%S'))  # 设置时间标签显示格式
        # axes.xticks(time_array[0], time_array[plot_i], pd.date_range(freq='1s'))
        # axes.set_xticks(time_array)
        for label in axes.xaxis.get_ticklabels():
            label.set_rotation(45)
        # matplotlib.rcParams['font.sans-serif'] = ['KaiTi']

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    historyLength = 20

    temperature_array = []
    heart_rate_array = []
    time_array = []

    main_window = MainWindow()

    thread_get = Thread(target=main_window.thread_get)
    thread_get.start()


    main_window.ui.show()
    app.exec_()
    main_window.com.close()
