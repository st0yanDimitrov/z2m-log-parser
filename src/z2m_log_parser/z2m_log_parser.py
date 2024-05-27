from datetime import datetime
import json
import os
import inspect

class MqttMessage(object):
    def __init__(self):
        self.topic: str = str
        self.payload: json = json

class LogEntryData(object):
    def __init__(self):
        self.is_mqtt_publish: bool = bool
        self.message: str = str
        self.mqtt_message: MqttMessage = MqttMessage()

class LogEntry(object):
    def __init__(self):
        self.type: str = str
        self.date: datetime =datetime
        self.data: LogEntryData = LogEntryData()

class Z2mLogParser:

    def __init__(self, pointer_path):
        self.pointer_path = pointer_path

    def __extract_date(self, line) -> datetime:
        date = datetime.strptime(line[6:25], '%Y-%m-%d %H:%M:%S')
        return date
    
    def __extract_type(self, line) -> str:
        type = line[0:4]
        return type

    def __extract_data_message(self, line: str) -> str:
        message = line[27:]
        return message
    
    def __extract_mqttmessage_topic(self, line: str) -> str:
        topic = line.split("topic")[1].rsplit(", payload")[0].strip().strip("'")
        return topic
    
    def __extract_mqttmessage_payload(self, line: str) -> json:
        payload = line.split("payload")[1].strip().strip("'")
        try:
            payload = json.loads("{\"payload\":" + "\""  + line.split("payload")[1].strip().strip("'") + "\"" + "}")
        except:
            payload = json.loads("{\"payload\":" + "\"Couldn't convert to JSON\"" + "}")
        return payload
    
    def __append_to_the_previous_entry(self, input_list: list[LogEntry], line: str):
        input_list[-1].data.message = input_list[-1].data.message + line

    def __get_last_event(self, entries: list[LogEntry]):
        last_event = datetime.strftime(entries[(len(entries))-1].date, '%Y-%m-%d %H:%M:%S')
        return last_event


    def parse_logs(self, path: str):
        try:
            with open(path) as log:
                entries = []
                for line in log:
                    entry= LogEntry()
                    try:
                        entry.date = self.__extract_date(line)
                    except:
                        try:
                            self.__append_to_the_previous_entry(entries, line)
                        except Exception:
                            pass
                        continue
                    entry.type = self.__extract_type(line)
                    entry.data.message = self.__extract_data_message(line)
                    if entry.data.message[0:12] == "MQTT publish":
                        entry.data.is_mqtt_publish = True
                        entry.data.mqtt_message.topic = self.__extract_mqttmessage_topic(line)
                        entry.data.mqtt_message.payload = self.__extract_mqttmessage_payload(line)
                    else:
                        entry.data.is_mqtt_publish = False
                        entry.data.mqtt_message.topic = None
                        entry.data.mqtt_message.payload = None
                    entries.append(entry)
            return entries
        except:
            raise FileExistsError(path + " doesn't exist")
    
    def parse_latest_logs(self, path: str):
            entries = self.parse_logs(path)
            pointer_file =  self.pointer_path + "/EventPointer.txt"
            last_event = self.__get_last_event(entries)
            if not os.path.exists(pointer_file):
                f = open(pointer_file, "w")
                f.write(last_event)
                f.close()
            else:
                f = open(pointer_file, "r+")
                date_string = f.read()
                date_dtatetime = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
                if date_string and date_dtatetime <= entries[(len(entries))-1].date:
                    entries = [x for x in entries if x.date > date_dtatetime]
                if entries:
                    f.seek(0)
                    f.truncate()
                    f.write(last_event)
            return entries
    

