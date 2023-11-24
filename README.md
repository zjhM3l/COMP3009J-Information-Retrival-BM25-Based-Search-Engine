# BM25 Information Retrieval Model(Zhang Jiahe 20205722)
## 1. Project Overview
This project implements a BM25 information retrieval model **for both small and large corpora**. The goal is to keep the running time of search_small_corpus **within 2 seconds (first time including index construction)** and the running time of search_large_corpus **within 50 seconds (first time including index construction, 3 seconds for search if index exist)**. The program, written in Python, allows the following operations:
- Document Extraction: Extracts documents from the provided document collection and appropriately splits them into terms.  
- Index Creation: Creates the necessary index data structure during the first run of the program for subsequent information retrieval.
- Manual Query: Displays the top 15 relevant documents' ranking, document ID, and similarity score based on user input queries in the command-line interface.
- Automated Query: Reads standard queries from the provided query file and outputs the results to the "results.txt" file, including query ID, ranking, document ID, and similarity score.
- Model Evaluation: Iterates through the query results and calculates various evaluation metrics. The average evaluation metrics for all queries will be printed.
## 2. Usage Instructions
Follow the steps below to run the program:

Ensure that Python is installed on your system.
Open the terminal or command prompt and navigate to the program directory.
Execute the following command to run the program:

### 2.1 Small Corpus
Note: The index based on document data processing will be stored in the "result.txt" file in the current folder and will be created **only during the first run**. Subsequent runs will only perform reading.  
####2.1.1 Automated Query
Note that the automated query part of search_small_corpus.py makes the following assumptions about the queries:  
- The document collection (processed by the process_documents function) is small enough that their full text and term frequencies can be stored in memory.  
- Each query in the "queries.txt" file does not contain a colon (":").

Run the following command for automated query:

- **python search_small_corpus.py -m automatic**

This command will read the standard query file "files/queries.txt" and output the query results to the "results.txt" file. The following will be displayed on the screen:  
- **finish index build/read in x seconds**  
- **finish search in y seconds**


####2.1.2 Manual Query
Run the following command for manual query:

- **python search_small_corpus.py -m interactive**

This command will display the following in the command-line interface:

- **Enter your query (or 'q' to quit):**

Wait for the user to input the query. The user can enter the query and press Enter to perform the search. The query results, including ranking, document ID, and similarity score, will be displayed on the screen. The user can enter 'q' to exit the query mode.

Example output:

- **Search Results:  
Results for query: what similarity laws must be obeyed when constructing aeroelastic models of heated high speed aircraft
1 51 19.216799  
2 486 18.598630  
3 12 16.451968  
4 184 15.837480  
5 878 14.830204  
6 665 12.985902  
7 573 12.810276  
8 944 11.770467  
9 141 11.397982  
10 746 11.197510  
11 78 11.073275  
12 14 10.616306  
13 453 10.154860  
14 879 10.005720  
15 13 9.969227  
finish search in 0.004960060119628906 seconds** 


#### 2.1.3 Explanation of Execution Results
During the program execution, some information will be output to the console, including index build time and query execution time.

For example:

- **finish index build/read in 2.1704936027526855 seconds
finish search in 0.051 seconds**

The above information indicates that the initial index construction process took 2.17 seconds, and the query process took 0.051 seconds (data obtained from final testing).

- Note: The query results may vary depending on the specific query content and dataset.
### 2.2 Large Corpus
- Note: The index based on document data processing will be stored in the "result.txt" file in the current folder and will be created only during the first run. Subsequent runs will only perform reading.

#### 2.2.1 Automated Query
- **python search_large_corpus.py -m automatic**

For the first run:

You will see the prompt: 
- **Index file('result.txt') not exist and need to be built, please wait...**

It will check for any non-readable files in all files and output the following prompt:  
- **Skipping non-text file: documents\.DS_Store**

Once the index is built and the result.txt file is completed, the terminal will output the following prompt:  
- **Index file('result.txt') not exist and build time: 42.972078800201416 seconds（based on the final testing data）**

This command will read the standard query file "files/queries.txt" and output the query results to the "results.txt" file. The following will be displayed on the screen:

For subsequent runs:    
- **Index file('result.txt') already exist and load time: 4.491275310516357 seconds**


####2.2.2 Manual Query
- **python search_large_corpus.py -m interactive**

For the first run, the prompt will be the same as mentioned above.

This command will display the following in the command-line interface:

- **Enter your query (or 'q' to quit):**

Wait for the user to input the query. The user can enter the query and press Enter to perform the search. The query results, including ranking, document ID, and similarity score, will be displayed on the screen. The user can enter 'q' to exit the query mode.

