import math
import random
import copy
from ordered_set import OrderedSet


class Board:
    def __init__(self):
        self.player = 1
        self.board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]

    def resetboard(self):
        self.board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
        self.player = 1

    def legalmoves(self):
        availablemoves = []
        for move in range(0, 9):
            if self.board[move] == " ":
                availablemoves.append(move)
        return availablemoves

    def win(self):
        if (
            self.board[0] == self.board[1]
            and self.board[0] == self.board[2]
            and self.board[0] != " "
        ):
            if self.board[0] == "O":
                return -1
            else:
                return 1
        elif (
            self.board[3] == self.board[4]
            and self.board[3] == self.board[5]
            and self.board[3] != " "
        ):
            if self.board[3] == "O":
                return -1
            else:
                return 1
        elif (
            self.board[6] == self.board[7]
            and self.board[6] == self.board[8]
            and self.board[6] != " "
        ):
            if self.board[6] == "O":
                return -1
            else:
                return 1
        elif (
            self.board[0] == self.board[3]
            and self.board[0] == self.board[6]
            and self.board[0] != " "
        ):
            if self.board[0] == "O":
                return -1
            else:
                return 1
        elif (
            self.board[1] == self.board[4]
            and self.board[1] == self.board[7]
            and self.board[1] != " "
        ):
            if self.board[1] == "O":
                return -1
            else:
                return 1
        elif (
            self.board[2] == self.board[5]
            and self.board[2] == self.board[8]
            and self.board[2] != " "
        ):
            if self.board[2] == "O":
                return -1
            else:
                return 1
        elif (
            self.board[0] == self.board[4]
            and self.board[0] == self.board[8]
            and self.board[0] != " "
        ):
            if self.board[0] == "O":
                return -1
            else:
                return 1
        elif (
            self.board[6] == self.board[4]
            and self.board[6] == self.board[2]
            and self.board[6] != " "
        ):
            if self.board[6] == "O":
                return -1
            else:
                return 1
        else:
            return False

    def move(self, position):

        if position in self.legalmoves():
            if self.player == 1:
                self.board[position] = "X"
            else:
                self.board[position] = "O"

        else:
            print("Invalid move, space allready used")
            position = int(input("Enter position: "))
            self.move(position)
            return

        if self.player == 1:
            self.player = 2

        else:
            self.player = 1

    def undo(self, position):

        self.board[position] = " "
        if self.player == 1:
            self.player = 2

        else:
            self.player = 1

    def printboard(self):
        print(self.board[0] + "|" + self.board[1] + "|" + self.board[2])
        print("-+-+-")
        print(self.board[3] + "|" + self.board[4] + "|" + self.board[5])
        print("-+-+-")
        print(self.board[6] + "|" + self.board[7] + "|" + self.board[8])

    def gamestate(self):
        return self.board


b = Board()


class Nodes:
    def __init__(self, result):
        self.visits = 0  # number of visits the node has
        self.score = 0  # the score of the node

        if (b.win() != False) or ((len(b.legalmoves())) == 0):  # added the draw section

            self.terminal = True  # can change from if

        else:
            self.terminal = False

        self.children = [-math.inf for _ in range(9)]

        self.reward = result


def ucb1(current_node, parent_node):
    # print("Parent visit =", parent_node.visits)
    # print("current visits =", current_node.visits)
    # print(type(parent_node.visits))
    # print(type(current_node.visits))
    # print("current score=", current_node.score)
    if current_node.visits == 0:
        return math.inf

    UCB = (current_node.score / current_node.visits) + 200 * (
        math.sqrt((math.log(parent_node.visits)) / current_node.visits)
    )
    # print("UCB=", UCB)
    return UCB


L = []


