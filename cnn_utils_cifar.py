# -*- coding: utf-8 -*-

import math
import numpy as np
import h5py
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.python.framework import ops
import pickle
from sklearn.preprocessing import LabelBinarizer

def load_dataset_mnist():
    
    train_dataset = h5py.File('mnist.h5', "r")
    train_set_x_orig = np.array(train_dataset["train"]["inputs"]) # your train set features
    train_set_y_orig = np.array(train_dataset["train"]["targets"]) # your train set labels
    
    test_set_x_orig = np.array(train_dataset["test"]["inputs"]) # your test set features
    test_set_y_orig = np.array(train_dataset["test"]["targets"]) # your test set labels
    
    train_y=np.zeros((10,len(train_set_y_orig)))
    test_y=np.zeros((10,len(test_set_y_orig)))
    
    for i in range(0,10):
        train_y[i,np.where(train_set_y_orig[:]==i)[0]]=1
        test_y[i,np.where(test_set_y_orig[:]==i)[0]]=1
       
    idx_train = np.arange(train_y.shape[1])
    np.random.shuffle(idx_train)
    
    idx_test = np.arange(test_y.shape[1])
    np.random.shuffle(idx_test)
    
    train_set_x_orig = train_set_x_orig.reshape((train_set_x_orig.shape[0], train_set_x_orig.shape[1], train_set_x_orig.shape[2]))    
    test_set_x_orig = test_set_x_orig.reshape((test_set_x_orig.shape[0], test_set_x_orig.shape[1], test_set_x_orig.shape[2]))

    train_dataset.close()
    
    return train_set_x_orig[idx_train, ...], train_y[:,idx_train], test_set_x_orig[idx_test, ...], test_y[:,idx_test]

def _load_label_names():
    """
    Load the label names from file
    """
    return ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']

def display_image_predictions(features, labels, predictions):
    n_classes = 10
    label_names = _load_label_names()
    label_binarizer = LabelBinarizer()
    label_binarizer.fit(range(n_classes))
#    label_ids = label_binarizer.inverse_transform(np.array(labels.T))
    
    fig, axies = plt.subplots(nrows=4, ncols=2)
    fig.tight_layout()
    fig.suptitle('Softmax Predictions', fontsize=20, y=1.1)

    n_predictions = 3
    margin = 0.05
    ind = np.arange(n_predictions)
    width = (1. - 2. * margin) / n_predictions

    for image_i, (feature, label_id, pred_indicies, pred_values) in enumerate(zip(features, labels.T, predictions.indices, predictions.values)):
        pred_names = [label_names[pred_i] for pred_i in pred_indicies]
#        print("label_id",label_id)
        
        correct_name = label_names[int(label_id)]
#        print("correct_name",correct_name)
        
        axies[image_i][0].imshow(feature*255)
        axies[image_i][0].set_title(correct_name)
        axies[image_i][0].set_axis_off()

        axies[image_i][1].barh(ind + margin, pred_values[::-1], width)
        axies[image_i][1].set_yticks(ind + margin)
        axies[image_i][1].set_yticklabels(pred_names[::-1])
        axies[image_i][1].set_xticks([0, 0.5, 1.0])

def batch_features_labels(features, labels, batch_size):
    """
    Split features and labels into batches
    """
#    print(0)
    for start in range(0, len(features), batch_size):
        end = min(start + batch_size, len(features))
#        print(end)
        yield features[start:end], labels[start:end]
        
