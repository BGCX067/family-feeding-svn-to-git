from feeding_modules . application_logic import application_logic
from feeding_modules . calculate_convertible_units_ratings import calculate_convertible_units_ratings
from feeding_modules . calculate_prices import calculate_prices
from feeding_modules . calculate_units_ratio import calculate_units_ratio
from feeding_modules . calculate_weekly_ingredient_amount import calculate_weekly_ingredient_amount
from feeding_modules . consts import consts
from feeding_modules . dishes_by_weekday_storage import dishes_by_weekday_storage
from feeding_modules . find_largest_convertible_unit import find_largest_convertible_unit
from feeding_modules . find_smallest_convertible_unit import find_smallest_convertible_unit
from feeding_modules . find_weekly_ingredients import find_weekly_ingredients
from feeding_modules . format_dishes_diff import format_dishes_diff
from feeding_modules . format_dishes_prices import format_dishes_prices
from feeding_modules . format_distinct_dishes import format_distinct_dishes
from feeding_modules . format_ingredients_amount import format_ingredients_amount
from feeding_modules . format_ingredients_diff import format_ingredients_diff
from feeding_modules . format_units_amount import format_units_amount
from feeding_modules . format_week_report import format_week_report
from feeding_modules . ingredients_by_department_storage import ingredients_by_department_storage
from feeding_modules . ingredients_by_dish_storage import ingredients_by_dish_storage
from feeding_modules . ingredients_prices_by_shop_storage import ingredients_prices_by_shop_storage
from feeding_modules . write_dishes_prices import write_dishes_prices
from feeding_modules . write_weekly_ingredients_prices import write_weekly_ingredients_prices

import re

