# Create a validator for security scanner configuration
# Validate a configuration dictionary with these rules:
#   1. scan_type: Must be port, vulnerability, or network
#   2. target_ips: List of valid IP addresses
#   3. scan_intensity: Integer between 1-10
#   4. output_file: Sanitized filename (if not suggest sanitized name)
#   5. timeout: Integer between 1-300 seconds
#
# Sample config (invalid output_file):
# config = {
#     'scan_type': 'port',
#     'target_ips': ['8.8.8.8', '1.1.1.1'],
#     'scan_intensity': 5,
#     'output_file': 'scan>results.txt',
#     'timeout': 60
# }

import re

def validate_scan_type(scan_type):
    if not isinstance(scan_type, str):
        raise ValueError('scan_type is not a string')
    if scan_type not in ['port', 'vulnerability', 'network']:
        raise ValueError('scan_type is not port, vulnerability or network')

def validate_ips(target_ips):
    if not isinstance(target_ips, list) or target_ips == []:
        raise ValueError('target_ips must be a non-empty list')

    ip_pattern = re.compile(
        r'^((25[0-5]|2[0-4]\d|1?\d{1,2})\.){3}'
        r'(25[0-5]|2[0-4]\d|1?\d{1,2})$'
    )

    for ip in target_ips:
        if not isinstance(ip, str):
            raise ValueError('target_ips must be strings')
        if not ip_pattern.match(ip):
            raise ValueError(f'Invalid IP address: {ip}')

def validate_scan_intensity(scan_intensity):
    if not isinstance(scan_intensity, int) or not 0 < scan_intensity < 11:
        raise ValueError('scan_intensity must be an integer between 1 and 10')

def validate_output_file(output_file):
    if not isinstance(output_file, str):
        raise ValueError('output_file must be a string')
    # Sanitize
    dangerous_chars = '<>:"\\|?*'
    for char in dangerous_chars:
        output_file = output_file.replace(char, '_')
    output_file = output_file.strip('. ')

    return output_file

def validate_timeout(timeout):
    if not isinstance(timeout, int) or not 0 < timeout < 301:
        raise ValueError('timeout must be an integer between 1 and 300')

def config_validator(config):
    # config validate
    if not isinstance(config, dict):
        raise ValueError('config is not a dictionary')

    # scan_type validate
    scan_type = config.get('scan_type', '')
    validate_scan_type(scan_type)

    # target_ips validate
    target_ips = config.get('target_ips', '')
    validate_ips(target_ips)

    # scan_intensity validate
    scan_intensity = config.get('scan_intensity', '')
    validate_scan_intensity(scan_intensity)

    # output_file validation
    output_file = config.get('output_file', '')
    config['output_file'] = validate_output_file(output_file)

    # timeout validation
    timeout = config.get('timeout', '')
    validate_timeout(timeout)

try:
    config = {
        'scan_type': 'port',
        'target_ips': ['8.8.8.8', '1.1.1.1'],
        'scan_intensity': 5,
        'output_file': 'scan>results.txt',
        'timeout': 60
    }
    config_validator(config)
    print(f'[OK] Valid config: {config}')
except ValueError as e:
    print(f'[ERROR] Invalid config: {e}')
