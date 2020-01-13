#Sudoku Generator 5
#This is a cleaned up version of my previous attempt at making a nice file to
#handle generating and solving of a Sudoku Puzzle while also providing some
#nice functions to help anything that uses this file to make a UI.  The
#biggest difference between this file and SudokuGenerator_4 is the inclusion of
#the SudokuBoard object which is a wrapper class to help describe and access
#the data of a Sudoku puzzle.

#This file contains the class SudokuBoard, which is a class designed to help
#storing the data of a sudoku while also allowing for easy access to different
#parts of the board in easy ways.  All functions in this file either take in or
#return a SudokuBoard object.

#There are 2 functions you can use to get a Sudoku puzzle:

#getHardPuzzle() generates a Sudoku Puzzle using a backtracking algorithm.  It
#then attempts to generate a uniquely solvable solution with a given number of
#starting moves.  This returns both a solved, and an unsolved version of the
#puzzle.

#getEasyPuzzle() generate a Sudoku Puzzle using a simple pattern with a bit of
#randomness.  These puzzles are not garunteed to have a unique solution, and
#combined with how they are generated are considered easy puzzle (regardless of
#how many starting moves given).  This returns both a solved, and an unsolved
#version of the puzzle.


#In addition the following functions can be useful when setting up a Sudoku UI:

#isValidPuzzle() checks if a puzzle has an duplicates in its rows, columns, or
#boxes.  It also checks that empty squares all have the same value.

#isSolved() checks if a puzzle is a valid completed solution (no duplicates in
#rows, column, boxes (and only numbers 1 - 9)).

#isValidMove() checks if a given row, column, and value is a legal move in a
#given Sudoku puzzle based on what is already in the puzzle.

#getValidMovesAt() given a row, column, and puzzle, returns a list of legal
#numbers that can be in that square.

import random
import math
import time

class SudokuBoard:
    '''This class is designed to be used instead of a simple list of lists to
    represent the sudoku puzzle board.  This class allows easy access of rows,
    columns and grid locations (x,y).  In addition, it allows access to all
    values within any of the 3x3 boxes that make up the 9x9 grid.'''

    def __init__(self, defaultValue = 0, rows = None, columns = None, map = None, boxLookup = None, reverseLookup = None):
        '''Given:
        A default value for each sqaure (defaults to 0).
        -OR-
        Several objects used to create a deep clone of this object.

        Creates a Sudoku Board and stores the data in multiple different
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
            xPosition = int(math.floor(key[0] / 3))
            yPosition = int(math.floor(key[1] / 3))
            position = (xPosition, yPosition)
            if position not in self.__reverseBoxLookup:
                self.__reverseBoxLookup[position] = []
            self.__reverseBoxLookup[position].append(key)

            self.__boxLookup[key] = position

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
        '''
        Given:
        A key (x, y) position in the puzzle
        A value to set the square in the grid to.

        Changes the current value in the grid to the new value.'''
        self.__rows[key[0]][key[1]] = value
        self.__columns[key[1]][key[0]] = value
        self.__map[key] = value

    def setRowValues(self, row, values):
        '''
        Given:
        A row number (0 - 8).
        A list of values (9 values).

        Changes the current value in each square in a given row to a new value.
        '''
        for i in range(9):
            self.setValue((row, i), values[i])

    def setColumnValues(self, column, values):
        '''
        Given:
        A column number (0 - 8).
        A list of values (9 values).

        Changes the current value in each sqaure in a given column to a new
        value.
        '''
        for i in range(9):
            self.setValue((i, column), values[i])

    def getCopy(self):
        '''Returns a deep copy of the SudokuBoard that can be modified without
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

        return SudokuBoard(0, cRows, cColumns, cMap, cLookup, cReverse)
        

    def __str__(self):
        return str(self.__rows)


def validatePuzzleObject(puzzle):
    '''
    Check that the given puzle is an instance of a SudokuBoard object.
    If it is not, an exception is raised.
    '''
    if type(puzzle) is not SudokuBoard:
        raise Exception(f"Given Puzzle: ({puzzle}) is not a valid Sudoku Board.")

