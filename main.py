import datetime
import hashlib
import json

content_type_dict = {
    1: 'Text',
    2: 'Image',
    3: 'Video',
    4: 'Audio',
    7: 'Location',
    8: 'Sticker',
    10: 'Contact',
}

event_type_dict = {
    '138311609000106303': 'Message',
    '138311609100106403': 'Operation',
}

class LogEntry:
    def __init__(self, mid, time, text, content_type, event_type):
        self.mid = hashlib.sha1(str.encode(mid)).hexdigest()
        self.time = datetime.datetime.fromtimestamp(time / 1000.0)
        self.text = text
        self.content_type = content_type_dict.get(content_type)
        self.event_type = event_type_dict.get(event_type)

    def output(self):
        pass

start_time = datetime.datetime(2016, 8, 19, 13, 22)
end_time = datetime.datetime(2016, 8, 23, 23, 59)

file = open('linebot.log', 'r', encoding='UTF-8')

line = file.readline()
a = json.loads(line)
print(a)
file.close()