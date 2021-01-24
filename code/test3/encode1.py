import csv
from numpy import array
from pickle import dump
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
 
# load doc into memory
def load_doc(filename):
	# open the file as read only
	file = open(filename, 'r')
	# read all text
	text = file.read()
	# close the file
	file.close()
	return text

# load data into lists
def get_lines(filename):
    raw_text = load_doc(filename)
    lines = raw_text.split('\n')
    lines = lines[:-1]
    return lines

# save sequences to csv files
def save_csv(filename, sequences):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(sequences)

#def encode(filename):
#    # load
#    in_filename = filename
#    raw_text = load_doc(in_filename)
#    lines = raw_text.split('\n')
#    # integer encode sequences of characters
#    chars = sorted(list(set(raw_text)))
#    mapping = dict((c, i) for i, c in enumerate(chars))
#    sequences = list()
#    for line in lines:
#    	# integer encode line
#    	encoded_seq = [mapping[char] for char in line]
#    	# store
#    	sequences.append(encoded_seq)
#    ## vocabulary size
#    #vocab_size = len(mapping)
#    #print('Vocabulary Size: %d' % vocab_size)
#    # save sequences to csv file
#    name = filename+'_encoded.csv'
#    with open(name, "w", newline="") as f:
#        writer = csv.writer(f)
#        writer.writerows(sequences)
#
##encode('../../data/clear/cmds.txt')
##encode('../../data/obfuscated/cmds.txt')


# load data into lists
clear_lines = get_lines('../../data/clear/cmds.txt')
obf_lines   = get_lines('../../data/obfuscated/cmds.txt')
clear_size  = len(clear_lines) 
obf_size    = len(obf_lines)
lines = clear_lines + obf_lines

# integer encode sequences of characters from clear and obf data
## create code
raw_clear = load_doc('../../data/clear/cmds.txt')
raw_obf   = load_doc('../../data/obfuscated/cmds.txt')
raw_text  = raw_clear + raw_obf
chars = sorted(list(set(raw_text)))
mapping = dict((c, i) for i, c in enumerate(chars))
## encode
sequences = list()
for line in lines:
	# integer encode line
	encoded_seq = [mapping[char] for char in line]
	# store
	sequences.append(encoded_seq)
# vocabulary size
vocab_size = len(mapping)
print('Vocabulary Size: %d' % vocab_size)

# split sequences into two lists: clear and obfuscated
clear_seqs = sequences[:clear_size]
obf_seqs   = sequences[-obf_size:]

# save sequences to csv files
save_csv('clear.csv', clear_seqs)
save_csv('obf.csv', obf_seqs)