def getHardPuzzle(numKnownValues, blankValue = 0, attemptUniqueSolution = True, maxDuration = 60):
    '''
    Given:
    A number of known values in the puzzle.
    If the puzzle should have only a single solution.
    The maximum amount of time to try and make a puzzle (in seconds).

    Generates a valid Sudoku puzzle using a backtracking recursive
    algorithm.
    If maxDuration seconds occure before the puzzle can be generated, an
    exception is raised.

    If attemptUniqueSolution is True, a unique puzzle is attempted to be
    generated, however if time runs out, the puzzle is not gaurenteed to have
    a unique solution.

    Returns both the solved puzzle, as well as an unsolved puzzle (both as
    a Sudoku Board object).
    '''
    #Calculate when our end time is.
    endTime = time.time() + maxDuration
    
    #Get a soon to be solved puzzle.
    solvedPuzzle = SudokuBoard()

    #Get a fully solved and valid puzzle.
    _getRecursivePuzzle(solvedPuzzle, blankValue, endTime)

    #Check that the puzzle is fully solved.  If it is not, raise an exception.
    if not isSolved(solvedPuzzle):
        print(getPuzzleAsString(solvedPuzzle))
        raise Exception(f"Sudoku Generator - getHardPuzzle: unable to generate a puzzle in {maxDuration} seconds.")

    #Now take our solved puzzle and remove moves from it until we only have
    #numKnownValues squares left filled in the puzzle.  If we are trying to
    #force a unique solution we will use an our backtracking recursive function
    #to check if removing a number makes the solution unique.
    numValuesRemoved = 0
    puzzle = solvedPuzzle.getCopy()
    if attemptUniqueSolution:
        #While we have not removed enough values from the solved puzzle.
        while numValuesRemoved != (81 - numKnownValues):
            #Check that we are not out of time.  If we are, break from the
            #loop.
            if _isOutOfTime(endTime):
                break

            #A slight hack to allow us to pass an integer by ref, we are
            #wrapping it in a list (which is passed by ref as we want).
            numSolutions = [0]
            maxSolutions = 2

            #Pick a random square in the grid to remove the value of.
            ranRow = random.randint(0, 8)
            ranCol = random.randint(0, 8)

            #If the randomly chosen square has already had its value removed,
            #continue and choose a different square.
            if puzzle.map[(ranRow, ranCol)] == blankValue:
                continue

            #Set the value of the square to blankValue and check if the puzzle
            #has a single unique solution.  Make sure to store the value of the
            #square in case we need to change it back.
            oldValue = puzzle.map[(ranRow, ranCol)]
            puzzle.setValue((ranRow, ranCol), blankValue)

            #Now check how many solutions the puzzle has.
            _getRecursiveNumSolutions(puzzle.getCopy(), blankValue, endTime, numSolutions, maxSolutions)

            #If there is more than 1 solution, set the square back to its
            #value, and continue the loop to try a new square.
            if numSolutions[0] > 1:
                puzzle.setValue((ranRow, ranCol), oldValue)
                continue

            #At this point we have removed a value from the puzzle and still
            #have a unique solution.  We just want to increase the counter of
            #how many values we have removed.
            numValuesRemoved += 1

    if numValuesRemoved != numKnownValues:
        #If either we have run out of time, to use our backtracking function or
        #we were never lookking for a unique solution, remove values from the
        #puzzle until we have the correct number of known starting values.
        puzzle = _getAnyUnsolvedPuzzle(puzzle, numKnownValues, blankValue)

    #Return both the solved and unsolved puzzle.
    return solvedPuzzle, puzzle

def _isOutOfTime(maxTime):
    '''
    Given:
    A number of seconds since the epoch.

    Returns true if the number of seconds has passed.
    Returns false if the number of seconds has not passed.
    '''
    return time.time() >= maxTime

