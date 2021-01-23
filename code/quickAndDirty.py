# Load libraries
import pandas as pd
from matplotlib import pyplot
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

###############################################################################
## Import the dataset

data_clear = pd.read_csv('../data/clear/cmds.txt', header=None, names=["a"])
data_obf   = pd.read_csv('../data/obfuscated/cmds.txt', header=None, names=["a"])
## add a column (bool defining if obfuscated or not)
l = [0] * len(data_clear.index)
data_clear["b"] = l
l = [1] * len(data_obf.index)
data_obf["b"] = l
## merge clear and obfuscated datasets
frames = [data_clear, data_obf]
data = pd.concat(frames)


###############################################################################
## Debug: Summarize the dataset

#print(data_clear)
#print(len(data_clear.index))
#print(data_clear.shape)    # shape
#print(data_clear.head(20)) # peek
#print(data_clear.describe())  # descriptions
#print(data_clear.groupby('b').size()) # class distribution

#print(data_obf)
#print(len(data_obf.index))
#print(data_obf.shape)    # shape
#print(data_obf.head(20)) # peek
#print(data_obf.describe())  # descriptions
#print(data_obf.groupby('b').size()) # class distribution

#print(data)
#print(len(data.index))
#print(data.shape)    # shape
#print(data.head(20)) # peek
#print(data.describe())  # descriptions
#print(data.groupby('b').size()) # class distribution


###############################################################################
## Create a Validation Dataset

X = data.drop(columns = ["b"])
y = data["b"]
#print(X)
#print(y)
X_train, X_validation, Y_train, Y_validation = train_test_split(X, y, test_size=0.20, random_state=1, shuffle=True)


## test
model = DecisionTreeClassifier()
model.fit(X, y)







### test
#model = DecisionTreeClassifier()
#model.fit(X_train, Y_train)
#predictions = model.predict(X_validation)
#score = accuracy_score(Y_validation, predictions)
#print (score)











################################################################################
### Import models
#
#models = []
#models.append(('LR', LogisticRegression(solver='liblinear', multi_class='ovr')))
#models.append(('LDA', LinearDiscriminantAnalysis()))
#models.append(('KNN', KNeighborsClassifier()))
#models.append(('CART', DecisionTreeClassifier()))
#models.append(('NB', GaussianNB()))
#models.append(('SVM', SVC(gamma='auto')))
#
#
################################################################################
## Evaluate each model in turn
#
#results = []
#names = []
#for name, model in models:
#	kfold = StratifiedKFold(n_splits=10, random_state=1, shuffle=True)
#	cv_results = cross_val_score(model, X_train, Y_train, cv=kfold, scoring='accuracy')
#	results.append(cv_results)
#	names.append(name)
#	print('%s: %f (%f)' % (name, cv_results.mean(), cv_results.std()))
