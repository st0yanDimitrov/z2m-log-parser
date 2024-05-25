from datetime import datetime
import json
import os

class MqttMessage(object):
    def __init__(self):
        self.topic = str
        self.payload = json

class LogEntryData(object):
    def __init__(self):
        self.isMqttPublish = bool
        self.message = str
        self.mqttMessage = MqttMessage()

class LogEntry(object):
    def __init__(self):
        self.type = str
        self.date = datetime
        self.data = LogEntryData()

class LogParser:
    '''
    Used to parse Zigbee2mqtt log entries from log.txt file
    '''

    def parseLogs(self, path):
        parsedLines = []
        with open(path) as log:
            for line in log:
                parsedLine= LogEntry()
                parsedLine.data.isMqttPublish
                try:
                    parsedLine.type = line[0:4]
                    parsedLine.date = datetime.strptime(line[6:25], '%Y-%m-%d %H:%M:%S')
                except:
                    parsedLines[1:].message + "/n" + parsedLine
                    continue

                parsedLine.data.message = line[27:]
                if parsedLine.data.message[0:12] == "MQTT publish":
                    parsedLine.data.isMqttPublish = True
                    parsedLine.data.mqttMessage.topic = line.split("topic")[1].rsplit(", payload")[0].strip().strip("'")
                    parsedLine.data.mqttMessage.payload = line.split("payload")[1].strip().strip("'")
                    try:
                        parsedLine.data.mqttMessage.payload = json.loads(line.split("payload")[1].strip().strip("'"))
                    except:
                        parsedLine.data.mqttMessage.payload = None
                else:
                    parsedLine.data.isMqttPublish = True
                    parsedLine.data.mqttMessage.topic = None
                    parsedLine.data.mqttMessage.payload = None
                parsedLines.append(parsedLine)
        return parsedLines

    def parseLatestLogs(self, path: str):
            events = self.parseLogs(path)
            pointerPath = "./eventPointer.txt"
            lastEvent = datetime.strftime(events[(len(events))-1].date, '%Y-%m-%d %H:%M:%S')
            if not os.path.exists(pointerPath):
                f = open(pointerPath, "w")
                f.write(lastEvent)
                f.close()
            else:
                f = open(pointerPath, "r+")
                dateSt = f.read()
                dateDt = datetime.strptime(dateSt, '%Y-%m-%d %H:%M:%S')
                if dateSt and dateDt <= events[(len(events))-1].date:
                    events = [x for x in events if x.date > dateDt]
                if events:
                    f.seek(0)
                    f.truncate()
                    f.write(lastEvent)
            if any(events):
                return events
            return None

lala = LogParser()
#lalalala = LogEntry()[]
lalalala = lala.parseLogs("log.txt")
print(lalalala[37].data.mqttMessage.topic)