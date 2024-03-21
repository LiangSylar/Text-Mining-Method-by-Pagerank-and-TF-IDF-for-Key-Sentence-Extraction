# -*- coding: utf-8 -*-
"""ERG3020 Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AaF8qMPwp2LuQrTfuzN_o8w1kfASbtnK
"""

# Chenang Li 118010135
# Jialu Liang 118010164
!pip install -q wordcloud
import wordcloud

import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger') 

import pandas as pd
import matplotlib.pyplot as plt
import io
import unicodedata
import numpy as np
import re
import string
import math

file_name = ['1.txt','2.txt','3.txt','4.txt','5.txt']
file = []
for i in range(len(file_name)):
  file.append([])
  with open(file_name[i], encoding='utf-8') as file_obj:
    contents = file_obj.read()
    file[i]=(re.split('[.\n]',contents.rstrip()))
  for j in file[i]:
    if (len(j)<=2):
      file[i].remove(j)
# POS (Parts Of Speech) for: nouns, adjectives, verbs and adverbs
DI_POS_TYPES = {'NN':'n', 'JJ':'a', 'VB':'v', 'RB':'r'} 
POS_TYPES = list(DI_POS_TYPES.keys())

# Constraints on tokens
MIN_STR_LEN = 3
RE_VALID = '[a-zA-Z]'

# Get stopwords, stemmer and lemmatizer
stopwords = nltk.corpus.stopwords.words('english')
stemmer = nltk.stem.PorterStemmer()
lemmatizer = nltk.stem.WordNetLemmatizer()

# Remove accents function
def remove_accents(data):
  return ''.join(x for x in unicodedata.normalize('NFKD', data) if x in string.ascii_letters or x == " ")

# Process all quotes
def extract_text(num_file):
  li_tokens = []
  li_token_lists = []
  li_lem_strings = []
  for i,text in enumerate(file[num_file]):
    # Tokenize by sentence, then by lowercase word
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]

    # Process all tokens per quote
    li_tokens_quote = []
    li_tokens_quote_lem = []
    for token in tokens:
      # Remove accents
      t = remove_accents(token)

      # Remove punctuation
      t = str(t).translate(string.punctuation)
      li_tokens_quote.append(t)
      
      # Add token that represents "no lemmatization match"
      li_tokens_quote_lem.append("-") # this token will be removed if a lemmatization match is found below

      # Process each token
      if t not in stopwords:
        if re.search(RE_VALID, t):
          if len(t) >= MIN_STR_LEN:
            pos = nltk.pos_tag([t])[0][1][:2]
            pos2 = 'n'  # set default to noun
            if pos in DI_POS_TYPES:
              pos2 = DI_POS_TYPES[pos]
            
            stem = stemmer.stem(t)
            lem = lemmatizer.lemmatize(t, pos=pos2)  # lemmatize with the correct POS
            
            if pos in POS_TYPES:
              li_tokens.append((t, stem, lem, pos))

              # Remove the "-" token and append the lemmatization match
              li_tokens_quote_lem = li_tokens_quote_lem[:-1] 
              li_tokens_quote_lem.append(lem)

    # Build list of token lists from lemmatized tokens
    li_token_lists.append(li_tokens_quote)
    
    # Build list of strings from lemmatized tokens
    str_li_tokens_quote_lem = ' '.join(li_tokens_quote_lem)
    li_lem_strings.append(str_li_tokens_quote_lem.split(" "))
  return(li_lem_strings, li_token_lists)

text_sentences=[]
token_list=[]
for i in range(len(file_name)):
  text,token=extract_text(i)
  text_sentences.append(text)
  token_list.append(token)

for sents in text_sentences[3]:
  for wrds in sents:
    print(wrds, end=' ')
  print('')
print(file[3][19])

lib_wrds=[]
num_sentences=0
for txts in text_sentences:
  num_sentences=num_sentences+len(txts)
  for sents in txts:
    for wrds in sents:
      if(wrds!='-' and wrds!=''):
        lib_wrds.append(wrds)
lib_wrds=np.unique(lib_wrds)
lib_wrds=sorted(lib_wrds)
total_occur = {'-': 0, '': 0}
for words in lib_wrds:
  for txts in text_sentences:
    for sents in txts:
      if(words in sents):
        if(words in total_occur.keys()):
          total_occur[words] = total_occur[words]+1
        else:
          total_occur[words] = 1