def _getRecursiveNumSolutions(puzzle, blankValue, maxTime, numSolutions, maxSolutions):
    '''
    Given:
    A solved puzzle (a SudokuBoard object).
    The value of the unsolved squares in the puzzle
    A maximum number of seconds since the epoch.
    A list of a single integer (so that it can be passed by ref).
    An integer of the maximum number of solutions to look for.

    Attempts to solve a given sudoku board.  Each time a soltion is found, the
    integer inside of numSolutions is increased by 1.  If either maxSolutions
    are found or, maxTime is reached, the function stops.

    Uses the same type of recusive logic as is used to generate the puzzle.

    Returns no actual data, but changes the integer within the numSolutions
    list.
    '''
    #Make sure we are working on a valid sudoku object.
    validatePuzzleObject(puzzle)
    #Because this function is recursive, we want to start by checking if we are
    #out of time.
    if _isOutOfTime(maxTime):
        return True

    #Next check if we have already found the maximum number of solutions that
    #we are looking for.
    if numSolutions[0] >= maxSolutions:
        return True

    #Loop through all squares in the grid.
    for i in range(81):
        #Get the current row and column of our puzzle.
        row = i // 9
        column = i % 9

        #If the value of the square is not a blank value, continue to the next
        #square.
        if puzzle.map[(row, column)] != blankValue:
            continue

        #Get the possible moves that can be at the sqaure.
        possibleValues = getValidMovesAt(puzzle, row, column)
        
        #Shuffle the list of possible moves.
        random.shuffle(possibleValues)

        #For each possible move, set the value of the square to the value and
        #check if the puzzle is solved.  If it is, we are done.  If not, see if
        #calling this function 1 more time will solve the puzzle.  If it will,
        #again we are done.  If not, set the value of the sqaure to a different
        #possible value, and try the entire recursive logic again.
        for value in possibleValues:
            #Because of how this recursive function works, this block of code
            #can be executed after we have run out of time, so it is important
            #to check if we have run out of time at the start of each iteration
            #of this loop.
            if _isOutOfTime(maxTime):
                return True

            #Set the value of the sqaure to a valid value and then look at the
            #puzzle as a whole.
            puzzle.setValue((row, column), value)

            #Check if the puzzle is completly solved.
            if isSolved(puzzle):
                #If the puzzle is solved, increase the number of solutions
                #found by 1.
                numSolutions[0] += 1
                return True
            else:
                #Otherwise, call this function to continue trying to generate
                #the puzzle.  If 1 more call of the function completes the 
                #puzzle then we are done.  Otherwise, try a different valid
                #value in the sqaure.
                #print(getPuzzleAsString(puzzle))
                if _getRecursivePuzzle(puzzle, blankValue, maxTime):
                    numSolutions[0] += 1
                    return True

        #If this square has no valid moves, then set this square to a blank
        #value and return False.
        puzzle.setValue((row, column), blankValue) 
        return False

def _getRecursivePuzzle(puzzle, blankValue, maxTime):
    '''
    Given:
    A solved puzzle (a SudokuBoard object).
    The value of the unsolved squares in the puzzle
    A maximum number of seconds since the epoch.

    Uses a backtracking recursive algorithm to generate a legal Sudoku puzzle.
    First it looks for the first unsolved square in the puzzle and then tries
    each valid value that can go into that square.  Once it has a value in the
    square it checks if the puzze is solved.  If not, it then calls itself to
    see if the puzzle will be solved.  If it reaches a dead end of numbers, it
    then backtracks by setting the square that it is looking at to a blank
    value.

    Returns value does not contain information.
    Changes the SudokuBoard object that is passed by reference into this
    function.
    '''
    #Make sure we are working on a valid sudoku object.
    validatePuzzleObject(puzzle)
    #Because this function is recursive, we want to start by checking if we are
    #out of time.
    if _isOutOfTime(maxTime):
        return True

    #Loop through all squares in the grid.
    for i in range(81):
        #Get the current row and column of our puzzle.
        row = i // 9
        column = i % 9

        #If the value of the square is not a blank value, continue to the next
        #square.
        if puzzle.map[(row, column)] != blankValue:
            continue

        #Get the possible moves that can be at the sqaure.
        possibleValues = getValidMovesAt(puzzle, row, column)
        
        #Shuffle the list of possible moves.
        random.shuffle(possibleValues)

        #For each possible move, set the value of the square to the value and
        #check if the puzzle is solved.  If it is, we are done.  If not, see if
        #calling this function 1 more time will solve the puzzle.  If it will,
        #again we are done.  If not, set the value of the sqaure to a different
        #possible value, and try the entire recursive logic again.
        for value in possibleValues:
            #Because of how this recursive function works, this block of code
            #can be executed after we have run out of time, so it is important
            #to check if we have run out of time at the start of each iteration
            #of this loop.
            if _isOutOfTime(maxTime):
                return True

            #Set the value of the sqaure to a valid value and then look at the
            #puzzle as a whole.
            puzzle.setValue((row, column), value)

            #Check if the puzzle is completly solved.
            if isSolved(puzzle):
                #If the puzzle is solved, we are done.
                return True
            else:
                #Otherwise, call this function to continue trying to generate
                #the puzzle.  If 1 more call of the function completes the 
                #puzzle then we are done.  Otherwise, try a different valid
                #value in the sqaure.
                #print(getPuzzleAsString(puzzle))
                if _getRecursivePuzzle(puzzle, blankValue, maxTime):
                    return True

        #If this square has no valid moves, then set this square to a blank
        #value and return False.
        puzzle.setValue((row, column), blankValue) 
        return False

