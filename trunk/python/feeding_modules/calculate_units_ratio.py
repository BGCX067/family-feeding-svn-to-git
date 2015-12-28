class calculate_units_ratio :
    def __init__ ( self ) :
        self . _consts = None
    def set_modules ( self , consts ) :
        self . _consts = consts
    def run ( self , from_amount , from_unit , to_amount , to_unit ) :
        if float ( to_amount ) > float ( 0 ) :
            if from_unit == to_unit :
                return float ( from_amount ) / float ( to_amount )
            elif from_unit in self . _consts . units_conversion :
                if to_unit in self . _consts . units_conversion [ from_unit ] :
                    return float ( from_amount ) * float ( self . _consts . units_conversion [ from_unit ] [ to_unit ] ) / float ( to_amount )
            elif to_unit in self . _consts . units_conversion :
                if from_unit in self . _consts . units_conversion [ to_unit ] :
                    return float ( from_amount ) / ( float ( to_amount ) * float ( self . _consts . units_conversion [ to_unit ] [ from_unit ] ) )
        return float ( 0 )
