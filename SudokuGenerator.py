#This file contains both my third and fourth attempt at making a class that
#can generate solved and solvable sudoku puzzles.
#
#A quick note:
#   2 underscores "__" are used to force a field or function to be private.
#
#   1 underscore "_" is used to mean that a field or function should be treated
#   as if it were private, but is not actually private.
#
#This means that you can call functions in this class that start with a single
#underscore "_", but the class was not designed for there to be a need to use
#these functions.
# 
#You do not need to know all of the workings of this class, but you do need to
#know about the public functions that you are intended to call.  Below are
#quick descriptions of these functions.  For more detail on any of them, look
#at the function header (the multi-line comments of each function):
#
#   getHardPuzzle() - returns a 2d list (a list of lists) that represents a
#      sudoku puzzle.  The function header has additional details.
#
#   getEasyPuzzle() - returns a 2d list (a list of lists) that represents a
#       sudoku puzzle.  The function header has additional details.
#
#   isSolved() - returns True if a given puzzle (a list of lists) is a valid
#       solution to the puzzle (following the rules)
#
#   getPuzzleAsString() - returns a string representation of the puzzle with
#       nice formating.  You can use this to print what the puzzle looks like
#       to the console.
#
#   isValueInRowOrColumn() - returns True if a given value exists in a given
#       row or column.  You can use this to validate moves as they are made in
#       the UI.
#
#   isFilledGrid() - returns True if a given puzzle only has values between 1
#       and 9.  If any value is not an integer between 1 and 9, false is
#       returned.
#
#   __init__() - sets up the generator's private and protected fields.  This is
#       called automatically when you create an instance of the class.
#
#   __str__() - attempts to return getPuzzleAsString().  If for some reason the
#       puzzle cannot be represented as a string, an error message is instead
#       returned.
#
#You are welcome to look at the rest of the functions of this class, however,
#do not get destracted by them, as some of them are rather complicated
#(especially the functions related to generating a hard puzzle).


#Definitly need to import random.  We will be using this a lot.
import random

