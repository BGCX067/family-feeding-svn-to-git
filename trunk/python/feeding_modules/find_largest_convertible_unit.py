class find_largest_convertible_unit :
    def __init__ ( self ) :
        self . _calculate_convertible_units_ratings = None
    def set_modules ( self , calculate_convertible_units_ratings ) :
        self . _calculate_convertible_units_ratings = calculate_convertible_units_ratings
    def run ( self , unit ) :
        units_by_ratio = self . _calculate_convertible_units_ratings . run ( unit )
        return units_by_ratio [ sorted ( units_by_ratio ) [ 0 ] ]