Example output:   
- **Search Results:  
Results for query: describe history oil industry  
1 documents\GX232\GX232-43-0102505 6.248369  
2 documents\GX255\GX255-56-12408598 5.976549  
3 documents\GX229\GX229-87-1373283 5.938620  
4 documents\GX253\GX253-41-3663663 5.916405  
5 documents\GX268\GX268-35-11839875 5.856646  
6 documents\GX064\GX064-43-9736582 5.851986  
7 documents\GX231\GX231-53-10990040 5.791729  
8 documents\GX063\GX063-18-3591274 5.771219  
9 documents\GX253\GX253-57-7230055 5.759280  
10 documents\GX262\GX262-28-10252024 5.745876  
11 documents\GX263\GX263-63-13628209 5.707570  
12 documents\GX006\GX006-76-15945590 5.656419  
13 documents\GX262\GX262-86-10646381 5.620741  
14 documents\GX255\GX255-59-12399984 5.620258  
15 documents\GX000\GX000-48-10208090 5.619713  
finish search in 0.3581116199493408 seconds**


## 3. Search Implementation Process
### 3.1 Small Corpus
The implementation of this program involves the following steps:

- **1. Document Processing**: Iterate through the document directory, read each document, and perform a series of processing steps, including text normalization, stop word removal, stemming, and filtering. The processed terms are added to the inverted index and the length of each document is tracked.  
- **2. Index Loading or Creation**: Check if the index file exists. If it does, try to load the index; otherwise, call the document processing function to build the index. The index is stored in memory as an inverted index and written to a file in a specific format.  
- **3. BM25 Model Query (Interactive Mode)**: In interactive mode, the user can input a query. The query is preprocessed, including stop word removal, stemming, and filtering. Then, the query is matched against the documents in the index, and the document scores are calculated using the BM25 formula. Finally, the documents are ranked based on the scores, and the top 15 query results are output.  
- **4. BM25 Model Query (Automatic Mode)**: In automatic mode, queries are read from a file, and the same steps as in interactive mode are performed for each query. The query results are appended to the "results.txt" file.  

The detailed implementation details are explained in the comments of the source code.

#### 3.1.1 Optimization Improvements and Data Structure Approach
- **Data Structure**: The inverted index uses nested dictionaries. The outer dictionary has integer keys representing the document numbers, and the values are inner nested dictionaries. The inner dictionaries have integer keys representing the document numbers, and the values represent the frequency of the term in that document.  
- **Preprocessing Steps**:
  - Replace punctuation with spaces.
  - Remove content containing numerical gibberish, such as: (000degre, 10degre, 18in, 4degre, 4x10, 50degre...).  
- **BM25**: A standard formula is used. For terms that are not in the document collection, their BM25 scores are ignored.
- **About the "result.txt" File (Index Data Structure)**:
  - If the code is run multiple times, the results will accumulate. To clear the previous results before processing queries, "open('results.txt', 'w').close()" is added at the beginning.
  - If the "result.txt" file exists, the existing index will be loaded. After loading the index, the existing index is traversed to update the "doc_lengths" dictionary.
  - An attempt is made to parse the content of the "result.txt" file in a specific format. However, this file may not always match the expected format. If any line in the "result.txt" file does not match the expected format, there may be an issue when trying to parse the file. In such cases, when trying to access item[1] (i.e., line.strip().split(": ")[1]), a "list index out of range" error will be raised. Therefore, each line is checked for the expected format before attempting to parse it. If it doesn't match, the line is ignored or an error can be raised.

  
### 3.2 Large Corpus
#### 3.2.1 Optimization Process (170s -> 90s)
The implementation of this program, based on search_small_corpus.py, underwent the following optimizations:  
- **Preprocessing and File Reading**:
  - Using the **os.walk** method to recursively process text files in all folders and subfolders can save approximately 12-14 seconds.
  - The '.DS_Store' file is typically present in each directory, so it is specifically skipped.
  - Further removal of special characters and gibberish like '' is performed.
