import nltk
from pylab import *

# ./data_1000/unhappy_tweets_100

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

    newfile = open("happy_file", "w")
    count = 0
    for key, value in vocab.iteritems():
        count += value
        newfile.write(str(key) + "\t" + str(value) + "\n")


if __name__ == "__main__":
    main()
