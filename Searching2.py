import sys 
from porterStemmer import PorterStemmer
import re # regex to rescue
from functools import reduce
from collections import defaultdict


ps = PorterStemmer()
inverteddict=defaultdict(list)
regex = re.compile("[^a-z0-9 ]+")

def Cleaning():
    # concatenate command line arguement
    words = " ".join(sys.argv[1:])
    # converting all to lowercase to ease in searching
    words = words.lower()
    # removing non-alphanumeric except for space
    words = regex.sub(" ", words).strip()
    words = words.split()
    # remove prepositions and all stopwords
    file = open("preposition.dat").read()
    filterwords = [w for w in words if not w in file]
    filterwords = []
    for w in words:
        if w not in file:
        	filterwords.append(w)
    # stem words so that text texting and texted are all considered text
    filterwords = [ps.stem(word,0,len(word)-1) for word in filterwords]
    filterwords = tuple(filterwords)
    return filterwords

def ReadingInvertedIndex():
    indexfile = open('indexedfile.dat')
    content = indexfile.read()
    for eachline in content.splitlines():
        # term|docID1:pos1,pos2;docID2:pos3,pos4;docID3:pos5,pos6
        # first split term and documentlist by |
        document = eachline.split('|')
        word = document[0]
        doclist = document[1]
        # split documentlist into documents by ;
        doclist = doclist.split(';')
        # split each document into docid and position by :
        doclist = [doc.split(':') for doc in doclist]
        # split list of positions for each docid by ,
        doclist = [ [int(doc[0]),doc[1].split(',')] for doc in doclist]
        inverteddict[word]=doclist
    indexfile.close()

def Intersect(docs):
    return (reduce(set.intersection, [set(item) for item in docs]))

def SearchQuery(cleaned):
    if (len(cleaned) == 1):
    # one word query
        try:
            # computing docids for a word
            docs = [doclist[0] for doclist in inverteddict[cleaned[0]]]
            return docs
        except:
            return {}
    else:
        # multi word query
        #try:
        # get the doclist(docid + position) for every word
        doclist = [inverteddict[word] for word in cleaned]
        # get the docid
        docs = [ [docid[0] for docid in doc] for doc in doclist]
        # get documents in which all words are present
        docs = Intersect(docs)
        for i in xrange(len(doclist)):
            doclist[i] = [x for x in doclist[i] if x[0] in docs]
            print(doclist[i])
        return docs
        #except:
        #return {}

def _main_():
    # necessary checks
    if len(sys.argv) == 1:
        print("No words typed!")
        exit(1)

    cleaned = Cleaning()
    ReadingInvertedIndex()
    docs = SearchQuery(cleaned)
    # print list of docs
    if not docs:
        print("Not Found")
    else:
        print(docs)


if __name__ == "__main__":
    _main_()
