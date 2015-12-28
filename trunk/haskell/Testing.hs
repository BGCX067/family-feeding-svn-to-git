module Testing where

data Test a = TestEqual String a a deriving Show
data TestsResult = TestsResult [ String ] [ String ] deriving ( Eq , Show )
data TestsSummary = TestsSucceeded Integer | TestsFailed [ String ] deriving ( Eq , Show )

countSuccess :: Show a => a -> TestsResult -> TestsResult
countSuccess test ( TestsResult succs fails ) = TestsResult ( succs ++ [ show test ] ) fails

countFailure :: Show a => a -> TestsResult -> TestsResult
countFailure test ( TestsResult succs fails ) = TestsResult succs ( fails ++ [ show test ] )

testsSummary :: TestsResult -> TestsSummary
testsSummary ( TestsResult succs [ ] ) = TestsSucceeded ( toInteger ( length succs ) )
testsSummary ( TestsResult _ fails ) = TestsFailed fails

runSuite :: ( TestsResult -> TestsResult ) -> TestsSummary
runSuite tests = testsSummary ( tests ( TestsResult [ ] [ ] ) )

runTest :: ( Eq a , Show a ) => Test a -> TestsResult -> TestsResult
runTest test @ ( TestEqual _ a b )
    | a == b    = countSuccess test
    | otherwise = countFailure test
