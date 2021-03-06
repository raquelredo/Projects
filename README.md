Projects
================

<span style="color:green">Last update: 25th July 2017

This is a brief introduction of some of the projects done concerning Machine Learning and Deep Learning models. In most cases data sets are public therefore the source is pointed out in the correspondent README file. Enjoy!

<span style="color:red">in R
============================

![](https://avatars2.githubusercontent.com/u/513560?v=3&s=200)

Kaggle - Predict Fraud
----------------------

[clic to go](https://github.com/raquelredo/Projects/blob/master/Machine%20Learning/Credit_Fraud_Script.md)

Anonymized credit card transactions labeled as fraudulent or genuine. Anonymization has been achieved performing Principal Component Analysis. 492 frauds out of 284,807 transactions.

-   Features: 30
-   Observations: 284,807
-   Tuples: 8,544,210

**Challenges:** Imbalanced data | Understanding PCA

Kaggle - Human Resources Analytics
----------------------------------

[clic to go](https://github.com/raquelredo/Projects/blob/master/Machine%20Learning/HR_analytics.md)

Why are our best and most experienced employees leaving prematurely?

-   Features: 9
-   Observations: 14,999
-   Tuples: 134,991

**Challenges:** Detect outliers

Indoor localization wifi Footprint
----------------------------------

[clic to go](https://github.com/raquelredo/Projects/blob/master/Machine%20Learning/Indoor_localization_Wifi_Footprint.md)

Many real world applications need to know the localization of a user in the world to provide their services. Therefore, automatic user localization has been a hot research topic in the last years. Automatic user localization consists of estimating the position of the user (latitude, longitude and altitude) by using an electronic device, usually a mobile phone. Outdoor localization problem can be solved very accurately thanks to the inclusion of GPS sensors into the mobile devices. However, indoor localization is still an open problem mainly due to the loss of GPS signal in indoor environments. Although, there are some indoor positioning technologies and methodologies, this database is focused on WLAN fingerprint-based ones (also know as WiFi Fingerprinting).

-   Features: 529
-   Observations: 19,937
-   Tuples: 10,546,673

**Challenges:** Reduce data set for downloading time computation | Indoor localization

Kaggle - Titanic survival prediction
------------------------------------

[clic to go](https://github.com/raquelredo/Projects/blob/master/Machine%20Learning/Titanic_Script.md)

It is your job to predict if a passenger survived the sinking of the Titanic or not.

-   Features: 11
-   Observations: 891
-   Tuples: 10,692

**Challenges:** Missing values Treatment | Working with text

Association with Market Basket Analysis (MBA)
---------------------------------------------

[clic to go](https://github.com/raquelredo/Projects/blob/master/Machine%20Learning/MBA_Script.md)

The main purpose is to analyze the Basket composition from purchase tickets to study how consumers buy products together. This analysis might the foundation base for a cluster customer analysis or a product system recommendation.

-   Type: list of lists
-   Observations: 9835 ticket lists

**Challenges:** Association Analysis per se

<span style="color:red">in Python
=================================

![](https://www.python.org/static/opengraph-icon-200x200.png)

Kaggle - 911 Calls
------------------

[clic to go](https://github.com/raquelredo/Projects/blob/master/Machine%20Learning/Data_Exploration.md)

The intention here is just Explore the Dataset. Put in action some Data visualization libraries and tools.

-   Features: 9
-   Observations: 205,580
-   Tuples: 1,850,220

**Challenges:** Work with different visualization tools | work with Python

LendingClub
-----------

[clic to go](https://github.com/raquelredo/Projects/blob/master/Machine%20Learning/Lendingclub_project.md)

For this project I will be exploring a public available data from [LendingClub.com](https://www.lendingclub.com/). Lending Club is a peer to peer lending platform connecting people who need money (the borrower) with people who have the money (investors). As an investor I would want to invest in people who sowed a profile of having a high probability of paying me back. I am going to create a model that will help me to predict this.

I am going to use [data](../inputs/loan_data.csv) from 2007 to 2010 and be trying to classify and predict whether or not the borrower paid back their loan in full. Webpage repository with this data set is [here](https://www.lendingclub.com/info/download-data.action)

-   Features: 18
-   Observations: 9,578
-   Tuples: 172,404

**Challenges:** ML with Python

NLP - SMS Spam detection
------------------------

[clic to go](https://github.com/raquelredo/Projects/blob/master/Machine%20Learning/Spam_detection.md)

This data set is a compendium from different sources, of SMS classified as Spam /Ham. We will need to build a model that easily can detect when a SMS is relevant or not. Similarly to what, nowadays, spam filters do, NLP tools and techniques will help to do it.

-   Observations: 5,574
-   One label + one string as feature

**Challenges:** Natural Language Processing with Python

<span style="color:red">Deep Learning
=====================================

![](https://www.polarising.com/site/wp-content/uploads/2017/04/deep-learning.png)

P01 My first Neural Network
---------------------------

[clic to go](https://github.com/raquelredo/Projects/tree/master/Deep%20Learning/P01%20First-neural-Network)

This project has been done in the context of [Udacity](https://www.udacity.com/)'s Deep Learning Nano degree. It is my first Neural Network and for that the challenges were multiple. This data set consists on information about a business bike rental. I need to build a NN to predict daily bike rental ridership.

The dataset is from UCI repository and can be downloaded [here](https://archive.ics.uci.edu/ml/datasets/Bike+Sharing+Dataset)

-   Features: 17
-   Observations: 17,380
-   Tuples: 295,460

**Challenges:** My first Neural Network, understanding the concepts: back propagation, forward pass, gradient descent and their programming the math without using any deep learning package.

Banknote authentication
-----------------------

[clic to go](https://github.com/raquelredo/Projects/tree/master/Deep%20Learning/Bank%20Authentication)

This data is the result of a Wavelet transformation on pictures of banknotes. The class to be predicted is whether the bank note has been forget or, on the contrary, it is authentic.

-   Features: 3
-   Observations: 1,372
-   Tuples: 4,116

**Challenges:** use of Tensor Flow

P02 Image Classification
------------------------

[clic to go](https://github.com/raquelredo/Projects/tree/master/Deep%20Learning/P02%20Image-classification)

In this project, I'll classify images from the [CIFAR-10 dataset](https://www.cs.toronto.edu/~kriz/cifar.html). The dataset consists of airplanes, dogs, cats, and other objects.

The CIFAR-10 dataset consists of 60000 32x32 colour images in 10 classes, with 6000 images per class. There are 50000 training images and 10000 test images.

**Challenges:** preprocess the images,build a convolutional, max pooling, dropout, and fully connected layers. Cloudcomputing using Floydhub.

P03 TV Script generation
------------------------

[clic to go](https://github.com/raquelredo/Projects/tree/master/Deep%20Learning/P03%20Script%20gen)

In this project, I'll generate my own Simpsons TV script using RNNs. I'll be using part of the Simpsons dataset of scripts from 27 seasons. The Neural Network I'll build will generate a new TV script for a scene at Moe's Tavern.

Full dataset can be found on Kaggle's database [here](https://www.kaggle.com/wcukierski/the-simpsons-by-the-data)

**Challenges:** preprocess text (tokenization, embedding), build a recurrent Neural network, work with LSTM and Word2Vec arquitectures.

P04 Language Translator
-----------------------

[clic to go](https://github.com/raquelredo/Projects/tree/master/Deep%20Learning/P04%20Translation%20Project)

In this project, I am going to take a peek into the realm of neural network machine translation. I'll be training a sequence to sequence model on a dataset of English and French sentences that can translate new sentences from English to French.

**Challenges:** build a sequence to sequence architecture

P05 Face Generation
-------------------

[clic to go](https://github.com/raquelredo/Projects/tree/master/Deep%20Learning/P05%20Face-generation)

In this project, I am going to use Generative Adversarial Networks to generate new images of faces. The input will be a bunch of celebrities images that my generator will try to imitate so a new face is created and seen by the discriminator as "Real".

**Challenges:** GAN
