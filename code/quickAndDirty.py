# Load libraries
import pandas as pd

## import the dataset
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

## Debug: Summarize the dataset
#print(len(data_clear.index))
#print(data_clear.shape)    # shape
#print(data_clear.head(20)) # peek
#print(data_clear.describe())  # descriptions
#print(data_clear.groupby('b').size()) # class distribution

#print(len(data_obf.index))
#print(data_obf.shape)    # shape
#print(data_obf.head(20)) # peek
#print(data_obf.describe())  # descriptions
#print(data_obf.groupby('b').size()) # class distribution

print(len(data.index))
print(data.shape)    # shape
print(data.head(20)) # peek
print(data.describe())  # descriptions
print(data.groupby('b').size()) # class distribution
