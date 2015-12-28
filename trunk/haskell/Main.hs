module Main where

import System.Environment ( getArgs )
import Feeder ( makeDishesNutrition )

interactWith function inputFile outputFile = do
    input <- readFile inputFile
    writeFile outputFile ( function input )

main = interactWith function inputFile outputFile
    where
        inputFile = "../wiki/IngredientsByDishes.wiki"
        outputFile = "../wiki/DishesNutrition.wiki"
        function = makeDishesNutrition
