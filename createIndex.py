#!/usr/bin/python
import re
from porterStemmer import PorterStemmer
from collections import defaultdict
from array import array
from __init__ import *
import xml.sax

porter = PorterStemmer()
index = defaultdict(list)

class MovieHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.dict = {}  # d is a dictionary/hashtable
        self.id = False
        self.title = False
        self.text = False
        self.cnt1 = 0
        self.cnt2 = 0
        self.pageid = 0
        self.pagetitle =""
        self.pagetext = ""
        # Call when an element starts

    def startElement(self, tag, attributes):
        #print("in startElement function")
        self.CurrentData = tag
        if tag == "id" and self.cnt1 == 0:
            self.id = True
            self.cnt1 += 1
        elif tag == "title":
            self.title = True
        elif tag == "text":
            self.text = True

        # Call when an elements ends

    def endElement(self, tag):
        #print("in endElement function")
        if self.CurrentData == "id" and self.cnt2 == 0:
            self.cnt2 += 1
            self.id = False
        elif self.CurrentData == "title":
            self.title = False
        elif self.CurrentData == "text":
            self.text = False
            self.id = False
            self.cnt1 = 0
            self.cnt2 = 0
            lines = '\n'.join((self.pagetitle, self.pagetext))  # lines = title \n text
            terms = self.removeStopWords(lines)  # remove stopwords from lines and put into terms
            #print("stopwords removed")
            dict = {}  # another dictionary
            for position, term in enumerate(terms):  # enumerate is like a counter
                try:
                    dict[term][1].append(position)  # in termdictPage, we have the word and a list of
                except:
                    dict[term] = [int(self.pageid),array('I', [position])]  # in dictionary termdictPage, key = term,
                    # value = pageid and array of positions in that page
            #print("positions and terms done")
        elif self.CurrentData == "root":
            return dict

        # Call when a character is read

    def characters(self, content):
        if self.CurrentData == "id" and self.id:
            self.id = content
            print("id {}".format(content))
        elif self.CurrentData == "title":
            self.title = content
        elif self.CurrentData == "text":
            self.pagetext += content

    def removeStopWords(self, words):
        #print("in removeStopWords function")
        words = words.lower()
        words = re.sub("[^a-z0-9 ]", "", words)
        file = open("preposition.dat").read()
        words = words.split()
        filterwords = [w for w in words if not w in file]
        filterwords = []
        for w in words:
            if w not in file:
                filterwords.append(w)
        filterwords = [porter.stem(word,0,len(word)-1) for word in filterwords]
        #print("exiting removeStopWords function")
        return filterwords

class Index:
    def __init__(self):
        self.index = defaultdict(list)
        print("start")

    def main(self):
        # create an XMLReader
        parser = xml.sax.make_parser()
        # turn off namepsaces
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)

        # override the default ContextHandler
        Handler = MovieHandler()
        parser.setContentHandler(Handler)
        dict = parser.parse("twoPages.xml")

        #print("positions and terms done")
        for termpage, postingpage in dict.items():  # The method items() returns a list of
            # dict's (key,value) tuple pairs
            # term = page id , postingpage = object(docid, positions)
            self.index = [termpage].append(postingpage)  # term page = pageid and uss page me word or uss ki position
            print(self.index)
            self.writeIndex(self.index)
        #print("out of sorting function")
        # self.getstopwords()  # open stopwords file. Create a hashtable of words in stopwords file in variable self.sw.
        # here sw is a dictionary/hastable
        self.writeIndex()

    def writeIndex(self):
        try:
            #print("in writeIndex function")
            f = open("indexedfile.dat", 'w')
            for term in self.index.keys():
                postinglist = []  # a list
                print(self.index)
                for p in self.index[term]:
                    print(self.index)
                    docID = p[0]
                    print(p[0])
                    positions = p[1]
                    print(p[1])
                    postinglist.append(':'.join([str(docID), ','.join(map(str, positions))]))
                    f.write(''.join((term, '|', ';'.join(postinglist))))
        except IOError:
            print("Couldn't open file")

        f.close()

if __name__ == "__main__":
    c = Index()  # just initialize the dictionary(lists) i.e. hashtable + lists data structure as index
    c.main()
