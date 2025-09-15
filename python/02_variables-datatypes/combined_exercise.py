# Combined exercise
# Make a script doing the following:
# 1.  Create empty list, "first_list"
# 2.  Declare 3 number variables and add to list
# 3.  Declare 3 strings and add to list
# 4.  Make new list, "second_list", that contains all elements of "first_list" TWICE
# 5.  Add "first_list" and "second_list" to a dictionary and give them appropriate keys
# 6.  Delete any reference to "first_list" and "second_list" (first_list, second_list = None)
# 7.  Using dictionary, delete all strings from first key/value pair
# 8.  Add new key/value pair to dictionary - key is "age", value is an age
# 9.  Print the full dictionary
# 10. Print only age from dictionary
# 11. Print the first number of what used to be "second_list", from the dictionary

first_list = []

first_list.extend([1,2,3])
first_list.extend(['One', 'Two', 'Three'])
print('First list with 3 numbers and 3 strings: ' + str(first_list))

second_list = first_list*2

the_dictionary = {
    "first_list": first_list,
    "second_list": second_list
}
print('The dictionary: ' + str(the_dictionary))

del first_list, second_list

the_dictionary['first_list'] = [e for e in the_dictionary['first_list'] if not isinstance(e, str)]

the_dictionary['age'] = 42

print('Full dictionary in current state: ' + str(the_dictionary))
print('Age from dictionary: ' + str(the_dictionary['age']))
print('First number from original second list in dictionary: ' + str(the_dictionary['second_list'][0]))
