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
* The sentence extraction method is located in the src/sentence_extraction.py file.

Relevant parts of the code and how they work:
* The program loops over a list of urls and for each url does the following:
  * Extract all the text from the article linked by the url using the newspaper API's Article methods
  * Break down the article's text into individual sentences using the Spacy API's add_pipe and sentencizer methods (sourced from stack overflow)
  * Store the url and sentences in a list named sentences
  * Add the sentences list to a master list - input that stores the sentences for all the urls - by converting the sentences list into a tuple
 * The input list is then converted into a pandas dataframe
 * Quality control sentences are inserted into columns 2, 5, and 9
 * The dataframe is converted into a csv

Improvements for the final version:
* The newspaper api we are using faces issues with webpages that have complicated formatting, and a potential improvement would be to find ways to enhance the api's functionality

**Slider Bar UI**  
Where to find it:  
* slider_nets213.html, style.css, script.js

Relevant parts of the code and how they work:  
* The HTML file (slider_nets213.html) sets up the major components of the UI, which are the upload components, slider bar, and back button
* The CSS file (style.css) sets up the style for the slider bar
* The JavaScript (script.js) file does a few things. First, it "gets" all of the components on the page to manipulate them. Second, it records the value of the slider bar and from that it makes the sentences with the least number of 'keep' votes disappear first. The Upload function shows each of the elements (slider bar, text, and back button), reads the uploaded file, and sorts the sentences based on keep votes (sortInLeastAmountOfKeepVotes function) to be referenced when determining which sentences to hide first.

**Coreference resolution**  
Where to find it:  
* coref_qc_and_aggregation.py

Relevant parts of the code and how they work:  
* The coreference resolution is integrated into the quality control and aggregation module (see coref_qc_and_aggregation.py).
* The coref function retrieves the full original text and replaces coreferences with their main mention utilizing AllenNLP’s CorefPredictor Model. The function then tokenizes the resolved text into individual sentences.
* The original sentences are replaced with the corresponding resolved sentences in the output csv, allowing for the final UI to display the resolved sentences in any chosen summary (see ‘coref_list’ in the majority_vote function and main method #MAJORITY VOTING)

**Survey results**
Where to find it:
* a

Relevant parts of the code and how they work:
* a


**Analysis**  
* We will compare TLDR’s results against an existing non-crowdsourcing method, specifically "SMMRY" (https://smmry.com/about)
* SMMRY uses an algorithm to summarize articles. It calculates the occurrence of each word in the text, assigns each word a number of points depending on the word's popularity, and ranks sentences by the sum of their words' points.
* We are interested in seeing whether, on average, TLDR produces higher quality summaries than SMMRY.
* We will create a HIT that asks workers to vote on which summary for a given article (TLDR's summary or SMMRY's summary) is higher quality, and see which summary gets more votes from workers.
