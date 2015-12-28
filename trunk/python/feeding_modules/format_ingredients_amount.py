class format_ingredients_amount :
    def __init__ ( self ) :
        self . _calculate_prices = None
        self . _calculate_weekly_ingredient_amount = None
        self . _consts = None
        self . _find_weekly_ingredients = None
        self . _format_units_amount = None
        self . _ingredient = None
        self . _ingredient_format = None
        self . _ingredients_by_department_storage = None
        self . _output = None
        self . _price_max_format = None
        self . _price_min_format = None
        self . _price_unit = None
        self . _total_price_max = None
        self . _total_price_max_format = None
        self . _total_price_min = None
        self . _total_price_min_format = None
    def set_modules \
        ( self 
        , calculate_prices
        , calculate_weekly_ingredient_amount
        , consts
        , find_weekly_ingredients
        , format_units_amount
        , ingredients_by_department_storage
        ) :
        self . _calculate_prices = calculate_prices
        self . _calculate_weekly_ingredient_amount = calculate_weekly_ingredient_amount
        self . _consts = consts
        self . _find_weekly_ingredients = find_weekly_ingredients
        self . _format_units_amount = format_units_amount
        self . _ingredients_by_department_storage = ingredients_by_department_storage
    def run ( self ) :
        self . _output = [ ]
        self . _append_top_header ( )
        self . _append_all_ingredients ( )
        self . _append_total_price ( )
        return self . _output
    def _append_all_ingredients ( self ) :
        self . _total_price_min = float ( 0 )
        self . _total_price_max = float ( 0 )
        self . _price_unit = str ( )
        weekly_ingredients = self . _find_weekly_ingredients . run ( )
        ingredients_by_department = { }
        for ingredient in weekly_ingredients :
            department = self . _ingredients_by_department_storage . department ( ingredient )
            if len ( department ) == 0 :
                department = self . _consts . no_department
            if department not in ingredients_by_department :
                ingredients_by_department [ department ] = [ ]
            ingredients_by_department [ department ] += [ ingredient ]
        for department in sorted ( ingredients_by_department . keys ( ) ) :
            self . _output += [ str ( ) ]
            self . _output += \
                [ self . _consts . wiki_subheader
                + self . _consts . whitespace
                + department
                + self . _consts . whitespace
                + self . _consts . wiki_subheader
                ]
            self . _output += [ self . _consts . ingredients_for_a_week_table_title ]
            for self . _ingredient in ingredients_by_department [ department ] :
                self . _calculate_ingredient ( )
                self . _append_ingredient ( )
    def _calculate_ingredient ( self ) :
        self . _calculate_weekly_ingredient_amount . run ( self . _ingredient )
        unit = self . _calculate_weekly_ingredient_amount . unit ( )
        amount = self . _calculate_weekly_ingredient_amount . amount ( )
        self . _calculate_prices . run ( self . _ingredient , amount , unit )
        self . _price_unit = self . _calculate_prices . price_unit ( )
        self . _ingredient_format = self . _format_units_amount . run ( unit , amount )
    def _append_ingredient ( self ) :
        prices = self . _calculate_prices . prices ( )
        if len ( prices ) > 0 :
            price_min = min ( prices )
            price_max = max ( prices )
            self . _total_price_min += price_min
            self . _total_price_max += price_max
            self . _price_min_format = self . _format_units_amount . run ( self . _price_unit , price_min )
            self . _price_max_format = self . _format_units_amount . run ( self . _price_unit , price_max )
            if price_min == price_max :
                self . _append_row_ingredient_price ( )
            else :
                self . _append_row_ingredient_price_min_max ( )
        else :
            self . _append_row_ingredient_no_price ( )
    def _append_total_price ( self ) :
        self . _output += [ str ( ) ]
        self . _total_price_min_format = self . _format_units_amount . run ( self . _price_unit , self . _total_price_min )
        self . _total_price_max_format = self . _format_units_amount . run ( self . _price_unit , self . _total_price_max )
        if self . _total_price_min == self . _total_price_max :
            self . _append_row_total_price ( )
        else :
            self . _append_row_total_price_min_max ( )
    def _append_top_header ( self ) :
        self . _output += [ self . _consts . ingredients_for_a_week_header ]
    def _append_row_total_price ( self ) :
        self . _output += [ unicode \
            ( self . _consts . total_price
            + self . _consts . whitespace
            + self . _consts . wiki_bold
            + self . _total_price_min_format 
            + self . _consts . wiki_bold
            ) ]
    def _append_row_total_price_min_max ( self ) :
        self . _output += [ unicode \
            ( self . _consts . total_price
            + self . _consts . whitespace
            + self . _consts . price_from
            + self . _consts . whitespace
            + self . _consts . wiki_bold
            + self . _total_price_min_format 
            + self . _consts . wiki_bold
            + self . _consts . whitespace
            + self . _consts . price_to 
            + self . _consts . whitespace
            + self . _consts . wiki_bold
            + self . _total_price_max_format
            + self . _consts . wiki_bold
            ) ]
    def _append_row_ingredient_price ( self ) :
        self . _output += [ unicode \
            ( self . _consts . wiki_table
            + self . _consts . whitespace 
            + self . _ingredient 
            + self . _consts . whitespace 
            + self . _consts . wiki_table
            + self . _consts . whitespace 
            + self . _ingredient_format
            + self . _consts . whitespace 
            + self . _consts . wiki_table
            + self . _consts . whitespace 
            + self . _price_min_format
            + self . _consts . whitespace 
            + self . _consts . wiki_table
            + self . _consts . whitespace 
            + self . _consts . wiki_table
            ) ]
    def _append_row_ingredient_price_min_max ( self ) :
        self . _output += [ unicode \
            ( self . _consts . wiki_table
            + self . _consts . whitespace 
            + self . _ingredient
            + self . _consts . whitespace
            + self . _consts . wiki_table
            + self . _consts . whitespace
            + self . _ingredient_format
            + self . _consts . whitespace
            + self . _consts . wiki_table
            + self . _consts . whitespace
            + self . _price_min_format
            + self . _consts . whitespace
            + self . _consts . wiki_table
            + self . _consts . whitespace
            + self . _price_max_format
            + self . _consts . whitespace
            + self . _consts . wiki_table
            ) ]
    def _append_row_ingredient_no_price ( self ) :
        self . _output += [ unicode \
            ( self . _consts . wiki_table
            + self . _consts . whitespace 
            + self . _ingredient
            + self . _consts . whitespace
            + self . _consts . wiki_table
            + self . _consts . whitespace
            + self . _ingredient_format
            + self . _consts . whitespace
            + self . _consts . wiki_table
            + self . _consts . whitespace
            + self . _consts . wiki_bold
            + self . _consts . no_price
            + self . _consts . wiki_bold
            + self . _consts . whitespace
            + self . _consts . wiki_table
            + self . _consts . whitespace
            + self . _consts . wiki_table
            ) ]

