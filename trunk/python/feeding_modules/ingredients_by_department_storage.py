class ingredients_by_department_storage :
    def __init__ ( self ) :
        self . _department_by_ingredient = None
        self . _consts = None
        self . _re = None
    def set_modules ( self , consts , re ) :
        self . _consts = consts
        self . _re = re
    def department ( self , ingredient ) :
        if ingredient in self . _department_by_ingredient :
            return self . _department_by_ingredient [ ingredient ]
        else :
            return unicode ( )
    def all_ingredients ( self ) :
        return set ( self . _department_by_ingredient . keys ( ) )
    def load ( self ) :
        wiki_file_name = self . _consts . wiki_path + self . _consts . ingredients_by_department_file_name + self . _consts . dot_wiki
        try :
            wiki_contents = open ( wiki_file_name , self . _consts . open_file_for_read ) . readlines ( )
        except IOError :
            wiki_contents = [ ]
        self . _department_by_ingredient = { }
        current_department = unicode ( )
        for wiki_line in wiki_contents :
            unicode_wiki_line = wiki_line . decode ( self . _consts . utf8 )
            match = self . _re . match ( self . _consts . header_regexp , unicode_wiki_line , self . _re . UNICODE )
            if match :
                current_department = match . group ( 1 )
            match = self . _re . match ( self . _consts . list_regexp , unicode_wiki_line , self . _re . UNICODE )
            if match :
                ingredient = match . group ( 1 ) . lower ( )
                self . _department_by_ingredient [ ingredient ] = current_department

