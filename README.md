

# 进度

- [x] # 1.调用QTimer出现Bug

**问题查找：**

debug发现问题出在语句`timer.timeout.connect(self.insert_data())`，前两个周期运行正常，在程序经过`app.exec_()`后会出现错误。因为释放了对象，再次运行到这时，self指向None,于是报错。

**解决方法：**

![image-20210510223911063](C:/Users/Administrator/AppData/Roaming/Typora/typora-user-images/image-20210510223911063.png)

将timer改成self.timer即可。猜测不加self则局部变量会自动清空。

- [x] # 2.数据库中表格创建问题


在创建成功一次表格后，后续每次运行程序都会执行创建表格语句，但是由于表格已经存在，故报错

**解决方法：**

```python
try:
    c.execute('''CREATE TABLE if not exists DATA
            (ID INT PRIMARY KEY NOT NULL,
            TIME TEXT NOT NULL,
            TEMPERATURE FLOAT NOT NULL);''')
    print("Table created successfully")
except :
    print("Create table failed")
    return False
```

创建时添加if not exists

- [ ] # 3.重复点确认按钮会闪退


错误代码`Process finished with exit code -1073740791 (0xC0000409)`





- [x] # 4.sqlite3插入变量问题

方法：

```python
c.execute("INSERT INTO DATA(ID,TIME,TEMPERATURE)\
        VALUES(?,?,?)", (self.i, self.showTime(), result))
```



- [x] # **5.表格内有内容的情况下，怎么不覆盖老数据存储新数据。**

- [ ] ```python
  c.execute("SELECT COUNT(*) FROM DATA")
  num =c.fetchall()
  print(num[0][0])
  self.i = num[0][0]
  ```

  使用SELECT COUNT(*) FROM DATA可以读取出DATA表中的行数

  fetchall显示读取结果，读取到的结果为一个列表中存储的元组，所以num[0] [0]即可读取出行数。

- [ ] 

  

- [x] # **6.ui上的表格数据插入问题，插入数据类型错误**

  ![image-20210511110745319](C:/Users/Administrator/AppData/Roaming/Typora/typora-user-images/image-20210511110745319.png)

  解决方法：

  ```python
  from PyQt5.QtWidgets import QTableWidgetItem
  self.ui.tableWidget.setItem(table_id, 0, QTableWidgetItem(str(table_id)))
  
  ```

  tableWidget.setItem的第一个和第二个参数表示的是坐标（行、列），第三个参数需要为QTableWidgetItem对象，使用QTableWidgetItem（）,参数设置为需要传入的数据即可。且其种的参数需要为str格式。

- [x] # 7.数据插入表格会不停循环插入重复数据，怎么让同一数据只调用一次。

  ```python
  for row in cursor:
      if row[0] > self.roll_i or (self.roll_i == 0 and row[0] == 0):
          table_id = row[0]
          table_time = row[1]
          table_temperature = row[2]
          self.ui.tableWidget.insertRow(table_id)
          self.ui.tableWidget.setItem(row[0], 0, QTableWidgetItem(str(table_id)))
          self.ui.tableWidget.setItem(row[0], 1, QTableWidgetItem(table_time))
          self.ui.tableWidget.setItem(row[0], 2, QTableWidgetItem(str(table_temperature)))
          self.roll_i = table_id  # 令roll_i参数等于最新数据的id，跳出for循环后，roll_i为最大值，用于判断
  ```

  曾江一个全局变量roll_i，每次进入循环时判断读取的数据中的id是否大于roll_i，同时在循环中实时更新roll_i，则可防止数据重复调用。

- [x] # 8.表格显示异常，列名消失，并且新的行插入为空

  解决方法：qtdesigner中tableWidget表格处的<img src="C:/Users/Administrator/AppData/Roaming/Typora/typora-user-images/image-20210511170450964.png" alt="image-20210511170450964" style="zoom: 50%;" />被删掉了，导致出错。修改回来以后正常。

- [x] # 9.plot图横坐标无法修改成时间字符

  

- [x] # 10.折线图刷新后会残留历史波形。

  每次绘制新点前执行plot.clear()清空画板。

- [ ] # 11.每过几秒就会丢失一秒的数据，猜测是此时在中断中导致发送过来的数据没有处理而丢失。

  （暂时解决）串口调试工具改为单条发送，问题消失。

  未找到是调试工具的问题还是程序的问题。

- [x] # 12.pyqtgraph无法使用时间轴横坐标，注意到matplot可以，尝试使用matplot取代pygraph嵌入到pyqt.

- [ ] ## 12.1寻找matplot嵌入pyqt方法

- [ ] 解决

- [ ] ### 12.1.1新问题：嵌入后的matplot使用方法与原matplot不同，很多命令无法使用，如何将命令同步或者找到嵌入后的模块的操作方法？

- [ ] # 13.

# 2021.5.11

准备将接收到的数据添加进sqlite3表格中，并在ui界面显示出来。

ui显示表格成功。

串口调试增加心率数据，尝试添加心率数据。

心率数据增加成功。

可实时显示折线图。

**文件：**

 [2021.5.12.1906_sqlite_table_plot.py](2021.5.12.1906_sqlite_table_plot.py) 

 [MainWindow.ui](MainWindow.ui) 

# 2021.5.24

**已实现功能：**

实现matplot替换pyqtgraph

替换后matplot的命令使用存在问题，嵌入qt的模块操作方法与直接使用Matplot不同。

**文件：**

 [2021.5.24.1931_matplotlib_notime.py](2021.5.24.1931_matplotlib_notime.py) 

 [MainWindow_matplotlib.ui](MainWindow_matplotlib.ui) 

**后续工作任务：**

