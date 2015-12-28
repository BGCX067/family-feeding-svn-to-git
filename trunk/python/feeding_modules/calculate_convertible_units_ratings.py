class calculate_convertible_units_ratings :
    def __init__ ( self ) :
        self . _consts = None
    def set_modules ( self , consts ) :
        self . _consts = consts
    def run ( self , unit ) :
        units_by_ratio = { float ( 1 ) : unit }
        for from_unit , to_units in self . _consts . units_conversion . items ( ) :
            for to_unit , to_amount in to_units . items ( ) :
                if from_unit == unit :
                    units_by_ratio [ float ( to_amount ) ] = to_unit
                if to_unit == unit :
                    units_by_ratio [ float ( 1 ) / float ( to_amount ) ] = from_unit
        return units_by_ratio
