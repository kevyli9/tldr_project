from __future__ import unicode_literals, print_function
import spacy
from spacy.lang.en import English
from spacy.language import Language
from newspaper import Article
import pandas as pd
import csv as csv



urls = ['https://www.reuters.com/article/us-eurozone-economy-pmi-idUSKBN2BG133', 'https://www.reuters.com/article/us-usa-fed-beigebook-idINKBN2C12NK', 'https://www.reuters.com/article/us-health-coronavirus-usa-airlines-idUSKBN2BE1L3']
input = []
input_paragraph = []
pos_ctrl = []
neg_ctrl = []
size = 0


for url in urls:
    
    pos_ctrl.append('Please click on this sentence.')
    neg_ctrl.append('Please do NOT click on this sentence.')
    
    article = Article(url)
    article.download()
    article.parse()
    raw_text = article.text
 
    
    #Code adapted from https://stackoverflow.com/questions/46290313/how-to-break-up-document-by-sentences-with-with-spacy       
    nlp = English()
    nlp.add_pipe('sentencizer') # updated
    doc = nlp(raw_text)
    sentences = [sent.text.strip() for sent in doc.sents]
    
    
    
    temp_sentence = [url]
    for sentence in sentences:
        sentence_split = sentence.split('\n')
        for sent in sentence_split:
                if (sent != ''):
                    temp_sentence.append(sent)
    
    sentences = temp_sentence
    if (len(sentences) > size):
        size = len(sentences) 
    
    first = [False, False, False]
    paragraph = ''
    i = 1
        
    while (i < size):
        #print(i)
        if (i == 2 and (not first[0])):
            paragraph = paragraph + pos_ctrl[0] + '|'
            i -= 1
            first[0] = True
        elif (i == 5 and (not first[1])):
            paragraph = paragraph + neg_ctrl[0] + '|'
            i -= 1
            first[1] = True
        elif (i == 9 and (not first[2])):
            paragraph = paragraph + pos_ctrl[0] + '|'
            i -= 1
            first[2] = True
        elif (i >= len(sentences)):
            paragraph = paragraph + '*|'
        else:
            paragraph = paragraph + sentences[i] + '|' 
        i += 1
    
    
    paragraphs = (url, paragraph)
    
    input.append(tuple(sentences))
    input_paragraph.append(paragraphs)

columns = ['url'] 

for i in range(1, size):
    if (i < 10):
        columns.append('sentence_0' + str(i))
    else:
        columns.append('sentence_' + str(i))

    
input = pd.DataFrame(input)
input_paragraph = pd.DataFrame(input_paragraph)
input.columns = columns
input_paragraph.columns = ['url', 'article']
input.insert(2, 'pos_qual_ctrl1', pos_ctrl)
input.insert(5, 'neg_qual_ctrl', neg_ctrl)
input.insert(9, 'pos_qual_ctrl2', pos_ctrl)
input.fillna('*', inplace=True)

input.to_csv('input.csv', index = False, quoting = csv.QUOTE_NONNUMERIC)
input_paragraph.to_csv('input_paragraph.csv', index = False)
