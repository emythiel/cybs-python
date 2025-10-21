# Create an IP address validator function for a security scanner
# 1. Accept user input for IP address
# 2. Validate IP format using regex
# 3. Check each octet is between 0-255
# 4. Reject private IP ranges for external scanning:
#   a. 10.0.0.0/8 (10.0.0.0 - 10.255.255.255)
#   b. 172.16.0.0/12 (172.16.0.0 - 172.31.255.255)
#   c. 192.168.0.0/16 (192.168.0.0 - 192.168.255.255)
# 5. Return validated IP or raise appropriate error

import re

def validate_ip(ip):
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'

    # Check if basic format is met
    if not re.match(pattern, ip):
        raise ValueError('Invalid IP address format')

    octets = ip.split('.')

    # Check if octets between 0-255
    for octet in octets:
        if int(octet) > 256:
            raise ValueError('IP address octets must be 0-255')

    # Reject private IP ranges
    if int(octets[0]) == 10:
        raise ValueError('Private IP rejected (10.0.0.0/8 range)')
    if int(octets[0]) == 172 and 16 <= int(octets[1]) <= 31:
        raise ValueError('Private IP rejected (172.16.0.0/12 range)')
    if int(octets[0]) == 192 and int(octets[1]) == 168:
        raise ValueError('Private IP rejected (192.168.0.0/16 range)')

    return ip

# The ugly regex method
def validate_ip_regex(ip):
    ip_pattern = re.compile(
        r'^(?!(10\.|172\.(1[6-9]|2\d|3[0-1])\.|192\.168\.))'
        r'((25[0-5]|2[0-4]\d|1?\d{1,2})\.){3}'
        r'(25[0-5]|2[0-4]\d|1?\d{1,2})$'
    )

    if not ip_pattern.match(ip):
        raise ValueError('Invalid or private IP address')

    return ip

try:
    ip = input('Enter IP address: ')
    valid_ip = validate_ip_regex(ip)
    print(f'[OK] Valid IP: {ip}')
except ValueError as e:
    print(f'[ERROR] Invalid input: {e}')
