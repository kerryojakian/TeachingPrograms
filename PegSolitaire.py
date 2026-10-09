'''
By Kerry Ojakian
Fall 2019
'''

from random import *

class PegGame:

    def __init__(self, height, width, numHoles = 0):

        self.board = PegSolitaire(height, width)
        self.UI    = UserInterface(self.board)

        for r in range(1,height+1):
            for c in range(1,width+1):
                self.board.placePeg(r,c)

        if numHoles == 0:
            self.board.removePeg(height, width)
        else:
            self.board.removePeg(height, width) # for now, same!
        # Maybe change later
        '''
        for h in numHoles:
            if self.board.getValue()
        ''' 

    def playGame(self):
        self.UI.printIntro()

        while not(self.board.isStuck()):
            self.UI.printBoardHeader()
            self.board.display()
            startPos = self.UI.getStartPos()
            endPos = self.UI.getEndPos()
            jumpResult = self.board.jumpPeg(startPos, endPos)
            if jumpResult == False:
                self.UI.errorMsg()

        self.UI.endMsg()


class UserInterface:

    def __init__(self, board):
        self.board = board

    def printIntro(self):
        print("********** The game is peg solitaire *********")
        print("*** Jump pegs to get to as few as possible ***")
        print()
        print()

    
    def printBoardHeader(self):
        print("***** GAME BOARD *****")

    def errorMsg(self):
        print()
        print("*** Illegal Move! ***")
        print()
        print()


    def endMsg(self):
        print()
        self.board.display()
        print()
        print("*** GAME OVER ***")
        print()


    def _getTwoIntegers(self, requestStr):
        while True:
            inString = input(requestStr)
            inList   = inString.split(',')
            
            if len(inList) != 2:
                self.errorMsg()
                
            else:
                try:
                    x = float(inList[0])
                    y = float(inList[1])
                    if x == int(x) and y == int(y):
                        return int(x), int(y)
                    else:
                        self.errorMsg()
                except:
                    self.errorMsg()


    def getStartPos(self):
        x, y = self._getTwoIntegers("Which peg do you want to move (give as comma separated integers)?: ")
        return (x, y)

    def getEndPos(self):
        x, y = self._getTwoIntegers("Where do you want to move your peg (give as comma separated integers)?: ")
        return (x, y)

        