def getEasyPuzzle(numKnownValues, blankValue = 0):
    '''
    Given:
    A number of known values in the puzzle.
    The value of the unsolved squares in the puzzle (optional).

    Generates a valid Sudoku puzzle using a simple pattern.

    Returns both the solved puzzle, as well as an unsolved puzzle (both as
    a Sudoku Board object).
    '''
    #First validate that numKnownValue is at between 0 and 81.
    if numKnownValues < 0:
        numKnownValues = 0
    elif numKnownValues > 81:
        numKnownValues = 81

    #Get a completed sudoku puzzle.  This puzzle is generated by using a simple
    #pattern.  This makes the puzzle rather easy to solve if you know the
    #pattern, or are aware how the puzzle was generated.
    solvedPuzzle = _getSolvedPatternPuzzle(blankValue)

    #Given our solved puzzle, get a non unique solvable puzzle by removing
    #numbers at random from the puzzle, until there are only the given number
    #of known values in the puzzle.
    unsolvedPuzzle = _getAnyUnsolvedPuzzle(solvedPuzzle, numKnownValues, blankValue)

    #Return both the solved puzzle, and the unsolved puzzle.
    return solvedPuzzle, unsolvedPuzzle

def _getSolvedPatternPuzzle(blankValue):
    '''
    Generates a valid completed Sudoku puzzle using a simple pattern with a
    random start.

    Returns a completed Sudoku puzzle (a SudokuBoard object).
    '''
    #First get a blank sudoku board.
    puzzle = SudokuBoard(defaultValue=blankValue)

    #Next randomly generate the first row of the puzzle.
    for i in range(9):
        ranNum = random.randint(1, 9)
        #Make sure that we do not include duplicates in the row.
        while ranNum in puzzle.rows[0]:
            ranNum = random.randint(1, 9)

        puzzle.setValue((0, i), ranNum)

    #For all following rows of the puzzle shift the index of values of the
    #previous row by 3, unless the row number is divisible by 3, in which case
    #we only shift the index by 1 per value.
    for i in range(1, 9):
        shift = 3
        if i % 3 == 0:
            shift = 1

        for j in range(9):
            index = j + shift
            if index >= 9:
                index -= 9

            puzzle.setValue((i, j), puzzle.rows[i - 1][index])

    #At this point we have an easy puzzle generated using a simple pattern.
    #Now we want to do a small bit of shuffling so that the pattern is a little
    #bit harder to see (especially when solving the puzzle).  To do this we
    #will shift the position of the first 3 rows of the puzzle with one of the
    #following: the second 3 rows or the final 3 rows.  This should help to
    #make the pattern a bit harder to see when solving the puzzle.
    
    print(getPuzzleAsString(puzzle))

    #Get a random box position (1 or 2)
    newPosition = random.randint(1, 2)

    #Get a copy of the puzzle, so that we can swap row values.
    copy = puzzle.getCopy()

    #Switch the values of the first 3 rows with either the second or third
    #three rows, based on what the value of newPosition is.
    for i in range(3):
        otherRow = (newPosition * 3) + i
        puzzle.setRowValues(i, copy.rows[otherRow])
        puzzle.setRowValues(otherRow, copy.rows[i])

    #Return the solved puzzle.
    return puzzle
    
