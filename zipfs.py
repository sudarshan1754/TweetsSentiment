from __future__ import division
from pylab import *

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