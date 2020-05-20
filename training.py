from nltk.lm import WittenBellInterpolated
from nltk.lm.preprocessing import padded_everygram_pipeline
from nltk.util import everygrams
from nltk import word_tokenize, sent_tokenize, ngrams
import dill as pickle
from nltk.util import pad_sequence
n = 7
INTERVAL_OF_SAVING: int = 2000
from HelperClasses import CHARS
from HelperClasses import DIGITS
def train():
    model = WittenBellInterpolated(n)
    data = open("wikiData.txt",'r',encoding="utf-8")
    i = 0
    line = ''

    vocab = []
    for c in CHARS:
        vocab.append(c)

    for c in DIGITS:
        vocab.append(c)
    #for i in range(39, 42):
    #    vocab.append(chr(i))
    #for i in range(44, 60):
    #    vocab.append(chr(i))
    vocab.append(' ')
    vocab.append('<s>')
    vocab.append('</s>')

    try:
        while True:
            linep = data.readline()
            if linep == '':
                break
            line = line + linep
            #temp = word_tokenize(sent)
            #temp2 = map(str.lower, word_tokenize(sent))
            i+=1
            if i%100 == 0:
                print(i)
            if i % INTERVAL_OF_SAVING == 0:
                tokens = sent_tokenize(line)
                #s.update(word_tokenize(line))
                for j in range(tokens.__len__()):
               #    if tokens[j] == '~':
               #        tokens[j] = ''
               #        continue
               #    if ord(tokens[j][0]) == 40:
               #        k = 1
               #        tokens[j] = ' '+tokens[j]
               #        while j+k < tokens.__len__() and tokens[j+k][0] != ')':
               #            if tokens[j+k] == '~':
               #                k += 1
               #                continue
               #            tokens[j] = tokens[j] + tokens[j+k]
               #            tokens[j+k] = '~'
               #            k += 1
               #        tokens[j+k] = tokens[j+k] + ') '
               #        tokens[j+k] = '~'


               #    if j+1 != tokens.__len__():
               #        if ord(tokens[j+1][0]) in range(65, 90) or ord(tokens[j+1][0]) in range(97, 122)or ord(tokens[j+1][0]) in range(48, 58):
               #            tokens[j] = ' '+tokens[j]+' '
               #        elif ord(tokens[j+1][0]) in range(32, 34) or ord(tokens[j+1][0]) in range(39, 40) or ord(tokens[j+1][0]) in range(44,59) or ord(tokens[j+1][0]) == 63:
               #            tokens[j] = ' '+tokens[j]+tokens[j+1]+' '
               #            tokens[j+1] = '~'
               #    else:
                    tokens[j] = ' '+tokens[j]+' '
                train_data = padded_everygram_pipeline(n,tokens )
                model.fit(train_data[0],vocab)
                print(len(model.vocab))
                line = ''
                try:
                    with open('(char&int)kilgariff_ngram_model_'+str(i)+'.pkl', 'wb') as fout:
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
        return  pickle.load(fin)

def main():
    train()
    test()

def test():
    model = loadModel("kilgariff_ngram_model_16000.pkl")
    #print(model.counts[['a','d','m','i']]['n'])
    string = 'The term I'
    print(list(model.vocab))
    print(string)
    print( str(model.score(',',context=string.split())) )
    #for i in range(65, 91):
    #    print( chr( i )+': '+str(model.score(chr( i ),context=tokenlize(string))) )
    #    print( chr( i+32 )+': '+str(model.score(chr( i+32 ),context=tokenlize(string))) )
#
    #for i in range(32, 35):
    #    print( chr( i )+': '+str(model.score(chr( i ),context=tokenlize(string))) )
    #for i in range(39, 42):
    #    print( chr( i )+': '+str(model.score(chr( i ),context=tokenlize(string))) )
    #for i in range(44, 60):
    #    print( chr( i )+': '+str(model.score(chr( i ),context=tokenlize(string))) )

    #print( chr( 63 )+': '+str(model.score(chr( 63 ),context=tokenlize(string))) )

       #print( chr( 97+i )+': '+str(model.counts['admi'.split()][chr( 97+i )]) )


def tokenlize(s: str):
    l = list(s)
    #for i in range(7-s.__len__()):
    #    l.append('<s>')
    #if(s.__len__() == 0):
    #    l.append(" ")
    #else:
    #    l.extend(list(s))
    #for i in range(l.__len__()):
    #    if l[i] == ' ':
    #        if i != 0 and l[i-1] != '<s>':
    #            l[i] = '</s>'
    #        else:
    #            l[i] = '<s>'
    return l

if __name__ == '__main__':
    main()
