# Teaching Programs
Some fun little programs used in teaching programming.

## Dice Poker (DicePokerGraphicsVersion.py)

The dice poker game shows the use of Tkinter for graphics and the use of an event loop.  In the game there are 5 dice that are given an initial roll.  The player can choose to carry out up to two re-rolls: on each re-roll the player selects some dice that are re-rolled.  At the end of a round, the player gets money according to the value of their final roll: there is some scoring system like poker, where the hand gets better as you go from one pair, to two pair, to three of a kind, and so on. 


## Peg Solitaire (PegSolitaire.py)

This program is an example of a basic console game, without the use of graphics.  It is a solitaire game in which there is a rectangle with slots for pegs: initially all the slots, except for one, are occupied by a peg (at the console, a "P" refers to a peg, and an "X" refers to empty slot).  On a turn, the player can jump one peg over a single peg (in the vertical or horizontal direction) and must land at an empty slot; the jumped peg is removed from the board.  The goal of the game is to end with as few pegs left as possible.  A move is entered by first giving the coordinates of the peg which is to be moved; for example "2,3" indicates the peg in row 2 and column 3.  Then the player enters the coordinates of the empty location to move that peg to; for example "4,3" in order to move the peg down 2 rows.
