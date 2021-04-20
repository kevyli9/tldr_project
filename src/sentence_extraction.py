from __future__ import unicode_literals, print_function
import spacy
from spacy.lang.en import English
from spacy.language import Language
from newspaper import Article
import pandas as pd



urls = ['https://www.reuters.com/article/us-usa-fed-beigebook-idINKBN2C12NK', 'https://www.cnn.com/2021/04/14/weather/climate-change-india-monsoon-agriculture-heavy-rain/index.html', 'https://www.cnbc.com/2021/04/15/jeff-bezos-releases-final-letter-to-amazon-shareholders.html']
input = []
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
    sentences = [url] + [sent.text.strip() for sent in doc.sents]
    
    if (len(sentences) > size):
        size = len(sentences)  
    
    input.append(tuple(sentences))

columns = ['url']   
for i in range(1, size):
    columns.append('Sentence' + str(i))

    
input = pd.DataFrame(input)
input.columns = columns
input.insert(2, 'pos_qual_ctrl1', pos_ctrl)
input.insert(5, 'neg_qual_ctrl', neg_ctrl)
input.insert(9, 'pos_qual_ctrl2', pos_ctrl)
input.fillna('*', inplace=True)

input.to_csv('input.csv', index = False)