def load_preprocess_training_batch(batch_id, batch_size):
    """
    Load the Preprocessed Training data and return them in batches of <batch_size> or less
    """
    filename = 'C:\\Users\\Familiamadcas2\\Downloads\\RedesConvolucionales_Clase1_full (1)\\RedesConvolucionales_Clase1_full\\cifar-10-batches-py\\data_batch_' + str(batch_id) 
    with open(filename, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
        features= dict[b'data'] #- se cambia para que no tome la B en las 2 lineas
        labels= dict[b'labels']
    return batch_features_labels(features, labels, batch_size)

def load_preprocess_test_batch(batch_size):
    """
    Load the Preprocessed Training data and return them in batches of <batch_size> or less
    """
    filename = 'C:\\Users\\Familiamadcas2\\Downloads\\RedesConvolucionales_Clase1_full (1)\\RedesConvolucionales_Clase1_full\\cifar-10-batches-py\\test_batch'
    with open(filename, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
        features= dict[b'data']
        labels= dict[b'labels']
#        print(features.shape)
#        print(len(labels))
        
#        print(batch_features_labels(features, labels, batch_size))
    # Return the training data in batches of size <batch_size> or less
#        print(len(features))
#    batch_features_labels(features, labels, batch_size)
#    print(len(features))
    return batch_features_labels(features, labels, batch_size)

def load_dataset_cifar():

    for i in range (1,6):
        data=unpickle('datasets/cifar-10-batches-py/data_batch_' + str(i))
        if i==1:
             dataTrain=data[b'data']
             labelTrain=data[b'labels']
        else:
            dataTrain=np.concatenate((dataTrain, data[b'data']), axis=0)
            labelTrain=np.concatenate((labelTrain, data[b'labels']), axis=0)

    testTrain= unpickle('datasets/cifar-10-batches-py/test_batch')
    dataTest= testTrain[b'data']
    labelTest= testTrain[b'labels']
    
    X_train_orig= dataTrain.reshape(len(dataTrain),3,32,32).transpose([0,2,3,1])
    Y_train_orig= np.array(labelTrain,dtype=np.uint8)[:,np.newaxis].T
    
    X_test_orig= dataTest.reshape(len(dataTest),3,32,32).transpose([0,2,3,1])
    Y_test_orig= np.array(labelTest,dtype=np.uint8)[:,np.newaxis].T
    
    return X_train_orig, Y_train_orig, X_test_orig, Y_test_orig

def load_test_cifar():

    testTrain= unpickle('C:\\Users\\Familiamadcas2\\Downloads\\RedesConvolucionales_Clase1_full (1)\\RedesConvolucionales_Clase1_full\\cifar-10-batches-py\\test_batch')
    dataTest= testTrain[b'data']
    labelTest= testTrain[b'labels']
    
    X_test_orig= dataTest.reshape(len(dataTest),3,32,32).transpose([0,2,3,1])
    Y_test_orig= np.array(labelTest,dtype=np.uint8)[:,np.newaxis].T
    
    return X_test_orig, Y_test_orig

def unpickle(file):
    import pickle
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    return dict

def load_dataset():
    train_dataset = h5py.File('datasets/train_signs.h5', "r")
    train_set_x_orig = np.array(train_dataset["train_set_x"][:]) # your train set features
    train_set_y_orig = np.array(train_dataset["train_set_y"][:]) # your train set labels

    test_dataset = h5py.File('datasets/test_signs.h5', "r")
    test_set_x_orig = np.array(test_dataset["test_set_x"][:]) # your test set features
    test_set_y_orig = np.array(test_dataset["test_set_y"][:]) # your test set labels

    classes = np.array(test_dataset["list_classes"][:]) # the list of classes
    
    train_set_y_orig = train_set_y_orig.reshape((1, train_set_y_orig.shape[0]))
    test_set_y_orig = test_set_y_orig.reshape((1, test_set_y_orig.shape[0]))
    
    return train_set_x_orig, train_set_y_orig, test_set_x_orig, test_set_y_orig, classes


def random_mini_batches(X, Y, mini_batch_size = 64, seed = 0):
    """
    Creates a list of random minibatches from (X, Y)
    
    Arguments:
    X -- input data, of shape (input size, number of examples) (m, Hi, Wi, Ci)
    Y -- true "label" vector (containing 0 if cat, 1 if non-cat), of shape (1, number of examples) (m, n_y)
    mini_batch_size - size of the mini-batches, integer
    seed -- this is only for the purpose of grading, so that you're "random minibatches are the same as ours.
    
    Returns:
    mini_batches -- list of synchronous (mini_batch_X, mini_batch_Y)
    """
    
    m = X.shape[0]                  # number of training examples
    mini_batches = []
    np.random.seed(seed)
#    print(m)
    
    # Step 1: Shuffle (X, Y)
    permutation = list(np.random.permutation(m))
    shuffled_X = X[permutation,:,:,:]
    shuffled_Y = Y[permutation,:]

    # Step 2: Partition (shuffled_X, shuffled_Y). Minus the end case.
    num_complete_minibatches = math.floor(m/mini_batch_size) # number of mini batches of size mini_batch_size in your partitionning
    for k in range(0, num_complete_minibatches):
        mini_batch_X = shuffled_X[k * mini_batch_size : k * mini_batch_size + mini_batch_size,:,:,:]
        mini_batch_Y = shuffled_Y[k * mini_batch_size : k * mini_batch_size + mini_batch_size,:]
        mini_batch = (mini_batch_X, mini_batch_Y)
        mini_batches.append(mini_batch)
    
    # Handling the end case (last mini-batch < mini_batch_size)
    if m % mini_batch_size != 0:
        mini_batch_X = shuffled_X[num_complete_minibatches * mini_batch_size : m,:,:,:]
        mini_batch_Y = shuffled_Y[num_complete_minibatches * mini_batch_size : m,:]
        mini_batch = (mini_batch_X, mini_batch_Y)
        mini_batches.append(mini_batch)
    
    return mini_batches


def convert_to_one_hot(Y, C):
    Y = np.eye(C)[Y.reshape(-1)].T
    return Y


def forward_propagation_for_predict(X, parameters):
    """
    Implements the forward propagation for the model: LINEAR -> RELU -> LINEAR -> RELU -> LINEAR -> SOFTMAX
    
    Arguments:
    X -- input dataset placeholder, of shape (input size, number of examples)
    parameters -- python dictionary containing your parameters "W1", "b1", "W2", "b2", "W3", "b3"
                  the shapes are given in initialize_parameters

    Returns:
    Z3 -- the output of the last LINEAR unit
    """
    
    # Retrieve the parameters from the dictionary "parameters" 
    W1 = parameters['W1']
    b1 = parameters['b1']
    W2 = parameters['W2']
    b2 = parameters['b2']
    W3 = parameters['W3']
    b3 = parameters['b3'] 
                                                           # Numpy Equivalents:
    Z1 = tf.add(tf.matmul(W1, X), b1)                      # Z1 = np.dot(W1, X) + b1
    A1 = tf.nn.relu(Z1)                                    # A1 = relu(Z1)
    Z2 = tf.add(tf.matmul(W2, A1), b2)                     # Z2 = np.dot(W2, a1) + b2
    A2 = tf.nn.relu(Z2)                                    # A2 = relu(Z2)
    Z3 = tf.add(tf.matmul(W3, A2), b3)                     # Z3 = np.dot(W3,Z2) + b3
    
    return Z3

def predict(X, parameters):
    
    W1 = tf.convert_to_tensor(parameters["W1"])
    b1 = tf.convert_to_tensor(parameters["b1"])
    W2 = tf.convert_to_tensor(parameters["W2"])
    b2 = tf.convert_to_tensor(parameters["b2"])
    W3 = tf.convert_to_tensor(parameters["W3"])
    b3 = tf.convert_to_tensor(parameters["b3"])
    
    params = {"W1": W1,
              "b1": b1,
              "W2": W2,
              "b2": b2,
              "W3": W3,
              "b3": b3}
    
    x = tf.placeholder("float", [12288, 1])
    
    z3 = forward_propagation_for_predict(x, params)
    p = tf.argmax(z3)
    
    sess = tf.Session()
    prediction = sess.run(p, feed_dict = {x: X})
        
    return prediction

#def predict(X, parameters):
#    
#    W1 = tf.convert_to_tensor(parameters["W1"])
#    b1 = tf.convert_to_tensor(parameters["b1"])
#    W2 = tf.convert_to_tensor(parameters["W2"])
#    b2 = tf.convert_to_tensor(parameters["b2"])
##    W3 = tf.convert_to_tensor(parameters["W3"])
##    b3 = tf.convert_to_tensor(parameters["b3"])
#    
##    params = {"W1": W1,
##              "b1": b1,
##              "W2": W2,
##              "b2": b2,
##              "W3": W3,
##              "b3": b3}
#
#    params = {"W1": W1,
#              "b1": b1,
#              "W2": W2,
#              "b2": b2}    
#    
#    x = tf.placeholder("float", [12288, 1])
#    
#    z3 = forward_propagation(x, params)
#    p = tf.argmax(z3)
#    
#    with tf.Session() as sess:
#        prediction = sess.run(p, feed_dict = {x: X})
#        
#    return prediction