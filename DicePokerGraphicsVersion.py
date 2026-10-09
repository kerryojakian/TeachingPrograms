
'''
By Kerry Ojakian

Dice Poker program - Graphics Version
Ideas of this appears in a book somewhere; I forget where I got the idea
'''
from random import *
from tkinter import *
from time import *



class DicePokerGraphical:
    '''
    This is the top-level class that runs the game.
    '''

    def __init__(self, m):

        self.initialMoney = m # keeps track of start amount of money
        self.cost = 10        # cost to play one round


        root = Tk() # START EVENT LOOP

        self.setUpWidgets(root)
        self.placeWidgets(root)
        self.resetGame()

        root.mainloop() # END EVENT LOOP


    def setUpWidgets(self,root):
        
        # Sets up the dice with corresponding check boxes
        self.dice = SetOfDice(root)

        # Displays the player's current hand and money in one frame
        self.handAndMoney = Frame(root)
        self.handLabel = HandLabel(self.handAndMoney)
        self.money = MoneyLabel(self.handAndMoney)

        # A button which re-rolls the dice that are checked
        self.reRollButton = ReRollButton(root, self.dice, self.handLabel)
        
        # A button for the player to indicate they are done with the round
        # along with a label to indicate earnings, put into a frame
        self.doneAndResults = Frame(root)
        self.doneRound = MyButton(self.doneAndResults, self.endRound)
        self.doneRound.configure( text = "Done Rerolling", bg = 'pink')
        self.earnings = MyLabel(self.doneAndResults)


        # Player clicks to play another round
        self.playButton = MyButton(root, lambda event : self.resetRound())
        self.playButton.configure( text = "Play Again?", bg = 'white')

        # Restart entire game, reinitializing money
        self.resetButton = Button(root, text = "Reset Entire Game")
        self.resetButton.bind('<Button-1>', lambda event : self.resetGame())

    
        
        

    def placeWidgets(self, root):
        
        self.dice.pack()

        self.handLabel.pack(side = LEFT, padx = 20, pady = 40)
        self.money.pack(side = RIGHT, padx = 20, pady = 40)
        self.handAndMoney.pack()

        self.doneRound.pack(side = LEFT, padx = 20, pady = 40)
        self.earnings.pack(side = RIGHT, padx = 20, pady = 40)
        self.doneAndResults.pack()
        
        self.reRollButton.pack(pady = 20)
        self.doneAndResults.pack(pady = 10)
        self.playButton.pack(pady = 10)
        self.resetButton.pack(pady = 10)
        

    def resetRound(self):
        self.playButton.deactivate()
        self.doneRound.activate()
        self.reRollButton.reset()
        self.dice.rollAll()
        score, handDescription = self.dice.score()
        self.handLabel.set(handDescription)
        self.earnings.set('')
        self.money.change(-self.cost)
        


    def resetGame(self):
        self.money.set(self.initialMoney)
        self.resetRound()
        

    def endRound(self, event):
        score, hand = self.dice.score()
        self.earnings.set('You earned: $' + str(score))
        self.money.change(score)
        self.doneRound.deactivate()
        self.reRollButton.deactivate()
        self.playButton.activate()




class MyLabel(Label):

    def __init__(self, root):
        self.strVal = StringVar()
        Label.__init__(self, root, textvariable = self.strVal)

    def set(self, s):
        self.strVal.set(s)
        

class HandLabel(MyLabel):

    def set(self, s):
        self.strVal.set('Your hand is: ' + s)        


class MoneyLabel(MyLabel):

    def __init__(self, root, startMoney = 0):
        self.amount = startMoney

        MyLabel.__init__(self, root)
        #self.label = MyLabel(root)

        self.root = root


    def change(self, x):
        self.amount = self.amount + x
        self.set(self.amount)

    def get(self):
        return self.amount

    def set(self, x):
        self.amount = x
        MyLabel.set(self, 'Modifying your account')
        self.root.update_idletasks()
        sleep(2)
        MyLabel.set(self, 'You currently have: $' + str(self.amount))
  



class MyButton(Button):

    def __init__(self, root, callback):
        self.callback = callback
        Button.__init__(self, root)
        self.activate()
        

    def activate(self):
        self.configure( state = NORMAL )
        self.bind('<Button-1>', self.callback)


    def deactivate(self):
        self.configure( state = DISABLED )
        self.unbind('<Button-1>')



