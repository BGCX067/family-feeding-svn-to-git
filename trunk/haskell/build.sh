rm -rf ../../../temp/haskell
rm -rf ../../../build/haskell
mkdir -p ../../../build/haskell/tests

ghc Main.hs -outputdir ../../../temp/haskell -o ../../../build/haskell/Main
ghc TestingTest.hs -outputdir ../../../temp/haskell -o ../../../build/haskell/tests/TestingTest

../../../build/haskell/tests/TestingTest
