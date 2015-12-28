module Main where

import Testing

main = print ( runSuite tests ) where 
    tests
      = runTest ( TestEqual "test equal success" 
            ( TestsResult [ "TestEqual \"success\" 1 1" ] [ ] ) 
            ( runTest ( TestEqual "success" 1 1 ) ( TestsResult [ ] [ ] ) ) 
        )
      . runTest ( TestEqual "test equal failure"
            ( TestsResult [ ] [ "TestEqual \"failure\" 1 2" ] )
            ( runTest ( TestEqual "failure" 1 2 ) ( TestsResult [ ] [ ] ) ) 
        )
      . runTest ( TestEqual "tests summary success" 
            ( TestsSucceeded 1 ) 
            ( testsSummary ( TestsResult [ "a" ] [ ] ) ) 
        )
      . runTest ( TestEqual "tests summary failure" 
            ( TestsFailed [ "b" ] ) 
            ( testsSummary ( TestsResult [ ] [ "b" ] ) ) 
        )
      . runTest ( TestEqual "tests summary mixed" 
            ( TestsFailed [ "b" ] ) 
            ( testsSummary ( TestsResult [ "a" ] [ "b" ] ) ) 
        )
