# Mandatory 01 - Programming
# Emily, Natasha, Sigurd & Thomas

import json, csv
from pathlib import Path

# Define paths
json_path = Path.cwd() / 'incident.json'
csv_dir = Path.cwd() / 'csv'
csv_dir.mkdir(exist_ok=True) # Create csv dir if needed

# Output CSV filenames
csv_fields = {
    'domains': 'csv_domains.csv',
    'fileHashes': 'csv_filehashes.csv',
    'ips': 'csv_ips.csv',
    'processes': 'csv_processes.csv'
}

# Init csv data storage with headers
csv_data = {
    key: [['alertId', 'machineId', 'firstActivity', key]] for key in csv_fields
}

# Function to write CSV
def write_csv(path, data):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        writer.writerows(data)

# Read JSON
try:
    with open(json_path, 'r') as file:
        data = json.load(file)
except FileNotFoundError:
    print('Error: incident.json not found.')
    exit(1)
except json.JSONDecodeError:
    print('Error: invalid JSON format.')
    exit(1)

# Loop through and process each alert
for alert in data.get('alerts', []):
    alert_id = alert.get('alertId', '')
    machine_id = alert.get('machineId', '')
    first_activity = alert.get('firstActivity', '')
    entities = alert.get('entities', {})

    for key in csv_fields:
        for value in entities.get(key, []):
            row = [alert_id, machine_id, first_activity, value]
            csv_data[key].append(row)

# Write CSV files
for key, filename in csv_fields.items():
    path = csv_dir / filename
    write_csv(path, csv_data[key])
