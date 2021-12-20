##2021.12.17
1.监听部分代码修改为所有通道监听（暂未增加监听成功、失败的返回函数）
2.发现代码中的数据库、图像显示和树状图标签运行出现问题，需要修复。

##2021.12.18
1. 修复了部分BUG：
    1. 上位机树状图部分所有通道可更新
    2. 波形图与数据库可重新显示
2. 接下来需要解决的问题：
    1. 接收数据处理问题（从接受到的数据中提取正确信息）
    2. 数据如何实时显示不丢帧（实时接收？实时波形？）
    3. 传感器数据接收还原。
    4. 数据库部分如果删掉数据库后插入数据（创建新的数据库）是否正常还需要检查


##2021.12.19
1. 修复gatt包的内容缺少了descriptors的问题(已解决从Github复制源码对gatt内的代码进行了替换，但是无法读取descriptors的具体数值。)
2. 规范了接收到的数据格式
3. 下阶段任务：
   1. 优化波形显示逻辑
   2. 上一阶段所需解决问题仍未解决部分继续解决
   3. 传感器数据接收还原
   
###接收到的数据格式
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


##2021.12.20
###完成
1. 修改时间毫秒级显示
2. 优化了下拉菜单逻辑
###bug
1. 板子增加数据传输频率后，断开连接按钮失灵
2. 板子设置频率为50Hz，但是数据接收仅3Hz（可能是板载蓝牙发送数据的频率问题，后续发送数据形式会变成每过一段时间发送一段数据，到时再处理后续部分）
3. 连接成功后上位机运行肉眼可见变卡
###下一步计划
1. 修复下拉栏更新数据后重置的bug
2. 修改ble部分，combox显示
###小笔记
####获取毫秒级时间戳
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
####获取当前日期时间
```python
dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
dt_ms = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f') # 含微秒的日期时间，来源 比特量化
print(dt)
print(dt_ms)
```
####QT获取毫秒级时间
```python
 # 获取系统当前时间
        current_time = QDateTime.currentDateTime()
        # 设置系统时间的显示格式
        timeDisplay = current_time.toString('yyyy-MM-dd ddd hh:mm:ss.zzz')
```
显示格式为：年-月-日 周几 时:分:秒.毫秒