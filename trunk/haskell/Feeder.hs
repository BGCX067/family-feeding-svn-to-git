module Feeder where

type Name = String
type Amount = Integer
data Unit = Kilogram | Gram | Milligram | Microgram | Liter | Milliliter | Item
data IngredientInDish = IngredientInDish Name Amount Unit
data DishIngredients = DishIngredients Name [ IngredientInDish ]

dishesIngredientsToString x = unlines x
dishesIngredientsFromString x = lines x

makeDishesNutrition =
    dishesIngredientsToString . dishesIngredientsFromString
