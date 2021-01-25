import pandas as pd
from scipy.stats import entropy

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

# Features
## 1. Length of the command line
## 2. proportion of upper case letters
## 3. proportion of operators (%, *, /, +, -, =, <, >)
## 4. proportion of white space in the command line
## 5. proportion of special characters
## 6. The frequency of the strings “cmd” and “power” in the command line
## 7. The count of pipe symbols
## 8. The number of carets in the command line
## 9. frequency of -f and -F
## x. (not used for now) Entropy of the string (Shannon) (H=−∑︁(i) (PilogPi) )
## x. (not used for now) character frequency: frequency of all characters (ignore case)



# load doc into memory
def load_doc(filename):
    file = open(filename, 'r')
    text = file.read()
    file.close()
    lines = text.split('\n')
    lines[:] = [x for x in lines if x]
    return lines

# get features of a string
def get_features(string):
    features_nb = 9
    features = [0] * features_nb
    features[0] = len(string)
    for char in string:
        if char.isupper(): features[1] += 1
        if char in ["%", "*", "/", "+", "-", "=", "<", ">"]: features[2] += 1
        if char == ' ': features[3] += 1
        if char in ' !\"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~': features[4] += 1
        if char == '|': features[6] += 1
        if char == '^': features[7] += 1
    features[5] = string.count("cmd") + string.count("power")
    features[8] = string.count("-f") + string.count("-F")
    for i in range(1, features_nb):
        features[i] /= features[0]
    #print(features)
    return features




# data files
clearfile = '../../data/clear/cmds.txt'
obffile = '../../data/obfuscated/cmds.txt'

# load text into list of strings
clear_lines = load_doc(clearfile)
obf_lines = load_doc(obffile)


###############################################################################
# feature extraction
clear_features = []
for line in clear_lines:
    clear_features.append(get_features(line))
#print(clear_features)
obf_features = []
for line in obf_lines:
    obf_features.append(get_features(line))
#print(obf_features)


###############################################################################
# import dataset
names = ['length', 'upper', 'operator', 'white', 'special', 'cmdpower', 'pipe', 
        'carets', 'fF']
clear_dataset = pd.DataFrame.from_records(clear_features, columns=names)
obf_dataset   = pd.DataFrame.from_records(obf_features, columns=names)
# add obf/not obf bool
l = [0] * len(clear_dataset.index)
clear_dataset.insert(loc=0, column='obf', value=l)
l = [1] * len(obf_dataset.index)
obf_dataset.insert(loc=0, column='obf', value=l)
## merge clear and obfuscated datasets
frames = [clear_dataset, obf_dataset]
data = pd.concat(frames)
#print(data)
#print(data.describe()) # descriptions

###############################################################################
# Split-out validation dataset
array = data.values
X = array[:,1:]
y = array[:,:1]
X_train, X_validation, Y_train, Y_validation = train_test_split(X, y, test_size=0.20, random_state=1)


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


















