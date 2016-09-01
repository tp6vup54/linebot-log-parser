import datetime
import hashlib
import json

start_time = datetime(2016, 8, 19, 13, 22)
end_time = datetime(2016, 8, 23, 23, 59)

file = open('linebot.log', 'r', encoding='UTF-8')
line = file.readline()
print(line)