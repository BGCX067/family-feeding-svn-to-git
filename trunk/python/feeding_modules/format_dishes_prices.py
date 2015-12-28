class format_dishes_prices :
    def __init__ ( self ) :
        self . _calculate_prices = None
        self . _calculate_units_ratio = None
        self . _consts = None
        self . _find_smallest_convertible_unit = None
        self . _format_units_amount = None
        self . _ingredients_by_dish_storage = None
        self . _lines = None
        self . _current_dish = None
        self . _current_ingredient = None
        self . _current_ingredient_unit_amount_format = None
        self . _current_ingredient_prices = None
        self . _current_ingredient_price_unit = None
        self . _current_ingredient_price_min_format = None
        self . _current_ingredient_price_max_format = None
        self . _dish_price_min = None
        self . _dish_price_max = None
        self . _dish_price_unit = None
        self . _dish_price_min_format = None
        self . _dish_price_max_format = None
    def set_modules \
        ( self
        , calculate_prices
        , calculate_units_ratio
        , consts
        , find_smallest_convertible_unit
        , format_units_amount
        , ingredients_by_dish_storage
        ) :
        self . _calculate_prices = calculate_prices
        self . _calculate_units_ratio = calculate_units_ratio
        self . _consts = consts
        self . _find_smallest_convertible_unit = find_smallest_convertible_unit
        self . _format_units_amount = format_units_amount
        self . _ingredients_by_dish_storage = ingredients_by_dish_storage
    def run ( self ) :
        self . _lines = [ ]
        self . _add_starting_stuff ( )
        self . _add_dishes ( )
        return self . _lines
    def _add_starting_stuff ( self ) :
        self . _lines += [ self . _consts . dishes_prices_summary ]
        self . _lines += [ self . _consts . wiki_labels ]
        self . _lines += [ self . _consts . wiki_side_bar_navigation ]
        self . _lines += [ str ( ) ]
        self . _lines += [ self . _consts . wiki_table_of_contents ]
        self . _lines += [ str ( ) ]
    def _add_dishes ( self ) :
        for self . _current_dish in sorted ( self . _ingredients_by_dish_storage . all_dishes ( ) ) :
            self . _add_dish ( )
    def _add_dish ( self ) :
        self . _add_dish_header ( )
        self . _add_empty_line ( )
        self . _add_table_header ( )
        self . _reset_dish_prices ( )
        for self . _current_ingredient in sorted ( self . _current_dish_ingredients ( ) ) :
            self . _calculate_ingredient_unit_amount ( )
            self . _calculate_ingredient_prices ( )
            self . _format_ingredient_unit_amount ( )
            self . _format_ingredient_prices ( )
            self . _count_dish_prices ( )
            self . _add_table_row ( )
        self . _add_dish_prices ( )
        self . _add_empty_line ( )
    def _add_dish_prices ( self ) :
        if self . _dish_price_min > float ( 0 ) :
            self . _add_empty_line ( )
            self . _format_dish_prices ( )
            if self . _dish_price_min_format == self . _dish_price_max_format :
                self . _add_dish_price_min ( )
            else :
                self . _add_dish_prices_min_max ( )
    def _add_dish_price_min ( self ) :
        self . _lines += \
            [ self . _consts . total_price
            + self . _consts . whitespace
            + self . _consts . wiki_bold
            + self . _dish_price_min_format
            + self . _consts . wiki_bold
            ]
    def _add_dish_prices_min_max ( self ) :
        self . _lines += \
            [ self . _consts . total_price
            + self . _consts . whitespace
            + self . _consts . price_from
            + self . _consts . whitespace
            + self . _consts . wiki_bold
            + self . _dish_price_min_format
            + self . _consts . wiki_bold
            + self . _consts . whitespace
            + self . _consts . price_to
            + self . _consts . whitespace
            + self . _consts . wiki_bold
            + self . _dish_price_max_format
            + self . _consts . wiki_bold
            ]
    def _reset_dish_prices ( self ) :
        self . _dish_price_min = float ( 0 )
        self . _dish_price_max = float ( 0 )
        self . _dish_price_unit = str ( )
    def _count_dish_prices ( self ) :
        if len ( self . _current_ingredient_prices ) > 0 :
            self . _dish_price_min += min ( self . _current_ingredient_prices )
            self . _dish_price_max += max ( self . _current_ingredient_prices )
            self . _dish_price_unit = self . _current_ingredient_price_unit
    def _format_dish_prices ( self ) :
        if self . _dish_price_min > float ( 0 ) :
            self . _dish_price_min_format = self . _format_units_amount . run ( self . _dish_price_unit , self . _dish_price_min ) 
        if self . _dish_price_max > float ( 0 ) :
            self . _dish_price_max_format = self . _format_units_amount . run ( self . _dish_price_unit , self . _dish_price_max ) 
    def _add_dish_header ( self ) :
        dish_to_print = self . _current_dish [ 0 ] . upper ( ) + self . _current_dish [ 1 : ]
        self . _lines += [ self . _consts . wiki_header_format % dish_to_print ]
    def _add_empty_line ( self ) :
        self . _lines += [ str ( ) ]
    def _add_table_header ( self ) :
        self . _lines += [ self . _consts . dishes_prices_table_title ]
    def _current_dish_ingredients ( self ) :
        return self . _ingredients_by_dish_storage . dish_ingredients ( self . _current_dish )
    def _calculate_ingredient_unit_amount ( self ) :
        self . _current_ingredient_unit = str ( )
        self . _current_ingredient_amount = float ( 0 )
        for unit , amount in self . _current_ingredient_unit_amount ( ) :
            self . _current_ingredient_unit = self . _find_smallest_convertible_unit . run ( unit )
            self . _current_ingredient_amount += self . _calculate_units_ratio . run ( amount , unit , float ( 1 ) , self . _current_ingredient_unit )
    def _current_ingredient_unit_amount ( self ) :
        return self . _ingredients_by_dish_storage . dish_ingredient_unit_amount ( self . _current_dish , self . _current_ingredient ) . items ( )
    def _format_ingredient_unit_amount ( self ) :
        self . _current_ingredient_unit_amount_format = self . _format_units_amount . run ( self . _current_ingredient_unit , self . _current_ingredient_amount )
    def _calculate_ingredient_prices ( self ) :
        self . _calculate_prices . run ( self . _current_ingredient , self . _current_ingredient_amount , self . _current_ingredient_unit )
        self . _current_ingredient_prices = self . _calculate_prices . prices ( )
        self . _current_ingredient_price_unit = self . _calculate_prices . price_unit ( )
    def _format_ingredient_prices ( self ) :
        if len ( self . _current_ingredient_prices ) > 0 :
            price_min = min ( self . _current_ingredient_prices )
            price_max = max ( self . _current_ingredient_prices )
            self . _current_ingredient_price_min_format = self . _format_units_amount . run ( self . _current_ingredient_price_unit , price_min )
            self . _current_ingredient_price_max_format = self . _format_units_amount . run ( self . _current_ingredient_price_unit , price_max )
        else :
            price_format = self . _consts . wiki_bold + self . _consts . no_price + self . _consts . wiki_bold
            self . _current_ingredient_price_min_format = price_format
            self . _current_ingredient_price_max_format = price_format
    def _add_table_row ( self ) :
        if self . _current_ingredient_price_min_format == self . _current_ingredient_price_max_format :
            self . _add_table_row_min_price ( )
        else :
            self . _add_table_row_min_max_prices ( )
    def _add_table_row_min_price ( self ) :
        self . _lines += \
            [ self . _consts . wiki_table
            + self . _consts . whitespace
            + self . _current_ingredient
            + self . _consts . whitespace
            + self . _consts . wiki_table
            + self . _consts . whitespace
            + self . _current_ingredient_unit_amount_format
            + self . _consts . whitespace
            + self . _consts . wiki_table
            + self . _consts . whitespace
            + self . _current_ingredient_price_min_format
            + self . _consts . whitespace
            + self . _consts . wiki_table
            + self . _consts . whitespace
            + self . _consts . wiki_table
            ]
    def _add_table_row_min_max_prices ( self ) :
        self . _lines += \
            [ self . _consts . wiki_table
            + self . _consts . whitespace
            + self . _current_ingredient
            + self . _consts . whitespace
            + self . _consts . wiki_table
            + self . _consts . whitespace
            + self . _current_ingredient_unit_amount_format
            + self . _consts . whitespace
            + self . _consts . wiki_table
            + self . _consts . whitespace
            + self . _current_ingredient_price_min_format
            + self . _consts . whitespace
            + self . _consts . wiki_table
            + self . _consts . whitespace
            + self . _current_ingredient_price_max_format
            + self . _consts . whitespace
            + self . _consts . wiki_table
            ]

