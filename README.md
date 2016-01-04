# 0hy3s
This is an implementation of a solver for 0hn0.com

So far it is a basic solver. Works for most 4x4 grids.

It breaks on the 5x5 grid on the samples because it can't infer the location of a red tile on (3, 2). In order to get around this, I'm gonna need to add the red tiles to the patterns.

There's also room for improvement on the way we find blue tiles, by remembering the patterns of the already calculated tiles and also keeping track of which are the still unsolved initial tiles.
