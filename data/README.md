**Data**  
Raw data input ('HIT_input.csv'):
* This input is the CSV we upload to MTurk when releasing our HIT. The file contains the individual sentences of articles.
* Total number of columns: 3 + number of sentences in the article with the most sentences (3 attention checks + sentences in the articles)
* Column 0: article url
* Column 1: first sentence
* Column 2: pos_qual_ctrl1 ('Please click on this sentence.')
* Column 5: neg_qual_ctrl ('Please do NOT click on this sentence.')
* Column 9: pos_qual_ctrl2 ('Please click on this sentence.')
* Other columns: actual sentences in the articles with the order preserved
* For articles that don't have the maximum number of sentences, the extra input columns are filled with an asterisk ('*')
  
Format of input for QC module ('sample_QC_input.csv'):  
* Our QC module will directly take as input the HIT results CSV from MTurk. We make use of the 'WorkTimeInSeconds' to confirm that the worker spent at least 1 minute on their HIT, else their vote is not counted.
* The columns titled 'Input.pos_qual_ctrl1' and 'Input.pos_qual_ctrl2' contain our 'positive' attention check sentences (i.e. 'Please click on this sentence'). The column titled 'Input.neg_qual_ctrl' contains our 'negative' attention check sentence (i.e. 'Please do NOT click on this sentence.')
* The columns in the 'Input.sentence_x' format represent all of the actual sentences in the text of the article.
* The answer column names are in the 'Answer.deletion_mask_x' format for x from 1 to n+3, where n is the number of sentences in the article with the most number of sentences and 3 represents the 3 quality control sentences. MTurk sorts these columns alphabetically (meaning 'Answer.deletion_mask_10' comes before 'Answer.deletion_mask_2'). However, the order of the input columns is the correct order. For example, the **second** input column is name 'Input.pos_qual_ctrl1' which will correspond to the column  'Answer.deletion_mask_**2**'. We account for this ordering in our QC module code.
* Answers in the answer columns take 1 of 2 formats. First, '{}' means the worker did not click on the sentence (i.e. the worker wants to keep that sentence). Second, a value that is not '{}' (typically an 11-12 digit binary number) means the worker clicked on that sentence (i.e. the worker wants to remove that sentence).
* We do not make use of other columns in the MTurk results CSV.

QC module output ('sample_QC_output.csv'):
* CSV with 3 columns: 'sentence', 'label', and 'keep_votes'
* 'sentence' contains all of the sentences in the original text, in the same order
* 'label' contains the label for each sentence, determined by a majority vote of qualified workers. Qualified meaning the worker 1) spent at least a minute on the HIT 2) correctly clicked/didn't click each of the quality control sentencs 3) clicked at least 5 non-quality control sentences. If most qualified workers clicked on the sentence, it was labeled 'remove' else 'keep'. 
* Ties were broken by randomly labeling the sentence 'remove' or 'keep'. As such, given that there were only 2 qualified workers from 'sample_QC_input.csv', sentences with disagreement (1 'remove' vote and 1 'keep' vote) could either have been labeled 'remove' or 'keep'. 
* 'keep_votes' contains the number of votes for 'keep' a sentence received

Aggregation module input ('sample_QC_output.csv'):
* The aggregation module takes as input a list of tuples in the format (sentence, label, # of 'keep' votes) that is returned from the QC module (our code for the aggregation module is in the same notebook as the QC code). In this repo, we represent the list of tuples as a 3-column CSV, which is the same as 'sample_QC_output.csv'

Aggregation module output ('sample_agg_output.txt'):
* This is a .txt file that contains the concatentation of the sentences labeled 'keep' in the aggregation module input. Sentences are separated by a space.  
