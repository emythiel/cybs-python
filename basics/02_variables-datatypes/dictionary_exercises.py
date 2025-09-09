# Book Prices
# Start with an empty dictionary, "book_prices"
# - Add three books and their prices
#   - "Lord of the Rings": 150
#   - "Cybersikkerhed 101": 500
#   - "Mad Max": 399
# - Print price of "Mad Max"
# - Access a book not in dictionary using .get()
# - Update price of "Lord of the Rings" to 200
# - Add a new book to the list of your choosing
# - Delete "Cybersikkerhed 101" from dictionary
# - Do a check if "Cybersikkerhed 101" still exists
# - Do a check if "Mad Max" still exists

book_prices = {}

book_prices["Lord of the Rings"] = 150
book_prices["Cybersikkerhed 101"] = 500
book_prices["Mad Max"] = 399

print('Books: ' + str(book_prices))
print('Mad Max price: ' + str(book_prices["Mad Max"]))

print('Getting something nonexistant: ' + str(book_prices.get('Waluigi')))

book_prices["Lord of the Rings"] = 200
print('New LotR price: ' + str(book_prices["Lord of the Rings"]))

book_prices["Waluigi"] = 420
print('Book list with new book: ' + str(book_prices))

del(book_prices["Cybersikkerhed 101"])
print('Book list without "Cybersikkerhed": ' + str(book_prices))

print('Does "Cybersikkerhed 101" exist: ' + str('Cybersikkerhed 101' in book_prices))
print('Does "Mad Max" exist: ' + str('Mad Max' in book_prices))
