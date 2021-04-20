# -*- coding: utf-8 -*-
"""QC and Aggregation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MwkZLEKGl8t57ZfYQDFIdwN2LiHWP1zu
"""

import pandas as pd
import numpy as np

# adds columns to input csv to filter workers and returns new df with new columns
def add_filters(mturk_res):
  mturk_res = mturk_res.rename(columns={"Answer.deletion_mask_1" : "Answer.sentence_1", 
                                        "Answer.deletion_mask_2": "Answer.pos_qual_ctrl_1",
                                        "Answer.deletion_mask_3" : "Answer.sentence_2",
                                        "Answer.deletion_mask_4" : "Answer.sentence_3",
                                        "Answer.deletion_mask_5": "Answer.neg_qual_ctrl",
                                        "Answer.deletion_mask_6" : "Answer.sentence_4",
                                        "Answer.deletion_mask_7" : "Answer.sentence_5",
                                        "Answer.deletion_mask_8" : "Answer.sentence_6",
                                        "Answer.deletion_mask_9": "Answer.pos_qual_ctrl_2",
                                        "Answer.deletion_mask_10" : "Answer.sentence_7",
                                        "Answer.deletion_mask_11" : "Answer.sentence_8",
                                        "Answer.deletion_mask_12" : "Answer.sentence_9",
                                        "Answer.deletion_mask_13" : "Answer.sentence_10"})
  mturk_res['time_spent'] = mturk_res['WorkTimeInSeconds'].apply(lambda x : x >= 60)
  mturk_res['neg_qual_ctrl_correct'] = mturk_res['Answer.neg_qual_ctrl'].apply(lambda x : x == '{}')
  mturk_res['pos_qual_ctrl_correct'] = mturk_res.apply(lambda x: True
             if  (isinstance(x['Answer.pos_qual_ctrl_1'], int)) &
                 (isinstance(x['Answer.pos_qual_ctrl_2'], int)) 
                 else False, axis = 1)
  mturk_res['num_clicks'] = 0
  for index in mturk_res.index:
    count = 0
    for i in range(1, 11):
      ans = 'Answer.sentence_' + str(i)
      if mturk_res[ans][index] != '{}':
        count += 1
    mturk_res['num_clicks'][index] = count
  mturk_res['filtered'] = mturk_res.apply(lambda x: True
                                          if (x['time_spent'] & x['neg_qual_ctrl_correct'] 
                                              & x['pos_qual_ctrl_correct'] & (x['num_clicks'] >= 5))
                                          else False, axis = 1)
  return mturk_res

# returns df with bad workers filtered out
def get_qualified_workers(mturk_res):
  updated = add_filters(mturk_res)
  return updated[updated['filtered']]

# returns list of bad workers
def get_bad_workers(mturk_res):
  updated = add_filters(mturk_res)
  bad_workers = []
  for index in updated.index:
    if not updated['filtered'][index]:
      bad_workers.append(updated['WorkerId'][index])
  return bad_workers

# majority vote using only good workers
def majority_vote(article_HITs):
  label_list = []
  for i in range(1, 11):
    input_str = 'Input.sentence_' + str(i)
    answer_str = 'Answer.sentence_' + str(i)
    keep = 0
    remove = 0
    for index, row in article_HITs.iterrows():
      if row[answer_str] == '{}':
        keep += 1
      else: 
        remove += 1
    if keep > remove:
      label_list.append((row[input_str], "keep", keep))
    elif keep == remove:
      rand_num = np.random.random()
      if rand_num >= 0.5:
        label_list.append((row[input_str], "keep", keep))
      else: 
        label_list.append((row[input_str], "remove", keep))
    else:
      label_list.append((row[input_str], "remove", keep))
  return label_list

#AGGREGATION: aggregate the majority votes and send them to a new text file!
def vote_to_text(fileName, article_HITs):
  f = open(fileName, "w")
  for (index, row) in article_HITs.iterrows():
    if row['label'] == 'keep':
      f.write(row['sentence'] + " ")
  f.close()

def main():
    # Read in CVS result file with pandas
    mturk_res = pd.read_csv('sample_QC_input.csv')

    # get list of bad workers based on updated df
    bad_workers = get_bad_workers(mturk_res)

    # get df with bad workers filtered out
    filtered = get_qualified_workers(mturk_res)
    
    # count votes based on filtered workers
    HIT_ids = filtered['HITId'].unique()
    for id in HIT_ids:
      #MAJORITY VOTING
      article_HITs = filtered.loc[filtered['HITId'] == id]
      label_list = majority_vote(article_HITs)
      df = pd.DataFrame(label_list, columns=['sentence', 'label', 'keep_votes'])
      df.to_csv('output.csv', index = False)
      #AGGREGATION
      vote_to_text(id, df) 
      
if __name__ == '__main__':
    main()