- **Data Structure**:
  - An improved version of the inverted index is used, storing each term and its corresponding document IDs in a linked list. The code for building the index is placed inside the process_documents function, which now returns a dictionary. The keys of the dictionary are terms, and the values are another dictionary where the keys are docIDs and the values represent the frequency of the term in that document.
  - Python's built-in linked list data structure was not used because dictionaries in Python are highly efficient in this case.
  - (An optimization approach that was ultimately not used as it didn't provide significant efficiency improvement) Using a hash table (dict) to represent the inverted index: Each term is used as a key, and the corresponding document and frequency information are stored as values in the dictionary.
  - In the attempt to optimize index loading and access efficiency, it was found that the time actually increased. This could be due to factors such as data size, hardware configuration, or other reasons. The effectiveness of optimizations can vary depending on the situation, and different optimization methods may yield different results in different environments. The nested dictionary data structure may be suitable in some cases, especially for smaller datasets and resource-limited environments.
  
The detailed implementation details can be found in the comments of the source code.
#### 3.2.2 Core Optimization Strategy (90s -> 45s)
**Usage of threads**:  
Parallel processing can improve processing speed, but it needs to be considered that Python's parallel processing, due to the Global Interpreter Lock (GIL), typically requires the use of external libraries such as multiprocessing or joblib to achieve. However, I attempted to use Python threads for parallel processing, but for CPU-intensive tasks like your text processing task, I might not achieve the desired effect. This is because Python threads cannot execute in parallel on multiple CPU cores due to the GIL.

Due to Python's Global Interpreter Lock (GIL), parallel processing is typically more suitable for I/O-bound tasks rather than CPU-bound tasks. However, since I'm using the multiprocessing library (which creates new processes to bypass the GIL), this is not an issue.

I used the Pool object to create a group of worker processes and used the map function to distribute the document set to these processes. Each process was responsible for processing its assigned documents and creating a partial inverted index. Finally, I merged all the partial inverted indices together.

Since I needed to share data between different processes, I had to use special data structures (such as Manager.dict), which could impact performance. (It turned out that the reading speed actually improved.)

The multiprocessing module is used in the system, but the entry point of the main program is not properly protected. When using the multiprocessing module, it is necessary to ensure that the entry point of the main program is protected by if __name__ == '__main__':. This is due to a feature of the multiprocessing implementation on Windows platforms: it needs to be able to safely import the main module.

To address this issue, I defined the process_document function before the main function and passed stop_words and stemmer as parameters to the process_document function. This way, the process_document function can access these variables. Additionally, the process_documents function needs to be updated accordingly.

First run:  
- **Index build time: 39.5242874622345 seconds
finish search in 28.932120323181152 seconds**

Second run: Search time takes a long time  
- **Index build time: 2.12763738474842 seconds
finish search in 25.73831789371911 seconds**

Therefore, I ultimately chose to lock the creation of the index in the multi-threading process during the first run. For each subsequent run, it will be based on the optimized single-threaded small version. This ensures that the first run involves creating the index and searching, while the subsequent search time is significantly reduced.

First run:  
- **Index build time: 39.2783848232312 seconds
finish search in 28.3923840982340 seconds**
Second run:  
- **Index build time: 2.7383127484321 seconds
finish search in 1.2391283181239 seconds**

#### 3.2.3 Trade Off
**Space for time**:

Reducing file operations: In the small version of my code, I wrote to the file immediately after processing each line. This results in frequent disk operations, which are typically much slower than memory operations. Therefore, I tried to save all the results in memory first and then write them to the file in one go. However, this approach may increase memory usage.
One solution I adopted is to read the entire file into memory and process the data all at once. I used Python's readlines() method to read the entire file at once and then processed each line. However, this approach may increase memory usage because the content of the entire file is loaded into memory.  
But in the end, I found that it didn't significantly improve the efficiency of my code.
## 4. Evaluation
The program also includes an evaluation section to assess the effectiveness of the BM25 model. You can run the evaluation program using the following commands:

- **python evaluate_small_corpus.py**

- **python evaluate_large_corpus.py**

###4.1 Evaluation Results
The evaluation program calculates the following evaluation metrics based on the results in the "results.txt" file and the relevance judgments in the "qrels.txt" file:

- Precision
- Recall
- P@10
- R-precision
- Mean Average Precision (MAP)
- bpref

The evaluation results will be displayed on the command line interface as follows:  
- **Precision: 0.01012455908343267  
Recall: 0.9554113026757381  
P@10: 0.3031111111111111  
R-precision: 0.3958804279837376  
MAP: 0.41831563261641286  
bpref: 0.86933909750401**
(Data obtained from the evaluation of the results in the automatic mode of "search_small_corpus")  

or

large automatic：   
- **Precision: 0.01984832675490674  
Recall: 0.9970909243998191  
P@10: 0.5629629629629628  
R-precision: 0.5151120783875084  
MAP: 0.5734032564316254  
bpref: 0.9853212832773209**
(Data obtained from the evaluation of the results in the automatic mode of "search_large_corpus")


###4.2 Runtime Efficiency Evaluation
The runtime measurements are based on running the automatic mode queries on a local computer with the following configuration:
Intel(R) Core(TM) i7-10750H CPU @ 2.60GHz   2.59 GHz/32.0 GB  

search_small_corpus.py:
- First run: 2.17s (index construction time) + 0.051s (search time)
- Subsequent runs: 0.03s (index loading time) + 0.047s (search time)


search_large_corpus.py:
- First run: 42.97s (index construction time) + 12s (search time)
- Subsequent runs: 4.49s (index loading time) + 2.43s (search time)

###4.3 Evaluation Strategy Analysis
During the evaluation testing, it was observed that if the number of retrieved documents for each query is smaller than the number of relevant documents, the precision and recall will be the same.

##5. Notes
- The program needs to be run in the current directory that contains the "documents" and "files" directories.
- Apart from the provided Porter stemmer, no other non-standard libraries are used.
