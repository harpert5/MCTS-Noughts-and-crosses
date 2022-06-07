import sys


def printboard(board):
    print(board[0] + "|" + board[1] + "|" + board[2])
    print("-+-+-")
    print(board[3] + "|" + board[4] + "|" + board[5])
    print("-+-+-")
    print(board[6] + "|" + board[7] + "|" + board[8])


# simplify how board is stored
# e.g store as a string
def resetboard():
    board = {0: " ", 1: " ", 2: " ", 3: " ", 4: " ", 5: " ", 6: " ", 7: " ", 8: " "}
    return board


def freespace(position, board):

    if board[position] == " ":
        return True
    else:
        return False


def checkdraw(board):
    for key in board.keys():
        if board[key] == " ":
            return False

    return True


def checkwin(board):

    if board[0] == board[1] and board[0] == board[2] and board[0] != " ":
        return True
    elif board[3] == board[4] and board[3] == board[5] and board[3] != " ":
        return True
    elif board[6] == board[7] and board[6] == board[8] and board[6] != " ":
        return True
    elif board[0] == board[3] and board[0] == board[6] and board[0] != " ":
        return True
    elif board[1] == board[4] and board[1] == board[7] and board[1] != " ":
        return True
    elif board[2] == board[5] and board[2] == board[8] and board[2] != " ":
        return True
    elif board[0] == board[4] and board[0] == board[8] and board[0] != " ":
        return True
    elif board[6] == board[4] and board[6] == board[2] and board[6] != " ":
        return True
    else:
        return False


def play(letter, position, board):  # board so coppies can be made

    if freespace(position, board):
        board[position] = letter

        if checkwin(board):
            if letter == "X":
                return
                # print('X wins')
                # sys.exit()

            else:
                return
                # print('O wins')
                # sys.exit()

        if checkdraw(board):
            return
            # print('Draw')
            # sys.exit()

    else:
        print("Invalid move, space allready used")
        position = int(input("Enter new position: "))
        play(letter, position, board)
        return


# test for legality, instead of list- is move legal return True/false
def leagalmoves(board):
    availablemoves = []
    for move in range(0, 9):
        if board[move] == " ":
            availablemoves.append(move)
    return availablemoves


def currentplayer(player):
    if player == "X":
        player = "O"
        return player
    if player == "O":
        player = "X"
        return player


import math
import random

# need to make a class that defines nodes.
# counts number of node visits, the score and a dictionary of children nodes
# requires the board state, and the parent node
# check if terminal node


class Nodes:
    def __init__(self, board):
        self.visits = 0  # number of visits the node has
        self.score = 0  # the score of the node

        if checkwin(board) or checkdraw(board):  # need these functions

            self.terminal = True  # can change from if

        else:
            self.terminal = False

        self.children = [
            -math.inf for _ in range(9)
        ]  # list of children nodes----- changed from dict
        # print('node made')
        # maybe reward??
        # or maybe define if parent


#################################scoring

# UCB1 score, UCB = (Winning score of current node) + c(controles how often to search for new possibilities)*sqrt(ln(N)/ni)
# N = number of parent node visites, ni= number of child node visits

# check all child nodes, score each one using formular bellow


def ucb1(current_node, parent_node):
    if current_node.visits == 0:
        return float(math.inf)
    # print('Parent visit =',parent_node.visits)
    # print('current visits =',current_node.visits)
    # print(type(parent_node.visits))
    # print(type(current_node.visits))
    # print('current score=',current_node.score)
    UCB = current_node.score + 100 * (
        math.sqrt(math.log(parent_node.visits) / current_node.visits)
    )
    # current_node.score +
    # print('UCB=',UCB)
    return UCB


# find equal moves and append to list maybe to randomly choose one? or just pick first one


#################################Selecting

# check node in none terminal
# check node is fully expanded or not
# do stuff- find move or expand node
L = []


def selection(current_node, List, player):

    List.append(current_node)  # list is used for backprop

    # check if node has any children or if node is terminal

    if (current_node.children == [-math.inf for _ in range(9)]) or (
        current_node.terminal == True
    ):
        return (
            current_node.terminal,
            current_node,
        )  # returns true/false and the currenct node

    # if above does not occure then need to find the child node with the highest score
    first = False
    bestchild = 0
    # checks all the child nodes to find the one with the highest UCB1 score
    for child in range(0, len(current_node.children)):
        if current_node.children[child] != -math.inf:
            UCB1 = ucb1(
                current_node.children[child], current_node
            )  ######################################################

            if first == False:
                Max_value = UCB1
                bestchild = current_node.children[child]
                bestmove = child
                first = True
            if UCB1 > Max_value:
                Max_value = UCB1
                bestchild = current_node.children[child]
                bestmove = child

    # need to play the moves to change the board state
    play(player, bestmove, baseboard)
    player = currentplayer(player)
    L.append(
        "\n"
        + "###############"
        + "\n"
        + baseboard[0]
        + "|"
        + baseboard[1]
        + "|"
        + baseboard[2]
        + "\n"
        + "-+-+-"
        + "\n"
        + baseboard[3]
        + "|"
        + baseboard[4]
        + "|"
        + baseboard[5]
        + "\n"
        + "-+-+-"
        + "\n"
        + baseboard[6]
        + "|"
        + baseboard[7]
        + "|"
        + baseboard[8]
    )

    return selection(bestchild, List, player)


