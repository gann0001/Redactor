#!/usr/bin/python
# coding=utf-8
# ^^ because https://www.python.org/dev/peps/pep-0263/

from __future__ import division

import codecs
import subprocess
import json
import os
import nltk
from nltk.tag import StanfordNERTagger
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk import ne_chunk
import sklearn
import itertools
from sklearn.feature_extraction.text import CountVectorizer
from itertools import chain
import nltk, re, pprint
from nltk import word_tokenize
from nltk.corpus import wordnet
from bs4 import BeautifulSoup as BS
# Usage: PYTHONIOENCODING=UTF-8 python process-data.py > output.txt
import glob
import sys
import re
#all the text files in same location and otherfiles in different location


def concept(text):
	dates_found = []
	concept_found = []
	length = len(sys.argv)
	for i in range(length):
		if(sys.argv[i] == '--concept'):
			concept = sys.argv[i+1]
			sents = nltk.sent_tokenize(text)
			concept = wordnet.synsets(concept)
			concept_synonyms = list(set(chain.from_iterable([word.lemma_names() for word in concept])))
			for sent in sents:
				if any(each.lower() in sent.lower() for each in concept_synonyms):
					concept_found.append(sent)
	return concept_found
#ADDRESS
def address(text):
	text = text.split("\n")
	add_found = []
	for each in text:
		regex = re.compile("\d{1,4}[\w]?[\s]+(?:[A-Za-z]*[\s,\]+)+(?:[[a-zA-Z]*)[\s,\\\.]+(?:\d{5}(?:\-?\d{1,4})?)?", re.IGNORECASE)
		found = regex.findall(each)
		add_found.extend(found)
	return add_found

#MALE FEMALE HIM HER HIMSELF
def genders(text):
	redact_genders = []
	gender = ['male','female','himself','herself','him','her','she','he']
	for each in gender:
		r = re.findall('\\b'+each+'\\b',text, re.IGNORECASE)
		redact_genders.extend(r)
		s = '#'
		text = re.sub('\\b'+each+'\\b', s*len(each), text, flags=re.IGNORECASE)
	return text,redact_genders
#Phone numbers code
def phones(text):
	text_phone = []
	text = text.split('\n')
	for each in text:
		regex = re.compile(r'''((\+\d{1,2})?  (\s|-|\.)? (\(?\d{3}\)?)(\s|-|\.)? (\(?\d{3}\(?) (\s|-|\.)? (\d{4}) (\s*(ext|x\.?|ext.|extension|Extension)?\s*(\d{2,5}))? )''', re.IGNORECASE|re.VERBOSE|re.MULTILINE)
		found = regex.findall(each)
		found = [a[0] for a in found if len(a) > 1]
		text_phone.extend(found)
	return text_phone
