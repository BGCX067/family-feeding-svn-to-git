from calculate_units_ratio import calculate_units_ratio
import unittest

class test_consts :
    conversion_value = 12
    from_amount = 34
    from_unit = 'from unit'
    my_unit = 'my unit'
    some_other_unit = 'some other unit'
    to_amount = 56
    to_unit = 'to unit'
    unknown_from_unit = 'unknown from unit'
    unknown_to_unit = 'unknown to unit'

class consts_fake :
    def __init__ ( self ) :
        self . units_conversion = { }

class calculate_units_ratio_tests ( unittest . TestCase ) :
    def setUp ( self ) :
        self . _consts = consts_fake ( )
        self . _calculate_units_ratio = calculate_units_ratio ( )
        self . _calculate_units_ratio . set_modules ( consts = self . _consts )
    def test_same_units ( self ) :
        self . assertEqual ( self . _calculate_units_ratio . run \
            ( test_consts . from_amount 
            , test_consts . my_unit 
            , test_consts . to_amount 
            , test_consts . my_unit
            )
            , float ( test_consts . from_amount ) / float ( test_consts . to_amount )
        )
    def test_to_amount_is_zero ( self ) :
        self . assertEqual ( self . _calculate_units_ratio . run \
            ( test_consts . from_amount
            , test_consts . from_unit
            , 0
            , test_consts . to_unit 
            )
            , float ( 0 )
        )
    def test_to_amount_is_negative ( self ) :
        self . assertEqual ( self . _calculate_units_ratio . run \
            ( test_consts . from_amount 
            , test_consts . from_unit
            , - test_consts . to_amount
            , test_consts . to_unit
            )
            , float ( 0 )
        )
    def test_unknown_unit ( self ) :
        self . _consts . units_conversion [ test_consts . from_unit ] = \
            { test_consts . to_unit : test_consts . conversion_value }
        self . assertEqual ( self . _calculate_units_ratio . run \
            ( test_consts . from_amount 
            , test_consts . unknown_from_unit
            , test_consts . to_amount
            , test_consts . unknown_to_unit
            )
            , float ( 0 )
        )
    def test_from_unit_in_conversion ( self ) :
        self . _consts . units_conversion [ test_consts . from_unit ] = \
            { test_consts . to_unit : test_consts . conversion_value }
        self . assertEqual ( self . _calculate_units_ratio . run \
            ( test_consts . from_amount 
            , test_consts . from_unit
            , test_consts . to_amount
            , test_consts . to_unit
            )
            , float ( test_consts . conversion_value * test_consts . from_amount ) 
            / float ( test_consts . to_amount )
        )
    def test_from_unit_in_conversion_but_to_unit_is_not ( self ) :
        self . _consts . units_conversion [ test_consts . from_unit ] = \
            { test_consts . some_other_unit : test_consts . conversion_value }
        self . assertEqual ( self . _calculate_units_ratio . run \
            ( test_consts . from_amount
            , test_consts . from_unit
            , test_consts . to_amount
            , test_consts . to_unit
            )
            , float ( 0 )
        )
    def test_to_unit_in_conversion ( self ) :
        self . _consts . units_conversion [ test_consts . to_unit ] = \
            { test_consts . from_unit : test_consts . conversion_value }
        self . assertEqual ( self . _calculate_units_ratio . run \
            ( test_consts . from_amount
            , test_consts . from_unit
            , test_consts . to_amount
            , test_consts . to_unit
            )
            , float ( test_consts . from_amount ) 
            / float ( test_consts . to_amount * test_consts . conversion_value ) 
        )
    def test_to_unit_in_conversion_but_from_unit_is_not ( self ) :
        self . _consts . units_conversion [ test_consts . to_unit ] = \
            { test_consts . some_other_unit : test_consts . conversion_value }
        self . assertEqual ( self . _calculate_units_ratio . run \
            ( test_consts . from_amount
            , test_consts . from_unit
            , test_consts . to_amount
            , test_consts . to_unit
            )
            , float ( 0 )
        )

