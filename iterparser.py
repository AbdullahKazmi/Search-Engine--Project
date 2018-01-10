import re
from porterStemmer import PorterStemmer
from collections import defaultdict
import xml.etree.ElementTree as et

from array import array

porter = PorterStemmer()

class ParseAndIndex:
    def __init__(self):
        self.index = defaultdict(list) # a hashtable with lists/vectors

    def removeStopWords(self, words):
        # print("in removeStopWords")
        # print("in removeStopWords function")
        words = words.lower()
        words = re.sub("[^a-z0-9 ]", "", words)
        file = open("preposition.dat").read()
        words = words.split()
        filterwords = [w for w in words if not w in file]
        filterwords = []
        for w in words:
            if w not in file:
                filterwords.append(w)
        filterwords = [porter.stem(word, 0, len(word)-1) for word in filterwords]
        # print("out of removeStopWords")
        # print(filterwords)
        return filterwords

    def Parsing(self, fileName):
        d = {}  # d is a dictionary/hashtable
        # print("in Parsing")
        id, title, text = 0, "", ""
        context = et.iterparse(fileName, events=("start", "end"))

        # turn it into an iterator
        context = iter(context)
        cnt = 0
        for event, elem in context:
            tag = elem.tag
            value = elem.text
            if value:
                value = value.encode('utf-8').strip()
            if event == 'start':
                if tag == "title":
                    title = value
                elif tag == "id" and cnt == 0:
                    print(value)
                    id = value
                    cnt += 1
            if event == 'end' and tag == 'text':
                cnt = 0
                text = value
                elem.clear()
                lines = '\n'.join((title, text))  # lines = title \n text
                terms = self.removeStopWords(lines) #remove stopwords from lines and put into terms
                for position, term in enumerate(terms): #enumerate is like a counter
                    try:
                        d[term][1].append(position) #in d, we have the word and a list of
                        #print(d)
                    except:
                        d[term] = [int(id), array('I', [position])] #in dictionary d, key = term, value = pageid and array of positions in that page
        # print("out of Parsing")
        return d  # return dictionary

    def writeIndex(self):
        print("in writeIndex")
        try:
            f = open("indexedfile.dat", 'w')
            for term in self.index.keys():
                #print(self.index)
                postinglist = []  # a list
                for p in self.index[term]:
                    docID = p[0]
                    positions = p[1]
                    postinglist.append(':'.join([str(docID), ','.join(map(str, positions))]))
                    #print(postinglist)
                f.write(''.join((term, '|', ';'.join(postinglist))))
                f.write("\n")
        except IOError:
            print("Couldn't open file")
        print("out writeIndex")
        f.close()

    def main(self):
        file = "final.xml"
        try:
            self.collectionfile = open(file, 'r') # open xml file and put it in collection file
        except IOError:
            print("Couldn't open file")

        pagedict = {}  #empty variable
        pagedict = self.Parsing(file)  # return dictionary/hashtable with id, title and text
        #print(pagedict)
        for termpage, postingpage in pagedict.items():# The method items() returns a list of dict's (key, value) tuple pairs
                self.index[termpage].append(postingpage) # term page = pageid and uss page me word or uss ki position
        self.writeIndex()

if __name__ == "__main__":
    c = ParseAndIndex() # just initialize the dictionary(lists) i.e. hashtable + lists data structure as index
    c.main() # start main

