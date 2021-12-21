"""
目前实现的功能:
将蓝牙设备扫描到后，名字显示在下拉栏，选中后点击确定建立连接
"""


"""
计划：
1. 建立连接后，读取serves和channal，并在窗口中显示选项
2. 实时接受数据，并显示到另一个子窗口(解决）
3. 将接收到的数据解码为人可读的数据(解决)
"""


"""
2021.7.1：
1.添加了重新扫描按钮，手动刷新解决以解决设备扫描不到后下拉列表中设备仍为删除的问题
2.实现了实时读取
3.解决了读取到的数据解码后乱码的问题（读取到的数据会自动变成ascii码的形式，起初板子发送数据时发送的是数字，gatt库中读取时会转化为bytes的格式
                                bytes()在转化数字时会之间变成ascii码的序号，比如1转化成0x01，导致decode解码时出现错误，出现乱码，
                                板子发送时发送字符即直接发送ascii码即解决了该问题）
4.添加了断开连接按钮

"""

"""
2021.7.2:
1. 将Service、Characteristic存储到字典中
2. 通过位读取获得心率数据

"""