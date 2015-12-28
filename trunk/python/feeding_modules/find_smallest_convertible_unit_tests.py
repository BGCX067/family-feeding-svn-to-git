from find_smallest_convertible_unit import find_smallest_convertible_unit
import unittest

class test_consts :
    key1 = 'key1'
    key2 = 'key2'
    key3 = 'key3'
    my_unit = 'my unit'
    value1 = 'value last'
    value2 = 'value first'
    value3 = 'value in the middle'

class calculate_convertible_units_ratings_fake :
    def __init__ ( self ) :
        self . _run_unit = None
        self . _run_return = None
    def run ( self , unit ) :
        self . _run_unit = unit
        return self . _run_return

class find_smallest_convertible_unit_tests ( unittest . TestCase ) :
    def setUp ( self ) :
        self . _calculate_convertible_units_ratings = calculate_convertible_units_ratings_fake ( )
        self . _find_smallest_convertible_unit = find_smallest_convertible_unit ( )
        self . _find_smallest_convertible_unit . set_modules \
            ( calculate_convertible_units_ratings = self . _calculate_convertible_units_ratings )
    def test_sorted_keys ( self ) :
        self . _calculate_convertible_units_ratings . _run_return = \
            { test_consts . key1 : test_consts . value1 
            , test_consts . key2 : test_consts . value2
            , test_consts . key3 : test_consts . value3
            }
        result = self . _find_smallest_convertible_unit . run ( test_consts . my_unit )
        self . assertEqual ( result , test_consts . value3 )
        self . assertEqual ( self . _calculate_convertible_units_ratings . _run_unit , test_consts . my_unit )