#print (sorted(total_occur.items(), key=lambda total_occur: total_occur[0]))
idf = {'-': 0, '': 0}
for kys in total_occur.keys():
  idf[kys]=total_occur[kys]/(num_sentences+1)

def cal_tf(num_file):
  res=[]
  for sents in text_sentences[num_file]:
    tmp_tf=[0]*len(lib_wrds)
    mx_cnt = {'-': 0, '': 0}
    for words in sents:
      if(words!='-' and words!=''):
        for j in range(len(lib_wrds)):
          if(words==lib_wrds[j]):
            tmp_tf[j]=tmp_tf[j]+1
            break;
        if(words in mx_cnt.keys()):
          mx_cnt[words]=mx_cnt[words]+1;
        else: mx_cnt[words]=1;
    mx=0
    for kys in mx_cnt.keys():
      mx=max(mx,mx_cnt[kys])
    for j in range(len(lib_wrds)):
      #tmp_tf[j]=tmp_tf[j]/len(sents)idf
      if(mx!=0):
        tmp_tf[j]=tmp_tf[j]/mx*idf[lib_wrds[j]]
    res.append(tmp_tf)
  return(res)

num_text=0 # Change this number to run algorithm on different articles
crit=0.01
top_k=3
#num_div=3  # k^2/num_div edges will be selected
vect=cal_tf(num_text)
m_vect=np.matrix(vect)
sent_map = np.zeros([len(vect),len(vect)])
#cos_all=[]
#non_zero_cos=0
for i in range(len(vect)):
  for j in range(len(vect)):
    u1=np.array(m_vect[i])
    u2=np.array(m_vect[j])
    cs=np.sum(u1*u2)/(math.sqrt(np.sum(np.square(u1)))*math.sqrt(np.sum(np.square(u2))))
    #print(cs,end=" ")
    if(i!=j):
      if(abs(cs)>crit):
        #non_zero_cos=non_zero_cos+1
        #cos_all.append(cs)
        sent_map[i][j]=1
        sent_map[j][i]=1
  #print('')
# cos_all=np.array(cos_all)
# boundry=int(min(non_zero_cos, m_vect.shape[0]*m_vect.shape[0]/num_div)) # How many edges 
# print(non_zero_cos > m_vect.shape[0]*m_vect.shape[0]/num_div)
# min_cos_crt=sorted(cos_all[np.argpartition(cos_all,-boundry)[-boundry:]])[0]
# #print(min_cos_crt)
# for i in range(len(vect)):
#   for j in range(len(vect)):
#     if(sent_map[i][j]>=min_cos_crt):
#       sent_map[i][j]=1
#       sent_map[j][i]=1
#     else:
#       sent_map[i][j]=0
#       sent_map[j][i]=0
non_empty_nodes=np.apply_along_axis(sum, 0, sent_map)>0
cnt_graph=np.matrix(sent_map)[non_empty_nodes]
cnt_graph=cnt_graph[:,non_empty_nodes]
#print(len(sent_map),len(file[num_text]))
markov_graph=cnt_graph
for i in range(cnt_graph.shape[0]):
  markov_graph[:,i]=markov_graph[:,i]/np.sum(markov_graph[:,i])
init=np.ones(cnt_graph.shape[0])/cnt_graph.shape[0]
init=np.matrix(init).T
#markov_graph.shape
for i in range(100):
  init=np.matmul(markov_graph,init)
flg=-1
res_importance=np.zeros(len(non_empty_nodes))
for i in range(len(non_empty_nodes)):
  if(non_empty_nodes[i]!=0):
    flg=flg+1
    res_importance[i]=init[flg]
print(res_importance)
# flg=-1
# for sents in text_sentences[num_text]:
#   flg=flg+1
#   if(non_empty_nodes[flg]==0): continue
#   for wrds in sents:
#     print(wrds, end=' ')
#   print('')
top_imp=sorted(res_importance[np.argpartition(res_importance,-top_k)[-top_k:]],reverse=True)
done=np.zeros(len(res_importance))
for i in range(len(top_imp)):
  for j in range(len(res_importance)):
    if(res_importance[j]==top_imp[i] and done[j]==0):
      done[j]=1
      print(i+1,":",file[num_text][j])
      break
print(top_imp)