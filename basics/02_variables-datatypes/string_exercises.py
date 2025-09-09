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

print("Length (letters): " + str(len(full_name) - 1))

print("Print 50 times:\n" + ((full_name + " ") * 50))

print("Last letter: " + full_name[-1])
print("Is there z: " + str('z' in full_name))


# String split exercise
# Make a full name variable and give it a first, middle and last name
# - Make a list from the string, each element is part of name
# - Print the list
# - Show the list is a list type
# - Make a new list from full_name, but split on "a"
# - Make a new list "full_name_restored" where it's put back together

full_name = 'Jane Cool Doe'
split_full_name = full_name.split()
print("Full name as list: " + str(split_full_name))
print("List type: " + str(type(split_full_name)))

split_on_a = full_name.split("a")
print("Split on a: " + str(split_on_a))

full_name_restored = " ".join(split_full_name)
print("Name restored: " + full_name_restored)
full_name_restored_a = "a".join(split_on_a)
print("Name split on a restored: " + full_name_restored_a)
