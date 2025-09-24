# Process thread intelligence data from JSON and export filtered results to CSV
# 1. Read from the threat_processing.json file:
#    https://raw.githubusercontent.com/alex-prog/CYBS-Programming/refs/heads/main/threat_intel.json
# 2. Filter for threats with confidence > 80 and severity = 'high'
# 3. Export filtered threats to threat_processing.csv
# 4. Print total count of high-priority threats found
#
# Expected output format (CSV):
# IOC,Type,Severity,Confidence,Last_Seen
# 192.168.1.100,ip,high,95,2025-09-15T14:30:00Z
# malware.example.com,domain,high,88,2025-09-16T09:15:00Z

import json, csv

try:
    with open('threat_processing.json', 'r') as file:
        data = json.load(file)
except FileNotFoundError:
    print('threat_processing.json not found')
except json.JSONDecodeError:
    print('Invalid JSON format')

threats = [['IOC', 'Type', 'Severity', 'Confidence', 'Last_Seen']]

for e in data['indicators']:
    if e['confidence'] > 80 and e['severity'] == 'high':
        l = [e['ioc_value'], e['ioc_type'], e['severity'], e['confidence'], e['last_seen']]
        threats.append(l)

with open('threat_processing.csv', 'w', newline='') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerows(threats)

print(f'High priority threats found: {len(threats) - 1}')
