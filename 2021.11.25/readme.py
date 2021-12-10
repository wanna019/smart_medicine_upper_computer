"""
目前实现的功能:
将蓝牙设备扫描到后，名字显示在下拉栏，选中后点击确定建立连接
"""


"""
计划：
1. 建立连接后，读取serves和channal，并在窗口中显示选项（解决）
2. 实时接受数据，并显示到另一个子窗口(解决）
3. 将接收到的数据解码为人可读的数据(解决)
4. 将监听绑定部分代码简化，且可以根据设备不同自定变更绑定的uuid。
5. 连接状态添加到ui界面显示（可以使用flag操作）
6. 添加数据发送功能。（解决）
7. 调试Bug.
"""

"""
目前存在的BUG：
1. 蓝牙设备发送数据间隔1秒，但是接收数据频率很奇怪，一秒能接收好几次数据。(flag_value_change=True  #存在一个问题：每次值出现变化都会置1,导致不同characteristic都会唤醒，频繁变化。)
2. 程序部分位置运行效率过低，程序运行有明显卡顿
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
3. 将数据通过树状图形式显示在ui上，实时更新
"""


"""
2021.7.5:
1. 实现了数据发送功能。
2. 解决了ui连接状态显示延迟问题（使用       QtWidgets.qApp.processEvents()      函数，强制更新GUI）
3. 尝试修复读取数据时间不稳定的Bug,通过增加Flag等都没有达到效果（notify触发机制有点奇怪，没有弄明白），现将数据存储数据库和绘图的数据强制每秒读取一次。
"""