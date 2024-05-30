import unittest
from datetime import datetime
import json
from types import SimpleNamespace
from src.z2m_log_parser import *



test_data_no_mqtt = "info  2024-05-25 22:53:36: Starting Zigbee2MQTT version 1.35.1 (commit #9eaaa0f)"
test_data_mqtt = '''info  2024-05-28 10:42:38: MQTT publish: topic 'zigbee2mqtt/0x84fd27fffe9f718e', payload '{"linkquality":54,"power_on_behavior":"previous","state":"OFF","update":{"installed_version":537019939,"latest_version":587765297,"state":"available"}}'''
test_data_error_stack = '''error 2024-05-25 22:53:58: Error: Failed to connect to the adapter (Error: SRSP - SYS - ping after 6000m\n
                               at ZStackAdapter.start (/app/node_modules/zigbee-herdsman/src/adapter/z-stack/adapter/zStackAdapter.ts:103:2\n
                               at Controller.start (/app/node_modules/zigbee-herdsman/src/controller/controller.ts:132:2\n
                               at Zigbee.start (/app/lib/zigbee.ts:60:2\n
                               at Controller.start (/app/lib/controller.ts:98:2\n
                               at start (/app/index.js:107:5)\n'''
test_data_mqtt_invalid_payload = '''info  2024-05-28 10:42:38: MQTT publish: topic 'zigbee2mqtt/0x84fd27fffe9f718e', payload '{"linkquality":54,"power_on_behavior":"previous","state":"OFF","update":{"installed_version":537019939,"latest_version":587765297,"state":"available"}'''



class TestZ2mLogParser(unittest.TestCase):

    def test_extract_date(self):
        parser = Z2mLogParser()
        expected_result = datetime.strptime('2024-05-28 10:42:38', '%Y-%m-%d %H:%M:%S')
        test_result = parser._Z2mLogParser__extract_date(test_data_mqtt)
        self.assertEqual(expected_result, test_result)

    def test_extract_type(self):
        parser = Z2mLogParser()
        expected_result = "info"
        test_result = parser._Z2mLogParser__extract_type(test_data_mqtt)
        self.assertEqual(expected_result, test_result)

    def test_extract_data_message(self):
        parser = Z2mLogParser()
        expected_result = '''MQTT publish: topic 'zigbee2mqtt/0x84fd27fffe9f718e', payload '{"linkquality":54,"power_on_behavior":"previous","state":"OFF","update":{"installed_version":537019939,"latest_version":587765297,"state":"available"}}'''
        test_result = parser._Z2mLogParser__extract_data_message(test_data_mqtt)
        self.assertEqual(expected_result, test_result)
    
    def test_extract_mqttmessage_topic(self):
        parser = Z2mLogParser()
        expected_result = "zigbee2mqtt/0x84fd27fffe9f718e"
        test_result = parser._Z2mLogParser__extract_mqttmessage_topic(test_data_mqtt)
        self.assertEqual(expected_result, test_result)

    def test_extract_mqttmessage_payload(self):
        parser =  Z2mLogParser()
        expected_result = json.loads('''{"linkquality":54,"power_on_behavior":"previous","state":"OFF","update":{"installed_version":537019939,"latest_version":587765297,"state":"available"}}''', object_hook=lambda d: SimpleNamespace(**d))
        test_result = parser._Z2mLogParser__extract_mqttmessage_payload(test_data_mqtt)
        self.assertEqual(expected_result, test_result)

    def test_append_to_the_previous_entry(self):
        parser =  Z2mLogParser()
        data_to_append = "data_to_append"
        initial_data = "initial_data"
        line1 =  LogEntry()
        line2 =  LogEntry()
        line2.data.message = initial_data
        test_data_list = [line1 ,line2]
        parser._Z2mLogParser__append_to_the_previous_entry(test_data_list, data_to_append)
        self.assertEqual(test_data_list[1].data.message, initial_data + data_to_append)

    def test_get_last_event_date(self):
        parser =  Z2mLogParser()
        line1 =  LogEntry()
        line1.date = datetime.strptime('2024-05-28 10:42:38', '%Y-%m-%d %H:%M:%S')
        line2 = LogEntry()
        line2.date = datetime.strptime('2024-05-28 10:42:39', '%Y-%m-%d %H:%M:%S')
        line3 = LogEntry()
        line3.date = datetime.strptime('2024-05-28 10:42:40', '%Y-%m-%d %H:%M:%S')
        test_data = [line1, line2, line3]
        result = parser._Z2mLogParser__get_last_event_date(test_data)
        self.assertEqual(result, '2024-05-28 10:42:40')
    
    def test_parse_logs(self):
        pass

    def test_parse_latest_logs(self):
        pass

if __name__ == '__main__':
    unittest.main()