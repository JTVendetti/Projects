import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import gensim.downloader as api
import numpy.random as random

def word_tokenization_dataset(training_sentences):
    training_set = []
    for sentence in training_sentences:
        cur_sentence = [word.lower() for word in sentence.split(" ")]
        training_set.append(cur_sentence)
    return training_set

def word_tokenization_sentence(test_sentence):
    return [word.lower() for word in test_sentence.split(" ")]

def compute_vocabulary(training_set):
    vocabulary = set(word for sentence in training_set for word in sentence)
    V_dictionary = {word: idx for idx, word in enumerate(vocabulary)}
    return V_dictionary

def file_reader(file_path, label):
    list_of_lines = []
    list_of_labels = []
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                list_of_lines.append(line)
                list_of_labels.append(label)
    return list_of_lines, list_of_labels

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

def generate_vectors(sentences, wv):
    sentence_vectors = []
    for sentence in sentences:
        words = word_tokenization_sentence(sentence)
        vectors = [wv[word] for word in words if word in wv]
        if vectors:
            sentence_vectors.append(np.mean(vectors, axis=0))
        else:
            sentence_vectors.append(np.zeros(wv.vector_size))
    return np.array(sentence_vectors)

def train_and_evaluate(X_train, y_train, X_test, y_test, n_estimators=1000):
    rf = RandomForestClassifier(n_estimators=n_estimators)
    rf.fit(X_train, y_train)
    y_pred = rf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    return accuracy


TASK = "train"
if TASK=="train":
    source_dir = "data-sentiment/train/"  # Replace with actual path
    sentences, labels = data_reader(source_dir)

    # Split data into training and testing sets
    random.seed(42)
    indices = random.permutation(len(sentences))
    split = int(0.8 * len(sentences))
    train_indices, test_indices = indices[:split], indices[split:]

    train_sentences, train_labels = [sentences[i] for i in train_indices], labels[train_indices]
    test_sentences, test_labels = [sentences[i] for i in test_indices], labels[test_indices]

     # Load Word2Vec model
    print("Loading Word2Vec model...")
    wv = api.load('word2vec-google-news-300')

        # Generate vectors
    print("Generating sentence vectors...")
    X_train = generate_vectors(train_sentences, wv)
    X_test = generate_vectors(test_sentences, wv)

    # Train and evaluate Random Forest with different estimators
    for n_estimators in [100, 500, 1000]:
        print(f"Training Random Forest with {n_estimators} estimators...")
        accuracy = train_and_evaluate(X_train, train_labels, X_test, test_labels, n_estimators=n_estimators)
        print(f"Accuracy with {n_estimators} estimators: {accuracy:.4f}")

        # Accuracy study with smaller training sets
    for size in [25, 50, 150, 200, 300]:
        subset_indices = train_indices[:size]
        subset_sentences = [sentences[i] for i in subset_indices]
        subset_labels = labels[subset_indices]

        print(f"Training with {size} samples...")
        X_subset = generate_vectors(subset_sentences, wv)
        accuracy = train_and_evaluate(X_subset, subset_labels, X_test, test_labels)
        print(f"Accuracy with training size {size}: {accuracy:.4f}")

TASK = "test"
if TASK=="test":
    source_dir = "data-sentiment/test/"  # Replace with actual path
    sentences, labels = data_reader(source_dir)

    # Split data into training and testing sets
    random.seed(42)
    indices = random.permutation(len(sentences))
    split = int(0.8 * len(sentences))
    train_indices, test_indices = indices[:split], indices[split:]

    train_sentences, train_labels = [sentences[i] for i in train_indices], labels[train_indices]
    test_sentences, test_labels = [sentences[i] for i in test_indices], labels[test_indices]

    # Load Word2Vec model
    print("Loading Word2Vec model...")
    wv = api.load('word2vec-google-news-300')

    # Generate vectors
    print("Generating sentence vectors...")
    X_train = generate_vectors(train_sentences, wv)
    X_test = generate_vectors(test_sentences, wv)

    # Train and evaluate Random Forest with different estimators
    for n_estimators in [100, 500, 1000]:
        print(f"Training Random Forest with {n_estimators} estimators...")
        accuracy = train_and_evaluate(X_train, train_labels, X_test, test_labels, n_estimators=n_estimators)
        print(f"Accuracy with {n_estimators} estimators: {accuracy:.4f}")

    # Accuracy study with smaller training sets
    for size in [25, 50, 150, 200, 300]:
        subset_indices = train_indices[:size]
        subset_sentences = [sentences[i] for i in subset_indices]
        subset_labels = labels[subset_indices]

        print(f"Training with {size} samples...")
        X_subset = generate_vectors(subset_sentences, wv)
        accuracy = train_and_evaluate(X_subset, subset_labels, X_test, test_labels)
        print(f"Accuracy with training size {size}: {accuracy:.4f}")