class ReRollButton(Frame):

    def __init__(self, root, dice, hand, rollMax = 2):
        Frame.__init__(self, root)
        self.B = MyButton(self, lambda event : self.roll())
        self.B.configure( text = "Re-Roll Now" )
        self.dice = dice
        self.hand = hand
        self.rollsLeft = rollMax
        self.rollMax = rollMax

        # Results: description of hand
        self.results = MyLabel(self)
        self.setLabel()

        self.B.pack(side = LEFT, padx = 20)
        self.results.pack(side = RIGHT)
        

    def reset(self):
        self.activate()
        self.rollsLeft = self.rollMax
        self.setLabel()
        self.dice.clear()

    def setLabel(self):
        self.results.set("Number of rolls left: {}".format(self.rollsLeft))

    def activate(self):
        self.B.configure( bg = 'green' )
        self.B.activate()

    def deactivate(self):
        self.B.configure( bg = 'red' )
        self.B.deactivate()

    def roll(self):

        self.dice.roll()
        self.rollsLeft = self.rollsLeft - 1
        self.setLabel()

        if self.rollsLeft == 0:
            self.deactivate()

        score, handDescription = self.dice.score()

        self.hand.set(handDescription)    



  


class Die:

    def __init__(self, root, val):

        self.size = 100
        self.value = val
        self.sq = Canvas(root, width = self.size, height = self.size)
        self.sq.create_rectangle(2, 2, self.size-1, self.size-1)
        self.textId = \
                    self.sq.create_text(\
                        self.size//2, self.size//2, text=str(self.value))
        self.sq.pack()

    def setValue(self, val):
        self.value = val
        self.sq.create_text(self.size//2, self.size//2, text=str(self.value))
        

    def getValue(self):
        return self.value

    def roll(self):
        self.value = randint(1,6)
        self.sq.itemconfigure(self.textId, text = str(self.value))


    

class reRollIndicator:

    def __init__(self, root):

        self.value = IntVar()
        self.B = Checkbutton(root, variable = self.value)
        self.B.pack()

        #self.B.bind(self.display) # just for testing

    # Just for testing
    #def display(self):
    #    print(self.value.get())

    def clear(self):
        self.value.set(0)

    def isSelected(self):
        return self.value.get() == 1




class SetOfDice:
    '''
    This is a class that stores a representation of
    5 dice, each die with sides: 1,2,3,4,5,6.
    It allows for rolling and scoring of hands.
    '''



    def __init__(self, root):

        # self.numDice is the constant number of dice.
        # But just changing this not a good idea!
        # methods like score assume 5 dice.
        self.numDice = 5 
        self.dice = [NONE] * self.numDice
        self.rollInd = [NONE] * self.numDice
        self.collectionOfDice = Frame(root)
        for k in range(self.numDice):
            F = Frame(self.collectionOfDice)
            self.dice[k] = Die(F, k+1)
            self.rollInd[k] = reRollIndicator(F)
            F.grid(row = 0, column = k)

        # Dictionary of occurences, which means:
        # The keys are the numbers 1 through 6
        # and the corresponding value of each key,
        # is how many times that number appears in
        # the roll
        # This is only updated when score method called.
        self.occurences = {} 


    def pack(self):
        self.collectionOfDice.pack()

    def clear(self):
        for s in self.rollInd:
            s.clear()
            

    def rollAll(self):
        for s in range(self.numDice):
            self.dice[s].roll()

    def roll(self):

        for s in range(self.numDice):
            if self.rollInd[s].isSelected():
                self.dice[s].roll()




    # Put this in so we can reset the roll
    # for testing of the score method.
    def setDice(self, roll):
        self.dice = roll

    # Left in for testing
    def getDice(self):
        'Returns current die rolls as list'
        return self.dice
 
    def score(self):
        '''
        Returns the current score of the current dice.
        It does this by returning 2 arguments.
        First: a float which indicates the value
        (in dollars) of the roll.
        Second: a string which indicates the name
        of the roll
        '''

        # Create dictionary
        for k in range(1,7):
            count = 0
            for d in self.dice:
                if d.getValue() == k:
                    count = count + 1
            self.occurences[k] = count

        valList = list(self.occurences.values())


        if 5 in valList:
            reward = 30
            hand = '5 of a kind'

        elif 4 in valList:
            reward = 15
            hand = '4 of a kind'

        elif 3 in valList and 2 in valList:
            reward = 12
            hand = 'Full house'

        elif 3 in valList:
            reward = 8
            hand = '3 of a kind'

        elif valList.count(2) == 2:
            reward = 5
            hand = '2 pair'        

        elif valList.count(1) == 5 and \
             (self.occurences[1] == 0  or self.occurences[6] ==0):
            reward = 20
            hand = 'Straight'
            
        else:
            reward = 0
            hand = 'Garbage!'            

        return reward, hand



def main():

    game = DicePokerGraphical(100)


main()

    
