class format_distinct_dishes :
    def __init__ ( self ) :
        self . _consts = None
        self . _dishes_by_weekday_storage = None
    def set_modules ( self , consts , dishes_by_weekday_storage ) :
        self . _consts = consts
        self . _dishes_by_weekday_storage = dishes_by_weekday_storage
    def run ( self ) :
        lines = [ ]
        lines += [ self . _consts . dishes_for_a_week_header ]
        lines += [ str ( ) ]
        lines += [ self . _consts . dishes_for_a_week_table_title ]
        dishes_by_weekday = self . _dishes_by_weekday_storage
        dishes = { }
        for weekday_dishes in dishes_by_weekday . all_dishes ( ) :
            for dish in weekday_dishes :
                if dish not in dishes :
                    dishes [ dish ] = 0
                dishes [ dish ] += 1
        for dish in sorted ( dishes ) :
            lines += \
                [ self . _consts . wiki_table
                + self . _consts . whitespace
                + dish 
                + self . _consts . whitespace 
                + self . _consts . wiki_table
                + self . _consts . whitespace
                + str ( dishes [ dish ] ) 
                + self . _consts . whitespace 
                + self . _consts . wiki_table
                ]
        return lines
