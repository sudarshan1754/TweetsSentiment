import nltk
from pylab import *
from zipfs import *

# ./data_1000/unhappy_tweets_100

def splitdata():
    filename = raw_input("Enter the file name: ")
    filecontents = open(filename, "r")
    newtrain = open("unhappy_train", "w")
    newtest = open("unhappy_test", "w")
    for lno, line in enumerate(filecontents.readlines()):
        if lno < 800:
            newtrain.write(str(line))
        else:
            newtest.write(str(line))

def main():
    filename = raw_input("Enter the file name: ")
    filecontents = open(filename, "r")
    vocab = {}
    # wordscount = 0
    for line in filecontents.readlines():
        tokens = nltk.WhitespaceTokenizer().tokenize(line)
        for token in tokens:
            if token not in vocab:
                vocab[token.lower()] = 1
            else:
                vocab[token.lower()] += 1

    # newfile = open("unhappy_file", "w")
    # count = 0
    # for key, value in vocab.iteritems():
    #     count += value
    #     newfile.write(str(key) + "\t" + str(value) + "\n")



if __name__ == "__main__":
    splitdata()
    # main()
