from __future__ import unicode_literals, print_function
import spacy
from spacy.lang.en import English
from spacy.language import Language
import pandas as pd
import re

# Get filename from input
filename = 'survey_results.csv'
data_file = 'analysis.csv'

def counter(arg_df):
    mturk_results = arg_df.get("Answer.taskAnswers")
    results = [0,0,0]

    # Loops through Mturk output
    for choice in mturk_results:
        curr_sent = choice
    
        first_paragraph = choice.replace('[{"first_paragraph":{"first_paragraph":', '')
        ind = first_paragraph.find('}')
        curr_sent = first_paragraph[ind:]
        first_paragraph = first_paragraph[:ind]
    
        our_summary = curr_sent.replace('},"our_summary":{"our_summary":', '')
        ind = our_summary.find('}')
        curr_sent = our_summary[ind:]
        our_summary = our_summary[:ind]
    
        smmry_summary = curr_sent.replace('},"smmry_summary":{"smmry_summary":', '')
        ind = smmry_summary.find('}')
        smmry_summary = smmry_summary[:ind]
    
        if first_paragraph == 'true':
            results[0] += 1
        elif our_summary == 'true':
            results[1] += 1
        elif smmry_summary == 'true':
            results[2] += 1
        
    return results


# Reads the .csv input and converts into dataframe
df = pd.read_csv(filename)
daf = pd.read_csv(data_file)

length = {}
tup_len = {}
for iter, row in daf.iterrows():
    
    #Code adapted from https://stackoverflow.com/questions/46290313/how-to-break-up-document-by-sentences-with-with-spacy       
    nlp = English()
    nlp.add_pipe('sentencizer') # updated
    doc = nlp(row['tldr_summary'])
    sentences = [sent.text.strip() for sent in doc.sents]
    length[row['url']] = len(sentences)

for iter, row in df.iterrows():
    if int(row['WorkTimeInSeconds']) < 120:
        df.drop(labels = [iter], axis = 0, inplace = True)
        


# Stores the results outputted by Mturk
articles = df.groupby('Input.url')
for url, article in articles:
    counts = counter(article)
    percent_of_votes = counts[1]/(counts[0] + counts[1] + counts[2])
    sentence_length = length[url]
    tup_len[url] = (sentence_length, percent_of_votes)
    
    
    

# Creates a results column in the dataframe 
data = []
sent_len = []
percent_app = []

for key, value in tup_len.items():
    data.append((key, value[0], value[1]))
    sent_len.append(value[0])
    percent_app.append(value[1])
    
#Code from: https://www.learnpythonwithrune.org/how-to-export-pandas-dataframe-to-excel-and-create-a-trendline-graph-of-scatter-plot/
# Create a Pandas Excel writer using XlsxWriter
excel_file = 'survey_results_scatter.xlsx'
sheet_name = 'Length vs Approval'
writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')
data = pd.DataFrame(data)
data.to_excel(writer, sheet_name=sheet_name)

# Access the XlsxWriter workbook and worksheet objects from the dataframe.
workbook = writer.book
worksheet = writer.sheets[sheet_name]

# Create a scatter chart object.
chart = workbook.add_chart({'type': 'scatter'})

# Get the number of rows and column index

max_row = 10
col_x = 2
col_y = 3

# Create the scatter plot, use a trendline to fit it
chart.add_series({
    'name':       "Plot: Percent Approval vs Length",
    'categories': [sheet_name, 1, col_x, max_row, col_x],
    'values':     [sheet_name, 1, col_y, max_row, col_y],
    'marker':     {'type': 'circle', 'size': 4},
    'trendline': {'type': 'polynomial', 'order': 2},
})

# Set name on axis
chart.set_x_axis({'name': 'Length of Summary (# of sentences)'})
chart.set_y_axis({'name': 'Percent Preferred',
                  'major_gridlines': {'visible': False}})

# Insert the chart into the worksheet in field D2
worksheet.insert_chart('D2', chart)

# Close and save the Excel file
writer.save()

#End of Code from https://www.learnpythonwithrune.org/how-to-export-pandas-dataframe-to-excel-and-create-a-trendline-graph-of-scatter-plot/
