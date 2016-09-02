import datetime
import hashlib
import json
from collections import OrderedDict

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
        items = (
            ('time', self.time.strftime('%Y-%m-%d %H:%M:%S.%f')),
            ('mid', self.mid),
            ('event_type', self.event_type),
            ('content_type', self.content_type),
            ('text', self.text)
        )
        return json.dumps(OrderedDict(items), ensure_ascii=False)

def check_into_criteria(time):
    t = datetime.datetime.fromtimestamp(time / 1000.0)
    if t > start_time and t < end_time:

        return True
    return False

start_time = datetime.datetime(2016, 8, 19, 13, 22)
end_time = datetime.datetime(2016, 8, 23, 23, 59)

file = open('linebot.log', 'r', encoding='UTF-8')
entries = []
previous_time = datetime.datetime.fromtimestamp(1472637363.976)

while True:
    line = file.readline()
    if not line:
        break
    j = json.loads(line)['result']
    t = j[-1]['content'].get('createdTime') if j[-1]['content'].get('createdTime') else j[-1]['createdTime']
    t = datetime.datetime.fromtimestamp(t / 1000.0)
    if t >= previous_time:
        continue

    for _ in reversed(j):
        if not check_into_criteria(_['createdTime']):
            continue
        entries.append(LogEntry(_['content'].get('from') if _['content'].get('from') else _['content']['params'][0],
                                _['content'].get('createdTime') if _['content'].get('createdTime') else _['createdTime'],
                                _['content'].get('text'),
                                _['content'].get('contentType'),
                                _['eventType']))
    if entries:
        previous_time = entries[-1].time

with open('output.log', 'w', encoding='UTF-8') as out:
    for _ in reversed(entries):
        out.write(_.output() + '\n')
file.close()