class facade :
    def __init__ ( self ) :
        self . _create_modules ( )
        self . _link_modules ( )
    def run ( self ) :
        self . _application_logic . run ( )
    def _create_modules ( self ) :
        self . _application_logic = application_logic ( )
        self . _calculate_convertible_units_ratings = calculate_convertible_units_ratings ( )
        self . _calculate_prices = calculate_prices ( )
        self . _calculate_units_ratio = calculate_units_ratio ( )
        self . _calculate_weekly_ingredient_amount = calculate_weekly_ingredient_amount ( )
        self . _consts = consts ( )
        self . _dishes_by_weekday_storage = dishes_by_weekday_storage ( )
        self . _find_largest_convertible_unit = find_largest_convertible_unit ( )
        self . _find_smallest_convertible_unit = find_smallest_convertible_unit ( )
        self . _find_weekly_ingredients = find_weekly_ingredients ( )
        self . _format_dishes_diff = format_dishes_diff ( )
        self . _format_dishes_prices = format_dishes_prices ( )
        self . _format_distinct_dishes = format_distinct_dishes ( )
        self . _format_ingredients_amount = format_ingredients_amount ( )
        self . _format_ingredients_diff = format_ingredients_diff ( )
        self . _format_units_amount = format_units_amount ( )
        self . _format_week_report = format_week_report ( )
        self . _ingredients_by_department_storage = ingredients_by_department_storage ( )
        self . _ingredients_by_dish_storage = ingredients_by_dish_storage ( )
        self . _ingredients_prices_by_shop_storage = ingredients_prices_by_shop_storage ( )
        self . _re = re
        self . _write_dishes_prices = write_dishes_prices ( )
        self . _write_weekly_ingredients_prices = write_weekly_ingredients_prices ( )
    def _link_modules ( self ) :
        self . _application_logic . set_modules \
            ( dishes_by_weekday_storage = self . _dishes_by_weekday_storage 
            , format_dishes_prices = self . _format_dishes_prices
            , format_week_report = self . _format_week_report
            , ingredients_by_department_storage = self . _ingredients_by_department_storage
            , ingredients_by_dish_storage = self . _ingredients_by_dish_storage
            , ingredients_prices_by_shop_storage = self . _ingredients_prices_by_shop_storage
            , write_dishes_prices = self . _write_dishes_prices
            , write_weekly_ingredients_prices = self . _write_weekly_ingredients_prices
            )
        self . _calculate_convertible_units_ratings . set_modules \
            ( consts = self . _consts
            )
        self . _calculate_prices . set_modules \
            ( calculate_units_ratio = self . _calculate_units_ratio
            , find_smallest_convertible_unit = self . _find_smallest_convertible_unit
            , ingredients_prices_by_shop_storage = self . _ingredients_prices_by_shop_storage
            )
        self . _calculate_units_ratio . set_modules \
            ( consts = self . _consts
            )
        self . _calculate_weekly_ingredient_amount . set_modules \
            ( calculate_units_ratio = self . _calculate_units_ratio
            , consts = self . _consts
            , dishes_by_weekday_storage = self . _dishes_by_weekday_storage
            , find_smallest_convertible_unit = self . _find_smallest_convertible_unit
            , ingredients_by_dish_storage = self . _ingredients_by_dish_storage
            )
        self . _dishes_by_weekday_storage . set_modules \
            ( consts = self . _consts
            , re = self . _re
            )
        self . _find_largest_convertible_unit . set_modules \
            ( calculate_convertible_units_ratings = self . _calculate_convertible_units_ratings
            )
        self . _find_smallest_convertible_unit . set_modules \
            ( calculate_convertible_units_ratings = self . _calculate_convertible_units_ratings
            )
        self . _find_weekly_ingredients . set_modules \
            ( dishes_by_weekday_storage = self . _dishes_by_weekday_storage
            , ingredients_by_dish_storage = self . _ingredients_by_dish_storage
            )
        self . _format_dishes_diff . set_modules \
            ( consts = self . _consts
            , dishes_by_weekday_storage = self . _dishes_by_weekday_storage
            , ingredients_by_dish_storage = self . _ingredients_by_dish_storage
            )
        self . _format_dishes_prices . set_modules \
            ( calculate_prices = self . _calculate_prices
            , calculate_units_ratio = self . _calculate_units_ratio
            , consts = self . _consts
            , find_smallest_convertible_unit = self . _find_smallest_convertible_unit
            , format_units_amount = self . _format_units_amount
            , ingredients_by_dish_storage = self . _ingredients_by_dish_storage
            )
        self . _format_distinct_dishes . set_modules \
            ( consts = self . _consts
            , dishes_by_weekday_storage = self . _dishes_by_weekday_storage
            ) 
        self . _format_ingredients_amount . set_modules \
            ( calculate_prices = self . _calculate_prices
            , calculate_weekly_ingredient_amount = self . _calculate_weekly_ingredient_amount
            , consts = self . _consts
            , find_weekly_ingredients = self . _find_weekly_ingredients
            , format_units_amount = self . _format_units_amount
            , ingredients_by_department_storage = self . _ingredients_by_department_storage
            )
        self . _format_ingredients_diff . set_modules \
            ( consts = self . _consts
            , ingredients_by_department_storage = self . _ingredients_by_department_storage
            , ingredients_by_dish_storage = self . _ingredients_by_dish_storage
            , ingredients_prices_by_shop_storage = self . _ingredients_prices_by_shop_storage
            )
        self . _format_units_amount . set_modules \
            ( calculate_units_ratio = self . _calculate_units_ratio
            , consts = self . _consts
            , calculate_convertible_units_ratings = self . _calculate_convertible_units_ratings
            )
        self . _format_week_report . set_modules \
            ( consts = self . _consts
            , format_dishes_diff = self . _format_dishes_diff
            , format_distinct_dishes = self . _format_distinct_dishes
            , format_ingredients_amount = self . _format_ingredients_amount
            , format_ingredients_diff = self . _format_ingredients_diff
            )
        self . _ingredients_by_department_storage . set_modules \
            ( consts = self . _consts
            , re = self . _re
            )
        self . _ingredients_by_dish_storage . set_modules \
            ( consts = self . _consts
            , re = self . _re
            )
        self . _ingredients_prices_by_shop_storage . set_modules \
            ( consts = self . _consts
            , re = self . _re
            )
        self . _write_dishes_prices . set_modules \
            ( consts = self . _consts
            , format_dishes_prices = self . _format_dishes_prices
            )
        self . _write_weekly_ingredients_prices . set_modules \
            ( consts = self . _consts
            , format_week_report = self . _format_week_report
            )