#This class contains 2 ways to generate a valid sudoku puzzle, as well as a
#number of functions that are used both to help create the puzzle and that
#could be used to help validate a puzzle that is unrelated to what this class
#generates.
class SudokuGenerator:

    def __init__(self):
        '''The constructor of the class.  You do not need to manually call
        this, and this takes in no parameters.'''
        self._emptyMap = None
        self._puzzleMap = None
        self._puzzle = None
        self.__counter = 0
        self.__maxCounter = 1
        self.__maxAttempts = 3

    def getHardPuzzle(self, startingSolvedMoves):
        '''Given a number of moves that are known at the start of the puzzle,
        generate a 9x9 valid sudoku puzzle.  The puzzle is returned as a list
        of lists with values between 0 and 9.  Values of 0 are considered to be
        unknown values.

        The amount of time taken to generate a puzzle is related to how small
        the number of starting solved moves is.  Lower numbers take longer to
        generate a puzzle, and the puzzle may have multiple solutions.

        Puzzles with around 30 starting solved moves usually have a unique
        solution.'''

        #If startingSolvedMoves is less than 0 set it to 0 as there is no way
        #to generate a puzzle with less than 0 starting solved moves.
        if startingSolvedMoves < 0:
            startingSolvedMoves = 0

        while True:
            self._emptyMap = self._generateEmptyMap()
            self._puzzleMap = self._recursivePuzzleGenerator(self._copyPuzzle(self._emptyMap))
            #self._puzzle = self._generateUniqueSolvablePuzzle(self._copyPuzzle(self._puzzleMap), startingSolvedMoves)
            self._puzzle, numSolvedMoves = self._generateUniqueSolvablePuzzle(self._copyPuzzle(self._puzzleMap), startingSolvedMoves)

            #At this point we have a uniquely solvable puzzle.  However, we may
            #not have a puzzle with the number of starting moves that we want.
            #In this case, we will ignore the solution being unique, and just
            #randomly remove numbers until we have the given starting number of
            #moves.
            if numSolvedMoves != startingSolvedMoves:
                self._puzzle = self._generateSolvablePuzzle(self._puzzle, startingSolvedMoves)

            #Make sure that both the starting solved puzzle, and the current
            #unsolved puzzle are both valid.  If they are, return the unsolved
            #puzzle.
            if self._isCurrentPuzzleValid(self._puzzle) and self._isCurrentPuzzleValid(self._puzzleMap):
                return self._puzzle

    def getEasyPuzzle(self, startingSolvedMoves):
        '''Using a simply pattern generate an easy to solve sudoku puzzle.  The
        puzzle is returned as a list of lists, and the solved puzzle follows a
        very simple generating algorithm that follows a simple pattern.

        The puzzle returned is not guaranteed to have a single unique solution,
        and may have many solutions.'''

        #Validate that the starting solved moves are not less than 0.
        if startingSolvedMoves < 0:
            startingSolvedMoves = 0

        while True:
            try:
                self._emptyMap = self._generateEmptyMap()
                self._puzzleMap = self._generateCompletedPuzzle(self._emptyMap)
                self._puzzle = self._generateSolvablePuzzle(self._puzzleMap, startingSolvedMoves)
                return self._puzzle
            except:
                #raise e
                pass

    def isSolved(self, puzzle):
        '''Given a puzzle, checks both if the values of each square of the
        puzzle are valid (1 - 9) and if the puzzle follows all of the rules of
        Sudoku puzzles.
        Returns True if the puzzle is solved.
        Returns False if the puzzle is unsolved, or something is wrong with the
        puzzle.'''
        try:
            #If the puzzle is valid, then make sure that all values are between
            #1 and 9.  If they are, then the puzzle is solved.
            if self._isCurrentPuzzleValid(puzzleMap):
                for i in range(9):
                    for j in range(9):
                        if puzzleMap[i][j] < 1 or puzzleMap[i][j] > 9:
                            return False
                #If the above does not cause False to be returned, then the
                #puzzle is solved with valid entries, so return True.
                return True
            #If we have made it this far, the puzzle is not solved, return
            #false.
            return False
        except:
            return False

    def getPuzzleAsString(self):
        '''Returns a human readable string of the current puzzle.'''
        returnString = ""
        if self._puzzle == None:
            return "A Sudoku puzzle has not yet been generated."

        for i in range(len(self._puzzle)):
            if i > 0 and i % 3 == 0:
                returnString += "\n\n"
            else:
                returnString += "\n"

            for j in range(len(self._puzzle[i])):
                if j > 0 and j % 3 == 0:
                    returnString += f"{'|':2} "

                returnString += f"{self._puzzle[i][j]:2} "

        return f"{returnString}\n"

    def isValueInRowOrColumn(self, value, row, column, puzzle):
        '''Given a value, a row number, a column number, and a puzzle, checks
        if the given value exists in the row or column of the puzzle.
        Returns True if the value is in the row or column.
        Returns False if the value is not in the row or column.'''

        #Check if the value already exists in a given row and or column.  If it
        #does already exist, return True.  Otherwise, return false.
        for i in range(9):
            if puzzle[row][i] == value or puzzle[i][column] == value:
                return True

        #By default return false.
        return False

    def isFilledGrid(self, puzzle):
        '''Given a puzzle checks if every square of the puzzle has a non 0
        value.  This does not check if the puzzle is valid, only if the values
        of the puzzle are not None or 0.
        Returns True if the puzzle has a non 0 value in each square.
        Returns False if the puzzle has at least 1 non 0 value in each
        square.'''

        #Check if a given puzzle has any values in it that are 0.  If it does,
        #return False, otherwise return True.
        for i in range(9):
            for j in range(9):
                if puzzle[i][j] == 0:
                    return False

        return True

    def getValuesInBoxAt(self, row, column, puzzleMap):
        '''Given a row number, a column number, and a puzzle, gets the values
        of the 3x3 grid that exists within the whole puzzle.  Each puzzle is
        a 9x9 grid made up of 3x3 grids.  This function finds the 3x3 box and
        returns a list of values that are in that 3x3 box.'''

        #First we need to figure out which box we are in.
        currentBox = self._getBox(row, column, puzzleMap)

        #Next we want a list of all values that are in the currentBox.
        values = []
        for i in range(9):
            for j in range(9):
                lookBox = self._getBox(i, j, puzzleMap)
                #If the boxes are the same, add the value we are looking at, to
                #the list to be returned.
                if lookBox == currentBox:
                    values.append(puzzleMap[i][j])

        return values

    def __str__(self):
        '''Attempts to return a formated string version of what the puzzle
        currently looks like.  If unable to return a formated string of the
        puzzle, instead returns an error message.'''
        try:
            return self.getPuzzleAsString()
        except:
            return "A Sudoku puzzle has not yet been generated."

    def _generateEmptyMap(self, defaultValue=0):
        '''Creates a 2d list (list of lists) that is used to hold a 9x9 sudoku
        grid.  All values in the grid are set to 0 by default, but a different
        value can be chosen.
        Returns a list of lists.'''
        #We want to generate a list that can hold data in a 9x9 grid, so we will
        #use a double for loop to create a 9x9 list.
        puzzleMap = []
        for i in range(9):
            puzzleMap.append([])
            for j in range(9):
                puzzleMap[i].append(defaultValue)

        return puzzleMap

    def _generateCompletedPuzzle(self, startingGrid):
        '''Given a starting grid (which is assumed to be empty of values), uses
        a simple pattern based method to generate a completed sudoku puzzle.
        The rules of how the pattern works can be found at the following link:
        
        https://gamedev.stackexchange.com/a/138228

        This was my third attempt at generating a sudoku puzzle, and my first
        success.  While this method works, the puzzles it generates all follow
        a very simple pattern, that once seen is hard to unsee.  As such, this
        function is only used to generate easy puzzles.

        The login in this function is that we can start by generating the top
        most row of the puzzle with random non repeating values between 1 - 9.
        Then we take the first row of the puzzle, and shift the position of the
        numbers by some amount to get the second row.  Then we repeat with each
        row, until the puzzle is filled.
        As a final step, we randomize the order of some of the rows to try and
        help mask the obvious pattern that the puzzle follows. '''

        #First, we are going to generate the top most row of the puzzle with non
        #repeating random numbers between 1 and 9.
        previousRow = []
        while len(previousRow) != 9:
            ranNum = random.randint(1,9)
            if ranNum not in previousRow:
                previousRow.append(ranNum)

        #Next, we are going to set the top row of the puzzle map to these randomly
        #generated values.
        for i in range(9):
            startingGrid[0][i] = previousRow[i]

        #Now to fill in the next 8 rows, we will shift the position of our starting
        #9 numbers by an amount into a new list.  The amount we shift the items is:
        #3, 3, 1, 3, 3, 1, 3, 3.
        #So for the second row, the number at index 0 will be moved to index 3, and
        #the number at index 8 will be moved to index 2.
        for i in range(8):
            #Determin how much to shift the numbers by.
            shift = 3
            if i == 2 or i == 5:
                shift = 1

            #Create a new list for the currentRow, and move the items from the
            #previous row into the currentRow, with the elements shifted.
            currentRow = []
            for j in range(len(previousRow)):
                index = j + shift
                if index >= len(previousRow):
                    index -= 9

                currentRow.append(previousRow[index])

            #Now that we have the values for the current row, actually set the
            #values in the puzzleMap, and then set the values of previousRow to
            #be the same as the currentRow, so that on the next iteration, we will
            #be looking at the correct previous row values.
            for j in range(len(currentRow)):
                startingGrid[i + 1][j] = currentRow[j]
                previousRow[j] = currentRow[j]

        #Check that the current puzzle is solvable.
        if not self._isCurrentPuzzleValid(startingGrid):
            raise Exception(f"Invalid Puzzle!\n{self.getPuzzleAsString()}")

        #At this point we have a legal Sudoku puzzle, but it has a flaw.  It was
        #generated using a simple pattern.  So now we need to shuffle the order of
        #some of the columns and rows in such a way that we still have a legal
        #board, but that the pattern becomes less obvious, if not out right gone.

        #First lets get a copy of the starting grid.
        duplicatePuzzleMap = self._copyPuzzle(startingGrid)

        #Next swap the first 3 rows of the puzzle with: themselves (no swap), or
        #the second 3 rows (3 to 5), or the third 3 rows (6 to 8).  This should
        #make the pattern harder if not impossible to see, while keeping the
        #puzzle solvable.
        
        randRow = random.randint(0, 2)
                
        if randRow == 1:
            for i in range(0, 3):
                duplicatePuzzleMap[i] = startingGrid[i + 3]
                duplicatePuzzleMap[i + 3] = startingGrid[i]
        elif randRow == 2:
            for i in range(3, 6):
                duplicatePuzzleMap[i] = startingGrid[i + 3]
                duplicatePuzzleMap[i + 3] = startingGrid[i]

        #Validate that the puzzle is still solvable.
        if not self._isCurrentPuzzleValid(duplicatePuzzleMap):            
            raise Exception(f"Invalid Puzzle!\n{self.getPuzzleAsString()}")
        
        
        randColumn = random.randint(0, 2)
        if randColumn == 1:
            for i in range(0, 3):
                duplicatePuzzleMap[i][0] = startingGrid[i + 3][0]
                duplicatePuzzleMap[i + 3][0] = startingGrid[i][0]
        elif randColumn == 2:
            for i in range(3, 6):
                duplicatePuzzleMap[i][0] = startingGrid[i + 3][0]
                duplicatePuzzleMap[i + 3][0] = startingGrid[i][0]

        #Validate that the puzzle is still solvable.
        if not self._isCurrentPuzzleValid(duplicatePuzzleMap):
            raise Exception(f"Invalid Puzzle!\n{self.getPuzzleAsString()}")
        
        return duplicatePuzzleMap

    def _generateSolvablePuzzle(self, puzzleMap, startingMoves = 17):
        '''Given a fully solved (or completed) puzzle, remove values from the
        puzzle until we are left with a puzzle that only has the given number
        of starting moves left (all other values in the puzzle will be set to
        0).  This function does not make sure that the puzzle only has a sinle
        solution.
        Returns a puzzle (list of lists) that follows the rules of a sudoku
        puzzle and is possible to be solved.'''

        #Make sure that startingMoves is always at least 0.
        if startingMoves < 0:
            startingMoves = 0

        #Copy the puzzle so that we still have a copy of the solved puzzle.
        solvablePuzzle = self._copyPuzzle(puzzleMap)

        #Find out how many values have already been removed from the puzzle.
        solvedMoves = 81
        for i in range(9):
            for j in range(9):
                if puzzleMap[i][j] == 0:
                    solvedMoves -= 1
                
        while solvedMoves != startingMoves:
            #Remove a random value that we have no already removed.
            ranRow = random.randint(0,8)
            ranColumn = random.randint(0,8)

            if solvablePuzzle[ranRow][ranColumn] == 0:
                continue
            
            solvablePuzzle[ranRow][ranColumn] = 0
            solvedMoves -= 1

        #Validate that the puzzle is still solvable.
        if not self._isCurrentPuzzleValid(solvablePuzzle):
            raise Exception(f"Invalid Puzzle!\n{self.getPuzzleAsString()}")

        return solvablePuzzle
                    
    def _isCurrentPuzzleValid(self, currentMap):
        '''Given a puzzle, validates both that the structure of the given
        puzzle is what is expected (a list of 9 lists each containing 9
        elements).  Then validates that the puzzle does not break any of the
        rules of a sudoku puzzle (all values are between 0 and 9, and there are
        no duplicates in the same row, column, or 3x3 box).
        This does not check if a puzzle is solved, only if the puzzle currently
        only contains valid values.
        Returns True if the puzzle is valid.
        Returns False if the puzzle is not valid.'''

        #Start by validating the structure of the given map.
        if type(currentMap) is not list:
            return False

        if len(currentMap) != 9:
            return False

        for i in range(9):
            if type(currentMap[i]) is not list:
                return False

            if len(currentMap[i]) != 9:
                return False            
            

        #Check if any of the rows or columns have duplicate numbers.  If any value
        #is 0, skip it as 0 is the default value.
        for i in range(9):
            duplicates = []
            for j in range(9):
                if currentMap[i][j] == 0:
                    continue
                    
                for duplicate in duplicates:
                    if currentMap[i][j] == duplicate:
                        return False

                if currentMap[i][j] not in duplicates:
                    duplicates.append(currentMap[i][j])


        #Next check if each of the 3x3 grids contains any duplicated (again
        #ignoring 0).  To start we want to create a list of all of the boxes, so
        #that we can iterate over them.
        boxes = []
        for i in range(3):
            for j in range(3):
                boxes.append((i, j))

        #Now iterate over each box and look at all of the values in the box.  If
        #there are any duplicates (again other than 0) the box is invalid, and thus
        #the current puzzle is invalid.
        for box in boxes:
            values = self._getValuesInBox(box, currentMap)

            #Iterate over the values checking if any of the non 0 values are the
            #same as any other values.  If they are the box is invalid.
            for i in range(len(values)):
                if values[i] == 0:
                    continue

                for j in range(len(values)):
                    #If the value is 0 or we are looking at the same index
                    if values[j] == 0 or j == i:
                        continue

                    if values[i] == values[j]:
                        return False

        return True

    def _getBox(self, row, column, puzzleMap):
        '''Given a row number, a column number, and a puzzle detirmns which
        3x3 box (within the 9x9 grid) that the row and column intersect at.
        Returns the (x, y) coordinates of the box ((0 - 2), (0 - 2)).'''

        #Get the rowBox and columnBox value based on a simple if statement.
        if row >= 0 and row <= 2:
            rowBox = 0
        elif row >= 3 and row <= 5:
            rowBox = 1
        else:
            rowBox = 2

        if column >= 0 and column <= 2:
            columnBox = 0
        elif column >= 3 and column <= 5:
            columnBox = 1
        else:
            columnBox = 2

        return (rowBox, columnBox)

    def _getValuesInBox(self, currentBox, puzzleMap):
        '''Given a 3x3 box within a given puzzle, gets all of values in the
        3x3 box.  If an invalid box is given, an empty list is returned.
        Returns a list of values within a 3x3 grid.'''
        #Next we want a list of all values that are in the currentBox.
        values = []
        for i in range(9):
            for j in range(9):
                lookBox = self._getBox(i, j, puzzleMap)
                #If the boxes are the same, add the value we are looking at, to
                #the list to be returned.
                if lookBox == currentBox:
                    values.append(puzzleMap[i][j])

        return values

    def _copyPuzzle(self, puzzleMap):
        '''Returns a deep copy of a given puzzle as a new list of lists.'''
        
        copy = []
        for i in range(9):
            copy.append([])
            for j in range(9):
                copy[i].append(puzzleMap[i][j])
        return copy
    
    def _generateUniqueSolvablePuzzle(self, puzzle, startingSolvedMoves):
        '''This function takes in a completly solved puzzle, and removes a
        known value from a square of the puzzle until there are only the given
        startingSolvedMoves number of known values.  Each time a value is
        removed from the puzzle, the puzzle is solved, to check how many
        solutions the puzzle has.  Values are only removed if removing them
        keeps the solution to the puzzle unique.

        Only so many values can be removed from a puzzle.  After a certain
        number of attempts to remove a value from the puzzle, the loop breaks,
        and the solvable puzzle is returned.'''
        MAX_ATTEMPTS = self.__maxAttempts
        numSolvedMoved = 81
        numAttempts = MAX_ATTEMPTS
        while numSolvedMoved != startingSolvedMoves:
            #Get a random square of the puzzle.
            ranRow = random.randint(0, 8)
            ranColumn = random.randint(0, 8)

            #Make sure that the value is not 0.
            if puzzle[ranRow][ranColumn] == 0:
                continue

            #Store the current value of the square, so that we can put it back
            #after we remove it, if we need to.
            value = puzzle[ranRow][ranColumn]
            
            #Remove the value from the puzzle.
            puzzle[ranRow][ranColumn] = 0

            #Get a copy of the puzzle, which we will attempt to solve.
            copy = self._copyPuzzle(puzzle)

            #Keep track of how many solutions the puzzle now has.
            self.__counter = 0

            #Find out how many solutions the puzzle has.
            self._recursivePuzzleSolver(copy)

            #If the puzzle does not have exactly 1 solution, decrease the
            #number of attempts by 1, put the value back into its position
            #within the puzzle, and continue.
            if self.__counter > self.__maxCounter or self.__counter == 0:
                numAttempts -= 1
                puzzle[ranRow][ranColumn] = value

                #If numAttempts is less than 0, then we have already tried to
                #remove a value from the puzzle the maximum number of times
                #that is allowed.  In this case, we want to break.
                if numAttempts < 0:
                    break

                continue

            #If we reach this point, then we have succeeded in removing a value
            #from the puzzle, and we still have a unique solution.  Now we want
            #to increase numMovesRemoved by 1, and reset numAttempts to its
            #default starting value.
            numSolvedMoved -= 1
            numAttempts = MAX_ATTEMPTS

        #At this point we hopefully have a puzzle with only startingSolvedMoves
        #number of known values in the puzzle.  If we don't, then we were
        #unable to remove as many values as requested and still have a uniquely
        #solvable puzzle.  Either way, we are done, so we want to return the
        #puzzle.
        return puzzle, numSolvedMoved

    def _recursivePuzzleSolver(self, puzzle):
        '''This function takes in a puzzle and attempts to solve it, using a
        backtracking algorithm (the same that can be used to generate the
        puzzle).  If __maxCounter + 1 solutions have already been found, this
        function does nothing.
        This function is called by _generateUniqueSolvablePuzzle, and as such
        will only try so hard before giving up trying to solve a puzzle. ''' 

        #First check that the puzzle is not already solved.
        if self.isFilledGrid(puzzle) and self.__counter == 0:
            #If the puzzle is already solved, increase the counter to 1, and
            #return, ending the function.
            self.__counter == 1
            return 

        #Next check if the current puzzle already has a given max number of
        #solutions.  If it does, simply return and do not look for another
        #solution to the puzzle.
        if self.__counter >= self.__maxCounter + 1:
            return

        #Next go through each square of the puzzle until we find a value that
        #is not 0.  Once we have a non zero value, set it to a valid value.
        #Then check if the puzzle is now solved.  If not, this function is
        #called (recursion!) to solve the puzzle.  If the puzzle is solved, the
        #given counter is increased by 1, and the value of the square that we
        #are looking at is reset to 0.

        #For each square in the puzzle.
        for i in range(81):
            #Get the current row and column of our puzzle.
            row = i // 9
            column = i % 9

            #Check if the current value of the square is 0.  If the current
            #value is not 0, then continue with the loop.
            if puzzle[row][column] != 0:
                continue

            #Otherwise, we want to set the square to a random valid value.
            
            #Get a randomly ordered list of numbers between 1 and 9.
            possibleValues = list(range(1,10))
            random.shuffle(possibleValues)

            #Iterate through the values looking for a valid value.
            for value in possibleValues:

                #Check if the value already exists in the row or column.
                if not self.isValueInRowOrColumn(value, row, column, puzzle):

                    #Check if the value already exists in the 3x3 grid that
                    #contains the square that we are looking at.
                    if value not in self.getValuesInBoxAt(row, column, puzzle):
                        #At this point we have a valid possible value for the 
                        #square, and we now want to set the value of the square
                        #to the value that we have.
                        puzzle[row][column] = value

                        #Check if the puzzle is completly filled.
                        if self.isFilledGrid(puzzle):
                            #If the puzzle is now completed, increase the
                            #counter by 1 and break out of the loop.
                            self.__counter += 1
                            break
                        else:
                            #If the puzzle is not yet complete, check if
                            #calling this function will complete the puzzle.
                            #If it will, return, to stop modifing the puzzle.
                            if self.__counter < self.__maxCounter + 1:
                                if self._recursivePuzzleSolver(puzzle):
                                    return True                

            #If we make it to this point, then the above loop has executed on
            #all possible numbers bettwen 1 and 9 for this square of the
            #puzzle, and found that none of them can be placed in this square.
            #At this point, we need to backtrack, to undo our work.  So, we
            #want to break out of the top level loop, which is iterating over
            #all squares in the puzzle.
            break

	
        #This point in the code is called either once the puzzle has been
        #solved at least once, or the puzzle cannot be solved.  Either way set
        #the value of the sqaure back to 0.
        puzzle[row][column] = 0

    def _recursivePuzzleGenerator(self, puzzle):
