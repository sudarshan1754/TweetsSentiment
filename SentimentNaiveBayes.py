###********************************************************************************###
  # __author__ = 'sid'                                                             #
  # This program is written as part of the Natural Language Processing Project     #
  # @copyright: Sudarshan Sudarshan (Sid)                                          #
###********************************************************************************###

import math
import nltk
No_of_positive_tweets = 0
No_of_negative_tweets = 0
unigram_vocabulary = []
bigram_vocabulary = []
unigram_vocab_size = 0
bigram_vocab_size = 0


class NaiveBayes:
    def tokenization(self, filepath):

        # Store the < word: frequency> in dictionary
        word_frequency_unigrams = {}
        word_frequency_bigrams = {}

        tweetsCounter = 0
        unigramtotaltokens = 0
        bigramtotaltokens = 0
        filecontents = open(filepath, "r")
        for line in filecontents.readlines():
            tweetsCounter += 1
            tokens = nltk.WhitespaceTokenizer().tokenize(line)
            unigramtotaltokens += len(tokens)

            for index, token in enumerate(tokens):  # Create the dictionary
                # for unigrams
                if token in word_frequency_unigrams:
                    word_frequency_unigrams[token.lower()] += 1
                else:
                    word_frequency_unigrams[token.lower()] = 1
                    unigram_vocabulary.append(token.lower())

                # for bigrams
                if index < len(tokens) - 1:
                    if (tokens[index].lower() + " " + tokens[index + 1].lower()) in word_frequency_bigrams:
                        word_frequency_bigrams[(tokens[index].lower() + " " + tokens[index + 1].lower())] += 1
                        bigramtotaltokens += 1
                    else:
                        word_frequency_bigrams[(tokens[index].lower() + " " + tokens[index + 1].lower())] = 1
                        bigramtotaltokens += 1
                        bigram_vocabulary.append((tokens[index].lower() + " " + tokens[index + 1].lower()))

        return [tweetsCounter, unigramtotaltokens, word_frequency_unigrams, word_frequency_bigrams, bigramtotaltokens]

    def line_tokenization(self, tokens):
        uni_tokens = {}
        bi_tokens = {}
        for index, token in enumerate(tokens):
            # for unigrams
            if token in uni_tokens:
                uni_tokens[token.lower()] += 1
            else:
                uni_tokens[token.lower()] = 1

            # for bigrams
            if index < len(tokens) - 1:
                if (tokens[index].lower() + " " + tokens[index + 1].lower()) in bi_tokens:
                    bi_tokens[(tokens[index].lower() + " " + tokens[index + 1].lower())] += 1
                else:
                    bi_tokens[(tokens[index].lower() + " " + tokens[index + 1].lower())] = 1

        return [uni_tokens, bi_tokens]

    def testing(self, priors, cond_prob, N, class_metrics, pos_test, neg_test):

        correct_pos = 0
        correct_neg = 0
        pos_prior = priors[0]
        neg_prior = priors[1]

        # for postively labelled files
        total_test_tweets = 0
        poscontents = open(pos_test, "r")
        for line in poscontents.readlines():
            tokens = nltk.WhitespaceTokenizer().tokenize(line)
            total_test_tweets += 1
            # unigrams, bigrams
            tweet = self.line_tokenization(tokens)
            score_pos = math.log(pos_prior, 10)
            score_neg = math.log(neg_prior, 10)
            for word, occurence in tweet[0].iteritems():  # test file words
                # for positive
                if word not in cond_prob[0]:
                    new_cp = math.log((1 / float(class_metrics[0][1] + unigram_vocab_size)), 10)
                    score_pos += new_cp * occurence
                else:
                    score_pos += math.log(cond_prob[0][word], 10) * occurence

                # for negative
                if word not in cond_prob[1]:
                    new_cp = math.log((1 / float(class_metrics[1][1] + unigram_vocab_size)), 10)
                    score_neg += new_cp * occurence
                else:
                    score_neg += math.log(cond_prob[1][word], 10) * occurence

            if score_pos >= score_neg:
                correct_pos += 1

        poscontents.close()

        print "Correct Unigram Positives:" + str(correct_pos/ float(total_test_tweets) * 100)

        # for negatively labelled files
        total_test_tweets = 0
        negcontents = open(neg_test, "r")
        for line in negcontents.readlines():
            tokens = nltk.WhitespaceTokenizer().tokenize(line)
            total_test_tweets += 1
            # unigrams, bigrams
            tweet = self.line_tokenization(tokens)
            score_pos = math.log(pos_prior, 10)
            score_neg = math.log(neg_prior, 10)
            for word, occurence in tweet[0].iteritems():  # test unigram file words
                # for positive
                if word not in cond_prob[0]:
                    new_cp = math.log((1 / float(class_metrics[0][1] + unigram_vocab_size)), 10)
                    score_pos += new_cp * occurence
                else:
                    score_pos += math.log(cond_prob[0][word], 10) * occurence

                # for negative
                if word not in cond_prob[1]:
                    new_cp = math.log((1 / float(class_metrics[1][1] + unigram_vocab_size)), 10)
                    score_neg += new_cp * occurence
                else:
                    score_neg += math.log(cond_prob[1][word], 10) * occurence

            if score_pos <= score_neg:
                correct_neg += 1

        print "Correct Unigram Negatives:" + str(correct_neg/float(total_test_tweets) * 100)

        # __Bigrams__
        correct_pos = 0
        correct_neg = 0
        # for postively labelled bigram files
        total_test_tweets = 0
        poscontents = open(pos_test, "r")
        for line in poscontents.readlines():
            tokens = nltk.WhitespaceTokenizer().tokenize(line)
            total_test_tweets += 1
            # unigrams, bigrams
            tweet = self.line_tokenization(tokens)
            score_pos = math.log(pos_prior, 10)
            score_neg = math.log(neg_prior, 10)
            for word, occurence in tweet[1].iteritems():  # test file words
                # for positive
                if word not in cond_prob[2]:
                    new_cp = math.log((1 / float(class_metrics[0][4] + bigram_vocab_size)), 10)
                    score_pos += new_cp * occurence
                else:
                    score_pos += math.log(cond_prob[2][word], 10) * occurence

                # for negative
                if word not in cond_prob[3]:
                    new_cp = math.log((1 / float(class_metrics[1][4] + bigram_vocab_size)), 10)
                    score_neg += new_cp * occurence
                else:
                    score_neg += math.log(cond_prob[3][word], 10) * occurence

            if score_pos >= score_neg:
                correct_pos += 1

        poscontents.close()

        print "Correct Bigram Positives:" + str(correct_pos/ float(total_test_tweets) * 100)

        # for negatively labelled files
        total_test_tweets = 0
        negcontents = open(neg_test, "r")
        for line in negcontents.readlines():
            tokens = nltk.WhitespaceTokenizer().tokenize(line)
            total_test_tweets += 1
            # unigrams, bigrams
            tweet = self.line_tokenization(tokens)
            score_pos = math.log(pos_prior, 10)
            score_neg = math.log(neg_prior, 10)
            for word, occurence in tweet[1].iteritems():  # test unigram file words
                # for positive
                if word not in cond_prob[2]:
                    new_cp = math.log((1 / float(class_metrics[0][4] + bigram_vocab_size)), 10)
                    score_pos += new_cp * occurence
                else:
                    score_pos += math.log(cond_prob[2][word], 10) * occurence

                # for negative
                if word not in cond_prob[3]:
                    new_cp = math.log((1 / float(class_metrics[1][4] + bigram_vocab_size)), 10)
                    score_neg += new_cp * occurence
                else:
                    score_neg += math.log(cond_prob[3][word], 10) * occurence

            if score_pos <= score_neg:
                correct_neg += 1

        print "Correct Bigram Negatives:" + str(correct_neg/float(total_test_tweets) * 100)


    def naiveBayes(self, pos_train, neg_train, pos_test, neg_test):

        # totaltweets, unigramtotaltokens, unigramcount, bigramcount, bigramtotaltokens
        positive_metrics = self.tokenization(pos_train)
        negative_metrics = self.tokenization(neg_train)
        classes = [positive_metrics, negative_metrics]
        # print len(set(unigram_vocabulary))
        # print len(set(bigram_vocabulary))
        N = positive_metrics[0] + negative_metrics[0]  # total tweets

        # calculate the conditional probability
        priors = []
        unibigram_cond_prob = []

        # for unigram
        conditional_prob = []
        unigram_vocab_size = len(set(unigram_vocabulary))
        for i, each_class in enumerate(classes):
            priors.append(each_class[0] / float(N))  # add positive class prior
            conditional_prob_of_class = {}
            for each_word in set(unigram_vocabulary):
                if each_word in each_class[2]:
                    conditional_prob_of_class[each_word] = (each_class[2][each_word] + 1) / float(
                        each_class[1] + unigram_vocab_size)
                else:
                    conditional_prob_of_class[each_word] = 1 / float(each_class[1] + unigram_vocab_size)
            conditional_prob.append(conditional_prob_of_class)
            unibigram_cond_prob.append(conditional_prob_of_class)

        unimodel_file = open("unigram_file", "w")
        for each_word in set(unigram_vocabulary):
            unimodel_file.write(str(each_word) + "\t" + str(conditional_prob[0][each_word]) + "\t"
                                + str(conditional_prob[1][each_word]) + "\n")

        unimodel_file.close()

        # for bigram
        conditional_prob = []
        bigram_vocab_size = len(set(bigram_vocabulary))
        for i, each_class in enumerate(classes):
            conditional_prob_of_class = {}
            for each_word in set(bigram_vocabulary):
                if each_word in each_class[3]:
                    conditional_prob_of_class[each_word] = (each_class[3][each_word] + 1) / float(
                        each_class[4] + bigram_vocab_size)
                else:
                    conditional_prob_of_class[each_word] = 1 / float(each_class[4] + bigram_vocab_size)
            conditional_prob.append(conditional_prob_of_class)
            unibigram_cond_prob.append(conditional_prob_of_class)

        bimodel_file = open("bigram_file", "w")
        for each_word in set(bigram_vocabulary):
            bimodel_file.write(str(each_word) + "\t" + str(conditional_prob[0][each_word]) + "\t" + str(
                conditional_prob[1][each_word]) + "\n")
        bimodel_file.close()

        self.testing(priors, unibigram_cond_prob, N, classes, pos_test, neg_test)


def main():
    print "\n-------------------------WELCOME-------------------------\n"

    pos_train_filepath = raw_input("Enter the positive train file path:")
    # pos_train_filepath = "./final/ds2/train/pos"
    neg_train_filepath = raw_input("Enter the negative train file path:")
    # neg_train_filepath = "./final/ds2/train/neg"

    # pos_test_filepath = "./final/ds2/test/pos"
    pos_test_filepath = raw_input("Enter the positive test file path:")
    # neg_test_filepath = "./final/ds2/test/neg"
    neg_test_filepath = raw_input("Enter the negative test file path:")

    print "\n----------------------IMPLEMENTATION---------------------\n"

    nb = NaiveBayes()
    nb.naiveBayes(pos_train_filepath, neg_train_filepath, pos_test_filepath, neg_test_filepath)

    print "\n----------------------------BYE--------------------------\n"

if __name__ == "__main__":
    main()



