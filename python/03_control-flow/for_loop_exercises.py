# Security event analysis
# 1. Create a list of security events (strings) that includes:
#   a. Normal events: 'user login', 'file access', 'email sent'
#   b. Suspicious events: 'failed login', 'unauthorized access', 'malware detected'
# 2. Use a for loop to proccess each event and:
#   a. Count total events processed
#   b. Count suspicious events (events containing 'failed', 'unauthorized' or 'malware')
#   c. Print each suspicious event with 'ALERT:' prefix
#   d. Print normal events with 'OK:' prefix
# 3. After the loop, display:
#   a. Total events processed
#   b. Number of suspicious events found
#   c. Security status: 'SECURE' if no suspicious events, 'AT RISK' if any found
# Bonus:
#   1. Use break to stop processing if 'critical threat' is found
#   2. Use continue to skip events containing 'test'
#   3. Add event numbering in the output( Hint: enumerate() )

import re

event_list = ['user_login', 'user_login', 'test_email', 'email_sent', 'file_access', 'user_login', 'failed_login', 'file_access',
              'failed_login', 'unauthorized_access', 'user_login', 'malware_detected', 'failed_login', 'email_sent',
              'email_sent', 'email_sent', 'email_sent', 'email_sent', 'malware_detected', 'email_sent', 'user_login',
              'file_access', 'file_access', 'user_login', 'unauthorized_access', 'email_sent', 'malware_detected']

event_count = 0
sus_events = 0
for i, e in enumerate(event_list):
    # check if test event with regex
    if re.match(r'[Tt][Ee][Ss][Tt]', e):
        print(f'TEST EVENT, SKIPPING: {e}')
        continue

    event_count += 1

    # check if sus event
    if e in ('failed_login', 'unauthorized_access', 'malware_detected', 'critical_threat'):
        sus_events += 1

        # check if critical threat, if yes break out
        if e in ('critical_threat'):
            print(f'EVENT ID: {i} - CRITICAL THREAT: {e}')
            break

        print(f'EVENT ID: {i} - ALERT: {e}')
    else:
        print(f'EVENT ID: {i} - OK: {e}')

print(f'Total events processed: {event_count}')
print(f'Suspicious events found: {sus_events}')
if sus_events > 0:
    print('AT RISK')
else:
    print('SECURE')
