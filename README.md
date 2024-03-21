![image](https://github.com/LiangSylar/Text-Mining-Method-by-Pagerank-and-TF-IDF-for-Key-Sentence-Extraction-/assets/64362092/281e8f92-be73-48d3-9d0f-7213aa6651c8)# Text-Mining-Method-by-Pagerank-and-TF-IDF-for-Key-Sentence-Extraction

## Introduction 
In this project, we try a method that combines PageRank with TFIDF to extract key sentences from documents. The algorithm first preprocesses the data and obtains the TF-IDF value for each word
in each sentence. Then the sentence vectors for each sentence are built based on the TF-IDF values. For each pair of sentences in the same article, whether to add an edge between the two sentences depends on the comparison results of the cosine value and the threshold value. The most important sentence in the article can be found by the PageRank algorithm using the relationships suggested by edges

##  Term Frequency-Inverse Document Frequency (TF-IDF) 
* TF-IDF contains two separate parts:Term frequency (TF) and Inverse document frequency (IDF)
* TF: the more frequently a word appears, the more important it is.
<figure>
  <img 
    src="https://github.com/LiangSylar/Text-Mining-Method-by-Pagerank-and-TF-IDF-for-Key-Sentence-Extraction-/assets/64362092/3065459b-c848-4e14-a057-d3926b4dda2d" 
    alt="Image" 
    height="50"> 
</figure> 
* IDF: a word that appears frequently in many other documents suggests to be a common word.
<figure>
  <img 
    src="https://github.com/LiangSylar/Text-Mining-Method-by-Pagerank-and-TF-IDF-for-Key-Sentence-Extraction-/assets/64362092/b7905330-bf48-43ef-ae27-8614cf53112c" 
    alt="Image" 
    height="50"> 
</figure> 
![image]( )

## Stopwords Removal 
* Stopwords typically refer to the most common words in a language.
* They should be filtered out in text data preprocessing.
* Example: a, about, after, again, below, cannot, etc.

## Stemming 
* A process that transfers the words to their root form.
* Example: running --> run
* It helps to figure out the relationships among words by avoiding repetitious extractions.

## Sentence Vector  
* Sentence vector: a vector constructed to represent the key information of the sentence. 
![image](https://github.com/LiangSylar/Text-Mining-Method-by-Pagerank-and-TF-IDF-for-Key-Sentence-Extraction-/assets/64362092/78762dd0-8b55-4f21-959b-9162f324ee76)

* Step 1. Find out all words that appear in all available documents.
* Step 2. Represent each sentence using a vector.
* Example. Vector representation for the sentence "This horse runs fast".
<figure>
  <img 
    src="https://github.com/LiangSylar/Text-Mining-Method-by-Pagerank-and-TF-IDF-for-Key-Sentence-Extraction-/assets/64362092/b00fd7da-a814-4016-ad17-75a352951624" 
    alt="Image" 
    height="50"> 
</figure>  

## Cosine Distance of sentences 
* Cosine distance: a commonly used method to represent the correlation between two documents
* Given A and B as two sentence vectors, we can compute their correlation by:
<figure>
  <img 
    src="https://github.com/LiangSylar/Text-Mining-Method-by-Pagerank-and-TF-IDF-for-Key-Sentence-Extraction-/assets/64362092/24ab596e-c43f-4fcf-882c-ea54692903fc" 
    alt="Image" 
    height="50"> 
</figure>   

## Sentence Importance Representation by TF-IDF metric 
* The TF-IDF of each sentence represents the importance of each word in this sentence.
* Step 1. Calculate the cosine distance for each pair of sentences within the document.
* Step 2. If the cosine value is greater than the threshold, two sentences are believed to be correlated and an edge is drawn between them.
* Eventually, a graph representing the relationships of sentences will be obtained.
 
## PageRank Algorithm for key sentence extraction 
* PageRank is a website ranking algorithm used by Google to quantify correlations among different websites. It builds a graph that indicates whether the two websites are related. This graph can be represented by a matrix and the eigenvalues of the matrix stand for the importance of the corresponding website.
* In our application for key sentence extraction, the graph now represents the relations among sentences. The result of this algorithm is a vector where each entry represents the importance of a sentence in the document. 







  
