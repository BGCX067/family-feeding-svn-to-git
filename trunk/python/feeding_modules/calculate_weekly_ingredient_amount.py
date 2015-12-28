class calculate_weekly_ingredient_amount :
    def __init__ ( self ) :
        self . _unit = None
        self . _amount = None
        self . _calculate_units_ratio = None
        self . _consts = None
        self . _dishes_by_weekday_storage = None
        self . _find_smallest_convertible_unit = None
        self . _ingredients_by_dish_storage = None
    def set_modules \
        ( self
        , calculate_units_ratio
        , consts
        , dishes_by_weekday_storage 
        , find_smallest_convertible_unit
        , ingredients_by_dish_storage
        ) :
        self . _calculate_units_ratio = calculate_units_ratio
        self . _consts = consts
        self . _dishes_by_weekday_storage = dishes_by_weekday_storage
        self . _find_smallest_convertible_unit = find_smallest_convertible_unit
        self . _ingredients_by_dish_storage = ingredients_by_dish_storage
    def run ( self , ingredient ) :
        self . _unit = str ( )
        self . _amount = float ( 0 )
        dishes_by_weekday = self . _dishes_by_weekday_storage
        ingredients_by_dish = self . _ingredients_by_dish_storage
        for weekday_dishes in dishes_by_weekday . all_dishes ( ) :
            for dish in weekday_dishes :
                for dish_ingredient_unit , dish_ingredient_amount in ingredients_by_dish . dish_ingredient_unit_amount ( dish , ingredient ) . items ( ) :
                    unit = self . _find_smallest_convertible_unit . run ( dish_ingredient_unit )
                    if self . _unit != str ( ) and unit != self . _unit :
                        print self . _consts . invalid_units_in_dish , dish , ingredient , self . _unit , unit
                    else :
                        self . _unit = unit
                        self . _amount += self . _calculate_units_ratio . run ( dish_ingredient_amount , dish_ingredient_unit , float ( 1 ) , self . _unit )
    def unit ( self ) :
        return self . _unit
    def amount ( self ) :
        return self . _amount
