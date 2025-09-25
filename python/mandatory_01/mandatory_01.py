import json, csv
from pathlib import Path

# Path to JSON file
json_path = Path.cwd().joinpath('incident.json')

# Path to CSV files (in own csv directory)
csv_path_domains = Path.cwd().joinpath('csv', 'csv_domains.csv')
csv_path_filehashes = Path.cwd().joinpath('csv', 'csv_filehashes.csv')
csv_path_ips = Path.cwd().joinpath('csv', 'csv_ips.csv')
csv_path_processes = Path.cwd().joinpath('csv', 'csv_processes.csv')

# Read from JSON as try statement to handle potential errors
try:
    with open(json_path, 'r') as file:
        data = json.load(file)
except FileNotFoundError:
    print('incident.json not found')
except json.JSONDecodeError:
    print('Invalid JSON format')

# Create initial lists with csv headers
csv_domains = [['alertId','machineId','firstActivity','domains']]
csv_filehashes = [['alertId','machineId','firstActivity','filehashes']]
csv_ips = [['alertId','machineId','firstActivity','ips']]
csv_processes = [['alertId','machineId','firstActivity','processes']]

for alerts in data['alerts']:
    # Loop through domains and append to csv_domains list
    for domains in alerts['entities']['domains']:
        l = [f'{alerts['alertId']}', f'{alerts['machineId']}', f'{alerts['firstActivity']}', f'{domains}']
        csv_domains.append(l)
    # Loop through filehashes and append to csv_filehashes list
    for filehashes in alerts['entities']['fileHashes']:
        l = [f'{alerts['alertId']}', f'{alerts['machineId']}', f'{alerts['firstActivity']}', f'{filehashes}']
        csv_filehashes.append(l)
    # Loop through IPs and append to csv_ips list
    for ips in alerts['entities']['ips']:
        l = [f'{alerts['alertId']}', f'{alerts['machineId']}', f'{alerts['firstActivity']}', f'{ips}']
        csv_ips.append(l)
    # Loop through processes and append to csv_processes list
    for processes in alerts['entities']['processes']:
        l = [f'{alerts['alertId']}', f'{alerts['machineId']}', f'{alerts['firstActivity']}', f'{processes}']
        csv_processes.append(l)

# Create domain CSV
with open(csv_path_domains, 'w', newline='') as file:
    csv_writer = csv.writer(file, quoting=csv.QUOTE_ALL)
    csv_writer.writerows(csv_domains)

# Create filehashes CSV
with open(csv_path_filehashes, 'w', newline='') as file:
    csv_writer = csv.writer(file, quoting=csv.QUOTE_ALL)
    csv_writer.writerows(csv_filehashes)

# Create IPs CSV
with open(csv_path_ips, 'w', newline='') as file:
    csv_writer = csv.writer(file, quoting=csv.QUOTE_ALL)
    csv_writer.writerows(csv_ips)

# Create processes CSV
with open(csv_path_processes, 'w', newline='') as file:
    csv_writer = csv.writer(file, quoting=csv.QUOTE_ALL)
    csv_writer.writerows(csv_processes)
