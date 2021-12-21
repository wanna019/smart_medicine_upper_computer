# array1=[255]
#
# # array2=[50]
# array=["a","b","c",1,2]
# print(array)
# value=bytes(array)
# # print(value)
# # for i in value:
# #     i +=48
# #     print (i.decode())
#
# message=value.decode('utf-8')
# print(message)
# #########################################################################################################################
# uuid_list= {"Service":{"Hrate_Service":"0000180d-0000-1000-8000-00805f9b34fb"},"Characteristic":{}}
# for key,value in uuid_list["Service"].items():
#     print(key)
#     print(value)
#     if "0000180d-0000-1000-8000-00805f9b34fb" == value:
#         print("found key:",key)
# ##############################################################################################################################

#
# import struct

# value =b'\x14\x0c\x0b\x01\x0c\x01\r\x01\x0e\x01\x0f\x01\x10\x01\x11\x01\x12\x01\x13\x01\x14\x01\x15\x01\x16\x01\x17\x01\x18\x01\x19\x01\x1a\x01\x1b\x01\x1c\x01\x1d\x01\x1e\x01'
# print(type(value))
# print("原始值：",value)
# # str_value=value.decode('utf-8')
# str_value=str(value,encoding='utf-8')
# print(type(str_value))
# print("解码：",str_value)
# list=[]
# for values in value:
#     list.append(str(hex(values)))
#
# print(list)
####################################################################################
# uuid_list={
#             '0000180a-0000-1000-8000-00805f9b34fb':
#                 {
#                    '00002a29-0000-1000-8000-00805f9b34fb': None
#                 },
#             '0000180d-0000-1000-8000-00805f9b34fb':
#                 {'00002a38-0000-1000-8000-00805f9b34fb': None,
#                  '00002a37-0000-1000-8000-00805f9b34fb': None
#                 },
#             'bbb40a00-337f-4081-9a0b-10d0f09716d3':
#                 {'bbb40c00-337f-4081-9a0b-10d0f09716d3': None,
#                  'bbb40b00-337f-4081-9a0b-10d0f09716d3': None
#                  },
#             '00001801-0000-1000-8000-00805f9b34fb':
#                 {'00002a05-0000-1000-8000-00805f9b34fb': None
#                  }
#             }
# for Service, Characteristics in uuid_list.items():
#     for Characteristic,value in Characteristics.items():
#         uuid_list[Service][Characteristic] = 1
# print(uuid_list)

##############################################################################################
send_value=int('123')
print(send_value)
send_value=bytes([1,2])
print(send_value)