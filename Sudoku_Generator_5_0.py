#Sudoku Generator 5
#This is a cleanup version of attempts 3 and 4

import random



class SudokuPuzzle:
    '''This class is designed to be used instead of a simple list of lists to
    represent the sudoku puzzle.  This class allows easy access of rows,
    columns and grid locations (x,y).  In addition, it allows access to all
    values within any of the 3x3 boxes that make up the 9x9 grid.'''

    def __init__(self, defaultValue = 0, rows = None, columns = None, map = None, boxLookup = None, reverseLookup = None):
        '''Given:
        A default value for each sqaure (defaults to 0).
        -OR-
        Several objects used to create a deep clone of this object.

        Creates a Sudoku Puzzle and stores the data in multiple different
        connected ways.'''
        if rows != None and columns != None and map != None and boxLookup != None and reverseLookup != None:
            self.__rows = rows
            self.__columns = columns
            self.__map = map
            self.__boxLookup = boxLookup
            self.__reverseBoxLookup = reverseLookup
            return
                
        #Standard list of lists that can be used to make up a sudoku puzzle.
        self.__rows = []
        #A dictionary of grid position (x,y) to values of the puzzle.
        self.__map = {}
        #A list of values of each column of the puzzle.
        self.__columns = []
        #A dictionary of grid position (x,y) to 3x3 box position (x2,y2).
        self.__boxLookup = {}
        #A dictionary of 3x3 box positions (x,y) to grid position (x2,y2).
        self.__reverseBoxLookup = {}

        #Make the list of lists and dictionary of values.
        for i in range(9):
            self.__rows.append([])
            self.__columns.append([])
            for j in range(9):
                self.__rows[i].append(defaultValue)                
                self.__map[(i, j)] = defaultValue

        #Make the list of values of the columns.
        for i in range(9):
            for j in range(9):
                self.__columns[i].append(self.__rows[j][i])

        #Using our existing data structures, make the list of columns, as well
        #as the dictionaries to lookup box positions of any grid position, or
        #the reverse.
        for key in self.__map:
            if key[0] <= 2:
                xPosition = 0
            elif key[0] <= 5:
                xPosition = 1
            else:
                xPosition = 2

            if key[1] <= 2:
                yPosition = 0
            elif key[1] <= 5:
                yPosition = 1
            else:
                yPosition = 2
            position = (xPosition, yPosition)
            if position not in self.__reverseBoxLookup:
                self.__reverseBoxLookup[position] = []
            self.__reverseBoxLookup[(xPosition, yPosition)].append(key)

        for key in self.__reverseBoxLookup:
            for i in range(len(self.__reverseBoxLookup[key])):
                self.__boxLookup[self.__reverseBoxLookup[key][i]] = key

    @property
    def map(self):
        return self.__map

    @property
    def rows(self):
        return self.__rows

    @property
    def columns(self):
        return self.__columns

    @property
    def boxToGridMap(self):
        return self.__reverseBoxLookup

    @property
    def gridToBoxMap(self):
        return self.__boxLookup

    def setValue(self, key, value):
        '''Given:
        A key (x, y) position in the puzzle
        A value to set the square in the grid to.

        Changes the current value in the grid to the new value.'''
        self.__rows[key[0]][key[1]] = value
        self.__columns[key[1]][key[0]] = value
        self.__map[key] = value

    def getCopy(self):
        '''Returns a deep copy of the SudokuPuzzle that can be modified without
        changing the original.'''
        cRows = []
        cColumns = []
        cMap = {}
        cLookup = {}
        cReverse = {}

        #Copy the rows and columns.
        for i in range(9):
            cRows.append([])
            cColumns.append([])
            for j in range(9):
                cRows[i].append(self.__rows[i][j])
                cColumns[i].append(self.__columns[j][i])

        #Copy the dictionaries.
        for key in self.__map:
            cMap[key] = self.__map[key]

        for key in self.__boxLookup:
            cLookup[key] = self.__boxLookup[key]

        #This dictionary is slightly more complicated as it is a dictionary of
        #lists.
        for key in self.__reverseBoxLookup:
            for value in self.__reverseBoxLookup[key]:
                if key not in cReverse:
                    cReverse[key] = []

                cReverse[key].append(value)

        return SudokuPuzzle(0, cRows, cColumns, cMap, cLookup, cReverse)
        

    def __str__(self):
        return str(self.__rows)
            

