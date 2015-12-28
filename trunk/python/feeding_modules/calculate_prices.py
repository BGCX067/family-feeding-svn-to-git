class calculate_prices :
    def __init__ ( self ) :
        self . _prices = None
        self . _price_unit = None
        self . _calculate_units_ratio = None
        self . _find_smallest_convertible_unit = None
        self . _ingredients_prices_by_shop_storage = None
    def set_modules \
        ( self 
        , calculate_units_ratio
        , find_smallest_convertible_unit
        , ingredients_prices_by_shop_storage
        ) :
        self . _calculate_units_ratio = calculate_units_ratio
        self . _find_smallest_convertible_unit = find_smallest_convertible_unit
        self . _ingredients_prices_by_shop_storage = ingredients_prices_by_shop_storage
    def run ( self , ingredient , ingredient_amount , ingredient_unit ) :
        self . _prices = [ ]
        self . _price_unit = str ( )
        ingredients_prices_by_shop = self . _ingredients_prices_by_shop_storage
        for shop_unit in ingredients_prices_by_shop . ingredient_units ( ingredient ) :
            for shop_amount in ingredients_prices_by_shop . ingredient_units_amount ( ingredient , shop_unit ) :
                if self . _calculate_units_ratio . run ( float ( 1 ) , ingredient_unit , float ( 1 ) , shop_unit ) > float ( 0 ) :
                    ratio = self . _calculate_units_ratio . run ( ingredient_amount , ingredient_unit , shop_amount , shop_unit )
                    for shop_price in ingredients_prices_by_shop . ingredient_unit_amount_prices ( ingredient , shop_unit , shop_amount ) :
                        price = float ( 0 )
                        for price_unit , price_amount in shop_price . items ( ) :
                            smallest_price_unit = self . _find_smallest_convertible_unit . run ( price_unit )
                            smallest_price_amount = self . _calculate_units_ratio . run ( price_amount , price_unit , float ( 1 ) , smallest_price_unit )
                            self . _price_unit = smallest_price_unit
                            price += smallest_price_amount * ratio
                        self . _prices += [ price ]
    def prices ( self ) :
        return list ( self . _prices )
    def price_unit ( self ) :
        return self . _price_unit
