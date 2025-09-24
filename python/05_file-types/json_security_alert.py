# Use json_security_alert.json and:
# Read the JSON file
# Print: "Alert ALT-001: HIGH severity malware_detected from 192.168.1.100"

import json

try:
    with open ('json_security_alert.json', 'r') as file:
        data = json.load(file)

        alert_id = data['alert_id']
        severity = data['severity']
        source_ip = data['source_ip']
        alert_type = data['alert_type']

        print(f'Alert {alert_id}: {severity} severity {alert_type} from {source_ip}')
except FileNotFoundError:
    print('json_security_alert.json not found')
except json.JSONDecodeError:
    print('Invalid JSON format')
