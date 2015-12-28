class write_weekly_ingredients_prices :
    def __init__ ( self ) :
        self . _consts = None
        self . _format_week_report = None
    def set_modules ( self , consts , format_week_report ) :
        self . _consts = consts
        self . _format_week_report = format_week_report
    def run ( self ) :
        wiki_file = open \
            ( self . _consts . wiki_path 
            + self . _consts . weekly_ingredients_prices_file_name 
            + self . _consts . dot_wiki 
            , self . _consts . open_file_for_write
            )
        lines = self . _format_week_report . run ( )
        for line in lines :
            wiki_file . write ( line . encode ( self . _consts . utf8 ) + self . _consts . new_line )
        wiki_file . close ( )
