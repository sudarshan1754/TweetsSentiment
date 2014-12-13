from __future__ import division
import nltk
from pylab import *

# ./data_1000/unhappy_tweets_100

def zipflawplot(counts, tokens):

    # A Zipf plot
    ranks = arange(1, len(counts)+1)
    indices = argsort(-counts)
    frequencies = counts[indices]
    loglog(ranks, frequencies, marker=".")
    title("Zipf plot for happy tweets tokens")
    xlabel("Frequency rank of token")
    ylabel("Absolute frequency of token")
    grid(True)
    for n in list(logspace(-0.5, log10(len(counts)), 20).astype(int)):
        dummy = text(ranks[n], frequencies[n], " " + tokens[indices[n]],
                     verticalalignment="bottom",
                     horizontalalignment="left")

    show()

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
    del vocab["<s>"]
    del vocab["</s>"]
    tokencount = array(vocab.values())
    words = vocab.keys()
    # zipflawplot(tokencount, words)

if __name__ == "__main__":
    main()
