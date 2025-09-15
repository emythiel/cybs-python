import sys

# Network protocol classification
# Script that analyzes network traffic
# Get user input for a port number (integer)
# Use match-case to classify port:
# - 22 -> SSH
# - 80 -> HTTP
# - 443 -> HTTPS
# - 20 or 21 -> FTP
# - 53 -> DNS
# - 25 -> SMTP
# - default -> Unknown / custom port - investigate
# Bonus: Tell if system port (1-1023), user port (1024-49151), dynamic/private port (49152-65535)

port = input('Input port number: ')

if port.isdigit() == False:
    sys.exit('Not a valid port number dummy')

port = int(port)

if 1 <= port <= 1023:
    print('That\'s a system port')
elif 1024 <= port <= 49151:
    print('That\'s a user port')
elif 49152 <= port <= 65535:
    print('That\'s a dynamic/private port')

match port:
    case 22:      print('SSH Port')
    case 80:      print('HTTP Port')
    case 443:     print('HTTPS Port')
    case 20 | 21: print('FTP Port')
    case 53:      print('DNS Port')
    case 25:      print('SMTP Port')
    case _:       print('Unknown or custom port - must investigate')
