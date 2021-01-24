# test4
working featureless Machine Learning examples
using multiple models and comparing them

## Problems and Solutions
1. data: not of fixed size  
   solution: use pandas.read_csv with a range of names (range = longuest data 
   string)
2. add a validation column in the data
3. read_csv added NaN to fill data lines which can't be process later by models 
   solution: replace NaN with mean
4. error with some models "A column-vector y was passed when a 1d array was 
   expected"  
   solution: Y_train.ravel()
