# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 19:33:36 2024

@author: Marcel Tino
"""

import pandas as pd
from marcel_fse.inputs import SplitIndexedList
from marcel_fse.inputs import IndexedList
from .sif import SIF
from .usif import uSIF
import gensim.downloader as api
from nltk.tokenize import word_tokenize

def get_sentence_scores(df,model_name,custom_text):
    list1=df.values.tolist()
    
    s = SplitIndexedList(list1)
    
    list1=s.items
    
    list2=[]
    for elem in list1:
        for j in elem:
            list2.append(j)
            
    
    s=[word_tokenize(text) for text in list2]
    s = IndexedList(s)
    
    
    w2v_model=api.load(model_name)

    model = SIF(w2v_model, workers=1, lang_freq="en")
    model.train(s)
    model1=uSIF(w2v_model, workers=1, lang_freq="en")
    model1.train(s)
    
    #Sentence embedding using SIF
    sent=model.sv.similar_by_sentence(custom_text.split(), model=model, indexable=s.items)
    sent1=model.sv.similar_by_sentence(custom_text.split(), model=model, indexable=s.items)
    
    df1 = pd.DataFrame(sent, columns=['text', 'Row number', 'sentence embedding score using SIF'])
    df2 = pd.DataFrame(sent1, columns=['text', 'Row number', 'sentence embedding score using uSIF'])
    return df1,df2
