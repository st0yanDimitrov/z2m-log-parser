# zigbee2mqtt log parser

A simple module for parsing of zigbee2mqtt logs into Python object for further processing.

## How to install:

```sh
pip install z2m-log-parser
```

## How to use:

```py
from z2m_log_parser import *

***

parser = Z2mLogParser()
```

## Return type:

```py
class LogEntry(object):
    def __init__(self):
        self.type: str
        self.date: datetime
        self.data: LogEntryData

class LogEntryData(object):
    def __init__(self):
        self.is_mqtt_publish: bool
        self.message: str
        self.mqtt_message: MqttMessage

class MqttMessage(object):
    def __init__(self):
        self.topic: str
        self.payload: object
```

## Methods:

_**parse_logs(**<log_path>**) -> list[LogEntry]**_

```py
path: str = './log.txt'
logs: list[LogEntry] = parser.parse_logs(path)
```



This method will read the content of the target log file and return it's content as a list of python object representing each log entry.

_**parse_latest_logs(**<log_path>**) -> list[LogEntry]**_

```py
path: str = './log.txt'
logs: list[LogEntry] = parser.parse_latest_logs('path')
```

This method will do the same as the one above, but it will generate a pointer file in the execution directory, containing the timestamp of the latest log on the time of the execution.
Upon following executions, the method will use the pointer file as reference in order to determine and return only the latest entries, logged after the previous execution thus allowing the module to be used on a schedule base. The pointer file will be update after each execution.

## Examples:

**Input:**
```txt
info  2024-05-28 10:42:38: MQTT publish: topic 'zigbee2mqtt/0x84fd27fffe9f718e', payload '{"linkquality":54,"power_on_behavior":"previous","state":"OFF","update":{"installed_version":537019939,"latest_version":587765297,"state":"available"}}'
```

**Output:**
```py

'type': 'info',
'date': datetime.datetime(2024, 5, 28, 10, 42, 38),
'data': {
         'is_mqtt_publish': True,
         'message': 'MQTT publish: topic \'zigbee2mqtt/0x84fd27fffe9f718e\', payload \'{"linkquality":54,"power_on_behavior":"previous","state":"OFF","update";{"installed_version":537019939,"latest_version":587765297,"state":"available"}}\'\n',
         'mqtt_message': {
                          'topic': 'zigbee2mqtt/0x84fd27fffe9f718e',
                          'payload': {
                                      'linkquality'=54,
                                      'power_on_behavior'='previous',
                                      'state'='OFF',
                                      'update': {
                                                 'installed_version'=537019939,
                                                 'latest_version'=587765297,
                                                 'state=''available'
                                                }
                                     }
                         }
        }

```

**Input:**
```txt
info  2024-05-25 22:53:36: Starting Zigbee2MQTT version 1.35.1 (commit #9eaaa0f)
```

**Output:**
```py
{
'type': 'info',
'date': 'datetime.datetime(2024, 5, 25, 22, 53, 36)',
'data': {
          'is_mqtt_publish': False,
          'message': "Starting Zigbee2MQTT version 1.35.1 (commit #9eaaa0f)",
          'mqtt_message': {
                           'topic': None,
                           'payload': None
                          }
        }
}
```
**Input:**
```txt
error 2024-05-25 22:53:58: Error: Failed to connect to the adapter (Error: SRSP - SYS - ping after 6000ms)
    at ZStackAdapter.start (/app/node_modules/zigbee-herdsman/src/adapter/z-stack/adapter/zStackAdapter.ts:103:27)
    at Controller.start (/app/node_modules/zigbee-herdsman/src/controller/controller.ts:132:29)
    at Zigbee.start (/app/lib/zigbee.ts:60:27)
    at Controller.start (/app/lib/controller.ts:98:27)
    at start (/app/index.js:107:5)
```

**Output:**
```py
{
'type': 'error',
'date': datetime.datetime(2024, 5, 25, 22, 53, 58),
'data': {
         'is_mqtt_publish': False,
         'message': 'Error: Failed to connect to the adapter (Error: SRSP - SYS - ping after 6000ms)\n
          at ZStackAdapter.start (/app/node_modules/zigbee-herdsman/src/adapter/z-stack/adapter/zStackAdapter.ts:103:27)\n
          at Controller.start (/app/node_modules/zigbee-herdsman/src/controller/controller.ts:132:29)\n
          at Zigbee.start (/app/lib/zigbee.ts:60:27)\n    at Controller.start (/app/lib/controller.ts:98:27)\n
          at start (/app/index.js:107:5)',
         'mqtt_message': {
                          'topic': None,
                          'payload': None
                         }
        }
}
```
