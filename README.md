# Multi Modal Matching

## 0. How to run 

### Initial Setup

- [ ] Clone the repository on the cluster ```git clone https://git.informatik.uni-leipzig.de/wd83zadi/multimodalmatching.git```
- [ ] Place the directory Images with the folders Zalando, TommyHilfiger and GerryWeber next to the Project folder
- [ ] load Python3 module by executing: ```module load Python/3.9.6-GCCcore-11.2.0-bare```
- [ ] install virtual environment: ```pip install -- user  virtualenv```
- [ ] create virtual environment: ```virtualenv venv```
- [ ] active environment: ```source venv/bin/activate```
- [ ] load torchvision: ```module load torchvision/0.11.1-foss-2021a-CUDA-11.3.1``` 
- [ ] load Tensorflow: ```module load TensorFlow/2.6.0-foss-2021a-CUDA-11.3.1```
- [ ] Install requirements: ```pip install --user -r multimodalmatching/Rollout/requirements.txt```
- [ ] Run the matching task:  ```sbatch multimodalmatching/Rollout/matching-task.sh```

### Reoccuring Execution

- [ ] active environment: ```source venv/bin/activate```
- [ ] load Python3 module by executing: ```module load Python/3.9.6-GCCcore-11.2.0-bare```
- [ ] load torchvision: ```module load torchvision/0.11.1-foss-2021a-CUDA-11.3.1``` 
- [ ] load Tensorflow: ```module load TensorFlow/2.6.0-foss-2021a-CUDA-11.3.1```
- [ ] Run the matching task:  ```sbatch multimodalmatching/Rollout/matching-task.sh```

## 1. Abstract

Entity resolution has already been successfully employed to match various offers of products from multiple online stores. But in certain domains the textual or numerical attributes are not sufficient to make a reliable matching decision. The usage of images can provide an improvement in the results of product matching in the fashion domain.
Convolutional neural networks (CNNs) have yielded many breakthroughs in the field of computer vision in recent years resulting in many contributions to the widespread application of Deep Learning.
Multi modal matching implies the usage of text data and images in the same system. Within the scope of this practical, such a multi modal matching system has been implemented.

## 2. Workflow

![chart-relative text][chart-relative]


### 1. Text data Preprocessing