class SudokuGenerator:

    @staticmethod
    def getHardPuzzle(numKnownValues, forceUniqueSolution = False, maxDuration = 60):
        '''Given:
        A number of known values in the puzzle.
        If the puzzle should have only a single solution.
        The maximum amount of time to try and make a puzzle (in seconds).

        Generates a valid Sudoku puzzle using a backtracking recursive
        algorithm.
        If maxDuration seconds occure before the puzzle can be generated, an
        exception is raised.

        Returns both the solved puzzle, as well as an unsolved puzzle (both as
        a Sudoku Puzzle object).'''
        pass

    @staticmethod
    def getEasyPuzzle(numKnownValues):
        '''Given:
        A number of known values in the puzzle.

        Generates a valid Sudoku puzzle using a simple pattern.

        Returns both the solved puzzle, as well as an unsolved puzzle (both as
        a Sudoku Puzzle object).'''
        pass

    @staticmethod
    def isSolved(puzzle):
        '''Given:
        A puzzle (a SudokuPuzzle object).

        Returns True if each value in each list is between 1 and 9, and there
        are no duplicates in the rows, columns, or 3x3 boxes that make up a
        sudoku puzzle.'''
        #Make sure we are working on a valid sudoku object.
        SudokuGenerator._validatePuzzle(puzzle)

        #This is very similar to the function which checks if a puzzle is
        #solved.  However, a solved puzzle cannot have any blank values.

        #A list of valid moves.
        validMoves = list(range(1, 10))

        #First make sure that all squares have a valid value.  If any of them
        #do not, return False.
        for key in puzzle.map:
            if puzzle.map[key] not in validMoves:
                return False

        #Next check for duplicates within each row of the puzzle.
        for row in puzzle.rows:
            #For each value in the row check how many times the value occures 
            #the row.  If it occures in the row more than once, then the puzze
            #is invalid.
            for value in row:
                if row.count(value) > 1:
                    return False

        #Next check for duplicates within each column of the puzzle.
        for column in puzzle.columns:
            #Same process as what we did for the rows.
            for value in column:
                if column.count(value) > 1:
                    return False

        #Finally check for duplicates within each 3x3 box of the puzzle.
        for key in puzzle.boxToGridMap:
            values = []
            #For each grid position (x,y) in the 3x3 box, check if the list
            #of values already has a given value in it.  If it does, then the
            #value is a duplicate and we return False.
            for mapKey in puzzle.boxToGridMap[key]:
                value = puzzle.map[mapKey]
                if value in values:
                    return False
                else:
                    values.append(value)

        #If none of the above, the puzzle is valid, return True.
        return True

    @staticmethod
    def isValidPuzzle(puzzle, blankValue=0):
        '''Given:
        A puzzle (a SudokuPuzzle object).
        A value for what a blank value in the puzzle should be (defaults to 0).

        Returns True if there are no duplicates in any of the rows, columns, or
        3x3 boxes that make up a sudoku puzzle.  Ignores blank values.'''
        #Make sure we are working on a valid sudoku object.
        SudokuGenerator._validatePuzzle(puzzle)

        #A list of valid moves.
        validMoves = list(range(1, 10))
        validMoves.append(blankValue)

        #First make sure that all squares have a valid value.  If any of them
        #do not, return False.
        for key in puzzle.map:
            if puzzle.map[key] not in validMoves:
                return False

        #Next check for duplicates within each row of the puzzle.
        for row in puzzle.rows:
            #For each value in the row (ignoring values that are the same as
            #blankValue) check how many times the value occures the row.  If it
            #occures in the row more than once, then the puzze is invalid.
            for value in row:
                if value == blankValue:
                    continue

                if row.count(value) > 1:
                    return False

        #Next check for duplicates within each column of the puzzle.
        for column in puzzle.columns:
            #Same process as what we did for the rows.
            for value in column:
                if value == blankValue:
                    continue

                if column.count(value) > 1:
                    return False

        #Finally check for duplicates within each 3x3 box of the puzzle.
        for key in puzzle.boxToGridMap:
            values = []
            #For each grid position (x,y) in the 3x3 box, check if the list
            #of values already has a given value in it.  If it does, then the
            #value is a duplicate and we return False.
            for mapKey in puzzle.boxToGridMap[key]:
                value = puzzle.map[mapKey]
                if value == blankValue:
                    continue

                if value in values:
                    return False
                else:
                    values.append(value)

        #If none of the above, the puzzle is valid, return True.
        return True


    @staticmethod
    def isValidMove(puzzle, row, column, value):
        '''Given:
        A puzzle (a SudokuPuzzle object).
        A row (between 0 and 8).
        A column (between 0 and 8).
        A value (between 1 and 9).

        Assumes that the move has not already been made.

        Returns True if the given move is legal based on what values are
        already in the puzzle.  Returns False if the given puzzle is already
        invalid or the given move is invalid.'''
        #Make sure we are working on a valid sudoku object.
        SudokuGenerator._validatePuzzle(puzzle)

        #First check if the value already exists within the 3x3 box that the
        #move was made in.
        if value in SudokuGenerator._getValuesInBox(puzzle, row, column):
            return False

        #Next check if the value already exists in the row of the puzzle that
        #the move is about to be made in.
        if value in puzzle.rows[row]:
            return False

        #Finally check if the value already exists in the column of that the
        #move is about to be made in.
        if value in puzzle.columns[column]:
            return False

        #If none of the above, then the move is legal, return True.
        return True

    @staticmethod
    def getPuzzleAsString(puzzle):
        '''Given:
        A puzzle (a SudokuPuzzle object).

        Returns a formated string of the current values of the puzzle.'''
        #Make sure we are working on a valid sudoku object.
        SudokuGenerator._validatePuzzle(puzzle)

        string = ""
        #Apparently I cant put "\n" directly into an fString, so a simple
        #variable to let me do what I want to do.
        lineBreak = "\n"
        for i in range(9):
            string += f"{lineBreak + lineBreak if i % 3 == 0 else lineBreak}"
            for j in range(9):
                string += f"{puzzle.rows[i][j]:>{5 if j % 3 == 0 else 3}}"

        return string + "\n"
        
    @staticmethod
    def _getValuesInBox(puzzle, row, column):
        '''Given:
        A puzzle (a SudokuPuzzle object).
        A row (between 0 and 8)
        a column (between 0 and 8)

        Finds all of the values in the 3x3 box that contains the given row and
        column.  Returns all values in the 3x3 box (including the given row and
        column).'''        
        #Make sure we are working on a valid sudoku object.
        SudokuGenerator._validatePuzzle(puzzle)

        #Get the key of the box, based on the given row and column.
        key = puzzle.gridToBoxMap[(row, column)]

        #Using the key, get the value of position in the grid.
        values = []
        for position in puzzle.boxToGridMap[key]:
            values.append(puzzle.map[position])

        return values        


    @staticmethod
    def _validatePuzzle(puzzle):
        '''Check that the given puzle is an instance of a SudokuPuzzle object.
        If it is not, an exception is raised.'''
        if type(puzzle) is not SudokuPuzzle:
            raise Exception(f"Given Puzzle: ({puzzle}) is not a valid Sudoku Puzzle.")



puzzle = SudokuPuzzle()
copy = puzzle.getCopy()
copy.setValue((3,3), "X")

print(SudokuGenerator.getPuzzleAsString(puzzle))
print(SudokuGenerator.getPuzzleAsString(copy))


print("Breakpoint")
