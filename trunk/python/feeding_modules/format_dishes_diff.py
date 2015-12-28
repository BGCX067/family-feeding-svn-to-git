class format_dishes_diff :
    def __init__ ( self ) :
        self . _consts = None
        self . _dishes_by_weekday_storage = None
        self . _ingredients_by_dish_storage = None
    def set_modules ( self , consts , dishes_by_weekday_storage , ingredients_by_dish_storage ) :
        self . _consts = consts
        self . _dishes_by_weekday_storage = dishes_by_weekday_storage
        self . _ingredients_by_dish_storage = ingredients_by_dish_storage
    def run ( self ) :
        result = [ ]
        weekday_dishes = self . _dishes_by_weekday_storage . distinct_dishes ( )
        ingredients_dishes = self . _ingredients_by_dish_storage . all_dishes ( )
        correct_dishes = weekday_dishes . intersection ( ingredients_dishes )
        dishes_without_ingredients = weekday_dishes . difference ( correct_dishes )
        if len ( dishes_without_ingredients ) > 0 :
            result += [ str ( ) ]
            result += [ self . _consts . dishes_without_ingredients ]
            for dish in sorted ( list ( dishes_without_ingredients ) ) :
                result += [ self . _consts . wiki_list + dish ]
        return result

