import math
import matplotlib
import tkinter as tk

ROW = 9
COL = 10

# Creating a shortcut for (int, int) pair type
Pair = tuple[int, int]

# Creating a shortcut for (double, (int, int)) pair type
pPair = tuple[float, Pair]

# A structure to hold the necessary parameters
class cell:
    def __init__(self):
        self.parent_i = None
        self.parent_j = None
        self.f = float('inf')
        self.g = float('inf')
        self.h = float('inf')

# A Utility Function to check whether given cell (row, col) is a valid cell or not
def isValid(row, col):
    return (row >= 0) and (row < ROW) and (col >= 0) and (col < COL)

# A Utility Function to check whether the given cell is blocked or not
def isUnBlocked(grid, row, col):
    return grid[row][col] == 1

# A Utility Function to check whether destination cell has been reached or not
def isDestination(row, col, dest):
    return (row == dest[0]) and (col == dest[1])

# A Utility Function to calculate the 'h' heuristics
def calculateHValue(row, col, dest):
    return math.sqrt((row - dest[0])**2 + (col - dest[1])**2)

# A Utility Function to trace the path from the source to destination
def tracePath(cellDetails, dest):
    print("The Path is ", end="")
    row = dest[0]
    col = dest[1]

    Path = []

    while not (cellDetails[row][col].parent_i == row and cellDetails[row][col].parent_j == col):
        Path.append((row, col))
        temp_row = cellDetails[row][col].parent_i
        temp_col = cellDetails[row][col].parent_j
        row = temp_row
        col = temp_col

    Path.append((row, col))

    while Path:
        p = Path.pop()
        print(f"-> {p}", end=" ")

