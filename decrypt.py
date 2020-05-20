from blist import sortedlist

from HelperClasses import Layer
from HelperClasses import Node
from training import loadModel

LENGTH_OF_BATCH = 43  # If you want to decrypt in batch, set it different
LENGTH_OF_FILE = 43


def main():
    #   Load language model
    model = loadModel("(char&int)kilgariff_ngram_model_16000.pkl")
    x = []

    #   For test
    p0 = 'After two and a half years with her parents'
    p1 = 'The term Internet when used to refer to the'
    LENGTH_OF_BATCH = LENGTH_OF_FILE = p0.__len__()
    for i in range(LENGTH_OF_FILE):
        x.append(ord(p0[i]) ^ ord(p1[i]))

    # For real use
    # c0 = open("ctext0", 'rb').read(LENGTH_OF_FILE)
    # c1 = open("ctext1", 'rb').read(LENGTH_OF_FILE)
    #   for i in range(LENGTH_OF_FILE):
    #       x.append(c0[i] ^ c1[i])

    for i in range(0, LENGTH_OF_FILE, LENGTH_OF_BATCH):
        decrypt(model, x, i)


def decrypt(model, xorcypher, beginAt):
    baseNode = Node('', '')
    layers = []

    # generate first layer
    newLayer = Layer(model)
    layers.append(newLayer)
    baseNode.generateNodes(newLayer, xorcypher[beginAt], model)

    for i in range(beginAt + 1, min(beginAt + LENGTH_OF_BATCH, LENGTH_OF_FILE)):
        print("in char " + str(i))
        l = layers[-1]
        layers.append(l.generateNextLayer(xorcypher[i]))
        if l.nodeList.__len__() == 0:
            print("!!No possible solution, Ending process!!!")
            break
        if layers.__len__() > 5:
            layers.remove(layers[0])

    results = sortedlist(key=lambda e: -e.sumWeight)  # Sort from most likely to less
    for i in range(1, LENGTH_OF_BATCH if 5 > LENGTH_OF_BATCH else 5):
        for node in layers[-i].nodeList:
            results.add(node)
        if results.__len__() > 10:
            break

    # Output
    out = open('results_' + str(beginAt) + '_.txt', 'w')
    print("Output result")
    for node in results:
        print((node.p, node.q, node.sumWeight))
        out.write('{' + node.p + ',\n' + node.q + ',\n' + str(node.sumWeight) + '};\n')
    out.close()


main()
