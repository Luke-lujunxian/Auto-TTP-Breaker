from blist import sortedlist

from HelperClasses import Layer
from HelperClasses import Node
from HelperClasses import Edge
from nltk.lm import WittenBellInterpolated
from training import loadModel

LENGTH_OF_BATCH = 43
LENGTH_OF_FILE = 43

def main():
    model = loadModel("(char&int)kilgariff_ngram_model_16000.pkl")
    p0 = 'After two and a half years with her parents'
    p1 = 'The term Internet when used to refer to the'
    #c0 = open("ctext0", 'rb').read(LENGTH_OF_FILE)
    #c1 = open("ctext1", 'rb').read(LENGTH_OF_FILE)

    x = []
    for i in range(LENGTH_OF_FILE):
        x.append(ord(p0[i]) ^ ord(p1[i]))
    #print(x[1])
    for i in range(0,LENGTH_OF_FILE,LENGTH_OF_BATCH):
        decrypt(model,x,i)

def decrypt(model, xorcypher,beginAt):
    baseNode = Node('','')
    layers = []

    # generate first layer
    newLayer = Layer(model)
    layers.append(newLayer)
    baseNode.generateNodes(newLayer, xorcypher[beginAt], model)

    # visited = set()
    # length = baseNode.possibleEdges.__len__()
    # pos = 0
    # while pos < length:
    #     n:Edge = baseNode.possibleEdges[pos]
    #     if n.a in visited:
    #         baseNode.possibleEdges.remove(n)
    #         length -= 1
    #     else:
    #         visited.add(n.a)
    #         visited.add(n.b)
    #     pos += 1
    

    for i in range(beginAt+1, min(beginAt+LENGTH_OF_BATCH,LENGTH_OF_FILE)):
        print("in char "+str(i))
        l = layers[-1]
        layers.append(l.generateNextLayer(xorcypher[i]))
        if l.nodeList.__len__() == 0:
            print("!!No possible solution, Ending process!!!")
            break
        if layers.__len__() > 5:
            layers.remove(layers[0])
        #for node in l.nodeList:

        #   maxProb = None
        #   for edge in node.inEdge:
        #       if maxProb is None:
        #           maxProb = edge
        #       else:
        #           if maxProb.prob < edge.prob:
        #               maxProb.__del__()
        #               maxProb = edge

        #    node.inEdge = [node.inEdge[-1]]

        #node.generateNodes(l.nextLayer, x[i+1], model)

    results = sortedlist(key=lambda e: -e.sumWeight)
    for i in range(1, LENGTH_OF_BATCH if 5 > LENGTH_OF_BATCH else 5):
        for node in layers[-i].nodeList:
            results.add(node)
        if results.__len__()>10:
            break
    #for path in baseNode.possibleEdges:
    #    node = path.nextNode
    #    weightSum = path.prob
    #    while node.possibleEdges.__len__() != 0:
    #        weightSum = weightSum+node.possibleEdges[-1].prob
    #        node = node.possibleEdges[-1].nextNode
    #    results.append((node.p,node.q,weightSum))

    #results.sort(key=lambda res: res[2],reverse=True)
    out = open('results_'+str(beginAt)+'_.txt','w')
    print("Output result")
    for node in results:
        print((node.p,node.q,node.sumWeight))
        out.write('{'+node.p+',\n'+node.q+',\n'+str(node.sumWeight) +'};\n')
    out.close()



main()
