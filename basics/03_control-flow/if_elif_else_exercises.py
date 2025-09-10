import sys, datetime

# Finding the highest
# With the following variables, a, b, and c, using only 'if' statements,
# find the highest number no matter which of the three vars has the highest one.
# Assume the different vars are always different to each other.

a = 2
b = 5
c = 3

if a > b and a > c:
    print('A is highest')
elif b > a and b > c:
    print('B is highest')
elif c > a and c > b:
    print('C is highest')
else:
    print('They\'re all the same')


# Access control with if statements
# Python script that checks user access permissions
# Get user input for:
# user_role (admin, analyst, intern, guest)
# security_clearance (1-5, where 5 is highest)
# Use if-elif-else to determine access level:
# - User is "admin" -> grant "full access"
# - User is "analyst" AND clearance >= 3 -> grant "analyst access"
# - User is "intern" AND clearance >= 2 -> grant "limited access"
# - User is "guest" -> grant "public access only"
# - Else -> deny access
# Bonus: Deny access if outside business hours 9 to 17

current_time = datetime.datetime.now()
if current_time.hour < 9 or current_time.hour > 17:
    sys.exit('Outside of business hours')

user_role = input('Input your user role: ')
security_clearance = input('Input your security clearance (1-5): ')

if user_role == 'admin':
    print('Full access granted')
elif (user_role == 'analyst') and (security_clearance.isdigit() and int(security_clearance) >= 3):
    print('Analyst access granted')
elif (user_role == 'intern') and (security_clearance.isdigit() and int(security_clearance) >= 2):
    print('Limited access granted')
elif (user_role == 'guest'):
    print('Public access granted')
else:
    print('Access denied')