#################################Expanding

#  expand node and add to parent node dictionary
import copy


def expansion(current_node, player, List):
    copyboard = copy.deepcopy(baseboard)
    if List != []:
        if len(List) % 2 == 0:
            player = "O"
        else:
            player = "X"
    for move in leagalmoves(copyboard):

        play(player, move, copyboard)
        # print(current_node.children)
        current_node.children[move] = Nodes(copyboard)
        # print(current_node.children)
        # player = currentplayer(player)
        copyboard = copy.deepcopy(baseboard)


#################################Rollout


def rollout(current_node, board, player):
    boardcopy = copy.deepcopy(board)  # copy teh board
    while (checkwin(boardcopy) == False) and (checkdraw(boardcopy) == False):
        moves = leagalmoves(boardcopy)
        if moves != []:
            if len(moves) % 2 == 0:
                player = "O"
            else:
                player = "X"
        try:
            move = random.choice(moves)
            play(player, move, boardcopy)
            player = currentplayer(player)

        except:

            current_node.score = 0
            # print('draw')

    if (
        player == "O"
    ):  # x and o other way arround that would think as player changes imediatly after playing
        # if player == 'O' tehn X has won
        # print('added one')
        current_node.score = 1
    if player == "X":
        # print('minus one')
        current_node.score = -1


#################################Backpropagating


def backpropagation(result, List):

    for node in range(len(List)):
        if result == -1:
            List[node].score -= 1
        if result == 1:
            List[node].score += 1

        List[node].visits += 1


# update the nodes up to the root node
# update visits and score
# node is now parent node


# create root node, passing in false for terminal node

player = "X"
baseboard = resetboard()
rootnode = Nodes(baseboard)  # need to pass this to selection as a current node.
List = []
expansion(rootnode, player, List)
for i in range(100000):
    if i % 10000 == 0:
        print(i)
    List = []
    result = selection(rootnode, List, player)
    if result[0] == True:
        # this is the end of the game
        backpropagation(result[1].score, List)

    else:  # this means leaf node

        if result[1].visits == 0:
            rollout(result[1], baseboard, player)
            backpropagation(result[1].score, List)
        else:  # i changed this from somthing else
            expansion(result[1], player, List)
            result = selection(result[1], List, player)
            rollout(result[1], baseboard, player)
            backpropagation(result[1].score, List)
    # print(i)

    baseboard = resetboard()

# with open('boards.txt','a') as f:
#       f.writelines(L)
print(len(L))

se = set(L)

print(len(se))
# with open('setboards.txt','a') as f:
#       f.writelines(se)


def Bestmove(current_node):
    bestchild = 0
    max_value = -1000
    bestmove = -1
    if current_node != -math.inf:

        for child in range(0, len(current_node.children)):
            if current_node.children[child] != -math.inf:
                value = current_node.children[child].score
                # if child == 1:
                #  max_value = value
                # bestchild = current_node.children[child]
                # bestmove = child
                if value > max_value:
                    max_value = value
                    bestchild = current_node.children[child]
                    bestmove = child

        if bestmove == -1:
            moves = leagalmoves(baseboard)
            bestmove = random.choice(moves)
    # added this section to generate random moves
    else:
        moves = leagalmoves(baseboard)
        bestmove = random.choice(moves)

    return bestmove


def human(player):
    position = int(input("Enter position for 'O': "))
    play(player, position, baseboard)


# computer first
player = "X"
baseboard = resetboard()
print(baseboard)
current = rootnode

while (checkwin(baseboard) == False) and (checkdraw(baseboard) == False):
    move = Bestmove(current)
    current = current.children[move]
    print(current.children)
    play(player, move, baseboard)
    printboard(baseboard)
    player = currentplayer(player)

    position = int(input("Enter position for 'O': "))
    play(player, position, baseboard)

    current = current.children[position]
    player = currentplayer(player)
    printboard(baseboard)
