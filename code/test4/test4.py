# Load libraries
import pandas as pd
import csv
from numpy import array
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# Need to find the longest string in the dataset for read_csv
def get_size(filename):
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
        return(max(map(len, data)))

###############################################################################
## Import the dataset
fileclear = '../test3/clear.csv'
fileobf   = '../test3/obf.csv'

# Need to find the longest string in the dataset for read_csv
size_clear = get_size(fileclear)
size_obf = get_size(fileobf)
# read data
names = range(max(size_clear, size_obf))
data_clear = pd.read_csv(fileclear, sep=',', names=names, header=None)
data_obf   = pd.read_csv(fileobf, sep=',', names=names, header=None)
## add a column position 0 (bool defining if obfuscated or not)
l = [0] * len(data_clear.index)
data_clear.insert(loc=0, column='A', value=l)
l = [1] * len(data_obf.index)
data_obf.insert(loc=0, column='A', value=l)
## merge clear and obfuscated datasets
frames = [data_clear, data_obf]
data = pd.concat(frames)
#print(data)
# replace NaN in data
data.fillna(data.mean(), inplace=True)

###############################################################################
## Create a Validation Dataset
sequences = array(data)
#array = data.values
X = sequences[:,1:]
y = sequences[:,:1]
X_train, X_validation, Y_train, Y_validation = train_test_split(X, y, test_size=0.20, random_state=1, shuffle=True)

###############################################################################
## Import models
models = []
models.append(('LR', LogisticRegression(solver='liblinear', multi_class='ovr')))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC(gamma='auto')))

###############################################################################
# Evaluate each model in turn
results = []
names = []
for name, model in models:
#    model.fit(X_train, Y_train.ravel())
#    predictions = model.predict(X_validation)
#    score = accuracy_score(Y_validation, predictions)
#    names.append(name)
#    print('%s: %f' % (name, score))
    kfold = StratifiedKFold(n_splits=10, random_state=1, shuffle=True)
    cv_results = cross_val_score(model, X_train, Y_train.ravel(), cv=kfold, scoring='accuracy')
    results.append(cv_results)
    names.append(name)
    print('%s: %f (%f)' % (name, cv_results.mean(), cv_results.std()))

