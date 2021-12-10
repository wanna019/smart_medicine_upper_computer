# encoding=utf8

import traceback



from threading import Thread

import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer, QDateTime
from PyQt5 import uic
from PyQt5.uic import loadUi

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import matplotlib.dates as mdate
import matplotlib.pyplot as plt



import sqlite3

import time

from PyQt5.QtWidgets import QTableWidgetItem

import gatt

import chardet



plot_i = 0
ptr1 = 0
time_index_min = 0
time_index_max = 0
local_mac_address = None
local_alias = None
list_ble = {"name": [], "addr": []}  # 显示蓝牙设备的列表
message = None
Nordic_UART_TX=None
uuid_list= {}  # 根据该字典，显示到树状图，其中存储了每一个service以及characteristic和其值。

class AnyDeviceManager(gatt.DeviceManager):

    def device_discovered(self, device):
        if str(device.mac_address)[0:2] != str(device.alias().lower())[0:2]:
            if device.mac_address not in list_ble["addr"]:
                print("Discovered [%s] %s" % (device.mac_address, device.alias()))
                list_ble["addr"].append(device.mac_address)
                list_ble["name"].append(device.alias())


class AnyDevice(gatt.Device):


    def connect_succeeded(self):
        super().connect_succeeded()
        print("[%s] Connected" % (self.mac_address))

    def connect_failed(self, error):
        super().connect_failed(error)
        print("[%s] Connection failed: %s" % (self.mac_address, str(error)))


    def disconnect_succeeded(self):
        super().disconnect_succeeded()
        print("[%s] Disconnected" % (self.mac_address))

    def services_resolved(self):
        super().services_resolved()

        print("[%s] Resolved services" % (self.mac_address))
        for service in self.services:
            print("[%s]  Service [%s]" % (self.mac_address, service.uuid))
            uuid_list[str(service.uuid)]={}
            try:
                service.descriptors
            except AttributeError:
                pass
            else:
                for descriptor in service.descriptors:
                    print(
                        "[%s]\t\t\tDescriptor [%s] (%s)" % (self.mac_address, descriptor.uuid, descriptor.read_value()))
            for characteristic in service.characteristics:
                print("[%s]    Characteristic [%s]" % (self.mac_address, characteristic.uuid))
                uuid_list[str(service.uuid)][str(characteristic.uuid)]=None
                try:
                    characteristic.descriptors
                except AttributeError:
                    pass
                else:
                    for descriptor in characteristic.descriptors:
                        print("[%s]\t\t\tDescriptor [%s] (%s)" % (self.mac_address, descriptor.uuid, descriptor.read_value()))
        print("属性输出结束")
        print(uuid_list)
        global flag_Services_resolved_success
        flag_Services_resolved_success = True

        try:
            Nordic_UART_Service = next(
                s for s in self.services
                if s.uuid == 'bbb40a00-337f-4081-9a0b-10d0f09716d3'.lower())

        except StopIteration:
            psss
        try:
            Nordic_UART_RX = next(
                c for c in Nordic_UART_Service.characteristics
                if c.uuid == 'bbb40b00-337f-4081-9a0b-10d0f09716d3'.lower())
        except StopIteration:
            pass
        try:
            global Nordic_UART_TX
            Nordic_UART_TX = next(
                c for c in Nordic_UART_Service.characteristics
                if c.uuid == 'bbb40c00-337f-4081-9a0b-10d0f09716d3'.lower())
        except StopIteration:
            pass



        Nordic_UART_RX.read_value()
        Nordic_UART_RX.enable_notifications()



        try:
            Hrate_Service = next(
                s for s in self.services
                if s.uuid == '0000180d-0000-1000-8000-00805f9b34fb'.lower())

        except StopIteration:
            pass
        try:
            Hrate_Characteristics = next(
                c for c in Hrate_Service.characteristics
                if c.uuid == '00002a37-0000-1000-8000-00805f9b34fb'.lower())
        except StopIteration:
            pass

        # Nordic_UART_RX.read_value()
        Hrate_Characteristics.enable_notifications()




    def characteristic_value_updated(self, characteristic, value):
        # # 查看变量value的转码方式
        # ret = chardet.detect(value)
        # print("enconding=",end='')
        # print(ret)
        # print("type=",end='')
        # # 查看变量的type
        # print(type(value))

        # print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        global message
        global flag_value_change
        # for keys,values in uuid_list["Hrate_Service"].items():
        #     print("Hrate_Service")
        #     print("\t\t", keys, "[%s]\n" % values)
        # print("uuid:",characteristic.uuid,"原始值: ", value)
        for Service,Characteristics in uuid_list.items():
            for Characteristic,Value in Characteristics.items():
                if Characteristic == str(characteristic.uuid):
                    uuid_list[Service][Characteristic] = value
                    # print(uuid_list[Service][Characteristic])
        # print(value[1])
        # message = value[1]

        # print("uuid:",characteristic.uuid,"\t\t\tValue：",message)
        # main_window.ui.recv_textBrowser.insertPlainText("接收到的数据: "+ message[0:10] + "\n")  # 显示数据到窗口
        main_window.ui.recv_textBrowser.ensureCursorVisible()  # 滚动屏幕到最新
        if str(characteristic.uuid) == '00002a37-0000-1000-8000-00805f9b34fb':
            flag_value_change=True  #存在一个问题：每次值出现变化都会置1,导致不同characteristic都会唤醒，频繁变化。

    def characteristic_read_value_failed(self, characteristic, error):
        print(error)

    def characteristic_write_value_succeeded(self, characteristic):
        super().characteristic_write_value_succeeded(characteristic)
        print("[%s] wr ok" % (self.mac_address))

    def characteristic_write_value_failed(self, characteristic, error):
        super().characteristic_write_value_failed(characteristic, error)
        print("[%s] wr err %s" % (self.mac_address, error))



