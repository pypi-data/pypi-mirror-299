"""
Handles parsing arguments and passing them to the correct places when launching the application.
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import simplejson as json
import arklog
import logging

from thefuzz import fuzz, process

from komida import __version__
import urllib.request


class APIException(Exception):
    def __init__(self, error):
        message = f"{error}" if error else "Shit's fucked."
        super().__init__(message)


class Location(Enum):
    STADSCAMPUS = 8198
    MIDDELHEIM = 8199
    GROENENBORGER = 8200
    DRIE_EIKEN = 8201
    ONLINE = 9038


class Customer(Enum):
    ANTWERPEN = 7622


@dataclass
class Request:
    """"""
    location: Location = Location.MIDDELHEIM
    customer: Customer = Customer.ANTWERPEN
    date: datetime = field(default_factory=datetime.now)

    def as_parameters(self) -> dict:
        return {
            "locationId": self.location.value,
            "customerId": self.customer.value,
            "stringDate": self.date.strftime("%Y-%m-%d")
        }


@dataclass(frozen=True)
class Allergen:
    pass


@dataclass(frozen=True)
class DishTypeImage:
    komida_uri: str

    def get_component(self) -> str:
        return self.komida_uri.split("/")[-1].split(".")[0].lower()


@dataclass(frozen=True)
class AllergenImage:
    komida_uri: str

    def get_component(self) -> str:
        return self.komida_uri.split("/")[-1].split(".")[0].lower()


@dataclass(frozen=True)
class Ingredient:
    name: str
    ingredients: list[str] = field(default_factory=list)
    allergen_names: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class Dish:
    id: int
    location: Location
    customer: Customer
    date: datetime
    menu_item_id: int
    quantity: int
    section_name: str
    menu_name: str
    menu_name_en: str
    menu_unit_code: str
    real_food_cost: float
    gross_margin: float
    extra_cost: float
    event_planner_id: int
    has_invoice: bool
    status: int
    take_away_price_gross: float
    delivery_price_gross: float
    selling_price_gross: float
    menu_pos_id: str
    all_allergens: bool  # Not Sure
    section_order: int
    menu_order: int
    is_sub_recipe: bool
    menu_yeld: int  # Not Sure
    location_name: str
    ingredients: list[Ingredient] = field(default_factory=list)
    dish_type_images: list[DishTypeImage] = field(default_factory=list)
    allergen_images: list[AllergenImage] = field(default_factory=list)
    allergens: list[Allergen] = field(default_factory=list)


@dataclass(frozen=True)
class Menu:
    """"""
    dishes: list[Dish] = field(default_factory=list)

    def contains_dish(self, dish: Dish | str, threshold_ratio: int = 80) -> bool:
        if isinstance(dish, Dish):
            return dish in self.dishes
        dish_names = [d.menu_name.lower() for d in self.dishes]
        dish_names_en = [d.menu_name_en.lower() for d in self.dishes]
        extracted, certainty = process.extractOne(dish.lower(), dish_names + dish_names_en)
        return certainty >= threshold_ratio


class KomidaAPI:

    def __init__(self, **kwargs):
        """"""
        self.logger = logging.getLogger(__name__)
        config = {
            "version": 1, "incremental": False, "disable_existing_loggers": True,
            "formatters": {"color": {"()": "arklog.ColorFormatter", "format": "%(message)s"}},
            "handlers": {"console": {"class": "logging.StreamHandler", "level": "DEBUG", "formatter": "color"}},
            "root": {"level": "INFO", "handlers": ["console"], "propagate": True},
            "loggers": {__name__: {"level": "DEBUG", "handlers": ["console"], "propagate": False}},
        }
        config = kwargs.get("config", config)
        arklog.set_config_logging(config)
        self.logger.debug(f"Komida {__version__}.")
        self.base_uri = kwargs.get("base_uri", "https://app.growzer.be/MenuPlanner/GetMenuPlanner")

    def download_menu_data(self, request: Request) -> dict:
        """"""
        options = "&".join("{}={}".format(*p) for p in request.as_parameters().items())
        with urllib.request.urlopen(f"{self.base_uri}?{options}") as url:
            data = json.load(url)
            if not data.get("success"):
                raise APIException(data.get("error"))
            self.logger.debug(data)
            return data.get("data")

    @staticmethod
    def parse_dish(dish: dict) -> Dish:
        return Dish(
            id=dish.get("Id"),
            location=dish.get("LocationId"),
            customer=dish.get("CustomerId"),
            # date= datetime.fromtimestamp(int(dish.get("Date").split("(")[-1].split(")")[0])),
            date=dish.get("Date").split("(")[-1].split(")")[0],
            menu_item_id=dish.get("MenuItemId"),
            quantity=dish.get("Quantity"),
            section_name=dish.get("SectionName"),
            menu_name=dish.get("MenuName"),
            menu_name_en=dish.get("MenuNameEN"),
            menu_unit_code=dish.get("MenuUnitCode"),
            real_food_cost=dish.get("RealFoodCost"),
            gross_margin=dish.get("GrossMargin"),
            extra_cost=dish.get("ExtraCost"),
            event_planner_id=dish.get("EventPlannerId"),
            has_invoice=dish.get("HasInvoice"),
            status=dish.get("Status"),
            take_away_price_gross=dish.get("TakeawayPriceGross"),
            delivery_price_gross=dish.get("DeliveryPriceGross"),
            selling_price_gross=dish.get("SellingPriceGross"),
            menu_pos_id=dish.get("MenuPosId"),
            all_allergens=dish.get("AllAllergens"),  # TODO
            section_order=dish.get("SectionOrder"),
            menu_order=dish.get("MenuOrder"),
            is_sub_recipe=dish.get("IsSubrecipe"),
            menu_yeld=dish.get("MenuYeld"),
            location_name=dish.get("LocationName"),
            ingredients=[
                Ingredient(ingredient.get("Name"), ingredient.get("Ingredients"), ingredient.get("AllergenNames")) for
                ingredient in dish.get("Ingredients", [])],
            dish_type_images=[DishTypeImage(uri) for uri in dish.get("DishTypeImages", [])],
            allergen_images=[AllergenImage(uri) for uri in dish.get("AllergenImages", [])],
            allergens=[],  # TODO
        )

    def get_menu(self, request: Request) -> Menu:
        menu_planner = self.download_menu_data(request).get("menuPlannerList")
        dishes = [self.parse_dish(dish) for dish in menu_planner]
        return Menu(dishes=dishes)