def dates(text):
#Extract dates from text files
	text = text.split('\n')
	dates_found = []
	numbers = "(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand)"
	day = "(monday|tuesday|wednesday|thursday|friday|saturday|sunday)"
	month = "(jan|feb|march|apr|may|june|july|aug|sept|oct|november|december)"
	dmy = "(year|day|week|month)"
	exp1 = "(today|yesterday|tomorrow|tonight|tonite)"
	exp2 = "(before|after|earlier|later|ago|back)"
	exp3 = "(this|next|last)"
	exp4 = "(minute|second|hour|hr|min|sec)"
	stddate = "\d+[/-]\d+[/-]\d{2,4}"
	year = "(\d{4})"
	regxp1 = "((\d+|(" + numbers + "[-\s]?)+) " + dmy + "s? " + exp2 + ")"
	regxp2 = "(" + exp3 + " (" + dmy + "|" + day + "|" + month + "))"
	regxp3 = "((\d+|(" + numbers + "[-\s]?)+) " + exp4 + "s? " + exp2 + ")"
	regxp4 = "(" + month + '\w*' ")"
	regxp5 = "(" + day + ")"
	reg1 = re.compile(regxp1, re.IGNORECASE)
	reg2 = re.compile(regxp2, re.IGNORECASE)
	reg3 = re.compile(exp1, re.IGNORECASE)
	reg4 = re.compile(stddate)
	reg5 = re.compile(year)
	reg6 = re.compile(regxp3, re.IGNORECASE)
	reg7 = re.compile(regxp4, re.IGNORECASE)
	reg8 = re.compile(regxp5, re.IGNORECASE)

    # re.findall() finds all the substring matches, keep only the full
    # matching string. Captures expressions such as 'number of days' ago, etc.
	for stext in text:
		found = reg1.findall(stext)
		found = [a[0] for a in found if len(a) > 1]
		dates_found.extend(found)

    #This year last year kind of words
		found1 = reg2.findall(stext)
		found1 = [a[0] for a in found1 if len(a) > 1]
		dates_found.extend(found1)

    #today yesterday tomorrow kind of words
		found2 = reg3.findall(stext)
		dates_found.extend(found2)
    #standard date format stuff
		found3 = reg4.findall(stext)
		dates_found.extend(found3)
    #all years
		found4 = reg5.findall(stext)
		dates_found.extend(found4)
    #Five mins ago
		found5 = reg6.findall(stext)
		found5 = [a[0] for a in found5 if len(a) > 1]
		dates_found.extend(found5)
    #Months Jan Feb
		found6 = reg7.findall(stext)
		found6 = [a[0] for a in found6 if len(a) > 1]
		dates_found.extend(found6)
    #Monday Tuesday
		found7 = reg8.findall(stext)
		found7 = [a[0] for a in found7 if len(a) > 1]
		dates_found.extend(found7)
	dates_found = list(set(dates_found))
	dates_found.sort(key = lambda s: len(s), reverse = True)
	dates_found = list(filter(None, dates_found))
	#print(dates_found)
	return dates_found
# names and Places

def names(text):
	entity_names= {}
	entity_names["person"] = []
	name = []
	for sent in sent_tokenize(text):
		for chunk in nltk.ne_chunk(nltk.pos_tag(word_tokenize(sent))):
			if hasattr(chunk, 'label') and chunk.label() == 'PERSON':
				name.append(' '.join(c[0] for c in chunk.leaves()))
					#name.append(' '.join([child[0] for child in each]))
	name = list(set(name))
	for each in name:
		for each1 in re.finditer(each,text):
			entity_names["person"].append((each,each1.start(),each1.end()))
	return entity_names

def places(text):
	tokenized_sent = nltk.word_tokenize(text)
	st = StanfordNERTagger('stanford-ner-2016-10-31/classifiers/english.all.3class.distsim.crf.ser.gz','stanford-ner-2016-10-31/stanford-ner.jar',encoding = 'utf-8')
	classified_text = st.tag(tokenized_sent)
	entity_places= {}
	entity_places["location"] = []
	place = []
	grammar = "LOCATION: {<LOCATION>*<LOCATION>}"
	cp = nltk.RegexpParser(grammar)
	result = cp.parse(classified_text)
	for each in result:
		if hasattr(each, 'label') and each.label:
			if each.label() == 'LOCATION':
				place.append(' '.join([child[0] for child in each]))
	place = list(set(place))
	for each in place:
		for each1 in re.finditer(each,text):
			entity_places["location"].append((each,each1.start(),each1.end()))
	return entity_places
def replace_concept(text, redact_concept):
	for each in redact_concept:
		s = '@'
		text = text.replace(each,s*len(each))
	return text

def replace_address(text, redact_address):
	for each in redact_address:
		s = '+'
		text = text.replace(each,s*len(each))
		#text = re.sub('\\b'+each+'\\b', '$$$$$$$$', text, flags=re.IGNORECASE)
	
	return text

def replace_dates(text, redact_dates):
	for each in redact_dates:
		s = '&'
		text = text.replace(each, s*len(each))
	return text 
def replace_phones(text, redact_phones):
	for each in redact_phones:
		s = '$'
		text = text.replace(each, s*len(each))
	return text
def replace_names(text, redact_names):
	for key in redact_names.keys():
		for each in redact_names[key]:
			s = '█'
			text= text.replace(each[0],s*len(each[0]))

	return text

