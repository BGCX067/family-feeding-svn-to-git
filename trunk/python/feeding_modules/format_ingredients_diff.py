class format_ingredients_diff :
    def __init__ ( self ) :
        self . _consts = None
        self . _ingredients_by_department_storage = None
        self . _ingredients_by_dish_storage = None
        self . _ingredients_prices_by_shop_storage = None
    def set_modules \
        ( self 
        , consts 
        , ingredients_by_department_storage
        , ingredients_by_dish_storage 
        , ingredients_prices_by_shop_storage 
        ) :
        self . _consts = consts
        self . _ingredients_by_department_storage = ingredients_by_department_storage
        self . _ingredients_by_dish_storage = ingredients_by_dish_storage
        self . _ingredients_prices_by_shop_storage = ingredients_prices_by_shop_storage
    def run ( self ) :
        result = [ ]

        departments_ingredients = self . _ingredients_by_department_storage . all_ingredients ( )
        dishes_ingredients = self . _ingredients_by_dish_storage . all_ingredients ( )
        prices_ingredients = self . _ingredients_prices_by_shop_storage . all_ingredients ( )

        dishes_ingredients_with_prices = dishes_ingredients . intersection ( prices_ingredients )
        dishes_ingredients_without_prices = dishes_ingredients . difference ( dishes_ingredients_with_prices )
        prices_ingredients_without_dishes = prices_ingredients . difference ( dishes_ingredients_with_prices )

        dishes_ingredients_with_departments = dishes_ingredients . intersection ( departments_ingredients )
        departments_ingredients_without_dishes = departments_ingredients . difference ( dishes_ingredients_with_departments )

        if len ( dishes_ingredients_without_prices ) > 0 :
            result += [ str ( ) ]
            result += [ self . _consts . ingredients_without_prices ]
            for ingredient in sorted ( list ( dishes_ingredients_without_prices ) ) :
                result += [ self . _consts . wiki_list + ingredient ]
        if len ( prices_ingredients_without_dishes ) > 0 :
            result += [ str ( ) ]
            result += [ self . _consts . prices_without_dishes ]
            for ingredient in sorted ( list ( prices_ingredients_without_dishes ) ) :
                result += [ self . _consts . wiki_list + ingredient ]
        if len ( departments_ingredients_without_dishes ) > 0 :
            result += [ str ( ) ]
            result += [ self . _consts . departments_without_dishes ]
            for ingredient in sorted ( list ( departments_ingredients_without_dishes ) ) :
                result += [ self . _consts . wiki_list + ingredient ]
        return result