def selection(current_node, List):

    List.append(current_node)
    first = False

    if (current_node.children == [-math.inf for _ in range(9)]) or (
        current_node.terminal == True
    ):
        return (
            current_node.terminal,
            current_node,
        )

    bestchild = 0

    for child in range(0, len(current_node.children)):
        if current_node.children[child] != -math.inf:
            UCB1 = ucb1(current_node.children[child], current_node)

            if first == False:

                Max_value = UCB1
                bestchild = current_node.children[child]
                bestmove = child
                first = True
            if UCB1 > Max_value:
                Max_value = UCB1
                bestchild = current_node.children[child]
                bestmove = child

    b.move(bestmove)

    return selection(bestchild, List)


def expansion(current_node):

    for move in b.legalmoves():

        b.move(move)

        current_node.children[move] = Nodes(0)
        board = b.gamestate()  # not needed, for testing
        L.append(
            "\n"
            + "###############"
            + "\n"
            + board[0]
            + "|"
            + board[1]
            + "|"
            + board[2]
            + "\n"
            + "-+-+-"
            + "\n"
            + board[3]
            + "|"
            + board[4]
            + "|"
            + board[5]
            + "\n"
            + "-+-+-"
            + "\n"
            + board[6]
            + "|"
            + board[7]
            + "|"
            + board[8]
        )
        b.undo(move)





def rollout(current_node):
    
    while (b.win() == False) and (len(b.legalmoves()) != 0):  
        
        moves = b.legalmoves()
        try:
            move = random.choice(moves)
            b.move(move)
        except:

            current_node.score += 0  
            
    result = b.win()
    
    if result == False:
        result = 0
    current_node.reward = result  


def backpropagation(result, List):
    
    for node in range(len(List)):
        # if result == -1:
        #   List[node].score += -1
        if result == 1:
            List[node].score += 1
        # elif result == 0:
        #   List[node].score += 0  

        List[node].visits += 1


b.resetboard()
rootnode = Nodes(0)  
List = []

L_0 = 0
L_1 = 0
L_minus = 0

expansion(rootnode)
for i in range(500000):
    if i % 10000 == 0:

        print(i)
    List = []
    result = selection(rootnode, List)
    
    if result[0] == True:
        
        # rollout(result[1])

        backpropagation(result[1].reward, List)

    else:  

        if result[1].visits == 0:

            rollout(result[1])
            backpropagation(result[1].reward, List)

        else:  

            expansion(result[1])
            List = []
            result = selection(result[1], List)
            rollout(result[1])
            backpropagation(result[1].reward, List)

    if result[1].reward == 0:
        L_0 += 1
    if result[1].reward == 1:
        L_1 += 1
    if result[1].reward == -1:
        L_minus += 1

    b.resetboard()

print("draw:", L_0)
print("win:", L_1)
print("loss:", L_minus)

print("-----------")

with open("boards.txt", "a") as f:
    f.writelines(L)
print(len(L))
se = OrderedSet(L)
print(len(se))
with open("setboards.txt", "a") as f:
    f.writelines(se)


def Bestmove(current_node):
    bestchild = 0
    max_value = -1000
    bestmove = -1
    if current_node != -math.inf:

        for child in range(0, len(current_node.children)):
            if current_node.children[child] != -math.inf:
                value = current_node.children[child].score

                if value > max_value:
                    max_value = value
                    bestchild = current_node.children[child]
                    bestmove = child

        if bestmove == -1:
            moves = b.legalmoves()
            bestmove = random.choice(moves)

    return bestmove


# computer first

b.resetboard()
current = rootnode
while b.win() == False:
    move = Bestmove(current)
    b.move(move)
    current = current.children[move]

    b.printboard()

    position = int(input("Enter position for 'O': "))
    b.move(position)

    current = current.children[position]
    b.printboard()

# player first
b.resetboard()
current = rootnode
while b.win() == False:
    position = int(input("Enter position for 'O': "))
    b.move(position)
    current = current.children[position]
    b.printboard()

    move = Bestmove(current)
    current = current.children[move]
    b.move(move)

    b.printboard()
