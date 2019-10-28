import random 

#Board class
class Board:


    #Constructor 
    def __init__ (self):
        #Each 3 is a row
        self.board = [['+']*3, ['+']*3, ['+']*3]
        self.filledCount = 0

    #Get functions
    def getBoard(self):
        return self.board
    def getFilledCount(self):
        return self.filledCount    


    #Function to determine if desired spot is empty
    def isEmpty(self, row, spotInRow):
        if(self.board[row][spotInRow] == '+'):
            return True
        return False


    #Function to add symbol to board
    def addToBoard(self, row, spotInRow, symbol):
        if(2 < row or row < 0 or  2 < spotInRow  or spotInRow < 0 or (not self.isEmpty(row, spotInRow))):
            print("Invalid placement.")
            return
        else:
            self.board[row][spotInRow] = symbol
            self.filledCount = self.filledCount + 1


    #Function to generate random move         
    def playRandomMove(self, symbol):

        #Find random place that is empty on board
        row = random.randint(0, 2)
        spotInRow = random.randint(0,2)

        #If valid, add to space
        if(self.isEmpty(row, spotInRow) == True):
            self.addToBoard(row, spotInRow, symbol)

        #If not valid, either try again, or end game     
        else:
            if(self.filledCount == 9):
                return
            self.playRandomMove(symbol) 

    #Function to check if a player has won
    def checkForWin(self, symbol):
        if(self.filledCount < 3):
            return False
        b = self.board 
        #first row   
        if(b[0][0] == symbol and b[0][1] == symbol and b[0][2] == symbol):
            return True
        #second row
        elif(b[1][0] == symbol and b[1][1] == symbol and b[1][2] == symbol):
            return True
        #third row
        elif(b[2][0] == symbol and b[2][1] == symbol and b[2][2] == symbol):
            return True
        #first column
        elif(b[0][0] == symbol and b[1][0] == symbol and b[2][0] == symbol):
            return True
        #second column
        elif(b[0][1] == symbol and b[1][1] == symbol and b[2][1] == symbol):
            return True        
        #third column
        elif(b[0][2] == symbol and b[1][2] == symbol and b[2][2] == symbol):
            return True
        #diagonal
        elif(b[0][0] == symbol and b[1][1] == symbol and b[2][2] == symbol):
            return True 
        #diagonal
        elif(b[0][2] == symbol and b[1][1] == symbol and b[2][0] == symbol):
            return True 
        return False


    #Function to display the layout of board
    def displayLayout():
        print("~COLUMNS~")
        print(1,2,3, sep = "*")
        boardArr = [['+']*3, ['+']*3, ['+']*3]
        for i in range(0,3):
            print(boardArr[i][0], boardArr[i][1], boardArr[i][2], sep = "|")
        print("^ ROWS 1, 2, 3")

    #Function to print out board           
    def printBoard(self):
        for i in range(0,3):
            print(self.board[i][0], self.board[i][1], self.board[i][2], sep = '|')            



#Player class
class Player:
    def __init__(self, playerNumber, symbol, mode = None):
        self.playerNumber = playerNumber
        self.symbol = symbol
        self.name = "CPU"
        if(mode == None):
            self.name = input("What is your name, player " + str(self.playerNumber) + "?\n")
            if(self.name == "CPU"):
                print("You are now a machine!")
                
        if(self.name != "CPU"):
            print("Your letter is : " + str(self.symbol) + "\n")
        else:
            self.mode = mode    
        #self.mode = None
    
    #Get methods
    def getSymbol(self):
        return self.symbol
    def getName(self):
        return self.name
    def getMode(self):
        return self.mode  



#Gameplay class
class GamePlay: 

    #Constructor
    def __init__(self):
        self.turnLimit = 12
        self.players = [None]*2
        self.gameBoard = Board()
        self.start()


    #Function for playing a manual turn
    def turn(self,currentPlayer):
        if(currentPlayer.getName() != "CPU"):
            row = int(input("Which row would you like to add to? (1, 2, or 3) "))
            spotInRow = int(input("Which column would you like to add to in row " + str(row) + "? "))
            self.gameBoard.addToBoard(row-1, spotInRow-1, currentPlayer.getSymbol())
        else:
            self.gameBoard.playRandomMove(currentPlayer.getSymbol())    


    #Function for playing an automated turn    
    def turnAutomated(self,currentPlayer):

        #Hard mode
        if(currentPlayer.getMode() == "Hard" or currentPlayer.getMode() == "hard"):
            self.gameBoard.playBestMove(currentPlayer.getSymbol())

        #Medium mode    
        else:
            self.gameBoard.playRandomMove(currentPlayer.getSymbol())


    #Function for end game sequence        
    def endGame(self, winner):
        print("The game is now over")

        #Tied game
        if(winner == None):
            print("There is no winner!")

        #Won game    
        else:
            print("The winner is " + winner + "!") 


    #Function to start the game                   
    def start(self):

        #Set mode and create players
        mode = input("Which mode would you like? \n.Manual (Can control both players)\n.Medium (Vs CPU)\n")
        if(mode == "Manual" or mode == "manual"):
            self.players[0] = Player(1, 'X')
            self.players[1] = Player(2, 'O')
        elif(mode == "Medium" or mode == "medium"):
            self.players[0] = Player(1, 'X')
            self.players[1] = Player(2, 'O', mode)
        
        #If no valid command is entered, ask again
        else:
            print("Invalid command entered.")
            self.start()

        #Begin turns   
        turnCounter = 0
        playerCounter = 0

        #Show user how board is laid out 
        Board.displayLayout()

        #loop through turns, end after 12 turns have occurred or the board is filled 
        while(turnCounter < self.turnLimit and self.gameBoard.getFilledCount() < 9):
            
            #Display who is playing
            print("\nIt is " + self.players[playerCounter].getName() + "'s turn! \n")

            #Play turn
            self.turn(self.players[playerCounter])
        
            #Show user the current board 
            print()    
            self.gameBoard.printBoard() 

            #Check for if player has won
            playerWon = self.gameBoard.checkForWin(self.players[playerCounter].getSymbol())
            if(playerWon == True):
                self.endGame(self.players[playerCounter].getName())
                return

            #Increase turn count   
            turnCounter = turnCounter + 1
            
            #Get other player to play
            if(playerCounter == 0):
                playerCounter = 1
            else:
                playerCounter = 0

        #Once out of loop, end the game         
        self.endGame(None)                          

#Start the Game
startGame = GamePlay()


