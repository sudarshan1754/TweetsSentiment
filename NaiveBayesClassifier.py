import os
import math

__author__ = 'sid'

import nltk

vocabulary = []

def unigramTokenizer(filename):

    filecontents = open(filename, "r")
    unigrams = {}
    for line in filecontents.readlines():
        tokens = nltk.WhitespaceTokenizer().tokenize(line)
        for token in tokens:
            token = token.lower()
            if token not in unigrams:
                unigrams[token] = 1
            else:
                unigrams[token] += 1

    filecontents.close()
    return unigrams


def NaiveBayes(vocabulary, unigrams_per_class, class_tokens):

    conditional_probability = []
    for i, unig_class in enumerate(unigrams_per_class):
        conitional_prob_of_class = {}
        for each_token in vocabulary:
            if each_token in unig_class:
                conitional_prob_of_class[each_token] = (unig_class[each_token] + 1) / float(
                        class_tokens[i] + len(vocabulary))
            else:
                conitional_prob_of_class[each_token] = 1 / float(class_tokens[i] + len(vocabulary))
        conditional_probability.append(conitional_prob_of_class)

    conditional_probability_outcomes = {}
    model = open("model_cp", "w")
    for key in vocabulary:
        conditional_probability_outcomes[key] = [conditional_probability[0][key], conditional_probability[1][key]]
        model.write(str(key) + "\t" + str(conditional_probability[0][key]) + "\t" + str(conditional_probability[1][key]) + "\n")

    return conditional_probability_outcomes

def testing(filepath, clas, cp, classtokens):

    N = 1600
    Nc = 800

    correct_positive = 0
    correct_negative = 0
    score_pos = math.log(Nc/float(N), 10)
    score_neg = math.log(Nc/float(N), 10)
    test_contents = open(filepath, "r")
    for line in test_contents.readlines():
        tokens = nltk.WhitespaceTokenizer().tokenize(line)
        for each_token in tokens:
            each_token = each_token.lower()
            if each_token not in cp:
                new_cp = math.log((1 / float(classtokens[0] + len(vocabulary))), 10)
                score_pos += new_cp
                new_cp = math.log((1 / float(classtokens[1] + len(vocabulary))), 10)
                score_neg += new_cp
            else:
                score_pos += math.log(cp[each_token][0], 10)
                score_neg += math.log(cp[each_token][1], 10)

        # print score_pos, score_neg
        if clas == "positive":
            if score_pos > score_neg:
                correct_positive += 1
            # else:
            #     incorrect += 1
        else:
            if score_pos < score_neg:
                correct_negative += 1
            # else:
            #     incorrect += 1

    print correct_positive, correct_negative


def main():
    # ./data_1000/train/
    train_directory = raw_input("Enter the train file directory: ")
    unigrams_per_class = []
    for each_file in os.listdir(train_directory):
        print each_file
        unigram_tokens = unigramTokenizer(str(train_directory + each_file))
        unigrams_per_class.append(unigram_tokens)

    # get the vocabulary
    class_tokens = []
    for unig in unigrams_per_class:
        totaltokensInClass = 0
        for key, value in unig.iteritems():
            totaltokensInClass += value
            if key not in vocabulary:
                vocabulary.append(key)
        class_tokens.append(totaltokensInClass)

    # get the cond prob
    nb = NaiveBayes(vocabulary, unigrams_per_class, class_tokens)

    # get the test data
    classes = ["negative", "positive"]
    test_directory = raw_input("Enter the test file directory: ")
    for clas, each_file in enumerate(os.listdir(test_directory)):
        filepath = str(test_directory + each_file)
        print each_file
        # print classes[clas]
        testing(filepath, classes[clas], nb, class_tokens)

if __name__ == "__main__":
    main()
