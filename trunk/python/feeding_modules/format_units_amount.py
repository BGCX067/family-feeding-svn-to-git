class format_units_amount :
    def __init__ ( self ) :
        self . _calculate_units_ratio = None
        self . _consts = None
        self . _calculate_convertible_units_ratings = None
    def set_modules \
        ( self
        , calculate_units_ratio
        , consts
        , calculate_convertible_units_ratings
        ) :
        self . _calculate_units_ratio = calculate_units_ratio
        self . _consts = consts
        self . _calculate_convertible_units_ratings = calculate_convertible_units_ratings
    def run ( self , unit , amount ) :
        result = str ( )
        components = [ ]
        units_ratios = self . _calculate_convertible_units_ratings . run ( unit )
        for current_ratio , current_unit in sorted ( units_ratios . items ( ) ) :
            current_amount = self . _calculate_units_ratio . run ( amount , unit , float ( 1 ) , current_unit )
            current_amount = float ( int ( current_amount ) )
            amount -= self . _calculate_units_ratio . run ( current_amount , current_unit , float ( 1 ) , unit )
            component = str ( int ( current_amount ) ) + self . _consts . whitespace + current_unit 
            components += [ component ]
            if int ( current_amount ) > 0 :
                if len ( result ) > 0 :
                    result += self . _consts . whitespace
                result += component 
        if len ( result ) == 0 and len ( components ) > 0 :
            result = components [ - 1 ]
        return result
