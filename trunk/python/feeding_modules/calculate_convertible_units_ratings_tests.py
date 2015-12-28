from calculate_convertible_units_ratings import calculate_convertible_units_ratings
import unittest

class test_consts :
    from_unit1 = 'from unit1'
    from_unit2 = 'from unit2'
    my_unit = 'my unit'
    to_amount1 = 12
    to_amount2 = 34
    to_unit1 = 'to unit1'
    to_unit2 = 'to unit2'

class consts_fake :
    def __init__ ( self ) :
        self . units_conversion = { }

class calculate_convertible_units_ratings_tests ( unittest . TestCase ) :
    def setUp ( self ) :
        self . _consts = consts_fake ( )
        self . _calculate_convertible_units_ratings = calculate_convertible_units_ratings ( )
        self . _calculate_convertible_units_ratings . set_modules ( consts = self . _consts )
    def test_unknown_unit ( self ) :
        self . assertEqual \
            ( self . _calculate_convertible_units_ratings . run ( test_consts . my_unit )
            , { float ( 1 ) : test_consts . my_unit }
            )
    def test_conversion_from_unit ( self ) :
        self . _consts . units_conversion = { test_consts . my_unit : 
            { test_consts . to_unit1 : test_consts . to_amount1
            , test_consts . to_unit2 : test_consts . to_amount2 
            } }
        self . assertEqual \
            ( self . _calculate_convertible_units_ratings . run ( test_consts . my_unit )
            , { float ( 1 ) : test_consts . my_unit
              , float ( test_consts . to_amount1 ) : test_consts . to_unit1
              , float ( test_consts . to_amount2 ) : test_consts . to_unit2
              }
            )
    def test_conversion_to_unit ( self ) :
        self . _consts . units_conversion = \
            { test_consts . from_unit1 : { test_consts . my_unit : test_consts . to_amount1 }
            , test_consts . from_unit2 : { test_consts . my_unit : test_consts . to_amount2 }
            }
        self . assertEqual \
            ( self . _calculate_convertible_units_ratings . run ( test_consts . my_unit )
            , { float ( 1 ) : test_consts . my_unit
              , float ( 1 ) / float ( test_consts . to_amount1 ) : test_consts . from_unit1
              , float ( 1 ) / float ( test_consts . to_amount2 ) : test_consts . from_unit2
              }
            )

