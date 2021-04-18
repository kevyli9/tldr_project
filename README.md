# tldr_project
**Total points**: 17

**Folders in repository**
* Docs: holds all of the documents we need, the flowchart, mockups, and a readme
* Src: holds the quality control and aggregation script. This is modeled as a python main method with different functions performing transformations on a pandas DataFrame. It reads in the HIT csv, and ultimately outputs a file for each article with the keep/remove votes for each sentence that workers voted on. In the end, the aggregation model will take these votes, actually remove the sentences that were labeled "remove" and then output a .txt file for each article.

**Designing the HIT** (2 points)
In this component, we will design the main HIT for TLDR. This HIT will display the text from an article and allow Turkers to click on sentences that they think are not necessary for the summary of the article. The sentences that are clicked on will be highlighted black.  
**Milestones**:
* Adapt Professor Callison-Burch’s “shorten sentences” HIT, which allowed Turkers to remove words from sentences, to be at the sentence level rather than the word level
* Test the HIT on Sandbox to see if it is functioning properly

**Gather raw data** (1 point)
We will be gathering articles (3-4 minute read time) from major news publications. Initially, we ourselves will gather links to online articles that we can use as input to test the implementation of our modules. Later, we will be using MTurk to gather these links from workers.  
**Milestones**:
* Design a HIT for collecting the article links from workers
* Store these article links in a CSV file

**Prepare input CSV file** (2 points)
In this component, we will be taking the article links gathered from the last component and converting them into a format that can be used for the input file for our main HIT. Specifically, our input CSV file will be formatted such that each row represents an article, and each column represents 1 sentence in the article.  
**Milestones**:
* Use the newspaper python library to extract the actual text from articles given links
* Use the spacy library to split the text into sentences
* Embed attention checks within the CSV (e.g. “Please click on this sentence.”)

**Release HITs** (1 point)
After uploading our input CSV files to our main HIT, we will release the HITs. At this point, the workers will begin interacting with the data. We will be employing a parallel process where many workers will independently determine sentences to be removed.  
**Milestones**:
* Release the HIT batches
* Monitor to see if there are any issues that workers bring up
* Collect the HIT results

**Quality control** (3 points)
We will have a number of quality control measures in place. Workers that fail to click on the attention checks will have their work rejected. Workers that spend less than 1 minute completing a HIT will also have their work rejected (reading the article itself should on average take 3-4 minutes). After filtering out these responses, we will employ the EM algorithm to the remaining responses. We will do our best to give workers incremental feedback to avoid mass rejections.  
**Milestones**:
* Write a quality control program that will output labels for each sentence (“remove” or “keep”)
* Run our HIT results file through this program

**Aggregation** (1 point)
Take the sentences labeled “keep” from the quality control module and consolidate them into one output file. For each kept sentence, also store the number of weighted votes for “keep” that sentence received in the last iteration of the EM algorithm.  
**Milestones**:
* Write an aggregation program
* Run our quality-controlled HIT results file through this program

**Coreference Resolution** (4 points)
Perform coreference resolution on our output file from the aggregation component.  
**Milestones**:
* Learn how to use the Allen NLP tool in a program
* Run our output file through this program

**User Interface** (3 points)
We will develop a slider user interface (similar to Soylent). As the bar slides down, the sentences with the least number of “keep” votes will be removed first.  
**Milestones**:
* Develop the slider user interface
* Integrate this slider into the final article summary

