# String exercise
# Make two variables, "first_name" and "last_name" and assign them appropriate values
# - Combine the two strings into one
# - Print it
# - Print length of string
# - Print string 50 times in a row
# - Print ONLY last character of string
# - Check if string contains "z" and print true/false

first_name = 'John'
last_name = 'Doe'
full_name = first_name + ' ' + last_name

print("Full name: " + full_name)

print("\nLength (letters): " + str(len(full_name) - 1))

print("\nPrint 50 times:\n" + ((full_name + " ") * 50))

print("\nLast letter: " + last_name[-1])
print("\nIs there z: " + str('z' in full_name))