目前使用的方法：[使用Qt Designer 结合pyqt5与matplotlib_qq_26844337的博客-CSDN博客](https://blog.csdn.net/qq_26844337/article/details/107258318?utm_medium=distribute.pc_relevant.none-task-blog-2~default~BlogCommendFromBaidu~default-4.control&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2~default~BlogCommendFromBaidu~default-4.control)

  - [ ] 完善matplot，找到matplot嵌入qt后的操作方法

    1. 目前找的参考网站：[官网文档：user_interfaces example code: embedding_in_qt5.py — Matplotlib 2.0.2 documentation](https://matplotlib.org/2.0.2/examples/user_interfaces/embedding_in_qt5.html)

       [在PyQt5设计的GUI界面中显示matplotlib绘制的图形_panrenlong的博客-CSDN博客](https://blog.csdn.net/panrenlong/article/details/80183519)		

       [Matplotlib pyplot嵌入PYQT5的实战与反思_Carl.Cloud的博客-CSDN博客](https://blog.csdn.net/qq_31809257/article/details/89292824)

       [使用matplotlib绘制折线图，柱状图，柱线混合图_小胖_@的博客-CSDN博客_matplotlib绘制折线图](https://blog.csdn.net/weixin_45459224/article/details/100177163?ops_request_misc=%7B%22request%5Fid%22%3A%22162184049516780261978232%22%2C%22scm%22%3A%2220140713.130102334.pc%5Fall.%22%7D&request_id=162184049516780261978232&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_v2~hot_rank-6-100177163.first_rank_v2_pc_rank_v29&utm_term=matplotlib&spm=1018.2226.3001.4187)

       英文博客：[Building a Matplotlib GUI with Qt Designer: Part 1 – Ryan's Ramblings (rcnelson.com)](http://blog.rcnelson.com/building-a-matplotlib-gui-with-qt-designer-part-1/)

    2. 针对Axes属性设置的参考信息（[subplots, subplot, axes的参数和属性_韭浪的博客-CSDN博客](https://blog.csdn.net/weixin_43326122/article/details/107402205)）

  - [x] 将横坐标修改为滚动时间（现在的想法是在更新数据的函数中，添加一个存储时间信息的数组，将数组的首尾作为横坐标的范围

    [Matplotlib绘图双纵坐标轴设置及控制设置时间格式 - 推酷 (tuicool.com)](https://www.tuicool.com/articles/jmQzUzy)

    [matplotlib画X轴时间的显示问题_ZengHaihong的博客-CSDN博客](https://blog.csdn.net/zenghaihong/article/details/70747247)

    图形边框调整：[使用Python matplotlib绘制股票走势图 -解道Jdon](https://www.jdon.com/idea/matplotlib.html)

    ）

  - [x] 增加心率折线

  - [ ] 将串口通信方式修改为蓝牙方式（[Python之蓝牙通信模块pybluez学习笔记_zhouyuming_hbxt的博客-CSDN博客_pybluez](https://blog.csdn.net/zym326975/article/details/93897096?ops_request_misc=%7B%22request%5Fid%22%3A%22162183411616780269811217%22%2C%22scm%22%3A%2220140713.130102334.pc%5Fall.%22%7D&request_id=162183411616780269811217&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_v2~hot_rank-4-93897096.first_rank_v2_pc_rank_v29&utm_term=python蓝牙通信&spm=1018.2226.3001.4187)）

       


``` python
# ------------------------------------------------- -----
# -------------------- mplwidget.py --------------------
# -------------------------------------------------- ----
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
import matplotlib
import matplotlib.pyplot as plt

class MplWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.canvas = FigureCanvas(Figure(figsize=(4, 3)))

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)

        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.setLayout(vertical_layout)
        matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
```







# 2021.5.25

## **进展：**

1. 增加了心率图

2. 尝试提取数据数组中的非零元素用于绘图

3. 淘汰了之前列表的使用方式，改用append和pop。（灵感来源：[[Python\]用matplotlib画以时间日期为x轴的图像_祥的专栏-CSDN博客_matplotlib 日期](https://blog.csdn.net/humanking7/article/details/80802435?utm_medium=distribute.pc_relevant.none-task-blog-2~default~BlogCommendFromBaidu~default-3.control&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2~default~BlogCommendFromBaidu~default-3.control)）

## **文件：**

[2021.5.25_matplot_xtime_success.py](2021.5.25_matplot_xtime_success.py)

[2021.5.25_mplwidget(使用时删掉括号及时间).py](2021.5.25_mplwidget(使用时删掉括号及时间).py)

[2021.5.25_MainWindow_matplotlib.ui](2021.5.25_MainWindow_matplotlib.ui) 

## **问题：**

 1. - [ ] 程序运行速度变慢，接收数据时间变长，导致数据丢失

 2. - [x] 提取非零元素后出现错误

      `G:\Python\Python39\lib\site-packages\matplotlib\backends\backend_agg.py:203: RuntimeWarning: Glyph 8722 missing from current font.
       font.set_text(s, 0, flags=flags)`

     + 设置x轴范围后错误消失`axes.set_xlim(0, 100)`

     + 提取非零元素方法：

       ``` python
       plot_array.ravel()[np.flatnonzero(plot_array)]
       ```

       np.flatnonzero(c)可提取出c的展平状态下的非零元素的索引

       c.ravel()可以使用非零元素的索引作为索引数组来提取这些元素

       参考网址：[python库numpy使用技巧（一）——提取数组中非零元素_一只黍离-CSDN博客](https://blog.csdn.net/weixin_42201701/article/details/86387088)

 3. - [x] 横坐标暂时只能设置静态时间，不能改变为动态时间

     + 列表操作方式使用append和pop，创建列表时为[]，绘图数据添加到列表时用浮点型，x轴坐标添加时使用字符串。
      + 绘图是plot(x,y)同时传入横纵坐标的列表

## 后续工作任务：

1. 串口修改为蓝牙

2. 寻找修改两子图距离的方法

   1. python子图位置调整API，但是只适用于plt，如何在嵌入后的axes中使用？

      ``` python
      subplots_adjust(left=None, bottom=None, right=None, top=None,wspace=None, hspace=None)
      # 参数说明：
      top、bottom、left、right：整个图距离上下左右边框的距离
      wspace、hspace：这个才是调整各个子图之间的间距
      wspace：调整子图之间的横向间距
      hspace：调整子图之间纵向间距
      ```

3. 

## 参考网址：

### 用到了：

[python库numpy使用技巧（一）——提取数组中非零元素_一只黍离-CSDN博客](https://blog.csdn.net/weixin_42201701/article/details/86387088)

[Python列表（“数组”）操作_罗思洋的博客-CSDN博客_python 数组](https://blog.csdn.net/lsylsy726/article/details/82899571)

### 可能会用到：

#### 子图间距调整:

[python 作图中的图标题title 和坐标轴标签的axes的调整_lishangyin88的博客-CSDN博客](https://blog.csdn.net/lishangyin88/article/details/80287712?ops_request_misc=%7B%22request%5Fid%22%3A%22162193018716780271520740%22%2C%22scm%22%3A%2220140713.130102334.pc%5Fall.%22%7D&request_id=162193018716780271520740&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_v2~rank_v29-2-80287712.first_rank_v2_pc_rank_v29&utm_term=axes距离调整&spm=1018.2226.3001.4187)

[python子图之间的距离_python数据可视化学习笔记_weixin_39938522的博客-CSDN博客](https://blog.csdn.net/weixin_39938522/article/details/112206575?ops_request_misc=%7B%22request%5Fid%22%3A%22162193018716780271520740%22%2C%22scm%22%3A%2220140713.130102334.pc%5Fall.%22%7D&request_id=162193018716780271520740&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_v2~rank_v29-4-112206575.first_rank_v2_pc_rank_v29&utm_term=axes距离调整&spm=1018.2226.3001.4187)

#### x轴间隔显示：

[python matplotlib 设置x轴文本间隔显示（数字的话可以转为字符之后处理） - 猪突猛进！！！ - 博客园 (cnblogs.com)](https://www.cnblogs.com/z1141000271/p/11628079.html)

[Python设置matplotlib.plot的坐标轴刻度间隔以及刻度范围_Elvirangel的博客-CSDN博客_plt 刻度间隔](https://blog.csdn.net/Elvirangel/article/details/104560484?utm_medium=distribute.pc_relevant.none-task-blog-baidujs_title-1&spm=1001.2101.3001.4242)

[matplotlib绘图-设置横坐标为日期显示范围与间隔_hanling1216的博客-CSDN博客](https://blog.csdn.net/hanling1216/article/details/84964884)

# 2021.5.28

## 进度：

暂时解决子图间距离问题，将子图坐标设置为3行1列，分别在1、3行绘图。

### 解决方法：

``` python
#mplwidget.py
self.canvas.axes1 = self.canvas.figure.add_subplot(311)
self.canvas.axes2 = self.canvas.figure.add_subplot(313)
```

![image-20210528212447923](C:/Users/Administrator/AppData/Roaming/Typora/typora-user-images/image-20210528212447923.png)



## **参考网址**

官方的axes操作网址：[matplotlib.axes — Matplotlib 3.4.2 documentation](https://matplotlib.org/stable/api/axes_api.html)



([matplotlib.axes.Axes.set_axes_locator — Matplotlib 3.4.2 documentation](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.set_axes_locator.html#matplotlib.axes.Axes.set_axes_locator)、

[HBoxDivider demo — Matplotlib 3.4.2 documentation](https://matplotlib.org/stable/gallery/axes_grid1/demo_axes_hbox_divider.html#sphx-glr-gallery-axes-grid1-demo-axes-hbox-divider-py))感觉这个页面例程可以参考，关于分配子图间距离

`matplotlib.axes.Axes.set_axes_locator`

[matplotlib使用GridSpec调整子图位置大小 （非对称的子图） - Arkenstone - 博客园 (cnblogs.com)](https://www.cnblogs.com/arkenstone/p/6872079.html)这是matplotlib的修改子图位置方法，参考



# 2021.5.31

## 任务：

通讯方式由串口修改为蓝牙



步骤：

 1. 安装pybluez  ： cmd中`pip install pybluez`

 2. 搜索蓝牙设备

    ``` python
    #!/usr/bin/env python
    # --*--coding=utf-8--*--
    # pip install pybluez
    
    import time
    from bluetooth import *
    
    #列表，用于存放已搜索过的蓝牙名称
    alreadyFound = []
    
    #搜索蓝牙
    def findDevs():
        foundDevs = discover_devices(lookup_names=True)
        # 循环遍历,如果在列表中存在的就不打印
        for (addr,name) in foundDevs:
            if addr not in alreadyFound:
                print("[*]蓝牙设备:" + str(name))
                print("[+]蓝牙MAC:" + str(addr))
                # 新增的设备mac地址定到列表中,用于循环搜索时过滤已打印的设备
                alreadyFound.append(addr)
    
    # 循环执行,每5秒执行一次
    while True:
        findDevs()
        time.sleep(5)
    ```

    **常用的Api**

    - 获取蓝牙设备列表

    ```text
    import bluetooth
    devices = bluetooth.discover_devices(lookup_names=True)
    print(devices)
    ```

    返回数据为元组类型的列表，元组包含蓝牙名称和蓝牙mac地址:

    ![img](https://pic1.zhimg.com/80/v2-d0d9390aeac0d3b4f1104d5560aec6d4_720w.png)

    - 获取本机蓝牙addrs地址（pybluez==0.23）

    ```python
    import bluetooth
    print("本机蓝牙MAC地址:",bluetooth.read_local_bdaddr())
    ```



## 遇到的问题：

1. 安装pybluez模块后，调用find_service报错

   解决方法：安装python3.5版本，并安装pybluez==0.22

   参考网址：[ Pybluez Win10系统安装教程（蓝牙通信模块pybluez，Python完美安装）_caigen0001的专栏-CSDN博客](https://blog.csdn.net/caigen0001/article/details/110877401?utm_medium=distribute.pc_relevant.none-task-blog-2~default~BlogCommendFromMachineLearnPai2~default-11.control&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2~default~BlogCommendFromMachineLearnPai2~default-11.control)

   [Python:安装蓝牙依赖_Jcsim~-CSDN博客](https://blog.csdn.net/weixin_38676276/article/details/113027104?ops_request_misc=%7B%22request%5Fid%22%3A%22162245761516780271539770%22%2C%22scm%22%3A%2220140713.130102334.pc%5Fall.%22%7D&request_id=162245761516780271539770&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_v2~times_rank-6-113027104.first_rank_v2_pc_rank_v29&utm_term=pybluez+0.22&spm=1018.2226.3001.4187)

   

蓝牙测试部分目前有效代码：

``` python
import bluetooth
import sys
import time
name='Wanna Mi 10'#需连接的设备名字
nearby_devices = bluetooth.discover_devices(lookup_names=True)
print(nearby_devices)#附近所有可连的蓝牙设备


addr=None
for device in nearby_devices:
    if name==device[1]:
        addr = device[0]
        print("device found!",name," address is: ",addr)
        break
if addr==None:
    print("device not exist")
services = bluetooth.find_service(address=addr)
print(services)

for svc in services:
    print("Service Name: %s"    % svc["name"])
    print("    Host:        %s" % svc["host"])
    print("    Description: %s" % svc["description"])
    print("    Provided By: %s" % svc["provider"])
    print("    Protocol:    %s" % svc["protocol"])
    print("    channel/PSM: %s" % svc["port"])
    print("    svc classes: %s "% svc["service-classes"])
    print("    profiles:    %s "% svc["profiles"])
    print("    service id:  %s "% svc["service-id"])	#打印蓝牙设备的各种属性

sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
'''sock.connect((addr, 2))
print("连接成功，端口：")'''
i=0
while i<255:
    try:
        sock.connect((addr, i))
        print("连接成功，端口：",i)
        break
    except Exception as e:
        print("端口：",i,"连接失败",e)
        i=i+1							#遍历端口号，进行连接


```



2. 通信出现问题，connect后无法发送数据
3. server_socket.bind(("",1))报错:OSError: 以一种访问权限不允许的方式做了一个访问套接字的尝试。



## 参考网址：

[PyBluez — PyBluez master documentation](https://pybluez.readthedocs.io/en/latest/index.html)

[python实现蓝牙通信_python学习者的博客-CSDN博客_python蓝牙通信](https://blog.csdn.net/sinat_38682860/article/details/104019844?utm_medium=distribute.pc_relevant.none-task-blog-2~default~BlogCommendFromBaidu~default-6.control&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2~default~BlogCommendFromBaidu~default-6.control)

[ Python学习笔记之蓝牙模块通讯-Pybluez_悲丶落的博客-CSDN博客_pybluez](https://blog.csdn.net/weixin_50396804/article/details/109823229?utm_medium=distribute.pc_relevant_t0.none-task-blog-2~default~BlogCommendFromMachineLearnPai2~default-1.control&depth_1-utm_source=distribute.pc_relevant_t0.none-task-blog-2~default~BlogCommendFromMachineLearnPai2~default-1.control)

[Python之蓝牙通信模块pybluez学习笔记_zhouyuming_hbxt的博客-CSDN博客_pybluez](https://blog.csdn.net/zym326975/article/details/93897096?ops_request_misc=%7B%22request%5Fid%22%3A%22162245148116780269839249%22%2C%22scm%22%3A%2220140713.130102334..%22%7D&request_id=162245148116780269839249&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_positive~default-1-93897096.first_rank_v2_pc_rank_v29&utm_term=python+蓝牙&spm=1018.2226.3001.4187)



暂时没有用到：[windows -python3.7-pybluez蓝牙通信记录_biao169的博客-CSDN博客](https://blog.csdn.net/tjb132/article/details/109687068?ops_request_misc=%7B%22request%5Fid%22%3A%22160740955019724839551584%22%2C%22scm%22%3A%2220140713.130102334.pc%5Fall.%22%7D&request_id=160740955019724839551584&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_v2~rank_v29-6-109687068.first_rank_v2_pc_rank_v29&utm_term=pybluez win10&spm=1018.2118.3001.4449)



目前用到的例程：[Python学习笔记之蓝牙模块通讯-Pybluez_悲丶落的博客-CSDN博客_pybluez](https://blog.csdn.net/weixin_50396804/article/details/109823229?ops_request_misc=%7B%22request%5Fid%22%3A%22160740955019724839551584%22%2C%22scm%22%3A%2220140713.130102334.pc%5Fall.%22%7D&request_id=160740955019724839551584&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_v2~rank_v29-5-109823229.first_rank_v2_pc_rank_v29&utm_term=pybluez win10&spm=1018.2118.3001.4449)



树莓派程序：[树莓派3B使用板载蓝牙与手机蓝牙进行Socket通信(RFCOMM) - JerryZone](https://www.jerryzone.cn/raspi-bluetooth-socket/)





# 2021.6.1

## 进度：

寻找蓝牙通信方法，无进展。



## 参考：

Linux上python进行蓝牙通信：[(5条消息) Linux(RaspberryPi)上通过Python进行蓝牙BLE通信_小小屁孩007-CSDN博客](https://blog.csdn.net/qq_33433070/article/details/78671210?ops_request_misc=%7B%22request%5Fid%22%3A%22162254742716780264061319%22%2C%22scm%22%3A%2220140713.130102334.pc%5Fblog.%22%7D&request_id=162254742716780264061319&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~blog~first_rank_v2~rank_v29-19-78671210.pc_v2_rank_blog_default&utm_term=pythpn+蓝牙通信&spm=1018.2226.3001.4450)



# 2021.6.2

## 进度：

1. 蓝牙通信测试成功。（主要参考网址：[蓝牙开发快速入门 - 疯人院主任 - 博客园 (cnblogs.com)](https://www.cnblogs.com/erhuabushuo/p/10197463.html)）
2. 将蓝牙代码加入到了项目中，并将串口替换成功。
3. 注意：bluepy只有linux系统上可以用，win不能用，今天为了安装bluepy花的时间太久，最后发现windows不能用。



## 存在的问题：

1. 蓝牙部分的知识点依然不够明确
2. 断开连接后重新连接如何让代码重新回到发送数据
3. uuid概念依然不清晰（目前理解：由地址确定蓝牙设备，uuid作为功能需求（[关于蓝牙服务对应的UUID码_随手记两笔-CSDN博客](https://blog.csdn.net/u013749540/article/details/88043770?utm_medium=distribute.pc_relevant_bbs_down.none-task-blog-baidujs-2.nonecase&depth_1-utm_source=distribute.pc_relevant_bbs_down.none-task-blog-baidujs-2.nonecase)））

## 后续计划：

1. 弄明白蓝牙部分的代码
2. 调试完善程序功能
3. 修改ui界面
4. 弄明白uuid



# 2021.6.7

## 进度：



# 2021.6.8

进度：



遇到的问题：

调用`from bluetooth.ble import DiscoveryService`显示无gattlib模块，安装出现问题。

发现gattlib仅支持linux。

先准备在Linux上重新安装pybluez0.22

linux安装环境：

​			`sudo apt-get install build-essential libssl-dev libffi-dev python3-dev`

`sudo apt-get install libzbar-dev libzbar0`

失败

# 2021.6.21

尝试使用gatt蓝牙库[【Bluetooth LE】Python3实现基于bluez进行BLE设备的扫描，连接和控制_zhuo_lee_new的博客-CSDN博客](https://blog.csdn.net/zhuo_lee_new/article/details/108649169)

[【Bluetooth LE】Bluez中Bluetoothctl指令详解（连接iPhone为例）_zhuo_lee_new的博客-CSDN博客](https://blog.csdn.net/zhuo_lee_new/article/details/106626680)

linux打开蓝牙：`systemctl start bluetooth `

10:36依然无法扫描到LE设备，参考[Bluetooth LE scan as non root? - Unix & Linux Stack Exchange](https://unix.stackexchange.com/questions/96106/bluetooth-le-scan-as-non-root)可能是电脑蓝牙硬件不支持，但是win系统蓝牙可以看到板子的蓝牙，继续查找原因。

10:52[Bug #1290173 “'hcitool lescan' fails with 'Set scan parameters f...” : Bugs : Linux Mint (launchpad.net)](https://bugs.launchpad.net/linuxmint/+bug/1290173)蓝牙硬件过时，不支持BLE模式，所以lescan命令失败。

[如何判断蓝牙是否支持BLE低功耗外围角色-百度经验 (baidu.com)](https://jingyan.baidu.com/article/ceb9fb10e7eacacdad2ba0cc.html)![image-20210621105423036](C:/Users/Administrator/AppData/Roaming/Typora/typora-user-images/image-20210621105423036.png)

确定是电脑蓝牙不支持低功耗设备。



14:00 使用gatt:[【Bluetooth LE】Python3实现基于bluez进行BLE设备的扫描，连接和控制_zhuo_lee_new的博客-CSDN博客](https://blog.csdn.net/zhuo_lee_new/article/details/108649169)



16:40 试用蓝牙适配器后可以搜到板子蓝牙信号，准备购买蓝牙适配器后继续修改。

命令行搜索低功耗蓝牙：`hcitool lescan`

命令行查看蓝牙信息：`hciconfig -a`

[Linux(RaspberryPi)上使用BLE低功耗蓝牙_小小屁孩007-CSDN博客](https://blog.csdn.net/qq_33433070/article/details/78668105)

python使用BLE方法：[【Bluetooth LE】Python3实现基于bluez进行BLE设备的扫描，连接和控制_zhuo_lee_new的博客-CSDN博客](https://blog.csdn.net/zhuo_lee_new/article/details/108649169)

[【Bluetooth LE】Bluez中Bluetoothctl指令详解（连接iPhone为例）_zhuo_lee_new的博客-CSDN博客](https://blog.csdn.net/zhuo_lee_new/article/details/106626680)

Python调用hcitool方法：[(17条消息) Python使用hcitool实现低功耗蓝牙设备搜索详解_SpeculateCat-CSDN博客](https://blog.csdn.net/weixin_37272286/article/details/115760653?ops_request_misc=%7B%22request%5Fid%22%3A%22162424324816780264098068%22%2C%22scm%22%3A%2220140713.130102334.pc%5Fall.%22%7D&request_id=162424324816780264098068&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_v2~rank_v29-9-115760653.first_rank_v2_pc_rank_v29&utm_term=linux+低功耗蓝牙&spm=1018.2226.3001.4187)

# 2021.6.24



# 2021.6.25

实现了python通过gatt搜索板子并读数据（目前只读了第一次数据，没有实现同步）

准备将蓝牙部分代码移到上位机代码中，整合后继续调试

整合进度：

1. 将蓝牙代码放进了data_display中，功能还未添加进上位机，且原本的com数据接收方式未完全删除

2. 将扫描到的设备名称显示到comboBox中（按确认键）
3. 暂未实现设备断开连接后列表中删除元素。



整合计划：

1. 实时显示扫描到的设备到下拉菜单
2. 确认键的功能修改为建立连接
3. 建立连接后实时接收数据显示到文本框
4. 添加实现设备断开连接后列表中删除元素。



# 2021.12.17

1.监听部分代码修改为所有通道监听（暂未增加监听成功、失败的返回函数）
2.发现代码中的数据库、图像显示和树状图标签运行出现问题，需要修复。

# 2021.12.18

1. 修复了部分BUG：
    1. 上位机树状图部分所有通道可更新
    2. 波形图与数据库可重新显示
2. 接下来需要解决的问题：
    1. 接收数据处理问题（从接受到的数据中提取正确信息）
    2. 数据如何实时显示不丢帧（实时接收？实时波形？）
    3. 传感器数据接收还原。
    4. 数据库部分如果删掉数据库后插入数据（创建新的数据库）是否正常还需要检查

# 2021.12.19

1. 修复gatt包的内容缺少了descriptors的问题(已解决从Github复制源码对gatt内的代码进行了替换，但是无法读取descriptors的具体数值。)
2. 规范了接收到的数据格式
3. 下阶段任务：
   1. 优化波形显示逻辑
   2. 上一阶段所需解决问题仍未解决部分继续解决
   3. 传感器数据接收还原
   
### 接收到的数据格式
|   drm_data[i]   |  表示意思    |
| ---- | ---- |
|0|flags|
|1|heart_rate|
|2|heart_rate>>8|
|3|rr_val+10|
|4|0x01|
|5|rr_val+5|
|6|0x01|
|7|rr_val|
|8|0x01|


# 2021.12.20
### 完成
1. 修改时间毫秒级显示
2. 优化了下拉菜单逻辑
### bug
1. 板子增加数据传输频率后，断开连接按钮失灵
2. 板子设置频率为50Hz，但是数据接收仅3Hz（可能是板载蓝牙发送数据的频率问题，后续发送数据形式会变成每过一段时间发送一段数据，到时再处理后续部分）
3. 连接成功后上位机运行肉眼可见变卡
### 下一步计划
1. 优化运行速度

### 小笔记
#### 获取毫秒级时间戳
以下部分参考https://www.jb51.net/article/210276.htm
```python
import time
import datetime
  
t = time.time()
  
print (t)                       #原始时间数据
print (int(t))                  #秒级时间戳
print (int(round(t * 1000)))    #毫秒级时间戳
print (int(round(t * 1000000))) #微秒级时间戳
```
#### 获取当前日期时间
```python
dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
dt_ms = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f') # 含微秒的日期时间，来源 比特量化
print(dt)
print(dt_ms)
```
#### QT获取毫秒级时间
```python
 # 获取系统当前时间
        current_time = QDateTime.currentDateTime()
        # 设置系统时间的显示格式
        timeDisplay = current_time.toString('yyyy-MM-dd ddd hh:mm:ss.zzz')
```
显示格式为：年-月-日 周几 时:分:秒.毫秒


# 2021.12.21
### 修改部分
1. 添加了蓝牙部分属性为只读的通道的读参数功能。
### 下一步计划
1. 尝试修改讲数据画图方式由matplotlib转变为pyqtgraph，将在下一个版本中进行修改


# 2021.12.22
创建新的conda环境
遇到的问题：
1. No module named 'dbus'，解决方法：`conda install dbus-python`
2. No module named 'gi',解决方法：

# 2021.12.23
放弃配置新环境，conda环境问题太多
### 当前进展
1. 初步完成pyqtgraph与matplotlib的替换
### 出现的问题
1. pyqtgraph部分待完善，包括显示方式、横纵轴等等
2. 蓝牙接收数据出现重复的情况，会多次接收同一个数据。
### 下一步计划
1. 完善pyqtgraph
2. 完善数据接收问题









# 知识点（2021.6.2起）

## 参考网址汇总：

### Pybluez

官方文档：[PyBluez — PyBluez master documentation](https://pybluez.readthedocs.io/en/latest/index.html)

蓝牙开发教程（可用）：[蓝牙开发快速入门 - 疯人院主任 - 博客园 (cnblogs.com)](https://www.cnblogs.com/erhuabushuo/p/10197463.html)

### 格式转换

[python字符串/Bytes/16进制/x01等之间的转换_代码改变世界-CSDN博客](https://blog.csdn.net/weixin_42135087/article/details/105968066)



## UUID

[蓝牙 UUID 解释_jiangchao3392的专栏-CSDN博客_蓝牙uuid](https://blog.csdn.net/jiangchao3392/article/details/90213465?utm_medium=distribute.pc_relevant_download.none-task-blog-2~default~BlogCommendFromBaidu~default-1.nonecase&depth_1-utm_source=distribute.pc_relevant_download.none-task-blog-2~default~BlogCommendFromBaidu~default-1.nonecas)：

### 一，什么是 UUID

 UUID 可以简单理解为编号，唯一的编号，用于区分不同的个体。服务和特性都有各自的UUID。比如经典的9527。UUID 就跟身份证一样，不管是你是局长还是科长，人人都有身份证。

![img](https://img-blog.csdnimg.cn/20190514193649643.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2ppYW5nY2hhbzMzOTI=,size_16,color_FFFFFF,t_70)

这里的 Read, Notify，Write_Without_Response为该Characteristic UUID所具有的属性

### 二、 服务（Service） UUID

​    服务（Service）可以理解为组长，一个组里面至少有一个或多个特性（Characteristic），特性（Characteristic）可以理解为组员。不同的服务（Service）应该有不同的编号(UUID)，用以区分不同的服务(Service)。     我是重案组总督察黄启发, 这里已经被包围了, 限你三分钟之内投降，这里的黄Sir就是组长，组长一般是不干活的，真正干活的是组员（特性），比如谈判专家、拆弹专家和飞虎队。

### 三，特性（Characteristic）UUID

特性（Characteristic）是依附于某个服务（Service）的，可以理解为组员，每个组员至少要有一个编号（UUID）以及一个或多个属性（Property）每个特性（Characteristic）可以同时有一个或多个属性。 就比如 119 不光可以救火，像忘带钥匙打不开门，工头不发工资站到楼顶上想不开等等119都可以帮忙，这就是混合属性， 当然了，“Fire inthe hole”人家119 不管。

### 四，属性（Property）

  属性的概念非常好理解，在此不多阐述，只是简单描述一下，借用古诗一首：文能提笔安天下，武能上马定乾坤，上炕认识媳妇，下炕认识鞋。

常用的属性有如下几个，我们以手机和蓝牙模块进行通讯来举栗说明：

Read： 读属性，具有该属性的UUID 是可读的，也就是说这个属性允许手机来读取一些信息。手机可以发送这个指令来读取某个具有读属性UUID的信息，华茂的模块在读取的时候，会返回模块的蓝牙地址。

Notify： 通知属性， 具有该属性的 UUID是可以发送通知的，也就是说具有这个属性的特性（Characteristic）可以主动发送信息给手机。举个栗子，华茂蓝牙模块发送数据给手机，就是通过这个属性。

Write： 写属性， 具体该属性的 UUID 是可以接收写入数据的。通常手机发送数据给蓝模块就是通过这个属性完成的。这个属性在Write 完成后，会发送写入完成结果给手机，然后手机再可以写入下一包，这个属性在写入一包数据后，需要等待应用层返回写入结果，速度比较慢。

WriteWithout Response：写属性，从字面意思上看，只是写，不需要返回写的结果，这个属性的特点是不需要应用层返回，完全依靠协议层完成，速度快，但是写入速度超过协议处理速度的时候，会丢包。华茂的蓝牙模块，Read（读）和Notify（通知）是固定的属性，不能移除和修改，您可以根据需要配置Write（写）的属性。

看到这里，相信在这篇文章开始处列出的华茂模块的UUID 信息就一目了然了，扛把子（服务）是0xFFE0, 小弟只有一个（特性）是0xFFE1，小弟（特性）0xFFE1同时具有读、通知、不需要返回结果的写属性。顺道辟个谣，有些人认为用一个UUID 来读写会造成冲突，其实并不是这样，多个属性集合到一体是可以的，蓝牙协议是允许这么做的。

![img](https://img-blog.csdnimg.cn/20190514194353465.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2ppYW5nY2hhbzMzOTI=,size_16,color_FFFFFF,t_70)

蓝牙广播中对服务 UUID 格式定义都有三种 16 bit UUID、32 bit UUID、128 bit UUID。

但是熟悉安卓开发的小伙伴都知道接口都 UUID 格式，fromString 时候 16bit 的 UUID 该咋办呢？

16bit 和 32bit 的 UUID 与 128bit 的值之间转换关系：

128_bit_UUID = 16_bit_UUID * 2^96 + Bluetooth_Base_UUID

128_bit_UUID = 32_bit_UUID * 2^96 + Bluetooth_Base_UUID

其中 Bluetooth_Base_UUID 定义为 00000000-0000-1000-8000-00805F9B34FB 

如果你想说这是啥呀，那我这样说你应该可以明白点：

若 16 bit UUID为xxxx，那么 128 bit UUID 为 0000xxxx-0000-1000-8000-00805F9B34FB

若 32 bit UUID为xxxxxxxx，那么 128 bit UUID 为 xxxxxxxx-0000-1000-8000-00805F9B34FB

----------------------------

## BLE

### 1.介绍

BLE是Bluetooth Low Energy的缩写，又叫蓝牙4.0，区别于蓝牙3.0和之前的技术。BLE前身是NOKIA开发的Wibree技术，主要用于实现移动智能终端与周边配件之间的持续连接，是功耗极低的短距离无线通信技术，并且有效传输距离被提升到了100米以上，同时只需要一颗纽扣电池就可以工作数年之久。BLE是在蓝牙技术的基础上发展起来的，既同于蓝牙，又区别于传统蓝牙。BLE设备分单模和双模两种，双模简称BR，商标为Bluetooth Smart Ready，单模简称BLE或者LE,商标为Bluetooth Smart。Android是在4.3后才支持BLE，这说明不是所有蓝牙手机都支持BLE，而且支持BLE的蓝牙手机一般是双模的。双模兼容传统蓝牙，可以和传统蓝牙通信，也可以和BLE通信，常用在手机上，android4.3和IOS4.0之后版本都支持BR，也就是双模设备。单模只能和BR和单模的设备通信，不能和传统蓝牙通信，由于功耗低，待机长，所以常用在手环的智能设备上。



### 2.连接流程



![img](https:////upload-images.jianshu.io/upload_images/8413594-18a9d1769a765386.png?imageMogr2/auto-orient/strip|imageView2/2/w/626/format/webp)

android的ble连接流程图                                        

### 3.什么是GATT?

GATT全称Generic Attribute Profile，中文名叫通用属性协议，它定义了services和characteristic两种东西来完成低功耗蓝牙设备之间的数据传输。它是建立在通用数据协议Attribute Protocol (ATT),之上的，ATT把services和characteristic以及相关的数据保存在一张简单的查找表中，该表使用16-bit的id作为索引。

一旦两个设备建立了连接，GATT就开始发挥作用，同时意味着GAP协议管理的广播过程结束了。但是必须要知道的是，建立GATT连接必要经过GAP协议。

最重要的事情，GATT连接是独占的，也就意味着一个BLE周边设备同时只能与一个中心设备连接。一旦周边设备与中心设备连接成功，直至连接断开，它不再对外广播自己的存在，其他的设备就无法发现该周边设备的存在了。

周边设备和中心设备要完成双方的通信只能通过建立GATT连接的方式。





![img](https:////upload-images.jianshu.io/upload_images/8413594-4cd27b410b7f5a5a.png?imageMogr2/auto-orient/strip|imageView2/2/w/1123/format/webp)

GATT图解                                        



一个ble蓝牙设备有多个包括多个Profile

一个Profile中有多个服务Service（通过服务的uuid找到对应的Service）

一个Service中有多个特征Characteristic（通过特征的uuid找到对应的Characteristic）

一个Characteristic中包括一个value和多个Descriptor（通过Descriptor的uuid找到对应的Descriptor）

### 其次 要知道一些名词：

#### 1、profile

profile可以理解为一种规范，一个标准的通信协议，它存在于从机中。蓝牙组织规定了一些标准的profile，例如 HID OVER GATT ，防丢器 ，心率计等。每个profile中会包含多个service，每个service代表从机的一种能力。

#### 2、service

service可以理解为一个服务，在ble从机中，通过有多个服务，例如电量信息服务、系统信息服务等，每个service中又包含多个characteristic特征值。每个具体的characteristic特征值才是ble通信的主题。比如当前的电量是80%，所以会通过电量的characteristic特征值存在从机的profile里，这样主机就可以通过这个characteristic来读取80%这个数据

#### 3、characteristic

characteristic特征值，ble主从机的通信均是通过characteristic来实现，可以理解为一个标签，通过这个标签可以获取或者写入想要的内容。

#### 4、UUID

UUID，统一识别码，我们刚才提到的service和characteristic，都需要一个唯一的uuid来标识

UUID的格式：00001101-0000-1000-8000-00805F9B34FB

整理一下，每个从机都会有一个叫做profile的东西存在，不管是上面的自定义的simpleprofile，还是标准的防丢器profile，他们都是由一些列service组成，然后每个service又包含了多个characteristic，主机和从机之间的通信，均是通过characteristic来实现。

**以上快速浏览一遍即可**

在开发中我们需要获取设备的UUID字段，可以询问硬件工程师，也可以通过**蓝牙测试工具**查看service UUID 和characteristic UUID

#### 蓝牙测试工具

**工具地址：[github.com/SouthAve/bleTester ](https://link.jianshu.com?t=https://github.com/SouthAve/bleTester)**

（在Android studio编译运行即可 但需要将此项目编码格式从GBK转变为UTF-8以解决中文乱码问题）

在应用中搜索蓝牙找到：

![img](https:////upload-images.jianshu.io/upload_images/8413594-7982624e779c3b60.png?imageMogr2/auto-orient/strip|imageView2/2/w/234/format/webp)

service UUID                                         



![img](https:////upload-images.jianshu.io/upload_images/8413594-517935b39ac183e1.png?imageMogr2/auto-orient/strip|imageView2/2/w/243/format/webp)

characteristic UUID                                        

**在此强调 UUID是需要我们填写在程序里的 主要用的是service UUID 和characteristic UUID**

**一般读，写和通知的UUID 就是 characteristic UUID**

**一般我们写入数据后 设备会给我们立刻返回一个通知，所以我们需要在通知中获取数据（在这里不是用的读取数据）！**

![img](https:////upload-images.jianshu.io/upload_images/5717492-40d1e5931dd97218.png?imageMogr2/auto-orient/strip|imageView2/2/w/907/format/webp)

工作原因不能贴项目的代码，下面这个项目实现了搜索 连接 读写数据的功能，导入到项目中作为lib  需要将正确的UUID填入即可

[github.com/chaiming/BLEDemo ](https://link.jianshu.com?t=https://github.com/chaiming/BLEDemo)

在这里 BLUETOOTH_NOTIFY_D 和 UUID_NOTIFY 、 UUID_WRITE  我统一填的是 搜索到的 characteristic UUID

![img](https:////upload-images.jianshu.io/upload_images/5717492-e97d116e28af47bf.png?imageMogr2/auto-orient/strip|imageView2/2/w/490/format/webp)

​       **另外注意，连接设备前，请先关闭扫描蓝牙，否则连接成功后，再次扫描会发生阻塞，扫描不到设备。**  

作者：Mr_zhaoF1
链接：https://www.jianshu.com/p/3711cfbf7128
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

----------------------

## Bluetooth LE 设备扫描连接等

[Linux(RaspberryPi)上使用BLE低功耗蓝牙_小小屁孩007-CSDN博客](https://blog.csdn.net/qq_33433070/article/details/78668105)

[【Bluetooth LE】Python3实现基于bluez进行BLE设备的扫描，连接和控制_zhuo_lee_new的博客-CSDN博客](https://blog.csdn.net/zhuo_lee_new/article/details/108649169)

[【Bluetooth LE】Bluez中Bluetoothctl指令详解（连接iPhone为例）_zhuo_lee_new的博客-CSDN博客](https://blog.csdn.net/zhuo_lee_new/article/details/106626680)