def _getAnyUnsolvedPuzzle(solvedPuzzle, numKnownValues, blankValue):
    '''
    Given:
    A solved puzzle (a SudokuBoard object).
    A number of known values in the puzzle.
    The value of the unsolved squares in the puzzle (optional).

    Removes values from the solved sudoku at random until there are only
    numKnownValues values remaining in the puzzle.

    Returns a copy of the puzzle with values removed.
    '''
    #Make sure we are working on a valid sudoku object.
    validatePuzzleObject(solvedPuzzle)
    #Copy the puzzle.
    puzzle = solvedPuzzle.getCopy()

    #Get the number of blank values already in the puzzle.
    numBlanks = 0
    for key in puzzle.map:
        if puzzle.map[key] == blankValue:
            numBlanks += 1

    #Set values in the puzzle to the given blank value until the number of
    #blank values in the puzzle is equal to the number we were given.
    while numBlanks != (81 - numKnownValues):
        #Get a random square in the grid.
        ranRow = random.randint(0, 8)
        ranCol = random.randint(0, 8)

        #Check that the value has not already been set to the blank value.
        if puzzle.map[(ranRow, ranCol)] == blankValue:
            continue

        #Set the value of the square to the blank value, and increase the
        #newBlanks counter by 1.
        puzzle.setValue((ranRow, ranCol), blankValue)
        numBlanks += 1

    #Return the copy of the puzzle.
    return puzzle

def getPuzzleAsString(puzzle):
    '''
    Given:
    A puzzle (a SudokuBoard object).

    Returns a formated string of the current values of the puzzle.
    '''
    #Make sure we are working on a valid sudoku object.
    validatePuzzleObject(puzzle)

    string = ""
    #Apparently I cant put "\n" directly into an fString, so a simple
    #variable to let me do what I want to do.
    lineBreak = "\n"
    for i in range(9):
        string += f"{lineBreak + lineBreak if i % 3 == 0 else lineBreak}"
        for j in range(9):
            string += f"{puzzle.rows[i][j]:>{5 if j % 3 == 0 else 3}}"

    return string + "\n"
 
def getValuesInBox(puzzle, row, column):
    '''
    Given:
    A puzzle (a SudokuBoard object).
    A row (between 0 and 8)
    A column (between 0 and 8)

    Finds all of the values in the 3x3 box that contains the given row and
    column.  Returns all values in the 3x3 box (including the given row and
    column).
    '''        
    #Make sure we are working on a valid sudoku object.
    validatePuzzleObject(puzzle)

    #Get the key of the box, based on the given row and column.
    key = puzzle.gridToBoxMap[(row, column)]

    #Using the key, get the value of position in the grid.
    values = []
    for position in puzzle.boxToGridMap[key]:
        values.append(puzzle.map[position])

    return values        

def isValidPuzzle(puzzle, blankValue=0):
    '''
    Given:
    A puzzle (a SudokuBoard object).
    A value for what a blank value in the puzzle should be (defaults to 0).

    Returns True if there are no duplicates in any of the rows, columns, or
    3x3 boxes that make up a sudoku puzzle.  Ignores blank values.
    '''
    #Make sure we are working on a valid sudoku object.
    validatePuzzleObject(puzzle)

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

def isSolved(puzzle):
    '''
    Given:
    A puzzle (a SudokuBoard object).
    Returns True if each value in each row, column, and 3x3 box of the
    puzzle contain the numbers 1 - 9 with no duplicates in any row, column
    or 3x3 box.
    '''
    #Make sure we are working on a valid sudoku object.
    validatePuzzleObject(puzzle)

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

def isValidMove(puzzle, row, column, value):
    '''
    Given:
    A puzzle (a SudokuBoard object).
    A row (between 0 and 8).
    A column (between 0 and 8).
    A value (between 1 and 9).

    Assumes that the move has not already been made.

    Returns True if the given move is legal based on what values are
    already in the puzzle.  Returns False if the given puzzle is already
    invalid or the given move is invalid.'''
    #Make sure we are working on a valid sudoku object.
    validatePuzzleObject(puzzle)

    #First check if the value already exists within the 3x3 box that the
    #move was made in.
    if value in getValuesInBox(puzzle, row, column):
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

def getValidMovesAt(puzzle, row, column):
    '''
    Given:
    A puzzle (a SudokuBoard object).
    A row number (0 - 8)
    A column number (0 - 8)

    Finds all valid numbers that the given square in the grid could have.
    Returns a list of valid numbers.
    '''
    #Make sure we are working on a valid sudoku object.
    validatePuzzleObject(puzzle)

    #Using a list of possible values (1-9) check each value to see if it
    #is valid.  If it is, add it to the return list of values.
    values = []
    possibleValues = list(range(1, 10))
    for value in possibleValues:
        if isValidMove(puzzle, row, column, value):
            values.append(value)

    return values
