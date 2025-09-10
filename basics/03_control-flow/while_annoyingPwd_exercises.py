# Annoying pwd validator
# >:)
import re

is_pwd_valid = False
pwd_attempts = 0

while is_pwd_valid == False:
    pwd = input('Input password: ')

    pwd_attempts += 1

    # Min length
    if len(pwd) < 12:
        print('Password must be at least 12 characters')
        continue

    # 1 number
    if not any(char.isdigit() for char in pwd):
        print('Password must contain at least 1 number')
        continue

    # contains dennis
    dennis_regex = re.compile(r'dennis')
    if not dennis_regex.search(pwd):
        print('Password must contain "dennis"')
        continue

    # special character
    special_regex = re.compile(r'[\[\]@_!#$%^&*()<>?/\|}{~:]')
    if not special_regex.search(pwd):
        print('Password must contain a special character ( @_!#$%^&*()<>?/\\|}{~: )')
        continue

    # sum = 23
    temp = "0"
    sum = 0
    for char in pwd:
        if (char.isdigit()):
            sum += int(char)
    if sum != 23:
        print('The sum of all numbers must equal to 23')
        continue

    # if all checks passed, you're here and done - nice
    is_pwd_valid = True

print(f'Success! Number of attempts: {pwd_attempts}')
