from datetime import datetime

from komida import KomidaAPI, Request, Location, Customer


def test_example():
    api = KomidaAPI()
    my_request = Request(Location.MIDDELHEIM, Customer.ANTWERPEN, datetime(2024, 5, 15))
    data = api.get(my_request)
    menu = api.get_menu(data)
    assert len(menu.dishes) == 11

