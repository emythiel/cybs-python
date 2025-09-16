# First List
# Make a list with: 0,1,2,3,4,5,6,7,8
# - Print the full list
# - Print first element of list
# - Print last element of list
# - Print first 4 elements
# -  declare a new list and assign last 3 elements of original list

first_list = [0,1,2,3,4,5,6,7,8]

print(f'List: {first_list}')
print(f'First element: {first_list[0]}')
print(f'Last element: {first_list[-1]}')
print(f'First 4 elements: {first_list[:4]}')

new_first_list = first_list[-3:]
print(f'New list with last 3 elements of original list: {new_first_list}')


# Second list
# Make an empty list
# - Add int 2, 1, and 3
# - Add string "cyber"
# - Print index of "cyber"
# - Remove string from list
# - Put list in chronological order and print

second_list = []

second_list.extend([2,1,3])
print(f'Second list with 2,1,3 added: {second_list}')
second_list.append('cyber')
print(f'Second list with cyber added: {second_list}')
print(f'Index of cyber: {second_list.index('cyber')}')
second_list.remove('cyber')
second_list.sort()
print(f'Second list with cyber removed and sorted: {second_list}')


# Security Log
# Log tool shows following ips accessed system
# ['189.19.202.26', '124.124.86.154', '111.123.147.92', '191.194.49.89', '191.194.49.89', '3.100.186.196', '17.102.131.131',
#  '170.40.162.9', '66.23.103.242', '203.207.124.71', '3.100.186.196', '170.194.124.70', '3.100.186.196', '161.240.120.16',
#  '37.161.17.14', '3.100.186.196', '144.182.46.41', '3.100.186.196', '67.180.5.237', '182.44.178.202']
# - 8.8.8.8 is latest to access - add manually
# - How many entries in log
# - 5 latest IPs to access system
# - How many times did '3.100.186.196' access system

security_log = ['189.19.202.26', '124.124.86.154', '111.123.147.92', '191.194.49.89', '191.194.49.89', '3.100.186.196', '17.102.131.131',
                '170.40.162.9', '66.23.103.242', '203.207.124.71', '3.100.186.196', '170.194.124.70', '3.100.186.196', '161.240.120.16',
                '37.161.17.14', '3.100.186.196', '144.182.46.41', '3.100.186.196', '67.180.5.237', '182.44.178.202']
security_log.append('8.8.8.8')
print(f'Full security log with 8.8.8.8 added: {security_log}')
print(f'Entries in log: {len(second_list)}')
print(f'5 latest IPs to access: {security_log[-5:]}')
print(f'Times 3.100.186.196 appears: {security_log.count('3.100.186.196')}')
