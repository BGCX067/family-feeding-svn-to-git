class find_weekly_ingredients :
    def __init__ ( self ) :
        self . _dishes_by_weekday_storage = None
        self . _ingredients_by_dish_storage = None
    def set_modules \
        ( self
        , dishes_by_weekday_storage
        , ingredients_by_dish_storage 
        ) :
        self . _dishes_by_weekday_storage = dishes_by_weekday_storage
        self . _ingredients_by_dish_storage = ingredients_by_dish_storage
    def run ( self ) :
        ingredients = set ( )
        for weekday_dishes in self . _dishes_by_weekday_storage . all_dishes ( ) :
            for dish in weekday_dishes :
                ingredients = ingredients . union ( self . _ingredients_by_dish_storage . dish_ingredients ( dish ) )
        return sorted ( list ( ingredients ) )
