import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical

def create_token(lines):
	token = Tokenizer()
	token.fit_on_texts(lines)
	return token

"""
Encode the input and output seq to integers and pad to maximum phrase length
Will use word embeddings for input sequence and one hot encode the output seq
"""
def encode_sequences(token, len, lines):
	# integer encode sequences
	X = token.texts_to_sequences(lines)
	# pad sequences with 0 values
	X = pad_sequences(X, maxlen=len, padding='post')
	return X

"""
One hot encode target sequence. The output sequence needs to be
one-hot encoded. This is because the model will predict the probability
of each word in the vocabulary as output.
"""
def encode_output(sequences, vocab_size):
	ylist = list()
	for sequence in sequences:
		encoded = to_categorical(sequence, num_classes=vocab_size)
		ylist.append(encoded)
	y = np.array(ylist)
	y = y.reshape(sequences.shape[0], sequences.shape[1], vocab_size)
	return y

"""
Find the length of the longest sequence in the list of phrases in lines
"""
def max_len(lines):
	return max(len(line.split()) for line in lines)

# map an integer to a word
def word_for_id(integer, tokenizer):
    for word, index in tokenizer.word_index.items():
        if index == integer:
            return word
    return None

def prepare_token(dataset):
	# prepare english token
	eng_token = create_token(dataset[:, 0])
	eng_len = max_len(dataset[:, 0])
	print('English Max Length: %d' % (eng_len))

	# prepare translated language token
	trn_token = create_token(dataset[:, 1])
	trn_len = max_len(dataset[:, 1])
	print('TRANSLATED Max Length: %d' % (trn_len))

	return eng_token, eng_len, trn_token, trn_len
