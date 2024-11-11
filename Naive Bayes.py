from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import pickle
import math


def file_reader(file_path, label):
    list_of_lines = []
    list_of_labels = []

    for line in open(file_path):
        line = line.strip()
        if line=="":
            continue
        list_of_lines.append(line)
        list_of_labels.append(label)

    return (list_of_lines, list_of_labels)


def data_reader(source_directory):
    positive_file = source_directory+"Positive.txt"
    (positive_list_of_lines, positive_list_of_labels)=file_reader(file_path=positive_file, label=1)

    negative_file = source_directory+"Negative.txt"
    (negative_list_of_lines, negative_list_of_labels)=file_reader(file_path=negative_file, label=-1)

    neutral_file = source_directory+"Neutral.txt"
    (neutral_list_of_lines, neutral_list_of_labels)=file_reader(file_path=neutral_file, label=0)

    list_of_all_lines = positive_list_of_lines + negative_list_of_lines + neutral_list_of_lines
    list_of_all_labels = np.array(positive_list_of_labels + negative_list_of_labels + neutral_list_of_labels)

    return list_of_all_lines, list_of_all_labels


def evaluate_predictions(test_set,test_labels,trained_classifier):
    correct_predictions = 0
    predictions_list = []
    prediction = -1
    for dataset,label in zip(test_set, test_labels):
        probabilities = trained_classifier.predict(dataset)
        if probabilities[0] >= probabilities[1] and probabilities[0] >= probabilities[-1]:
            prediction = 0
        elif  probabilities[1] >= probabilities[0] and probabilities[1] >= probabilities[-1]:
            prediction = 1
        else:
            prediction=-1
        if prediction == label:
            correct_predictions += 1
            predictions_list.append("+")
        else:
            predictions_list.append("-")


    print("Total Sentences correctly: ", len(test_labels))

    print("Predicted correctly: ", correct_predictions)

    print("Accuracy: {}%".format(round(correct_predictions/len(test_labels)*100,5)))


    return predictions_list, round(correct_predictions/len(test_labels)*100)


class NaiveBayesClassifier(object):
    def __init__(self, n_gram=1, printing=False):
        self.prior = []
        self.conditional = []
        self.V = []
        self.n = n_gram
        self.BOW=[]
        self.classCounts=[]
        self.D=0
        self.N=0
        self.labelmap={}

    def word_tokenization_dataset(self, training_sentences):
        training_set = list()
        for sentence in training_sentences:
            cur_sentence = list()
            for word in sentence.split(" "):
                cur_sentence.append(word.lower())
            training_set.append(cur_sentence)
        return training_set

    def word_tokenization_sentence(self, test_sentence):
        cur_sentence = list()
        for word in test_sentence.split(" "):
            cur_sentence.append(word.lower())
        return cur_sentence

    def compute_vocabulary(self, training_set):
        vocabulary = set()
        for sentence in training_set:
            for word in sentence:
                vocabulary.add(word)
        V_dictionary = dict()
        dict_count = 0
        for word in vocabulary:
            V_dictionary[word] = int(dict_count)
            dict_count += 1
        return V_dictionary

    def train(self, training_sentences, training_labels):
        
        # See the HW_3_How_To.pptx for details
        
        # Get number of sentences in the training set


        # This will turn the training_sentences into the format described in the HW_3_How_To.pptx
        training_set = self.word_tokenization_dataset(training_sentences)

        # Get vocabulary (dictionary) used in training set
        self.V = self.compute_vocabulary(training_set)
        N_sentences = len(training_sentences)
        self.D = len(self.V)
        # Get set of all classes
        classes = set(training_labels)
       
        self.prior = {c: 0 for c in classes}  # Count of sentences per class
        word_counts = {c: np.zeros(self.D) for c in classes}  # Word counts for each class
        self.conditional = {}
        # Calculate priors and word counts per class
        for sentence, label in zip(training_set, training_labels):
            self.prior[label] += 1
            for word in set(sentence):  # Use set to avoid counting duplicate words
                if word in self.V:  # Ensure word is in vocabulary
                    word_index = self.V[word]
                    if 0 <= word_index < self.D:  # Ensure within bounds
                        word_counts[label][word_index] += 1

        # Convert counts to probabilities
        for c in classes:
            self.prior[c] /= len(training_labels)  # Normalize to get prior probabilities
            total_words = word_counts[c].sum()
            self.conditional[c] = (word_counts[c] + 1) / (total_words + self.D)  # Add-1 smoothing


    def predict(self, test_sentence):

        # The input is one test sentence. See the HW_3_How_To.pptx for details
        
        # Your are going to save the log probability for each class of the test sentence. See the HW_3_How_To.pptx for details
        label_probability = {
            0: 0,
            1: 0,
            -1:0,
        }

        # This will tokenize the test_sentence: test_sentence[n] will be the "n-th" word in a sentence (n starts from 0)
        test_sentence = self.word_tokenization_sentence(test_sentence)

        
        binary_bow = np.zeros(self.D)
        for word in set(test_sentence):
            if word in self.V:
                binary_bow[self.V[word]] = 1

        # Log probability for each class
        log_prob = {}
        for c in self.prior:
            log_prob[c] = math.log(self.prior[c])  # Start with log prior
            for d in range(self.D):
                if binary_bow[d] == 1:  # Word is present
                    log_prob[c] += math.log(self.conditional[c][d])
                else:  # Word is absent
                    log_prob[c] += math.log(1 - self.conditional[c][d])

        # -------- TO DO (end) --------#

        return label_probability

TASK = 'train'  #'train'  'test'

if TASK=='train':
    train_folder = "data-sentiment/train/"       
    training_sentences, training_labels = data_reader(train_folder)
        
    NBclassifier = NaiveBayesClassifier(n_gram=1)
    NBclassifier.train(training_sentences,training_labels)
    
    f = open('classifier.pkl', 'wb')
    pickle.dump(NBclassifier, f)
    f.close()
TASK = 'test'
if TASK == 'test':
    test_folder = "data-sentiment/test/"
    test_sentences, test_labels = data_reader(test_folder)
    f = open('classifier.pkl', 'rb')
    NBclassifier = pickle.load(f)
    f.close()    
    results, acc = evaluate_predictions(test_sentences, test_labels, NBclassifier)
