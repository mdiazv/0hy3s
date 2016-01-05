# 0hy3s
This is an implementation of a solver for 0hn0.com

#### v0.2

It can solve all the given example puzzles, featuring grids from 4x4 up to 9x9.

Some of the improvements discussed on the previous version were implemented:
- Adding red tiles to the patterns
- Better red tile inferring
- Pattern caching

Also some performance optimisations were made, with the help of cProfile.

#### v0.1

So far it is a basic solver. Works for most 4x4 grids.

It breaks on the 5x5 grid on the samples because it can't infer the location of a red tile on (3, 2). In order to get around this, I'm gonna need to add the red tiles to the patterns.

There's also room for improvement on the way we find blue tiles, by remembering the patterns of the already calculated tiles and also keeping track of which are the still unsolved initial tiles.
