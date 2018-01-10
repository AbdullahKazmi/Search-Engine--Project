# References: geeksforgeeks(stopwords), stackoverflow, tarturus.com(porter stemmer)

import re
from porterStemmer import PorterStemmer
from collections import defaultdict
from array import array
porter = PorterStemmer()
regex = re.compile("[^a-z0-9 ]+")
regex1 =re.compile("<text xml:space=\"preserve\">")
regex2 =re.compile("</text>")


class PAI: # parsing and indexing
    def __init__(self):
        self.index = defaultdict(list)  # a hashtable with lists/vectors

    def removeStopWords(self, words):
        words = words.lower()
        words = regex.sub("", words)
        file = open("preposition.dat").read()  # preposition.dat was taken from internet
        words = words.split()
        filterwords = [w for w in words if not w in file] 
        filterwords = []
        for w in words:
            if w not in file:
                filterwords.append(w)
        filterwords = [porter.stem(word, 0, len(word) - 1) for word in filterwords]
        return filterwords

    def Parse_Index_File(self):
        pid = 0
        title, text = "", ""
        pageid = 0
        pagetitle = ""
        cnt = 0
        d = defaultdict(list)  # d is a dictionary/hashtable
        text = ""
        pflag =False

        for line in self.collectionfile:  # for loop. Here "line" is literally a line ending with \n(enter) in our xml file.
            #if int(pid) >4000:
                #break

            if re.search("<title>", line) is not None:
                pagetitle = re.search("<title>(.*?)</title>", line, re.DOTALL)
                title = pagetitle.group(1)  # if title tags found store title text context

            elif re.search("<id>", line) is not None and cnt == 0:
                pageid = re.search("<id>(.*?)</id>", line, re.DOTALL)
                pid = pageid.group(1) # if id tags found store id text context
                print (pid)
                cnt += 1  # only store first id of page

            elif re.search("<text xml:space=\"preserve\">", line) is not None:
                line = regex1.sub("", line)
                text += line
                pflag=True

            elif pflag == True and re.search("</text>", line) is None:
                text += line
            elif re.search("</text>", line) is not None:
                pflag = False
                line = regex2.sub(" ", line)
                text += line
                cnt = 0
                lines = '\n'.join((title, text))  # lines = title \n text
                terms = self.removeStopWords(lines)  #remove stopwords from lines and put into terms
                for position, term in enumerate(terms):  #enumerate is like a counter
                    try:
                        d[term][1].append(position)  #in d, key = term (a word) and value = docids and list of positions of word in that docid
                    except:
                        d[term] = [int(pid), array('I', [position])]  # in dictionary d, key = term, value = pageid and array of positions in that page

        print("out of Parsing")

        return d  # return dictionary

    def writeIndexIntoFile(self):
        try:
            f = open("test.dat", 'w')
            for term in self.index.keys():
                # print(self.index)
                postinglist = []  # a list
                for p in self.index[term]:
                    docID = p[0]
                    positions = p[1]
                    postinglist.append(':'.join([str(docID), ','.join(map(str, positions))]))
                    #print(postinglist)
                f.write(''.join((term, '|', ';'.join(postinglist))))
                f.write("\n")
        except IOError:
            print("Cannot open file. Try again later.")

        f.close()

    def main(self):

        try:
            self.collectionfile = open("final.dat", 'r', encoding = "utf8")  # open xml file and put it in collection file
        except IOError:
            print("Cannot open file. Try again later.")
        pagedict = self.Parse_Index_File()  # return dictionary/hashtable with id, title and text
        for termpage, postingpage in pagedict.items():  # The method items() returns a list of dict's (key, value) tuple pairs
            self.index[termpage].append(postingpage)  # term page = pageid and uss page me word or uss ki position

        self.writeIndexIntoFile()


if __name__ == "__main__":
    c = PAI()  # just initialize the dictionary(lists) i.e. hashtable + lists data structure as index
    c.main()  # start main
