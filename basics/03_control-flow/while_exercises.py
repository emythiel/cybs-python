# Password validator
# - Use a while loop to repeatedly ask for password input
# - Password must meet criteria:
#   - At least 12 chars long
#   - Contain at least one number
#   - For each failed attempt, tell user what's missing
# - When valid password entered, display "Strong password accepted!"
# - Count and display total attemps made

is_pwd_valid = False
pwd_attempts = 0

while is_pwd_valid == False:
    pwd = input('Input password: ')

    is_pwd_valid = True
    pwd_attempts += 1

    if len(pwd) < 12:
        print(f'Not long enough (must be at least 12, current length: {len(pwd)})')
        is_pwd_valid = False

    if not any(char.isdigit() for char in pwd):
        print(f'Must contain at least 1 number')
        is_pwd_valid = False

    if is_pwd_valid == True:
        break

print(f'Strong password accepted!')
print(f'Amount of attempts: {pwd_attempts}')
