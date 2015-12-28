class ingredients_prices_by_shop_storage :
    def __init__ ( self ) :
        self . _ingredients_prices_by_shop = None
        self . _wiki_contents = None
        self . _current_shop = None
        self . _unicode_wiki_line = None
        self . _ingredient_match = None
        self . _ingredient_name = None
        self . _ingredient_amount = None
        self . _ingredient_unit = None
        self . _ingredient_price1 = None
        self . _ingredient_price_unit1 = None
        self . _ingredient_price2 = None
        self . _ingredient_price_unit2 = None
        self . _consts = None
        self . _re = None
    def set_modules ( self , consts , re ) :
        self . _consts = consts
        self . _re = re
    def get ( self ) :
        return self . _ingredients_prices_by_shop
    def ingredient_units ( self , ingredient ) :
        units = set ( )
        for shop , ingredients in self . _ingredients_prices_by_shop . items ( ) :
            if ingredient in ingredients :
                for unit in ingredients [ ingredient ] . keys ( ) :
                    units . add ( unit )
        return list ( units )
    def ingredient_units_amount ( self , ingredient , unit ) :
        amounts = set ( )
        for shop , ingredients in self . _ingredients_prices_by_shop . items ( ) :
            if ingredient in ingredients :
                if unit in ingredients [ ingredient ] :
                    for amount in ingredients [ ingredient ] [ unit ] . keys ( ) :
                        amounts . add ( amount )
        return list ( amounts )
    def ingredient_unit_amount_prices ( self , ingredient , unit , amount ) :
        prices = [ ]
        for shop , ingredients in self . _ingredients_prices_by_shop . items ( ) :
            if ingredient in ingredients :
                if unit in ingredients [ ingredient ] :
                    if amount in ingredients [ ingredient ] [ unit ] :
                        prices += ingredients [ ingredient ] [ unit ] [ amount ]
        return prices
    def all_ingredients ( self ) :
        ingredients = set ( )
        for shop , shop_ingredients in self . _ingredients_prices_by_shop . items ( ) :
            ingredients = ingredients . union ( shop_ingredients . keys ( ) )
        return ingredients
    def load ( self ) :
        self . _load_wiki_contents ( )
        self . _parse_wiki_contents ( )
    def _parse_wiki_contents ( self ) :
        self . _reset_parser ( )
        for wiki_line in self . _wiki_contents :
            self . _decode_line ( wiki_line )
            self . _parse_shop_name ( )
            self . _parse_ingredient_price ( )
    def _load_wiki_contents ( self ) :
        wiki_file_name = self . _consts . wiki_path + self . _consts . ingredients_prices_by_shop_file_name + self . _consts . dot_wiki
        try :
            self . _wiki_contents = open ( wiki_file_name , self . _consts . open_file_for_read ) . readlines ( )
        except IOError :
            self . _wiki_contents = [ ]
    def _reset_parser ( self ) :
        self . _ingredients_prices_by_shop = { }
        self . _current_shop = unicode ( )
    def _decode_line ( self , line ) :
        self . _unicode_wiki_line = line . decode ( self . _consts . utf8 )
    def _parse_shop_name ( self ) :
        match = self . _re . match ( self . _consts . header_regexp , self . _unicode_wiki_line , self . _re . UNICODE )
        if match :
            self . _current_shop = match . group ( 1 ) . lower ( )
            if self . _current_shop not in self . _ingredients_prices_by_shop :
                self . _ingredients_prices_by_shop [ self . _current_shop ] = { }
    def _parse_ingredient_price ( self ) :
        self . _match_ingredient_price_regexp ( )
        if self . _ingredient_price_matched ( ) :
            self . _unpack_ingredient_match_groups ( )
            self . _store_ingredient ( )
    def _match_ingredient_price_regexp ( self ) :
        self . _ingredient_match = self . _re . match ( self . _consts . ingredient_price_list_regexp , self . _unicode_wiki_line , self . _re . UNICODE )
    def _ingredient_price_matched ( self ) :
        if self . _ingredient_match :
            return True
        else :
            return False
    def _unpack_ingredient_match_groups ( self ) :
        self . _ingredient_name = self . _ingredient_match . groups ( ) [ 0 ] . lower ( )
        self . _ingredient_amount = float ( self . _ingredient_match . groups ( ) [ 1 ] )
        self . _ingredient_unit = self . _ingredient_match . groups ( ) [ 2 ] . lower ( )
        self . _ingredient_price1 = int ( self . _ingredient_match . groups ( ) [ 3 ] )
        self . _ingredient_price_unit1 = self . _ingredient_match . groups ( ) [ 4 ] . lower ( )
        if self . _ingredient_match . groups ( ) [ 5 ] != None :
            self . _ingredient_price2 = int ( self . _ingredient_match . groups ( ) [ 5 ] )
            self . _ingredient_price_unit2 = self . _ingredient_match . groups ( ) [ 6 ] . lower ( )
        else :
            self . _ingredient_price2 = 0
            self . _ingredient_price_unit2 = unicode ( )
    def _store_ingredient ( self ) :
        if self . _ingredient_price_is_meaning ( ) :
            self . _store_ingredient_name ( )
            self . _store_ingredient_unit ( )
            self . _store_ingredient_amount ( )
            self . _store_ingredient_price ( )
    def _ingredient_price_is_meaning ( self ) :
        return self . _ingredient_price1 > 0 or self . _ingredient_price2 > 0
    def _store_ingredient_name ( self ) :
        if self . _ingredient_name not in self . _ingredients_prices_by_shop \
            [ self . _current_shop ] :
            self . _ingredients_prices_by_shop \
                [ self . _current_shop ] \
                [ self . _ingredient_name ] \
                = { }
    def _store_ingredient_unit ( self ) :
        if self . _ingredient_unit not in self . _ingredients_prices_by_shop \
            [ self . _current_shop ] \
            [ self . _ingredient_name ] :
            self . _ingredients_prices_by_shop \
                [ self . _current_shop ] \
                [ self . _ingredient_name ] \
                [ self . _ingredient_unit ] \
                = { }
    def _store_ingredient_amount ( self ) :
        if self . _ingredient_amount not in self . _ingredients_prices_by_shop \
            [ self . _current_shop ] \
            [ self . _ingredient_name ] \
            [ self . _ingredient_unit ] :
            self . _ingredients_prices_by_shop \
                [ self . _current_shop ] \
                [ self . _ingredient_name ] \
                [ self . _ingredient_unit ] \
                [ self . _ingredient_amount ] \
                = [ ]
    def _store_ingredient_price ( self ) :
        price_dict = { }
        if self . _ingredient_price1 > 0 :
            price_dict [ self . _ingredient_price_unit1 ] = self . _ingredient_price1
        if self . _ingredient_price2 > 0 :
            price_dict [ self . _ingredient_price_unit2 ] = self . _ingredient_price2
        self . _ingredients_prices_by_shop \
            [ self . _current_shop ] \
            [ self . _ingredient_name ] \
            [ self . _ingredient_unit ] \
            [ self . _ingredient_amount ] \
            += [ price_dict ]