Text preprocessing is performed in the preprocess_text_data() method, contained in the ```TextPreprocessing/textPreprocessing.py```.
This step is kept simple, since the chosen NLP model is a sentence-transformer BERT model.
The model contains tokens for every special characters and numbers. 
Stop words are not removed as well, since those provide contextual information to the BERT model. (https://arxiv.org/pdf/1904.07531.pdf)
The few utilized cleaning steps are located in the ```TextPreprocessing/textCleaning.py```
Additionaly the add categories method (```TextPreprocessing/addCategories.py```) is utilized in this step to add different categories to the products. This will be required in a later blocking step.
Finally the files clean_GerryWeber.csv, clean_TommyHilfiger.csv and clean_Zalando.csv are created in the Datasets directory.

### 2. Blocking

In the main utility class (MatchingUtilities) from the ```Util/matchingUtilities.py``` blocking is conducted.
From this point on, the Tommy Hilfiger and Gerry Weber data are perceived as a single data set, as these two do not contain matches among one another. Their MPNs do not contain any intersections and can therefore be used as identifiers for the corresponding products within the Tommy Hilfiger / Gerry Weber dataset.
Besides blocking, in this class data is additionally prepared for further processing.
The method ```get_matching_text_data_as_df()``` returns two dataframes (```df_zal``` and ```th_gw```), that serve as a baseline for text embedding creation, while the ```get_matching_image_path_list()``` generates the base output for image embedding preprocessing and generation.
The ```MatchingUtilities``` class also includes the number of matching candidates before blocking and stores the potential matches after blocking was performed.
This information will be used at the end of the of the matching pipeline in the evaluation.

### 3. Text Feature Extraction

Since a number of english words appears in the german dataset a bilingual transformer model is utilized for feature extraction.
This step is performed in the ```TransformersEmbeddingGenerator``` class in ```EmbeddingCreation/createTextEmbeddings.py```
An instance of the ```TransformersEmbeddingGenerator``` is an attribute of the ```ManageTextEmbeddings``` class in the same file location, which initiates the Text Embedding Creation of a given string and stores the Embedding in the database.

### 4. Image Feature Managing

#### 4.1 Image Preprocessing

The images are preprocessed in the ```ImagePreprocessing``` module. 
The ```ImageBatchIterator``` (```ImagePreprocessing/imageBatchPreprocessing.py```) devides the data into batches of same size, while in the ```ImagePreprocessing/imagePreprocessing.py``` the image data is prepared for embedding creation.
Some images are corrupted or missing. Therefore these are downloaded.
Afterwards the images are resized, a dimension is added and they are preprocessed by the keras method ```preprocess_input``` for the pretrained ResNet model.

#### 4.2 Image Feature Extraction

Similar to text the ```ManageTextEmbeddings``` class (```EmbeddingCreation/createImageEmbeddings.py```) obtains image embeddings from its' instance of the ```ImageEmbeddingGenerator``` class (```EmbeddingCreation/createImageEmbeddings.py```). and stores the embeddings in the same tables as the text embeddings.
In contrast to text embedding generation the image vectors handling is conducted in batches.
First for the given batch the data is preprocessed. Then the image feature vector are computed and subsequently saved in the database.
The ```ManageTextEmbeddings``` class serves as an interface for these steps.

### 5. Similarty vector computation

The similarites for the name, variant, price and image are computed by the ```SimilarityGenerator``` (```Util/similartyGenerator.py```), which receives a pair of ids and reads the respective data from the database. Then the similarties can be computed for classification. Similarity Generation is a part of the sequential as well as the parallel Classification process

### 6. Classification

Can be performed in parallel or sequentially in the ```Classification``` module.

#### 6.1 Parallel Classification

The potential matches list obtained after blocking is splitted in equally sized sublists. The number of these sublists corresponds to the number of processes, that conduct similarity computation and classification in parallel on every pair of the appropriate sublist. Finally the classified matches are written to the database. The associated code can be found in the ```Classification/parallelClassification.py```.

#### 6.2 Sequential Classification

Sequentially for every pair of potential matches the similarities are calculated and classified. Every classified match is persisted in the database. This process can be viewed in more detail in the ```Classification/sequentialClassification.py```.


### 7. Evaluation

#### 7.1 Classification Evaluation

Some basic evaluation metrics for classification performance of the resulting matching pipeline are implemented in the ```Evaluation/classificationEvaluation.py```
This file includes the confusion matrix, as well as accuracy, precision, recall and f-measure as evaluation metrics. Those are shown in the table below.

#### 7.2 Blocking Evaluation

For the assessment of the blocking technique another evaluation approach was implemented in the ```Evaluation/blockingEvaluation.py```. It includes the metrics pairs completeness, reduction ratio and pairs quality. 

## 3. Matching Pipeline Evaulation

The table below displays the thresholds for similarities of the name, variant, image and price values that a product pair should exceed to be classified as a match.
In addition, the metrics precision, recall, f-measure and accuracy are shown there as well and the classified matches for the evaluation of the matching pipeline.
The selected thresholds are marked in the table (0.1, 0.3, 0.5, 0.7), since using those still results in clasifying over 70% of the true matches and a large amount of no matches correctly.

Table build with: (https://tableconvert.com/csv-to-markdown)
|**Name**  |**Variant**  |**Image**  |**Price**  |**Precision**  |**Recall**  |**F-Measure**  |**Accuracy**   |**Classified Matches** |
|:--------:|:-----------:|:---------:|:---------:|:-------------:|:----------:|:-------------:|:-------------:|:---------------------:|
|0,046	   |0,121	     |0,29	     |0,48943	 |0,00	  		 |0,99        |0,00           | 0,97    	  |6226946				  |
|0,074     |0,121        |0,35       |0,499      |0,00    		 |0,99        |0,00           | 0,97    	  |5792448				  |
|0,074     |0,121        |0,4        |0,499      |0,00    		 |0,98        |0,00           | 0,97    	  |5478051				  |
|0,074     |0,121        |0,4        |0,599      |0,00    		 |0,95        |0,00           | 0,98    	  |4333491				  |
|0,074     |0,121        |0,41       |0,6        |0,00    		 |0,98        |0,00           | 0,98    	  |4253486				  |
|0,074     |0,121        |0,44       |0,65       |0,00    		 |0,91        |0,00           | 0,98    	  |3457071				  |
|0,074     |0,2          |0,44       |0,65       |0,00    		 |0,90        |0,00           | 0,98    	  |3307262				  |
|0,074     |0,2          |0,44       |0,7        |0,00    		 |0,86        |0,00           | 0,99    	  |2800167				  |
|0,074     |0,22         |0,44       |0,7        |0,00    		 |0,85        |0,00           | 0,99    	  |2714048				  |
|0,074     |0,22         |0,44       |0,75       |0,00    		 |0,72        |0,00           | 0,99    	  |1821142				  |
|0,074     |0,22         |0,529      |0,75       |0,00    		 |0,70        |0,00           | 0,99    	  |1614101				  |
|0,074     |0,22         |0,5        |0,8        |0,00    		 |0,64        |0,00           | 0,99    	  |1410932				  |
|0,046     |0,121        |0,35       |0,6        |0,00    		 |0,96        |0,00           | 0,98    	  |4613521				  |
|0,046     |0,121        |0,35       |0,65       |0,00    		 |0,93        |0,00           | 0,98    	  |3998412				  |
|0,046     |0,121        |0,35       |0,7        |0,00    		 |0,89        |0,00           | 0,98    	  |3384077				  |
|0,046     |0,121        |0,4        |0,75       |0,00    		 |0,80        |0,00           | 0,99    	  |2611693				  |
|0,046     |0,121        |0,5        |0,75       |0,00    		 |0,74        |0,00           | 0,99    	  |1972316				  |
|0,0474    |0,22         |0,5        |0,75       |0,00    		 |0,72        |0,00           | 0,99    	  |1832319				  |
|0,0474    |0,22         |0,5        |0,7        |0,00    		 |0,81        |0,00           | 0,99    	  |2248597				  |
|0,1       |0,22         |0,5        |0,7        |0,00    		 |0,80        |0,00           | 0,99    	  |2209303				  |
|**0,1**   |**0,3**      |**0,5**    |**0,7**    |**0,00** 		 |**0,724**   |**0,002**      | **0,995**  	  |**1095314**			  |
|0,15      |0,35         |0,5        |0,7        |0,00    		 |0,71        |0,00           | 0,99    	  |1083906				  |
|0,15      |0,35         |0,55       |0,7        |0,00    		 |0,67        |0,00           | 1,00    	  | 934507				  |
|0,2       |0,35         |0,55       |0,7        |0,00    		 |0,65        |0,00           | 1,00    	  | 891144				  |


	     

[chart-relative]: img/chart.png "chart-relative Text"


---------------