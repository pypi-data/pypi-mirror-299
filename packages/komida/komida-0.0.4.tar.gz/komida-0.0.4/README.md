# Komida API (komida)

Returns structured data from the [komida calendar][calendar].

## Getting Started

Start by installing the dependencies using pip.
One way of doing this is `pip install -r requirements.txt`.
This will install **all** dependencies, including those used for development.
To only install the minimum set of requirements and the package use `pip install -e .`.

You can also install the latest release with `pip install kapi`.

## Example

```python
from datetime import datetime
from komida import KomidaAPI, Request, Location, Customer

api = KomidaAPI()
my_request = Request(Location.MIDDELHEIM, Customer.ANTWERPEN, datetime(2024, 10, 1))
menu = api.get_menu(my_request)
print(len(menu.dishes))
for dish in menu.dishes:
    for ingredient in dish.ingredients:
        print(ingredient)
print(menu.contains_dish("chicken"))
```

## Improvements

- Sanitize the data
- Fix allergens

[calendar]: https://app.growzer.be/komida-calendar
