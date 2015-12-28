class application_logic :
    def __init__ ( self ) :
        self . _dishes_by_weekday_storage = None
        self . _format_dishes_prices = None
        self . _format_week_report = None
        self . _ingredients_by_department_storage = None
        self . _ingredients_by_dish_storage = None
        self . _ingredients_prices_by_shop_storage = None
        self . _write_dishes_prices = None
        self . _write_weekly_ingredients_prices = None
    def set_modules \
        ( self
        , dishes_by_weekday_storage 
        , format_dishes_prices
        , format_week_report
        , ingredients_by_department_storage
        , ingredients_by_dish_storage
        , ingredients_prices_by_shop_storage
        , write_dishes_prices
        , write_weekly_ingredients_prices
        ) :
        self . _dishes_by_weekday_storage = dishes_by_weekday_storage
        self . _format_dishes_prices = format_dishes_prices
        self . _format_week_report = format_week_report
        self . _ingredients_by_department_storage = ingredients_by_department_storage
        self . _ingredients_by_dish_storage = ingredients_by_dish_storage
        self . _ingredients_prices_by_shop_storage = ingredients_prices_by_shop_storage
        self . _write_dishes_prices = write_dishes_prices
        self . _write_weekly_ingredients_prices = write_weekly_ingredients_prices
    def run ( self ) :
        self . _dishes_by_weekday_storage . load ( )
        self . _ingredients_by_department_storage . load ( )
        self . _ingredients_by_dish_storage . load ( )
        self . _ingredients_prices_by_shop_storage . load ( )
        for line in self . _format_week_report . run ( ) :
            print line
        print str ( )
        for line in self . _format_dishes_prices . run ( ) :
            print line
        self . _write_weekly_ingredients_prices . run ( )
        self . _write_dishes_prices . run ( )

