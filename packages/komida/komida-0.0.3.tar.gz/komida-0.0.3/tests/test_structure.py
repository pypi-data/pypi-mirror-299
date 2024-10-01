from datetime import datetime

from komida import KomidaAPI, Request, Location, Customer


def test_example():
    api = KomidaAPI()
    my_request = Request(Location.MIDDELHEIM, Customer.ANTWERPEN, datetime(2024, 10, 1))
    menu = api.get_menu(my_request)
    assert len(menu.dishes) == 11
    assert menu.contains_dish("chicken")
