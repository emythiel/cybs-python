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

book_prices.update({
    "Lord of the Rings": 150,
    "Cybersikkerhed 101": 500,
    "Mad Max": 399
})

print(f'Books: {book_prices}')
print(f'Mad Max price: {book_prices['Mad Max']}')

print(f'Getting something nonexistant: {book_prices.get('Waluigi')}')

book_prices["Lord of the Rings"] = 200
print(f'New LotR price: {book_prices['Lord of the Rings']}')

book_prices["Waluigi"] = 420
print(f'Book list with new book: {book_prices}')

del(book_prices["Cybersikkerhed 101"])
print(f'Book list without "Cybersikkerhed": {book_prices}')

print(f'Does "Cybersikkerhed 101" exist: {'Cybersikkerhed 101' in book_prices}')
print(f'Does "Mad Max" exist: {'Mad Max' in book_prices}')
