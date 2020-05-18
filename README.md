# There are few educational and work projects

### ROOT
- Richtracks prediction model

  Building a model that predicts whether the ride was made by a passenger or not based on data from incoming points.
  Score prediction measuring using raw prediction, data preprocessing with PCA method and configuration of hyperparameters
  [Link](https://github.com/Turakulov/Python/blob/master/richtracks%20model%20training.ipynb)

- Text classification to several categories using `20newsgroups` dataset
  [Link](https://github.com/Turakulov/Python/blob/master/text_classfication.ipynb)
  
- Review classification.
  
  The goal of the task is building a model that predicts type of movie review (negative or positive) using `sklearn`. We have two categories: "`negative`" and "`positive`", therefore `1`'s and `0`'s have been added to the target array. The folder contains two subfolders of `.txt` files divided into "`negative`" and "`positive`" reviews [Link](https://github.com/Turakulov/Python/blob/master/review_classification.ipynb)

- Spam, not spam sms prediction

  The aim of this task is to predict the category of the sms (spam or not spam) using logistic regression. Also we need to implement cross validation using `GridSearchCV` and finally compare scores (`precision`, `recall`, `accurracy`) of models. [Link](https://github.com/Turakulov/Python/blob/master/spam_notspam_prediction.ipynb) 
 
- News parsing&clustering

  Parsing news of various topics from the <https://iz.ru> website. Finding optimal clusters number of dataset using `elbow method`. For each number of clusters value we will initialize `K-means` and use the inertia attribute to identify the sum of square distances of samples to the nearest cluster centre. To visualize, we’ll plot the features in a 2D space. As we know the dimension of features that we obtained from `TFIDFVectorizer` is quite large ( > 10,000), we need to reduce the dimension before we can plot. For this, we’ll use `PCA` and `UMAP` to transform our high dimensional features into 2 dimensions [Link](https://github.com/Turakulov/Python/blob/master/News_parsing%26clustering.ipynb) 

### Education
 
- Image detecting using сonvolutional neural networks.

  The idea behind this figure is to show, that such neural network configuration 
  is identical with a 2D convolution operation and weights
  are just filters (also called kernels, convolution matrices, or masks)
  [Link](https://github.com/Turakulov/Python/blob/master/Education/Image%20detecting/Untitled.ipynb)
  
- Image clustering. 

  Clustering is a technique that helps in grouping similar items together based on particular attributes. 
  We are going to apply K-means clustering to the image with 6-7 colors [Link](https://github.com/Turakulov/Python/blob/master/Education/Clustering/clustering.ipynb)

- Moving object detecting using OpenCV

  At first we detect moving object then draw contours and fill with mean color between mask and source video frame
  [Link](https://github.com/Turakulov/Python/blob/master/Education/Moving%20object%20detecting/moving%20object%20detecting.ipynb)
  
- Vandermonde matrix implementation

  Implementing vandermonde matrix without using `numpy.vandermonde()` [Link](https://github.com/Turakulov/Python/blob/master/Education/Vandermonde_matrix/Vandermonde_matrix.ipynb)

- Marathon simulation
  
  Implementation of a marathon simulation where the speed of runners is determined using the distribution law (exponential distribution, normal, Poisson, Bernoulli) [Link](https://github.com/Turakulov/Python/blob/master/Education/marathon/marathon_simulating.ipynb)
  
- Advertising search on Avito webpage

  In this task, we have to write a function that parses `Avito` webpage (we will only consider Moscow city). This function accepts two parameters. The first parameter is what we are looking for on the page. The second parameter is the number of the page to parse information from. You need to download the following information:
    - ad name; 
    - ad url;
    - price; 
    - subway station (if available), you need to carefully handle `None` or use the `try-except` construction;
    - how many meters from the subway station (if available).
    
  [Link](https://github.com/Turakulov/Python/blob/master/Education/Advertising%20search%20on%20Avito/Advertising_search.ipynb)

  
### Work  
- Offline shop database.

  Данное приложение было написано на первом курсе обучения в рамках изучения дисциплины Python.
  Ознакомиться с руководством пользователя можно тут [Link](https://github.com/Turakulov/Python/tree/master/Work)