class PegSolitaire:
    '''
    Note: A "position" is a tuple (x,y) which refers to a board position,
          where the indices start at 1, not at 0.
    '''
    
    def __init__(self, X,Y):
        self.rows = X
        self.cols = Y
        self.empStr = 'X' # string for empty space
        self.pegStr = 'P' # string for space with peg

        self.board = []   # board of pegs or empty, initialized to all empty
        for r in range(self.rows):
            newRow = [self.empStr] * self.cols
            self.board.append(newRow)


    def _onBoard(self, pos):
        '''
        Input: A position
        Output: True if the position is on the board, False otherwise
        '''
        if (1 <= pos[0] <= self.rows)  and  (1 <= pos[1] <= self.cols):
            return True
        else:
            return False


    def _checkPiecesOfMove(self, start, middle, end):
        '''
        Input: 3 positions that are on the board
        Output: True if correct pieces in those positions, False otherwise
        '''
        if self.board [start[0]-1]  [start[1]-1] == self.pegStr and \
           self.board [middle[0]-1] [middle[1]-1] == self.pegStr and \
           self.board [end[0]-1] [end[1]-1] == self.empStr:
            return True
        else:
            return False

    def getValue(self, x, y):
        return self.board[x-1][y-1]

    def placePeg(self, x, y):
        if self._onBoard( (x, y) ):
            self.board[x-1][y-1] = self.pegStr

        
    def removePeg(self, x, y):
        if self._onBoard( (x, y) ):
            self.board[x-1][y-1] = self.empStr        


    def _findMiddle(self, P1, P2):
        '''
        Input: 2 positions
        Output: False if they are not 2 steps apart, horizontally or vertically
                Otherwise- The position of the unique middle position 
        '''
        if P1[0] == P2[0]:
            if abs(P2[1] - P1[1]) == 2:
                return ( P1[0], (P2[1] + P1[1]) // 2 )

        if P1[1] == P2[1]:
            if abs(P2[0] - P1[0]) == 2:
                return ( (P2[0] + P1[0]) // 2, P1[1] )

        # Otherwise, there is not a good middle
        return False


    def jumpPeg(self, P1, P2):
        '''
        Input: Start position and end position for a jump
        Result: Makes the jump, changing the board if legal
        Output: True if jump made, False if not because it was illegal
        '''

        if not( self._onBoard(P1) and self._onBoard(P2) ):
            return False
        
        middle = self._findMiddle(P1, P2)
        if middle == False:
            return False
        
        if self._checkPiecesOfMove(P1, middle, P2):
            self.removePeg(P1[0], P1[1])
            self.removePeg(middle[0], middle[1])
            self.placePeg(P2[0], P2[1])

        return True



    def isStuck(self):
        '''
        Returns True if the game is stuck (i.e. no more moves). False otherwise.
        '''
        
        for r in range(1, self.rows+1):
            for left in range(1, self.cols - 1):
                if self._checkPiecesOfMove( (r,left) , (r,left+1), (r,left+2) ) or \
                   self._checkPiecesOfMove( (r,left+2) , (r,left+1), (r,left) ):
                    return False

        for c in range(1, self.cols+1):
            for top in range(1, self.rows - 1):
                if self._checkPiecesOfMove( (top,c) , (top+1,c), (top+2,c) ) or \
                   self._checkPiecesOfMove( (top+2,c) , (top+1,c), (top,c) ):
                    return False

        # Otherwise, found no possible move, so it's stuck
        return True
                                            

    def display(self):
        for r in range(self.rows):
            for c in range(self.cols):
                print(self.board[r][c], end = '')
            print()
            
                
def main():
    game = PegGame(3,4)
    game.playGame()

main()


def test1():
    P = PegSolitaire(2,3)
    P.display()
    P.placePeg(1,2)
    P.display()
    P.placePeg(1,3)
    P.placePeg(2,1)
    P.placePeg(2,2)
    P.placePeg(2,3)
    #P.removePeg(2,2)
    P.display() # should print:
    # XPP
    # PPP


def test2():
    
    P = PegSolitaire(2,3)
    P.placePeg(1,2)
    P.placePeg(1,3)
    P.placePeg(2,1)
    P.placePeg(2,2)
    P.placePeg(2,3)
    P.removePeg(2,2)
    P.display() # should print:
    # XPP
    # PXP

    print("Should print False: ", end='')
    print(P.isStuck()) # should return False

    print("Should print False: ", end = '')
    print(P.jumpPeg( (2,1), (2,2) )) # returns False and nothing happens.

    print("Should print True: ", end = '') 
    print(P.jumpPeg( (1,3), (1,1) )) # returns True

    print("Should print True: ", end='')
    print(P.isStuck()) # should return True now
    P.display() # should print:
    # PXX
    # PXP

    print()
    P = PegSolitaire(4,3)
    P.placePeg(1,1)
    P.placePeg(2,2)
    P.placePeg(3,3)
    P.display() # should display diagonal
    

def test3():
    P = PegSolitaire(4,3)
    for r in range(1,4):
        for c in range(1,4):
            P.placePeg(r,c)

    print()
    P.display() # should display all but bottom row
    print()
    print("Stuck? - Should be False: ", P.isStuck())
    P.jumpPeg( (2,1), (4,1) )
    P.jumpPeg( (2,2), (4,2) )
    P.jumpPeg( (4,1), (4,3) )
    print("Stuck? - Should be True: ", P.isStuck())
    print()
    P.display()
    # Should be:
    #PPP
    #XXP
    #XXP
    #XXP
    print()

    
    





         
