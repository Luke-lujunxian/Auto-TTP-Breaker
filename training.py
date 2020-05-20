import dill as pickle
from nltk import word_tokenize
from nltk.lm import WittenBellInterpolated
from nltk.lm.preprocessing import padded_everygram_pipeline

from HelperClasses import CHARS
from HelperClasses import DIGITS

n = 7
INTERVAL_OF_SAVING: int = 2000


def train():
    model = WittenBellInterpolated(n)
    data = open("wikiData.txt", 'r', encoding="utf-8")
    i = 0
    line = ''

    vocab = []
    for c in CHARS:
        vocab.append(c)

    for c in DIGITS:
        vocab.append(c)
    vocab.append(' ')
    vocab.append('<s>')
    vocab.append('</s>')

    try:
        while True:
            linep = data.readline()
            if linep == '':
                break
            line = line + linep
            i += 1
            if i % 100 == 0:
                print(i)
            if i % INTERVAL_OF_SAVING == 0:
                tokens = word_tokenize(line)
                for j in range(tokens.__len__()):
                    tokens[j] = ' ' + tokens[j] + ' '
                train_data = padded_everygram_pipeline(n, tokens)
                for t in train_data[0]:
                    print(list(t))
                model.fit(train_data[0], vocab)
                print(len(model.vocab))
                line = ''
                try:
                    with open('(char&int)kilgariff_ngram_model_' + str(i) + '.pkl', 'wb') as fout:
                        pickle.dump(model, fout)
                        fout.close()
                except IOError:
                    continue
    finally:
        with open('kilgariff_ngram_model_final_.pkl', 'wb') as fout:
            pickle.dump(model, fout)
            fout.close()


def loadModel(path):
    with open(path, 'rb') as fin:
        return pickle.load(fin)


def main():
    train()
    test()


def test():
    model = loadModel("kilgariff_ngram_model_16000.pkl")
    string = 'The term I'
    print(list(model.vocab))
    print(string)
    print(str(model.score(',', context=string.split())))
    for i in range(65, 91):
        print(chr(i) + ': ' + str(model.score(chr(i), context=tokenlize(string))))
        print(chr(i + 32) + ': ' + str(model.score(chr(i + 32), context=tokenlize(string))))
    for i in range(32, 35):
        print(chr(i) + ': ' + str(model.score(chr(i), context=tokenlize(string))))
    for i in range(39, 42):
        print(chr(i) + ': ' + str(model.score(chr(i), context=tokenlize(string))))
    for i in range(44, 60):
        print(chr(i) + ': ' + str(model.score(chr(i), context=tokenlize(string))))

    print(chr(63) + ': ' + str(model.score(chr(63), context=tokenlize(string))))


def tokenlize(s: str):
    l = list(s)
    return l


if __name__ == '__main__':
    main()
