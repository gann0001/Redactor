#!/usr/bin/python
# -*- coding: utf-8 -*-
import glob
import io
import os
import pdb
import sys
import nltk
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk import pos_tag
from nltk import ne_chunk
from nltk.tag import StanfordNERTagger
import sklearn
import itertools
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from itertools import chain
import nltk, re, pprint
from nltk import word_tokenize
from nltk.corpus import wordnet
from bs4 import BeautifulSoup as BS
from sklearn.preprocessing import LabelBinarizer
import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.neighbors import KNeighborsClassifier
from nltk.corpus import stopwords
stopwords = stopwords.words('english')
import nltk
from nltk.util import ngrams

def word_grams(words, n):
	s = []
	for ngram in ngrams(words, n):
		s.append(' '.join(str(i) for i in ngram))
	return s
def training():
	list_files = []
	allfiles = glob.glob('train/*.txt')
	for each in allfiles:
		with open(each, 'r') as f:
			data = f.read()
			list_files.append(data)
	return list_files
	
def entities(list_data):
	entity_names = []
	entity_vect = []
	entity_wordlen = []
	entity_sent_len = []
	entity_count = []
	entity_space = []
	entity_n = []
	entity_1gram = []
	entity_2gram = []
	entity_3gram = []
	entity_1word = []
	entity_tspace =[]
	i = 1
	for i in range(3):
		for each in list_data:
			for sent in sent_tokenize(each):
				for chunk in ne_chunk(pos_tag(word_tokenize(sent))):
					if hasattr(chunk, 'label') and chunk.label() == 'PERSON':
						names = ' '.join(c[0] for c in chunk.leaves())
						entity_n.append(names)
						entity_space.append(names.count(' '))
						entity_count.append(len(names))
						entity_tspace.append(len(names)-names.count(' '))
						x=nltk.word_tokenize(names)
						entity_wordlen.append(len(x))
						x = word_grams(names, 1)
						entity_1gram.append(len(x))
						y = word_grams(names, 2)
						entity_2gram.append(len(y))
						z = word_grams(names, 3)
						entity_3gram.append(len(z))
						entity_1word.append(len(x[0]))
	dict_vect = []
	for a,b,c,d,e,f,g,h,i in zip(entity_n,entity_count,entity_space,entity_tspace,entity_wordlen,entity_1gram,entity_2gram,entity_3gram,entity_1word):
		dict_names  = {}
		dict_names['name'] = a
		dict_names['length'] = b
		dict_names['space'] = c
		dict_names['tspace'] = d
		dict_names['wordlen'] = e
		dict_names['1gram'] = f
		dict_names['2gram'] = g
		dict_names['3gram'] = h
		dict_names['1word'] = i
		dict_vect.append(dict_names)
	return dict_vect, entity_n

def test(data):
	entity_names = []
	name = []
	reg = re.compile('\*+\s?\**\s?\*+')
	names = []
	entity_names = re.findall(reg,data)
	for sent in sent_tokenize(data):
		chunk = pos_tag(word_tokenize(sent))
		grammar = "Name: {<JJ>*<NN.?>*<NN.?>}"
		cp = nltk.RegexpParser(grammar)
		result = cp.parse(chunk)
		for each in result:
			if hasattr(each, 'label') and each.label:
				if each.label() == 'Name':
					name.append(' '.join([child[0] for child in each]))
	for each in name:
		if '**' in each:
			names.append(each)
	entity_vect = []
	entity_wordlen = []
	entity_sent_len = []
	entity_count = []
	entity_space = []
	entity_n = []
	entity_1gram = []
	entity_2gram = []
	entity_3gram = []
	entity_1word = []
	entity_tspace = []
	for each in entity_names:
		entity_n.append(each)
		entity_count.append(len(each))
		entity_space.append(each.count(' '))
		entity_tspace.append(len(each)-each.count(' '))
		x=nltk.word_tokenize(each)
		entity_wordlen.append(len(x))
		x = word_grams(each, 1)
		entity_1gram.append(len(x))
		y = word_grams(each, 2)
		entity_2gram.append(len(y))
		z = word_grams(each, 3)
		entity_3gram.append(len(z))
		entity_1word.append(len(x[0]))
	dict_vect = []
	for a,b,c,d,e,f,g,h,i in zip(entity_n,entity_count,entity_space,entity_tspace,entity_wordlen,entity_1gram,entity_2gram,entity_3gram,entity_1word):
		dict_names  = {}
		dict_names['name'] = a
		dict_names['length'] = b
		dict_names['space'] = c
		dict_names['tspace'] = d
		dict_names['wordlen'] = e
		dict_names['1gram'] = f
		dict_names['2gram'] = g
		dict_names['3gram'] = h
		dict_names['1word'] = i
		dict_vect.append(dict_names)
	return dict_vect, entity_n


def main():
	list_data = training()
	dict_vect, entity_names = entities(list_data)
	vec = DictVectorizer()
	transformer = TfidfTransformer()
	vectors = vec.fit_transform(dict_vect).toarray()
	#tfidf_vectors = transformer.fit_transform(vectors).toarray()
	
	clf = GaussianNB().fit(vectors, entity_names)
	ne = KNeighborsClassifier(n_neighbors=5).fit(vectors, entity_names)
	#clf = MultinomialNB().fit(tfidf_vectors, entity_names)
	#clf = BernoulliNB().fit(tfidf_vectors, entity_names)
	allfiles = glob.glob('test/*.txt')	
	for each in allfiles:
		with open(each, 'r') as f:
			data = f.read()
			dict_vectors, entity_n = test(data)
			vectors_pred = vec.transform(dict_vectors).toarray()
			#tfidf_vectors_pred = transformer.transform(vectors_pred).toarray()
			pred = clf.predict(vectors_pred)
			from sklearn.metrics import accuracy_score
			#print(accuracy_score(entity_names,clf.predict(vectors)))
			predict = ne.kneighbors(vectors_pred, n_neighbors= 5,return_distance=False)
			print("\n \nPredictions for the given file: \t"+each)
			print("\n GussianNB algorithm prediction: \t")
			for x,y in zip(entity_n,pred):
				print("\ninput word in the given file: \t"+x,"\n predicted word for the input: \t"+y)
			print("\n5 Nearest neighbors using k-nearest neighbors algorithm prediction: \n")
			for each,z in zip(predict,entity_n):
				print("The input word given in the file:\t"+z+"\n")
				for each1 in each:
					print(entity_names[each1])
				print("\n")


if __name__ == '__main__':
	main()

