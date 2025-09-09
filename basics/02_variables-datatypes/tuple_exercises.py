# Make a tuple with:
# 1, 2, 3, 4, 5, "Sebastian"
# Add "Alex" to the tuble
# Tubles are immutable, so need to work around this

tuple_list = (1,2,3,4,5, 'Sebastian')
print('Oritinal tuple: ' + str(tuple_list))
tuple_list = list(tuple_list)
tuple_list.append('Alex')
tuple_list = tuple(tuple_list)
print('"Fixed" tuple: ' + str(tuple_list))
