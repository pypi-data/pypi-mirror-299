"""Komida API."""
__version__ = "0.0.3"
__version_info__ = tuple((int(num) if num.isdigit() else num for num in __version__.replace("-", ".", 1).split(".")))

from komida.komida import KomidaAPI, Menu, AllergenImage, DishTypeImage, Location, Ingredient, APIException, Dish, Allergen, Customer, Request

__all__ = (
    "KomidaAPI", "Menu", "AllergenImage", "DishTypeImage", "Location", "Ingredient", "APIException", "Dish", "Allergen", "Customer", "Request", __version__, __version_info__
)
