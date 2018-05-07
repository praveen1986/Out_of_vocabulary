import gensim
import numpy as np
import os
import scipy

model=gensim.models.KeyedVectors.load_word2vec_format('./resources/GoogleNews-vectors-negative300.bin',binary=True)

import re
stoplist = set('for a of the and to in'.split())
stoplist.add('')
def parse_sentence(sentence):
    return [word for word in re.split(r'[;,\s,_,-]', sentence) if word not in stoplist]


def create_keywordvectors(concepts):
	collectvectors=dict()
	i=0
	for concept in concepts:
	    tokens=parse_sentence(concept)
	    vector=np.zeros(300)
	    foundone=False
	    for token in tokens:
	        if token in model.vocab.keys():
	            vector=vector + model.get_vector(token)
	            foundone=True
	    if foundone==True:
	        collectvectors[concept]=vector  
	   
	    i=i+1
	    
	    print 'processed: {} concepts'.format(i)

def load_synset_file(synset_file):

    pfile = open(synset_file, 'r')
    concepts = pfile.readlines()
    pfile.close()

    return [p.strip() for p in concepts]

def get_closest_topn_distance(q_vector,corpus,n):
    concept_list=corpus.keys()
    dist_list=[]
    for c in concept_list:
        dist_list.append(scipy.spatial.distance.cosine(corpus[c],q_vector))
    inds=np.argsort(dist_list)[0:n]
    
    return np.array(concept_list)[inds]

def similar_to_given_pos_neg(model,pos_entity1,corpus,n,neg_entity1=None):
    tokens=parse_sentence(pos_entity1)
    
    if neg_entity1 is not None:
        neg_tokens=parse_sentence(pos_entity1)
    else:
        neg_tokens=[]
    q_vector=np.zeros(300)
    foundone=False
    for token in tokens:
        if token in model.vocab.keys():
            q_vector=q_vector + model.get_vector(token)
            foundone=True
            
    for token in neg_tokens:
        if token in model.vocab.keys():
            q_vector=q_vector - model.get_vector(token)
            foundone=True   
    
    if foundone==True:
        return get_closest_topn_distance(q_vector,corpus,n)
    else: 
        return 'not in vocab'



synset_file='./resources/keywording_data-v4-2-22-12-2016-synset.txt'

try:
	concepts=load_synset_file(synset_file)
except Exception as e:
	raise




if os.path.exists('./resources/keywordvectors.npy'):
	keyword_dict=np.load('./resources/keywordvectors.npy').item()
else:
	create_keywordvectors(concepts)
	np.save('./resources/keywordvectors',collectvectors)


# f=open('./resources/oov.txt','r')
# temp = f.read().splitlines()

# q_oovs=[]
# for string in temp:
#     q_oovs.append(string.split()[0])

q_oovs=['true']


index=0
print similar_to_given_pos_neg(model,q_oovs[index],keyword_dict,200)
print q_oovs[index]







