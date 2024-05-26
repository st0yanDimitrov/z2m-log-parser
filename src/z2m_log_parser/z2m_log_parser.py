from datetime import datetime
import json
import os

class MqttMessage(object):
    def __init__(self):
        self.topic = str
        self.payload = json

class LogEntryData(object):
    def __init__(self):
        self.is_mqtt_publish = bool
        self.message = str
        self.mqtt_message = MqttMessage()

class LogEntry(object):
    def __init__(self):
        self.type = str
        self.date = datetime
        self.data = LogEntryData()

class Z2mLogParser:

    def parse_logs(path):
        parsed_lines = []
        with open(path) as log:
            for line in log:
                parsed_line= LogEntry()
                parsed_line.data.is_mqtt_publish
                try:
                    parsed_line.type = line[0:4]
                    parsed_line.date = datetime.strptime(line[6:25], '%Y-%m-%d %H:%M:%S')
                except:
                    try:
                        parsed_lines[-1].data.message = parsed_lines[-1].data.message + line
                    except Exception:
                        pass
                    continue
                parsed_line.data.message = line[27:]
                if parsed_line.data.message[0:12] == "MQTT publish":
                    parsed_line.data.is_mqtt_publish = True
                    parsed_line.data.mqtt_message.topic = line.split("topic")[1].rsplit(", payload")[0].strip().strip("'")
                    parsed_line.data.mqtt_message.payload = line.split("payload")[1].strip().strip("'")
                    try:
                        parsed_line.data.mqtt_message.payload = json.loads("{\"payload\":" + "\""  + line.split("payload")[1].strip().strip("'") + "\"" + "}")
                    except:
                        parsed_line.data.mqtt_message.payload = json.loads("{\"payload\":" + "\"Couldn't convert to JSON\"" + "}")
                else:
                    parsed_line.data.is_mqtt_publish = True
                    parsed_line.data.mqtt_message.topic = None
                    parsed_line.data.mqtt_message.payload = None
                parsed_lines.append(parsed_line)
        return parsed_lines
    
    def parse_latest_logs(self, path: str):
            events = self.parse_logs(path)
            pointer_file_name =  "/eventPointer.txt"
            last_event = datetime.strftime(events[(len(events))-1].date, '%Y-%m-%d %H:%M:%S')
            if not os.path.exists(pointer_file_name):
                f = open(pointer_file_name, "w")
                f.write(last_event)
                f.close()
            else:
                f = open(pointer_file_name, "r+")
                date_st = f.read()
                date_dt = datetime.strptime(date_st, '%Y-%m-%d %H:%M:%S')
                if date_st and date_dt <= events[(len(events))-1].date:
                    events = [x for x in events if x.date > date_dt]
                if events:
                    f.seek(0)
                    f.truncate()
                    f.write(last_event)
            if any(events):
                return events
            return None