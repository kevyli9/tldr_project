**Quality Control Module**  
Where to find it:
* The quality control module is located in the src/qc_and_aggregation.py file. 

Relevant parts of the code and how they work:
* The quality control module is comprised of the add_filters, get_qualified_workers, and majority_vote functions. The first step of the module is the add_filters function which takes the raw input data and adds an attribute “filtered” for every HIT instance. If the worker spent at least 1 minute on the HIT, answered all positive and negative quality control questions correctly, and clicked on at least 5 sentences, the “filtered” attribute will be true. Otherwise, it will be false. The get_qualified_workers function is then used to select all HITs which received a “filtered” label of true. For the set of filtered HITs, we then group them by article. Finally, the majority vote function is called on each set of filtered HITs for each article. For each of the 10 sentences of an article, we either add a “keep” or “remove” attribute depending on the worker’s response. We break ties with a random number generator when the count of “keep” and “remove” are equal. The function outputs a list of tuples of the form (sentence, label, keep_votes) which are turned into a dataframe and exported as a csv file. 

Improvements for the final version (Kevin):
* a

**Aggregation Module**  
Where to find it:
* The aggregation module is also located in the src/qc_and_aggregation.py file. 

Relevant parts of the code and how they work:
* The aggregation module is comprised of the vote_to_text function. This function takes as input a dataframe for each article that contains columns (sentence, label, keep_votes) which was created as a result of the quality control module. For each row, the sentence of the row is written to new file if it’s label is “keep”, while sentences with label “remove” are ignored.  

Improvements for the final version (Kevin):
* a
