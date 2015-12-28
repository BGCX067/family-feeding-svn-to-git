class format_week_report :
    def __init__ ( self ) :
        self . _consts = None
        self . _format_dishes_diff = None
        self . _format_distinct_dishes = None
        self . _format_ingredients_amount = None
        self . _format_ingredients_diff = None
    def set_modules \
        ( self
        , consts 
        , format_dishes_diff
        , format_distinct_dishes 
        , format_ingredients_amount 
        , format_ingredients_diff
        ) :
        self . _consts = consts
        self . _format_dishes_diff = format_dishes_diff
        self . _format_distinct_dishes = format_distinct_dishes
        self . _format_ingredients_amount = format_ingredients_amount
        self . _format_ingredients_diff = format_ingredients_diff
    def run ( self ) :
        lines = [ ]
        lines += [ self . _consts . weekly_ingredients_prices_summary ]
        lines += [ self . _consts . wiki_labels ]
        lines += [ self . _consts . wiki_side_bar_navigation ]
        lines += [ str ( ) ]
        lines += [ self . _consts . wiki_table_of_contents ]
        lines += [ str ( ) ]
        lines += self . _format_distinct_dishes . run ( )
        lines += [ str ( ) ]
        lines += self . _format_ingredients_amount . run ( )
        lines += self . _format_dishes_diff . run ( )
        lines += self . _format_ingredients_diff . run ( )
        return lines

