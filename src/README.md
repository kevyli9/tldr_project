**Quality Control Module**  
Where to find it:
* The quality control module is located in the src/qc_and_aggregation.py file. 

Relevant parts of the code and how they work:
* The quality control module is comprised of the **add_filters**, **get_qualified_workers**, and **majority_vote** functions. 
* The first step of the module is the add_filters function, which takes the raw input data and adds an attribute 'filtered' for every HIT instance. If the worker spent at least 1 minute on the HIT, answered all positive and negative quality control questions correctly, and clicked on at least 5 non-quality control sentences, the 'filtered' attribute will be true. Otherwise, it will be false. 
* The get_qualified_workers function is then used to select all HITs which received a 'filtered' label of true. For the set of filtered HITs, we then group them by article. 
* Finally, the majority_vote function is called on each set of filtered HITs for each article. For each of the sentences of an article, we either add a 'keep' or 'remove' attribute depending on the workers' responses. We break ties with a random number generator when the count of 'keep' and 'remove' are equal. The function outputs a list of tuples of the form (sentence, label, keep_votes) which are turned into a dataframe and exported as a CSV file. 

Improvements for the final version:
* Because of how we implemented the HTML for our HIT, our 'Answer.' columns follow a different naming format than our 'Input.' columns (explained in more detail in the data/README.md). Currently, we have hard-coded the re-naming process to work with articles of maximum length 10 sentences (number of sentences in our sample QC input CSV). For our final version, we will make this re-naming process dynamic such that it can work with articles of any number of sentences.

**Aggregation Module**  
Where to find it:
* The aggregation module is also located in the src/qc_and_aggregation.py file. 

Relevant parts of the code and how they work:
* The aggregation module is comprised of the **vote_to_text** function. This function takes as input a dataframe for each article that contains columns (sentence, label, keep_votes) which was created as a result of the quality control module. For each row, the sentence of the row is written to a new file if its label is 'keep', while sentences with label 'remove' are ignored.  

Improvements for the final version:
* No major improvements needed. We may need to slightly alter the format of the aggregation output, depending on how we implement the slider UI.

**Sentence Extraction** (raw data input creation)
Where to find it:  
* a

Relevant parts of the code and how they work:
* a

Improvements for the final version:
* a
