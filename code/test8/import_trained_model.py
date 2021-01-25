# make predictions
import pandas as pd
from pandas import read_csv
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import joblib


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
clear_dataset = pd.DataFrame.from_records(clear, columns=names)
obf_dataset   = pd.DataFrame.from_records(obf, columns=names)
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

################################################################################
## Load trained model
model = joblib.load('lda_trained.sav')

################################################################################
# make predictions
predictions = model.predict(X_validation)

###############################################################################
# Make predictions on validation dataset
# Evaluate predictions
print(accuracy_score(Y_validation, predictions))
print(confusion_matrix(Y_validation, predictions))
print(classification_report(Y_validation, predictions))
