# zigbee2mqtt log parser

A simple module for parsing of zigbee2mqtt logs into Python object for further processing.

**How to install:**

```sh
pip install z2m-log-parser
```

**How to use:**

```py
import z2m_log_parser

***

parser = Z2mLogParser()
```

**Return type**

```py
class LogEntry(object):
    def __init__(self):
        self.type: str
        self.date: datetime
        self.data: LogEntryData

class LogEntryData(object):
    def __init__(self):
        self.is_mqtt_publish: bool = bool
        self.message: str = str
        self.mqtt_message: MqttMessage

class MqttMessage(object):
    def __init__(self):
        self.topic: str
        self.payload: json
```

**Methods:**

parse_logs() -> list[]

```py
logs = parser.parse_logs()
```

parse_latest_logs()

```py
logs = parser.parse_latest_logs()
```
