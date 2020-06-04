from blist import sortedlist
from nltk.lm import WittenBellInterpolated
from nltk.lm.util import log_base2

# Threshold of cutting branches
POSSIBLE_BRANCH_THRESHOLD = -10

CHARS = {'A', 'a', 'B', 'b', 'C', 'c', 'D', 'd', 'E', 'e', 'F', 'f', 'G', 'g', 'H', 'h', 'I', 'i', 'J', 'j', 'K', 'k',
         'L', 'l', 'M', 'm', 'N', 'n', 'O', 'o', 'P', 'p', 'Q', 'q', 'R', 'r', 'S', 's', 'T', 't', 'U', 'u', 'V', 'v',
         'W', 'w', 'X', 'x', 'Y', 'y', 'Z', 'z'}
SYMBOLS = {'!', '"', '\'', '(', ')', '-', '.', '/', '0', ':', ';', '?'}
DIGITS = {'1', '2', '3', '4', '5', '6', '7', '8', '9', }


class Layer:
    nextLayer = None
    nodeList: sortedlist
    model: WittenBellInterpolated = None

    def __init__(self, model: WittenBellInterpolated):
        self.model = model
        self.nodeList = sortedlist(key=lambda node: node.sumWeight)

    def generateNextLayer(self, cypherChar: int):
        self.nextLayer = Layer(self.model)
        for node in self.nodeList:
            node.generateNodes(self.nextLayer, cypherChar, self.model)
        return self.nextLayer


class Node:
    p: str
    q: str
    sumWeight: float = 0
    possibleEdges: sortedlist
    inEdge: list

    def __init__(self, q, p):
        self.q = q
        self.p = p
        self.possibleEdges = sortedlist(key=lambda edge: edge.prob)
        self.inEdge = []

    def generateNodes(self, nextLayer: Layer, cypherChar, model: WittenBellInterpolated):

        for i in CHARS:
            if isPrintableChar(ord(i), cypherChar):
                self.addNodeandEdge(i, chr(ord(i) ^ cypherChar), nextLayer, model)
        for i in DIGITS:
            if isPrintableChar(ord(i), cypherChar):
                self.addNodeandEdge(i, chr(ord(i) ^ cypherChar), nextLayer, model)
        if isPrintableChar(ord(' '), cypherChar):
            self.addNodeandEdge(' ', chr(ord(' ') ^ cypherChar), nextLayer, model)

        visited = set()
        length = self.possibleEdges.__len__()
        pos = 0
        while pos < length:
            n: Edge = self.possibleEdges[pos]
            if n.a in visited:
                self.possibleEdges.remove(n)
                length -= 1
            else:
                visited.add(n.a)
                visited.add(n.b)
                pos += 1
        self.possibleEdges = self.possibleEdges[int(
            self.possibleEdges.__len__() * 0.7 if self.possibleEdges.__len__() > 10 else 0):self.possibleEdges.__len__()]
        # for e in self.possibleEdges:
        # print(self.p + e.a + "," + self.q + e.b + ": " + str(e.prob))

    def addNodeandEdge(self, a, b, nextLayer, model):
        score = 0

        if self.p.__len__() > 0 and (self.p[-1] == ' ' or self.q[-1] == ' '):
            ascore = 0
            bscore = 0
            if self.p[-1] == ' ':
                ascore = model.score(a, context=tokenlize(' '))
            else:
                ascore = model.score(a, context=tokenlize(self.p))
            if self.q[-1] == ' ':
                bscore = model.score(b, context=tokenlize(' '))
            else:
                bscore = model.score(b, context=tokenlize(self.q))
            score = log_base2(ascore * bscore)
        else:
            score = log_base2(model.score(a, context=tokenlize(self.p)) * model.score(b, context=tokenlize(self.q)))

        # print(self.p + a + "," + self.q + b + ": " + str(score))
        if score > POSSIBLE_BRANCH_THRESHOLD or (self.p.__len__() < 3 and score > -20):
            print(self.p + a + "," + self.q + b + ": " + str(score))
            newNode = Node(self.p + a, self.q + b)
            newEdge = Edge(a, b, self, newNode, score)

            newNode.inEdge.append(newEdge)
            newNode.sumWeight = newEdge.prevNode.sumWeight + score
            self.possibleEdges.add(newEdge)

            nextLayer.nodeList.add(newNode)


def tokenlize(s: str):
    l = list(s)
    if s == '':
        l = [' ']
    return l


class Edge:
    a: chr
    b: chr
    nextNode: Node = None
    prevNode: Node = None
    prob: float

    def __init__(self, a, b, this, next, prob):
        self.a = a
        self.b = b
        self.nextNode = next
        self.prevNode = this
        self.prob = prob

    def __del__(self):
        if self.nextNode is not None:
            try:
                self.nextNode.inEdge.remove(self)
            except ValueError:
                pass
        if self.prevNode is not None:
            try:
                self.prevNode.possibleEdges.remove(self)
            except ValueError:
                pass


def isPrintableChar(a: int, cypherChar: int):
    res = a ^ cypherChar
    if chr(res) in CHARS or chr(res) in DIGITS or res == ord(' '):
        return True
    else:
        return False
