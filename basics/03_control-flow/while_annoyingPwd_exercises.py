# Annoying pwd validator
# >:)
import re, datetime

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
        print('Password must contain 1 number')
        continue

    # contains dennis
    dennis_regex = re.compile(r'dennis')
    if not dennis_regex.search(pwd):
        print('Password must contain "dennis"')
        continue

    # current hour
    cur_hour = datetime.datetime.now().strftime('%H')
    cur_hour_pattern = rf'{cur_hour}'
    cur_hour_reg = re.compile(cur_hour_pattern)
    if not cur_hour_reg.search(pwd):
        print('Password must contain the current hour')
        continue

    # capital letter
    if not any(char.isupper() for char in pwd):
        print('Password must contain 1 uppercase character')
        continue

    # lowercase
    if not any(char.islower() for char in pwd):
        print('Password must contain 1 lowercase character')

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

    # Answer to universe
    universe_answer = re.compile(r'42')
    if not universe_answer.search(pwd):
        print('Password must contain the answer to the universe')
        continue

    # if all checks passed, you're here and done - nice
    is_pwd_valid = True

print(f'Success! Number of attempts: {pwd_attempts}')
