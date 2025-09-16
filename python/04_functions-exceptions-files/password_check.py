# Check my password
# Define a function called "password_checker".
# The function takes two arguments, "password" and "minimum_length"
# The function should handle the following scenarios:
#   - Password is good enough (meets minimum_length)
#   - Password is too short (shorter than minimum length OR less than 6 chars)
#   - minimum_length must be at least 6 chars
#   - minimum_length should not be above 64 chars
# Function should print appropriate messages for each of the scenarios.
# Make at least 4 function calls to test the scenarios.

def password_checker(pwd, min_length):
    # minimum length between 6 and 64 characters
    if not 6 <= min_length <= 64:
        print('Minimum length does not meet requirements: Between 6 and 64')
        return

    # password length above minimum length
    if len(pwd) < min_length:
        print('Password does not meet minimum length requirements')
        return

    print('Password meets the requirements')

password_checker('password', 4)  # minimum length too low
password_checker('password', 69) # minimum length too high
password_checker('password', 8)  # password good
password_checker('password', 12) # password does not meet minimum length
