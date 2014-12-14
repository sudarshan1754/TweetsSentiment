###********************************************************************************###
  # __author__ = 'sid'                                                             #
  # This program is written as part of the Natural Language Processing Project     #
  # @copyright: Sudarshan Sudarshan (Sid)                                          #
###********************************************************************************###


import nltk


def tokenize_dictionary(filepath):
    dictionary = []
    filecontents = open(filepath, "r")
    for line in filecontents.readlines():
        if line[0] != ";":
            dictionary.append(line.rstrip("\n"))
    filecontents.close()

    return dictionary


def classify(filepath, pos_dict_words, neg_dict_words, isPos):
    filecontents = open(filepath, "r")
    correct = 0
    total_tweets = 0
    for line in filecontents.readlines():
        total_tweets += 1
        positive_words_in_tweet = 0
        negative_words_in_tweet = 0
        tokens = nltk.WhitespaceTokenizer().tokenize(line)
        for token in tokens:
            if token.lower() in pos_dict_words:
                positive_words_in_tweet += 1
            elif token in neg_dict_words:
                negative_words_in_tweet += 1
        if isPos:
            if positive_words_in_tweet > negative_words_in_tweet:
                correct += 1
        elif not isPos:
            if positive_words_in_tweet < negative_words_in_tweet:
                correct += 1
    return correct / float(total_tweets) * 100


def main():
    print "\n-------------------------WELCOME-------------------------\n"

    pos_dict_path = raw_input("Enter the positive keywords file path:")
    neg_dict_path = raw_input("Enter the negative keywords file path:")
    # pos = "./dictionary/positive-words.txt"
    # neg = "./dictionary/negative-words.txt"
    pos_dict_words = tokenize_dictionary(pos_dict_path)
    neg_dict_words = tokenize_dictionary(neg_dict_path)

    pos_test_path = raw_input("Enter the positive test file path:")
    # "./final/ds2/test/pos"
    neg_test_path = raw_input("Enter the negative test file path:")
    # "./final/ds2/test/neg"
    print "\n-------------------------RESULTS-------------------------\n"

    pos_accuracy = classify(pos_test_path, pos_dict_words, neg_dict_words, True)
    neg_accuracy = classify(neg_test_path, pos_dict_words, neg_dict_words, False)

    print "Correct Positives:" + str(pos_accuracy)
    print "Correct Negatives:" + str(neg_accuracy)

    print "\n----------------------------BYE--------------------------\n"


if __name__ == "__main__":
    main()