class BLE_CTL:
    """读取端口信息，连接端口，关闭端口"""
    def __init__(self):
        self.ser = None  # 端口对象初始化
        self.ble_manager = AnyDeviceManager(adapter_name='hci0')



    def connect_device(self, addr):
        """实例化蓝牙类，建立连接。"""
        self.device = AnyDevice(manager=self.ble_manager, mac_address=addr)
        Thread(target=self.device.connect()).start()

    def disconnect_device(self):
        """断开连接。"""
        self.device.disconnect()


    def thread_ctl(self):
        self.ble_manager.start_discovery()
        self.ble_manager.run()


class MainWindow:
    def __init__(self, g_ble):
        self.roll_i = 0
        self.insert_i = 0
        self.ui = uic.loadUi('2021.7.1_MainWindow_matplotlib.ui')  # 动态读取ui文件
        self.ble = g_ble  # 创建COM实例
        self.child_list = {}  # 树状图子列名称与对象对应字典

        self.ui_init()
        self.timer_start()


    def ui_init(self):

        self.ui.connectButton.clicked.connect(self.connect_to_device)  # 点击连接按钮，connect
        self.ui.scanButton.clicked.connect(self.clear_device_list)  # 点击重新扫描按钮，清空设备列表，重新扫描
        self.ui.disconnectButton.clicked.connect(self.disconnect_to_device)  # 点击重新扫描按钮，清空设备列表，重新扫描
        self.ui.sendTextEdit.textChanged.connect(self.send_func)  # 输入回车则发送数据
        self.ui.tabWidget.currentChanged.connect(self.show_table)
        self.ui.sendTextEdit.setPlaceholderText('输入范围0-255')
        # self.ui.tab_2.changeEvent(self.show_table())
        self.ui.tableWidget.setHorizontalHeaderLabels(["ID", "时间", "温度", "心率"])
        self.ui.tableWidget.setColumnWidth(1, 150)  # 设置第2列宽度
        self.set_treeWidget()

        self.init_plot()

    def set_treeWidget(self):
        self.tree = self.ui.treeWidget
        self.tree.setColumnCount(2)
        self.tree.setHeaderLabels(['Key', 'Value'])
        self.tree.setColumnWidth(0, 150)


    def update_treeWidget(self):
        """
        更新树状图部分节点信息
        """
        global flag_Services_resolved_success
        if flag_Services_resolved_success:  # 如果读取到蓝牙设备的节点信息，设置树状图节点
            flag_Services_resolved_success = False
            self.tree.clear()
            for Service, Characteristics in uuid_list.items():
                self.root = QtWidgets.QTreeWidgetItem(self.tree)
                self.root.setText(0, str(Service))
                for Characteristic, value in Characteristics.items():
                    self.child_list[str(Characteristic)] = QtWidgets.QTreeWidgetItem(self.root)
                    child = self.child_list[str(Characteristic)]
                    child.setText(0, str(Characteristic))
                    child.setText(1, str(value))
        self.tree.expandAll()  # 展开全部节点
        if  len(self.child_list.items()):  # 如果存在子节点，向对应的子节点中存储数据。
            for Service,Characteristics in uuid_list.items():
                for Characteristic,value in Characteristics.items():
                    # print(Characteristic)
                    # print("child_list[str(Characteristic)=",self.child_list[str(Characteristic)])
                    # print("value=",value)
                    child = self.child_list[str(Characteristic)]
                    child.setText(1, str(value))




    def connect_to_device(self):
        self.ui.label_confim.setText("连接中")  # 设置label_tip的文本，用于确认
        print("连接中")

        com_label = self.ui.comboBox.currentText()  # 读取下拉菜单此时显示的字符串
        addr_index=list_ble['name'].index(com_label)
        addr=list_ble["addr"][addr_index]
        self.ble.connect_device(addr)


    def clear_device_list(self):
        list_ble["addr"].clear()
        list_ble["name"].clear()

    def disconnect_to_device(self):
        self.ble.disconnect_device()
        self.ui.label_confim.setText("连接断开")

    def update_info_to_comboBox(self):
        """update info to comboBox"""
        cur_time = self.showTime()
        comoBox_list=[]
        for i in range(self.ui.comboBox.count()):
            comoBox_list.append(self.ui.comboBox.itemText(i))
        if list_ble['name'] != comoBox_list :
            self.ui.comboBox.clear()
            self.ui.comboBox.addItems(list_ble['name'])  # 将获得的端口信息添加到下拉菜单。


    def send_func(self):
        send_str = self.ui.sendTextEdit.toPlainText()
        if "\n" in send_str:
            send_value=int(send_str[:-1])
            send_buf=[]
            send_buf.append(send_value)
            send_value=bytes(send_buf)
            if Nordic_UART_TX:
                Nordic_UART_TX.write_value(send_value)
            else:
                self.ui.sendTextEdit.setText('找不到发送接口')
            # self.com.ser.write(('%s' % send_str).encode('utf-8'))  # 如果有换行符，则发送数据
            self.ui.sendTextEdit.clear()  # 清空输入框

    def timer_start(self):
        self.timer = QTimer()
        self.timer.start(100)
        self.timer.timeout.connect(self.insert_data) #insert_data
        self.timer.timeout.connect(self.update_info_to_comboBox)
        self.timer.timeout.connect(self.update_treeWidget)


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
        global flag_value_change
        if flag_value_change:
            flag_value_change=False
            try:
                heart_rate = uuid_list['0000180d-0000-1000-8000-00805f9b34fb']['00002a37-0000-1000-8000-00805f9b34fb'][1]
                temperature = uuid_list['bbb40a00-337f-4081-9a0b-10d0f09716d3']['bbb40b00-337f-4081-9a0b-10d0f09716d3'][4:6]
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
        self.draw_canvas(p.axes1, plot_array1, "体温", "时间", "温度", 30, 40)
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
    flag_value_change = False
    flag_Services_resolved_success = False

    temperature_array = []
    heart_rate_array = []
    time_array = []

    g_ble = BLE_CTL()

    thread_ble_ctl = Thread(target=g_ble.thread_ctl)
    thread_ble_ctl.start()

    main_window = MainWindow(g_ble)

    thread_get = Thread(target=main_window.thread_get)
    thread_get.start()






    main_window.ui.show()
    app.exec_()