import collections
import queue

class Node:

    def __init__(self, puzzle, last=None):
            self.puzzle = puzzle
            self.last = last

    @property
    def seq(self):
        node, seq = self, []
        while node:
            seq.append(node)
            node = node.last
        yield from reversed(seq)

    @property
    def state(self):
        return str(self.puzzle.board)

    @property
    def isSolved(self):
        return self.puzzle.isSolved

    @property
    def getMoves(self):
        return self.puzzle.getMoves

class Puzzle:

    def __init__(self, startBoard):
        self.board = startBoard

    @property
    def getMoves(self):

        possibleNewBoards = []

        zeroPos = self.board.index(0)

        if zeroPos == 0:
            possibleNewBoards.append(self.move(0,1))
            possibleNewBoards.append(self.move(0,3))
        elif zeroPos == 1:
            possibleNewBoards.append(self.move(1,0))
            possibleNewBoards.append(self.move(1,2))
            possibleNewBoards.append(self.move(1,4))
        elif zeroPos == 2:
            possibleNewBoards.append(self.move(2,1))
            possibleNewBoards.append(self.move(2,5))
        elif zeroPos == 3:
            possibleNewBoards.append(self.move(3,0))
            possibleNewBoards.append(self.move(3,4))
            possibleNewBoards.append(self.move(3,6))
        elif zeroPos == 4:
            possibleNewBoards.append(self.move(4,1))
            possibleNewBoards.append(self.move(4,3))
            possibleNewBoards.append(self.move(4,5))
            possibleNewBoards.append(self.move(4,7))
        elif zeroPos == 5:
            possibleNewBoards.append(self.move(5,2))
            possibleNewBoards.append(self.move(5,4))
            possibleNewBoards.append(self.move(5,8))
        elif zeroPos == 6:
            possibleNewBoards.append(self.move(6,3))
            possibleNewBoards.append(self.move(6,7))
        elif zeroPos == 7:
            possibleNewBoards.append(self.move(7,4))
            possibleNewBoards.append(self.move(7,6))
            possibleNewBoards.append(self.move(7,8))
        else:
            possibleNewBoards.append(self.move(8,5))
            possibleNewBoards.append(self.move(8,7))

        return possibleNewBoards

    def move(self, current, to):

        changeBoard = self.board[:]
        changeBoard[to], changeBoard[current] = changeBoard[current], changeBoard[to]
        return Puzzle(changeBoard)

    def printPuzzle(self):

        copyBoard = self.board[:]
        return copyBoard


    @property
    def isSolved(self):
        return self.board == [0,1,2,3,4,5,6,7,8] # goal board

class Solver:

    def __init__(self, Puzzle):
        self.puzzle = Puzzle

    def solveBFS(self):
        startNode = Node(self.puzzle)
        myQueue = collections.deque([startNode])
        visited = set()
        visited.add(myQueue[0].state)
        while myQueue:
            currentNode = myQueue.pop()
            if currentNode.puzzle.isSolved:
                return currentNode.seq

            for board in currentNode.getMoves:
                nextNode = Node(board, currentNode)

                if nextNode.state not in visited:
                    myQueue.appendleft(nextNode)
                    visited.add(nextNode.state)

def startBFS(board_value):
    startingBoard = board_value

    myPuzzle = Puzzle(startingBoard) #starting board
    mySolver = Solver(myPuzzle)
    goalSeq = mySolver.solveBFS()

    counter = -1
    num_move = []
    for node in goalSeq:
        counter = counter + 1
        num_move.append(node.puzzle.printPuzzle())

    return num_move
