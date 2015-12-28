class dishes_by_weekday_storage :
    def __init__ ( self ) :
        self . _dishes_by_weekday = None
        self . _consts = None
        self . _re = None
    def set_modules ( self , consts , re ) :
        self . _consts = consts
        self . _re = re
    def all_dishes ( self ) :
        return list ( self . _dishes_by_weekday . values ( ) )
    def distinct_dishes ( self ) :
        dishes = set ( )
        for weekday_dishes in self . _dishes_by_weekday . values ( ) :
            dishes = dishes . union ( set ( weekday_dishes ) )
        return dishes
    def load ( self ) :
        wiki_file_name = self . _consts . wiki_path + self . _consts . dishes_by_weekday_file_name + self . _consts . dot_wiki
        try :
            wiki_contents = open ( wiki_file_name , self . _consts . open_file_for_read ) . readlines ( )
        except IOError :
            wiki_contents = [ ]
        self . _dishes_by_weekday = { }
        current_weekday = unicode ( )
        for wiki_line in wiki_contents :
            unicode_wiki_line = wiki_line . decode ( self . _consts . utf8 )
            match = self . _re . match ( self . _consts . header_regexp , unicode_wiki_line , self . _re . UNICODE )
            if match :
                current_weekday = match . group ( 1 ) . lower ( )
                if current_weekday not in self . _dishes_by_weekday :
                    self . _dishes_by_weekday [ current_weekday ] = [ ]
            match = self . _re . match ( self . _consts . list_regexp , unicode_wiki_line , self . _re . UNICODE )
            if match :
                dish = match . group ( 1 ) . lower ( )
                self . _dishes_by_weekday [ current_weekday ] += [ dish ]