def replace_places(text, redact_places):
	for key in redact_places.keys():
                for each in redact_places[key]:
                        s = '*'
                        text= text.replace(each[0],s*len(text[each[1]:each[2]]))
	return text
def variable():
	var_names, var_places, var_dates, var_phones, var_address, var_concept, var_genders = (False,)*7
	for each in sys.argv[0:]:
		if(each == '--names'):
			var_names = True
		elif(each == '--places'):
			var_places = True
		elif(each == '--dates'):
			var_dates = True
		elif(each == '--phones'):
			var_phones = True
		elif(each == '--addresses'):
			var_address = True
		elif(each == '--concept'):
			var_concept = True
		elif(each == '--genders'):
			var_genders = True
	return (var_names, var_places, var_dates, var_phones, var_address, var_concept, var_genders)

def main():
	length = len(sys.argv)
	for i in range(length):
		if (sys.argv[i] == '--output'):
			dname  = sys.argv[i+1]
			cmd = 'mkdir ' + dname.strip('/')
			sub = subprocess.Popen(cmd, executable = '/bin/bash', shell = True)

	for i in range(length):
		if(sys.argv[i] == '--input'):
			if(sys.argv[i+1] == '*.html'):
				htmlfiles = glob.glob(sys.argv[i+1], recursive=True)
				count1 = 1
				c = 1
				count3 = 1
				for each in htmlfiles:
					redact_names = {}
					redact_places = {}
					redact_concept = []
					redact_dates = []
					redact_address = []
					redact_phones = []
					redact_gender = []
					text = open(each)
					text = text.read()
					soup = BS(text,"html.parser")
					for script in soup(["script", "style"]):
						script.extract()
					text = soup.get_text()
					lines = (line.strip() for line in text.splitlines())
					lines = (phrase.strip() for line in lines for phrase in line.split("  "))
					text = '\n'.join(line for line in lines if line)
					redact_names = names(text)
					redact_places = places(text)
					redact_concept = concept(text)
					redact_dates = dates(text)
					redact_address = address(text)
					redact_phones = phones(text)
					var_names, var_places, var_dates, var_phones, var_address, var_concept, var_genders = variable()
					if(var_concept == True):
						text = replace_concept(text, redact_concept)
						var_concept = False
					if(var_address == True):
						text = replace_address(text, redact_address)
						var_address = False
					if(var_phones == True):
						text = replace_phones(text, redact_phones)
						var_phones = False
					if(var_dates == True):
						text = replace_dates(text, redact_dates)
						var_dates = False
					if(var_names == True):
						text = replace_names(text, redact_names)
						var_names = False
					if(var_places == True):
						text = replace_places(text, redact_places)
						var_places = False
					if(var_genders == True):
						text,redact_genders = genders(text)
						var_genders = False
					pdf_htfile = open(dname+"temphtml.txt", "w")
					pdf_htfile.write(text)
					cmd1 = "cupsfilter "+dname+"temphtml.txt > " + dname + "htmoutput" + str(c) + ".pdf"
					command = subprocess.Popen(cmd1, stdout=subprocess.PIPE, stderr=subprocess.PIPE,executable = '/bin/bash',shell = True)
					pdf_htfile.write(text)
					#count1 = count1+1
					c = c+1
					for i in range(length):
						if (sys.argv[i] == '--stats'):
							if(sys.argv[i+1] == 'stdout'):
								var_names, var_places, var_dates, var_phones, var_address, var_concept, var_genders = variable()
								if(var_concept == True):
									print("\n \n ------------------------- Concepts Redacted Below are the details. \n In Concept given in the command line arguments It will look for all the words related to given concept -Example prison- i.e. synonyms. Sentence which containing the word or related words -synonyms-, that whole sentences will be redacted. \n The sentence which related to given concept is \t"+ str(redact_concept)+ "\n Total number of sentences related to concept ::\t"+str(len(redact_concept)))
								if(var_address == True):
									print("\n ------------------------- Addresses Redacted Below are the details. \n The regular expression will look for the addresses in the given file and all the addresses in the files will be replaced:: \n The addresses are\t "+str(redact_address) + "\n Total count of addresses are \t "+ str(len(redact_address)))
								if(var_dates == True):
									print("\n ------------------------- Dates Redacted Below are the details. \n The regular expression will look for the all types of dates in the given file. The addresses are \t"+str(redact_dates)+"\nTotal no of items which are related to the dates \t"+str(len(redact_dates)))
								if(var_phones == True):
									print("\n ------------------------- Phone Numbers Redacted Below are the details. \n The regular expression will look for the all types of phone numbers in the given file and all the types of phone numbers in the file will be replaced. \n The phone numbers are\t"+str(redact_phones)+"\n The total count of phone numbers are \t"+str(len(redact_phones)))
								if(var_names == True):
									print("n ------------------------- Names Redacted Below are the details. \n All the names are redacted. In order to detect all the names stanford ner is used. \n The details of the names replaced are \t"+str(redact_names)+"\n The number of names replaced are\t"+ str([len(redact_names[key]) for key in redact_names.keys()]))
								if(var_places == True):
									print("\n ------------------------- Places Redacted Below are the details. \n All the locations are redacted. In order to detect all the locations stanford NER is used. \n The details of places replaced are \t "+str(redact_places)+"\n The Number of places replaed are\t"+ str([len(redact_places[key]) for key in redact_places.keys()]))
								if(var_genders == True):
									print("\n ------------------------- Genders Redacted Below are the details. \n It look for the gender category like Male Female and it hides the information. \n The details of genders replaced are \t " +str(redact_genders)+ "\n The no of genders replaced are \t"+str(len(redact_genders)))
								print("---------------------------------------------------------------------------------------------------------------------------------")
							else:
								var_names, var_places, var_dates, var_phones, var_address, var_concept, var_genders = variable()
								if(var_names == True):
									statfile = open(dname+"stathtm"+str(count3)+".log", "w")
									statfile.write("\n ------------------------- Names Redacted Below are the details. \n All the names are redacted. In order to detect all the names stanford ner is used. \n The details of the names replaced are \t"+str(redact_names)+"\n The number of names replaced are\t"+ str([len(redact_names[key]) for key in redact_names.keys()]))
								if(var_places == True):
									statfile = open(dname+"stathtm"+str(count3)+".log", "a")
									statfile.write("\n ------------------------- Places Redacted Below are the details. \n All the locations are redacted. In order to detect all the locations stanford NER is used. \n The details of places replaced are \t "+str(redact_places)+"\n The Number of places replaed are\t"+ str([len(redact_places[key]) for key in redact_places.keys()]))
								if(var_concept == True):
									statfile = open(dname+"stathtm"+str(count3)+".log", "a")
									statfile.write("\n \n ------------------------- Concepts Redacted Below are the details. \n In Concept given in the command line arguments It will look for all the words related to given concept -Example prison- i.e. synonyms. Sentence which containing the word or related words -synonyms-, that whole sentences will be redacted. \n The sentence which related to given concept is \t"+ str(redact_concept)+ "\n Total number of sentences related to concept ::\t"+str(len(redact_concept)))
								if(var_address == True):
									statfile = open(dname+"stathtm"+str(count3)+".log", "a")
									statfile.write("\n ------------------------- Addresses Redacted Below are the details. \nThe regular expression will look for the addresses in the given file and all the addresses in the files will be replaced:: \n The addresses are\t "+str(redact_address) + "\n Total count of addresses are \t "+ str(len(redact_address)))
								if(var_dates == True):
									statfile = open(dname+"stathtm"+str(count3)+".log", "a")
									statfile.write("\n ------------------------- Dates Redacted Below are the details. \n The regular expression will look for the all types of dates in the given file. The addresses are \t"+str(redact_dates)+"\nTotal no of items which are related to the dates \t"+str(len(redact_dates)))
								if(var_phones == True):
									statfile = open(dname+"stathtm"+str(count3)+".log", "a")
									statfile.write("\n ------------------------- Phone Numbers Redacted Below are the details. \n The regular expression will look for the all types of phone numbers in the given file and all the types of phone numbers in the file will be replaced. \n The phone numbers are\t"+str(redact_phones)+"\n The total count of phone numbers are \t"+str(len(redact_phones)))
								if(var_genders == True):
									statfile = open(dname+"stathtm"+str(count3)+".log", "a")
									statfile.write("\n ------------------------- Genders Redacted Below are the details. \n It look for the gender category like Male Female and it hides the information. \n The details of genders replaced are \t " +str(redact_genders)+ "\n The no of genders replaced are \t"+str(len(redact_genders))+"\n")
							count3 +=1

							
			elif(sys.argv[i+1] == 'otherfiles/*.txt'):
				txtfiles = glob.glob(sys.argv[i+1], recursive=True)
				count2 = 1
				count1 = 1
				count4 = 1
				c1 = 1
				for each in txtfiles:
					redact_names = {}
					redact_places = {}
					redact_concept = []
					redact_dates = []
					redact_address = []
					redact_phones = []
					redact_gender = []
					text = open(each)
					text = text.read()
					redact_names = names(text)
					redact_places = places(text)
					redact_concept = concept(text)
					redact_dates = dates(text)
					redact_address = address(text)
					redact_phones = phones(text)
					var_names, var_places, var_dates, var_phones, var_address, var_concept, var_genders = variable()
					if(var_address == True):
						text = replace_address(text, redact_address)
						var_address = False
					if(var_concept == True):
						text = replace_concept(text, redact_concept)
						var_concept = False
					if(var_phones == True):
						text = replace_phones(text, redact_phones)
						var_phone = False
					if(var_dates == True):
						text = replace_dates(text, redact_dates)
						var_dates = False
					if(var_names == True):
						text = replace_names(text, redact_names)
						var_names = False
					if(var_places == True):
						text = replace_places(text, redact_places)
						var_places = False
					if(var_genders == True):
						text,redact_genders = genders(text)
						var_genders = False
					pdf_txtfile = open(dname+"temptxt.txt", "w")
					pdf_txtfile.write(text)
					pdf_txtfile.close()
					cmd1 = "cupsfilter "+dname+"temptxt.txt > " + dname + "textoutput" + str(c1) + ".pdf"
					subprocess.Popen(cmd1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable = '/bin/bash', shell = True)
					#sub_output = sub.stdout.read().decode('utf-8')
					count2 = count2+1
					count1 = count1+1
					c1 = c1+1
					for i in range(length):
						if (sys.argv[i] == '--stats'):
							if(sys.argv[i+1] == 'stdout'):
								var_names, var_places, var_dates, var_phones, var_address, var_concept, var_genders = variable()
								if(var_concept == True):
									print("\n \n ------------------------- Concepts Redacted Below are the details. \n In Concept given in the command line arguments It will look for all the words related to given concept -Example prison- i.e. synonyms. Sentence which containing the word or related words -synonyms-, that whole sentences will be redacted. \n The sentence which related to given concept is \t"+ str(redact_concept)+ "\n Total number of sentences related to concept ::\t"+str(len(redact_concept)))
								if(var_address == True):
									print("\n ------------------------- Addresses Redacted Below are the details. \n The regular expression will look for the addresses in the given file and all the addresses in the files will be replaced:: \n The addresses are\t "+str(redact_address) + "\n Total count of addresses are \t "+ str(len(redact_address)))
								if(var_dates == True):
									print("\n ------------------------- Dates Redacted Below are the details. \n The regular expression will look for the all types of dates in the given file. The addresses are \t"+str(redact_dates)+"\nTotal no of items which are related to the dates \t"+str(len(redact_dates)))
								if(var_phones == True):
									print("\n ------------------------- Phone Numbers Redacted Below are the details. \n The regular expression will look for the all types of phone numbers in the given file and all the types of phone numbers in the file will be replaced. \n The phone numbers are\t"+str(redact_phones)+"\n The total count of phone numbers are \t"+str(len(redact_phones)))
								if(var_names == True):
									print("n ------------------------- Names Redacted Below are the details. \n All the names are redacted. In order to detect all the names stanford ner is used. \n The details of the names replaced are \t"+str(redact_names)+"\n The number of names replaced are\t"+ str([len(redact_names[key]) for key in redact_names.keys()]))
								if(var_places == True):
									print("\n ------------------------- Places Redacted Below are the details. \n All the locations are redacted. In order to detect all the locations stanford NER is used. \n The details of places replaced are \t "+str(redact_places)+"\n The Number of places replaed are\t"+ str([len(redact_places[key]) for key in redact_places.keys()]))
								if(var_genders == True):
									print("\n ------------------------- Genders Redacted Below are the details. \n It look for the gender category like Male Female and it hides the information. \n The details of genders replaced are \t " +str(redact_genders)+ "\n The no of genders replaced are \t"+str(len(redact_genders)))
								print("---------------------------------------------------------------------------------------------------------------------------------")
							else:
								var_names, var_places, var_dates, var_phones, var_address, var_concept, var_genders = variable()
								if(var_names == True):
									statfile = open(dname+"stattxt"+str(count4)+".log", "w")
									statfile.write("\n ------------------------- Names Redacted Below are the details. \n All the names are redacted. In order to detect all the names stanford ner is used. \n The details of the names replaced are \t"+str(redact_names)+"\n The number of names replaced are\t"+ str([len(redact_names[key]) for key in redact_names.keys()]))
								if(var_places == True):
									statfile = open(dname+"stattxt"+str(count4)+".log", "a")
									statfile.write("\n ------------------------- Places Redacted Below are the details. \n All the locations are redacted. In order to detect all the locations stanford NER is used. \n The details of places replaced are \t "+str(redact_places)+"\n The Number of places replaed are\t"+ str([len(redact_places[key]) for key in redact_places.keys()]))
								if(var_concept == True):
									statfile = open(dname+"stattxt"+str(count4)+".log", "a")
									statfile.write("\n \n ------------------------- Concepts Redacted Below are the details. \n In Concept given in the command line arguments It will look for all the words related to given concept -Example prison- i.e. synonyms. Sentence which containing the word or related words -synonyms-, that whole sentences will be redacted. \n The sentence which related to given concept is \t"+ str(redact_concept)+ "\n Total number of sentences related to concept ::\t"+str(len(redact_concept)))
								if(var_address == True):
									statfile = open(dname+"stattxt"+str(count4)+".log", "a")
									statfile.write("\n ------------------------- Addresses Redacted Below are the details. \nThe regular expression will look for the addresses in the given file and all the addresses in the files will be replaced:: \n The addresses are\t "+str(redact_address) + "\n Total count of addresses are \t "+ str(len(redact_address)))
								if(var_dates == True):
									statfile = open(dname+"stattxt"+str(count4)+".log", "a")
									statfile.write("\n ------------------------- Dates Redacted Below are the details. \n The regular expression will look for the all types of dates in the given file. The addresses are \t"+str(redact_dates)+"\nTotal no of items which are related to the dates \t"+str(len(redact_dates)))
								if(var_phones == True):
									statfile = open(dname+"stattxt"+str(count4)+".log", "a")
									statfile.write("\n ------------------------- Phone Numbers Redacted Below are the details. \n The regular expression will look for the all types of phone numbers in the given file and all the types of phone numbers in the file will be replaced. \n The phone numbers are\t"+str(redact_phones)+"\n The total count of phone numbers are \t"+str(len(redact_phones)))
								if(var_genders == True):
									statfile = open(dname+"stattxt"+str(count4)+".log", "a")
									statfile.write("\n ------------------------- Genders Redacted Below are the details. \n It look for the gender category like Male Female and it hides the information. \n The details of genders replaced are \t " +str(redact_genders)+ "\n The no of genders replaced are \t"+str(len(redact_genders))+"\n")
								count4 = count4+1
			else:
				print("It Seems you have given either html or text file. Please give both and parse the data")
				
				
	
if __name__ == '__main__':
	main()