# A Function to find the shortest path between a given source cell to a destination cell according to A* Search Algorithm
def aStarSearch(grid, src, dest):
    # If the source is out of range
    if not (0 <= src[0] < ROW and 0 <= src[1] < COL):
        print("Source is invalid")
        return

    # If the destination is out of range
    if not (0 <= dest[0] < ROW and 0 <= dest[1] < COL):
        print("Destination is invalid")
        return

    # Either the source or the destination is blocked
    if not (isUnBlocked(grid, src[0], src[1]) and isUnBlocked(grid, dest[0], dest[1])):
        print("Source or the destination is blocked")
        return

    # If the destination cell is the same as source cell
    if isDestination(src[0], src[1], dest):
        print("We are already at the destination")
        return

    # Create a closed list and initialise it to false which means that no cell has been included yet
    closedList = [[False for _ in range(COL)] for _ in range(ROW)]

    # Declare a 2D array of structure to hold the details of that cell
    cellDetails = [[cell() for _ in range(COL)] for _ in range(ROW)]

    i, j = src
    cellDetails[i][j].f = 0.0
    cellDetails[i][j].g = 0.0
    cellDetails[i][j].h = 0.0
    cellDetails[i][j].parent_i = i
    cellDetails[i][j].parent_j = j

    # Create an open list having information as- <f, <i, j>> where f = g + h, and i, j are the row and column index of that cell
    openList = [(0.0, (i, j))]

    # We set this boolean value as false as initially the destination is not reached.
    foundDest = False

    while openList:
        p = openList.pop(0)
        i, j = p[1]

        closedList[i][j] = True

        gNew, hNew, fNew = 0.0, 0.0, 0.0

        #----------- 1st Successor (North) ------------
        if isValid(i-1, j):
            if isDestination(i-1, j, dest):
                cellDetails[i-1][j].parent_i = i
                cellDetails[i-1][j].parent_j = j
                print("The destination cell is found")
                tracePath(cellDetails, dest)
                foundDest = True
                return
            elif closedList[i-1][j] == False and isUnBlocked(grid, i-1, j):
                gNew = cellDetails[i][j].g + 1.0
                hNew = calculateHValue(i-1, j, dest)
                fNew = gNew + hNew

                if cellDetails[i-1][j].f == float('inf') or cellDetails[i-1][j].f > fNew:
                    openList.append((fNew, (i-1, j)))

                    cellDetails[i-1][j].f = fNew
                    cellDetails[i-1][j].g = gNew
                    cellDetails[i-1][j].h = hNew
                    cellDetails[i-1][j].parent_i = i
                    cellDetails[i-1][j].parent_j = j

        #----------- 2nd Successor (South) ------------
        if isValid(i+1, j):
            if isDestination(i+1, j, dest):
                cellDetails[i+1][j].parent_i = i
                cellDetails[i+1][j].parent_j = j
                print("The destination cell is found")
                tracePath(cellDetails, dest)
                foundDest = True
                return
            elif closedList[i+1][j] == False and isUnBlocked(grid, i+1, j):
                gNew = cellDetails[i][j].g + 1.0
                hNew = calculateHValue(i+1, j, dest)
                fNew = gNew + hNew

                if cellDetails[i+1][j].f == float('inf') or cellDetails[i+1][j].f > fNew:
                    openList.append((fNew, (i+1, j)))

                    cellDetails[i+1][j].f = fNew
                    cellDetails[i+1][j].g = gNew
                    cellDetails[i+1][j].h = hNew
                    cellDetails[i+1][j].parent_i = i
                    cellDetails[i+1][j].parent_j = j

        #----------- 3rd Successor (East) ------------
        if isValid(i, j+1):
            if isDestination(i, j+1, dest):
                cellDetails[i][j+1].parent_i = i
                cellDetails[i][j+1].parent_j = j
                print("The destination cell is found")
                tracePath(cellDetails, dest)
                foundDest = True
                return
            elif closedList[i][j+1] == False and isUnBlocked(grid, i, j+1):
                gNew = cellDetails[i][j].g + 1.0
                hNew = calculateHValue(i, j+1, dest)
                fNew = gNew + hNew

                if cellDetails[i][j+1].f == float('inf') or cellDetails[i][j+1].f > fNew:
                    openList.append((fNew, (i, j+1)))

                    cellDetails[i][j+1].f = fNew
                    cellDetails[i][j+1].g = gNew
                    cellDetails[i][j+1].h = hNew
                    cellDetails[i][j+1].parent_i = i
                    cellDetails[i][j+1].parent_j = j

        #----------- 4th Successor (West) ------------
        if isValid(i, j-1):
            if isDestination(i, j-1, dest):
                cellDetails[i][j-1].parent_i = i
                cellDetails[i][j-1].parent_j = j
                print("The destination cell is found")
                tracePath(cellDetails, dest)
                foundDest = True
                return
            elif closedList[i][j-1] == False and isUnBlocked(grid, i, j-1):
                gNew = cellDetails[i][j].g + 1.0
                hNew = calculateHValue(i, j-1, dest)
                fNew = gNew + hNew

                if cellDetails[i][j-1].f == float('inf') or cellDetails[i][j-1].f > fNew:
                    openList.append((fNew, (i, j-1)))

                    cellDetails[i][j-1].f = fNew
                    cellDetails[i][j-1].g = gNew
                    cellDetails[i][j-1].h = hNew
                    cellDetails[i][j-1].parent_i = i
                    cellDetails[i][j-1].parent_j = j

        #----------- 5th Successor (North-East) ------------
        if isValid(i-1, j+1):
            if isDestination(i-1, j+1, dest):
                cellDetails[i-1][j+1].parent_i = i
                cellDetails[i-1][j+1].parent_j = j
                print("The destination cell is found")
                tracePath(cellDetails, dest)
                foundDest = True
                return
            elif closedList[i-1][j+1] == False and isUnBlocked(grid, i-1, j+1):
                gNew = cellDetails[i][j].g + math.sqrt(2)
                hNew = calculateHValue(i-1, j+1, dest)
                fNew = gNew + hNew

                if cellDetails[i-1][j+1].f == float('inf') or cellDetails[i-1][j+1].f > fNew:
                    openList.append((fNew, (i-1, j+1)))

                    cellDetails[i-1][j+1].f = fNew
                    cellDetails[i-1][j+1].g = gNew
                    cellDetails[i-1][j+1].h = hNew
                    cellDetails[i-1][j+1].parent_i = i
                    cellDetails[i-1][j+1].parent_j = j

        #----------- 6th Successor (North-West) ------------
        if isValid(i-1, j-1):
            if isDestination(i-1, j-1, dest):
                cellDetails[i-1][j-1].parent_i = i
                cellDetails[i-1][j-1].parent_j = j
                print("The destination cell is found")
                tracePath(cellDetails, dest)
                foundDest = True
                return
            elif closedList[i-1][j-1] == False and isUnBlocked(grid, i-1, j-1):
                gNew = cellDetails[i][j].g + math.sqrt(2)
                hNew = calculateHValue(i-1, j-1, dest)
                fNew = gNew + hNew

                if cellDetails[i-1][j-1].f == float('inf') or cellDetails[i-1][j-1].f > fNew:
                    openList.append((fNew, (i-1, j-1)))

                    cellDetails[i-1][j-1].f = fNew
                    cellDetails[i-1][j-1].g = gNew
                    cellDetails[i-1][j-1].h = hNew
                    cellDetails[i-1][j-1].parent_i = i
                    cellDetails[i-1][j-1].parent_j = j

        #----------- 7th Successor (South-East) ------------
        if isValid(i+1, j+1):
            if isDestination(i+1, j+1, dest):
                cellDetails[i+1][j+1].parent_i = i
                cellDetails[i+1][j+1].parent_j = j
                print("The destination cell is found")
                tracePath(cellDetails, dest)
                foundDest = True
                return
            elif closedList[i+1][j+1] == False and isUnBlocked(grid, i+1, j+1):
                gNew = cellDetails[i][j].g + math.sqrt(2)
                hNew = calculateHValue(i+1, j+1, dest)
                fNew = gNew + hNew

                if cellDetails[i+1][j+1].f == float('inf') or cellDetails[i+1][j+1].f > fNew:
                    openList.append((fNew, (i+1, j+1)))

                    cellDetails[i+1][j+1].f = fNew
                    cellDetails[i+1][j+1].g = gNew
                    cellDetails[i+1][j+1].h = hNew
                    cellDetails[i+1][j+1].parent_i = i
                    cellDetails[i+1][j+1].parent_j = j

        #----------- 8th Successor (South-West) ------------
        if isValid(i+1, j-1):
            if isDestination(i+1, j-1, dest):
                cellDetails[i+1][j-1].parent_i = i
                cellDetails[i+1][j-1].parent_j = j
                print("The destination cell is found")
                tracePath(cellDetails, dest)
                foundDest = True
                return
            elif closedList[i+1][j-1] == False and isUnBlocked(grid, i+1, j-1):
                gNew = cellDetails[i][j].g + math.sqrt(2)
                hNew = calculateHValue(i+1, j-1, dest)
                fNew = gNew + hNew

                if cellDetails[i+1][j-1].f == float('inf') or cellDetails[i+1][j-1].f > fNew:
                    openList.append((fNew, (i+1, j-1)))

                    cellDetails[i+1][j-1].f = fNew
                    cellDetails[i+1][j-1].g = gNew
                    cellDetails[i+1][j-1].h = hNew
                    cellDetails[i+1][j-1].parent_i = i
                    cellDetails[i+1][j-1].parent_j = j

    if not foundDest:
        print("Failed to find the Destination Cell")
    return

def visualizePath(grid, cellDetails, dest):
    ROW = len(grid)
    COL = len(grid[0])
    
    for i in range(ROW):
        for j in range(COL):
            if cellDetails[i][j].parent_i != -1 and cellDetails[i][j].parent_j != -1:
                parent_i = cellDetails[i][j].parent_i
                parent_j = cellDetails[i][j].parent_j
                print(f'({i},{j}) <-- ({parent_i},{parent_j})')

# Driver code
if __name__ == "__main__":
    grid = [[1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
            [1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
            [1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
            [0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1, 0, 1, 0],
            [1, 0, 1, 1, 1, 1, 0, 1, 0, 0],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
            [1, 1, 1, 0, 0, 0, 1, 0, 0, 1]]

    src = (0, 0)
    dest = (8, 1)

    aStarSearch(grid, src, dest)
