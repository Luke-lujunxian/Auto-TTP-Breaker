import time
import random
from urllib.request import ProxyHandler
from nltk.lm import MLE

from pattern.web import Wikipedia

def getFeaturedList():
    wiki = Wikipedia()
    article = wiki.search("Wikipedia:Featured articles")
    file = open("articalsTitle.txt",'w')
    for section in article.sections:
        if section.string != "":
            for title in article.string.split('\n'):
                file.write(((str)(title)).strip()+"\n")
    file.close()

def getFeaturedContent():
    wiki = Wikipedia()
    list = open("articalsTitle.txt",'r')
    file = open("wikiData.txt",'w')
    for i in range(2000):
        title = list.readline().replace("\n","")
        article = wiki.search(title)
        if article is not None:
            for section in article.sections:
                if section.string != "":
                    file.write(section.string+"\n")
            time.sleep(0.2)
            print(title+" Get! "+str(i)+"/2000")



def main():
    getFeaturedContent()



main()