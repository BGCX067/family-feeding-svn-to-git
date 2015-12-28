class ingredients_by_dish_storage :
    def __init__ ( self ) :
        self . _ingredients_by_dish = None
        self . _consts = None
        self . _re = None
    def set_modules ( self , consts , re ) :
        self . _consts = consts
        self . _re = re
    def get ( self ) :
        return self . _ingredients_by_dish
    def dish_ingredient_unit_amount ( self , dish , ingredient ) :
        units_amounts = { }
        if dish in self . _ingredients_by_dish :
            if ingredient in self . _ingredients_by_dish [ dish ] :
                for unit , amount in self . _ingredients_by_dish [ dish ] [ ingredient ] . items ( ) :
                    if unit not in units_amounts :
                        units_amounts [ unit ] = float ( 0 )
                    units_amounts [ unit ] += float ( amount )
        return units_amounts
    def dish_ingredients ( self , dish ) :
        ingredients = set ( )
        if dish in self . _ingredients_by_dish :
            ingredients = set ( self . _ingredients_by_dish [ dish ] . keys ( ) )
        return ingredients
    def all_ingredients ( self ) :
        ingredients = set ( )
        for dish , dish_ingredients in self . _ingredients_by_dish . items ( ) :
            ingredients = ingredients . union ( set ( dish_ingredients . keys ( ) ) )
        return ingredients
    def all_dishes ( self ) :
        return set ( self . _ingredients_by_dish . keys ( ) )
    def load ( self ) :
        wiki_file_name = self . _consts . wiki_path + self . _consts . ingredients_by_dish_file_name + self . _consts . dot_wiki
        try :
            wiki_contents = open ( wiki_file_name , self . _consts . open_file_for_read ) . readlines ( )
        except IOError :
            wiki_contents = [ ]
        self . _ingredients_by_dish = { }
        current_dish = unicode ( )
        for wiki_line in wiki_contents :
            unicode_wiki_line = wiki_line . decode ( self . _consts . utf8 )
            match = self . _re . match ( self . _consts . header_regexp , unicode_wiki_line , self . _re . UNICODE )
            if match :
                current_dish = match . group ( 1 ) . lower ( )
                if current_dish not in self . _ingredients_by_dish :
                    self . _ingredients_by_dish [ current_dish ] = { }
            match = self . _re . match ( self . _consts . ingredient_amount_list_regexp , unicode_wiki_line , self . _re . UNICODE )
            if match :
                ingredient = match . group ( 1 ) . lower ( )
                amount = float ( match . group ( 2 ) )
                unit = match . group ( 3 ) . lower ( )
                if ingredient not in self . _ingredients_by_dish [ current_dish ] :
                    self . _ingredients_by_dish [ current_dish ] [ ingredient ] = { }
                if unit not in self . _ingredients_by_dish [ current_dish ] [ ingredient ] :
                    self . _ingredients_by_dish [ current_dish ] [ ingredient ] [ unit ] = float ( 0 )
                self . _ingredients_by_dish [ current_dish ] [ ingredient ] [ unit ] += amount
