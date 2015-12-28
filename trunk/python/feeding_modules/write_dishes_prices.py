class write_dishes_prices :
    def __init__ ( self ) :
        self . _consts = None
        self . _format_dishes_prices = None
    def set_modules ( self , consts , format_dishes_prices ) :
        self . _consts = consts
        self . _format_dishes_prices = format_dishes_prices
    def run ( self ) :
        wiki_file = open \
            ( self . _consts . wiki_path 
            + self . _consts . dishes_prices_file_name 
            + self . _consts . dot_wiki 
            , self . _consts . open_file_for_write
            )
        lines = self . _format_dishes_prices . run ( )
        for line in lines :
            wiki_file . write ( line . encode ( self . _consts . utf8 ) + self . _consts . new_line )
        wiki_file . close ( )
