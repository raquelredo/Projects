---
title: "Spam detection"
layout: post
excerpt: "The identification of the text of spam messages in the claims is a very hard and time-consuming task. Can we build a model to detect when a message is ham or spam?
This data set is a compendium from different sources, of SMS classified as Spam /Ham. We will need to build a model that easily can detect when a SMS is relevant or not. Similarly to what, nowadays, spam filters do, NLP tools and techniques will help to do it.

-   Observations: 5,574
-   One label + one string as feature

**Challenges:** Natural Language Processing with Python"
tags: [python, spam, corpus, text processing]
header:
  teaser: spam.jpg
link:
share: true
categories: portfolio
---
This dataset can be downloaded [here](https://archive.ics.uci.edu/ml/datasets/sms+spam+collection)

## Data

5,574 instances

## Source
Tiago A. Almeida (talmeida ufscar.br) Department of Computer Science Federal University of Sao Carlos (UFSCar) Sorocaba, Sao Paulo - Brazil

José María Gómez Hidalgo (jmgomezh yahoo.es) R&D Department Optenet Las Rozas, Madrid - Spain

## Data Set Information

This corpus has been collected from free or free for research sources at the Internet:

1.  A collection of 425 SMS spam messages was manually extracted from the Grumbletext Web site. This is a UK forum in which cell phone users make public claims about SMS spam messages, most of them without reporting the very spam message received. The identification of the text of spam messages in the claims is a very hard and time-consuming task, and it involved carefully scanning hundreds of web pages. The Grumbletext Web site is: [Web Link](http://www.grumbletext.co.uk/).
2.  A subset of 3,375 SMS randomly chosen ham messages of the NUS SMS Corpus (NSC), which is a dataset of about 10,000 legitimate messages collected for research at the Department of Computer Science at the National University of Singapore. The messages largely originate from Singaporeans and mostly from students attending the University. These messages were collected from volunteers who were made aware that their contributions were going to be made publicly available. The NUS SMS Corpus is avalaible at [Web Link](http://www.comp.nus.edu.sg/~rpnlpir/downloads/corpora/smsCorpus/).
3.  A list of 450 SMS ham messages collected from Caroline Tag's PhD Thesis available at [Web Link](http://etheses.bham.ac.uk/253/1/Tagg09PhD.pdf).
4.  Finally, we have incorporated the SMS Spam Corpus v.0.1 Big. It has 1,002 SMS ham messages and 322 spam messages and it is public available at: [Web Link](http://www.esp.uem.es/jmgomez/smsspamcorpus/).

## Format

The files contain one message per line. Each line is composed by two columns: one with label (ham or spam) and other with the raw text. Here are some examples:

-   ham What you doing?how are you?
-   ham Ok lar... Joking wif u oni...
-   ham dun say so early hor... U c already then say...
-   ham MY NO. IN LUTON 0125698789 RING ME IF UR AROUND! H\*
-   ham Siva is in hostel aha:-.
-   ham Cos i was out shopping wif darren jus now n i called him 2 ask wat present he wan lor. Then he started guessing who i was wif n he finally guessed darren lor.
-   spam FreeMsg: Txt: CALL to No: 86888 & claim your reward of 3 hours talk time to use from your phone now! ubscribe6GBP/ mnth inc 3hrs 16 stop?txtStop
-   spam Sunshine Quiz! Win a super Sony DVD recorder if you canname the capital of Australia? Text MQUIZ to 82277. B
-   spam URGENT! Your Mobile No 07808726822 was awarded a L2,000 Bonus Caller Prize on 02/09/03! This is our 2nd attempt to contact YOU! Call 0871-872-9758 BOX95QU

Note: messages are not chronologically sorted.

# NLP for filtering Spam SMS

```python
import pandas as pd
```


```python
messages = pd.read_csv("smsspamcollection/SMSSpamCollection",
                       sep ="\t", names = ["label", "message"])
```


```python
messages.head()
```



<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>label</th>
      <th>message</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ham</td>
      <td>Go until jurong point, crazy.. Available only ...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>ham</td>
      <td>Ok lar... Joking wif u oni...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>spam</td>
      <td>Free entry in 2 a wkly comp to win FA Cup fina...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>ham</td>
      <td>U dun say so early hor... U c already then say...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>ham</td>
      <td>Nah I don't think he goes to usf, he lives aro...</td>
    </tr>
  </tbody>
</table>
</div>



# Exploratory Data Analysis


```python
messages.groupby("label").describe()
```


<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th colspan="4" halign="left">message</th>
    </tr>
    <tr>
      <th></th>
      <th>count</th>
      <th>unique</th>
      <th>top</th>
      <th>freq</th>
    </tr>
    <tr>
      <th>label</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>ham</th>
      <td>4825</td>
      <td>4516</td>
      <td>Sorry, I'll call later</td>
      <td>30</td>
    </tr>
    <tr>
      <th>spam</th>
      <td>747</td>
      <td>653</td>
      <td>Please call our customer service representativ...</td>
      <td>4</td>
    </tr>
  </tbody>
</table>
</div>



Let's do some feature engineering and make a new column to detect how long the text message is'

```python
messages["length"] = messages["message"].apply(len)
```


```python
messages.head()
```


<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>label</th>
      <th>message</th>
      <th>length</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ham</td>
      <td>Go until jurong point, crazy.. Available only ...</td>
      <td>111</td>
    </tr>
    <tr>
      <th>1</th>
      <td>ham</td>
      <td>Ok lar... Joking wif u oni...</td>
      <td>29</td>
    </tr>
    <tr>
      <th>2</th>
      <td>spam</td>
      <td>Free entry in 2 a wkly comp to win FA Cup fina...</td>
      <td>155</td>
    </tr>
    <tr>
      <th>3</th>
      <td>ham</td>
      <td>U dun say so early hor... U c already then say...</td>
      <td>49</td>
    </tr>
    <tr>
      <th>4</th>
      <td>ham</td>
      <td>Nah I don't think he goes to usf, he lives aro...</td>
      <td>61</td>
    </tr>
  </tbody>
</table>
</div>


# Data visualization


```python
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline
```
```python
messages["length"].plot(bins = 40, kind = "hist")
```

![](/Spam%20detection_11_1.png)


```python
messages.length.describe()
```


    count    5572.000000
    mean       80.489950
    std        59.942907
    min         2.000000
    25%        36.000000
    50%        62.000000
    75%       122.000000
    max       910.000000
    Name: length, dtype: float64


910 characters!!! I need to see this message


```python
messages[messages["length"]==910]["message"].iloc[0]
```

    "For me the love should start with attraction.i should feel that I need her every time around me.she should be the first thing which comes in my thoughts.I would start the day and end it with her.she should be there every time I dream.love will be then when my every breath has her name.my life should happen around her.my life will be named to her.I would cry for her.will give all my happiness and take all her sorrows.I will be ready to fight with anyone for her.I will be in love when I will be doing the craziest things for her.love will be when I don't have to proove anyone that my girl is the most beautiful lady on the whole planet.I will always be singing praises for her.love will be when I start up making chicken curry and end up makiing sambar.life will be the most beautiful then.will get every morning and thank god for the day because she is with me.I would like to say a lot..will tell later.."


```python
messages.hist(column = "length", by = "label", bins = 50, figsize = (12, 4))
```
![](/Spam%20detection_15_1.png)


It seems that chances that a message is spam are bigger when the string length is longer

# Text pre-processing

First step will be writting a function that will split a message into its individual words and return a list. I will also remove very common words ("the", "a", etc...). For this,  will use NLTK library.


```python
import string
from nltk.corpus import stopwords
```


```python
stopwords.words("english")[0:10]#explore some stopwords
```

    ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your']


```python
string.punctuation
```


    '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'


```python
def text_process(mess):
    #Check characters to see if there are punctuation
    nopunc = [char for char in mess if char not in string.punctuation]

    #Join the characters again
    nopunc = "".join(nopunc)

    #Remove stopwords
    return [word for word in nopunc.split() if word.lower() not in stopwords.words ("english")]
```

Now, I need to tokenize the terms. We are creating "lemmas".


```python
messages["message"].head(5).apply(text_process)
```


    0    [Go, jurong, point, crazy, Available, bugis, n...
    1                       [Ok, lar, Joking, wif, u, oni]
    2    [Free, entry, 2, wkly, comp, win, FA, Cup, fin...
    3        [U, dun, say, early, hor, U, c, already, say]
    4    [Nah, dont, think, goes, usf, lives, around, t...
    Name: message, dtype: object



# Vectorization

Now, that we already have lemmas, we need to convert each of those messages into a vector to work with. It is donde in 3 steps:

1.Term frequency. Which is counting how many times a word ocurr in each message.
2.Inverse Term frequency. Weight the count, so that frequent tokens get lower weight. Contrary to what intuation might suggest, most frequent words ("I", "a",...) are the less important giving meaning to the string.
3. Normalize the vectors to unit length, to abstract from the originanl text.

Let's begin!


```python
from sklearn.feature_extraction.text import CountVectorizer
```


```python
bow_transformer = CountVectorizer(analyzer = text_process).fit(messages["message"])

#Print total number of vocab words
print(len(bow_transformer.vocabulary_))
```

    11425


Let's take on text message and get its bag-of-words counts as a vector, putting to use our new `bow_transformer`


```python
message4 = messages["message"][3]
print(message4)
```

    U dun say so early hor... U c already then say...


Now, its vector representation


```python
bow4 = bow_transformer.transform([message4])
print(bow4)
print(bow4.shape)
```

      (0, 4068)	2
      (0, 4629)	1
      (0, 5261)	1
      (0, 6204)	1
      (0, 6222)	1
      (0, 7186)	1
      (0, 9554)	2
    (1, 11425)


this means, there are 7 unqiue words in this message after removing stop words. Two of them appear twice and the rest just once.
Let's generalize!


```python
messages_bow = bow_transformer.transform(messages["message"])
```


```python
print("Shape of Sparse matrix: ", messages_bow.shape)
print("Amount of Non-Zero ocurrences ", messages_bow.nnz)
```

    Shape of Sparse matrix:  (5572, 11425)
    Amount of Non-Zero ocurrences  50548



```python
sparsity = (100.0 * messages_bow.nnz / (messages_bow.shape[0] * messages_bow.shape[1]))
print("sparsity {}".format(round(sparsity)))
```

    sparsity 0


After counting normalization can be done with TF-IDF (Term Frequency- Inverse document frequency)


```python
from sklearn.feature_extraction.text import TfidfTransformer
```


```python
tfid_transformer = TfidfTransformer().fit(messages_bow)
```


```python
print(tfid_transformer.idf_[bow_transformer.vocabulary_["u"]]) #check word "u" frequency
print(tfid_transformer.idf_[bow_transformer.vocabulary_["university"]]) #check word "university" frequency
```

    3.28005242674
    8.5270764989


transforming, now, the entire bag of words...


```python
messages_tfidf = tfid_transformer.transform(messages_bow)
print(messages_tfidf.shape)
```

    (5572, 11425)


# Training a model

I am going to use Naive Bayes classifier algorithm. It seems to me that it is a good choice as at the end we need a good way to compute chances (probability), of classifying as spam | ham.


```python
from sklearn.naive_bayes import MultinomialNB
```


```python
spam_detect_model = MultinomialNB().fit(messages_tfidf, messages["label"])
```

# Model Evaluation


```python
all_predictions = spam_detect_model.predict(messages_tfidf)
print(all_predictions)
```

    ['ham' 'ham' 'spam' ..., 'ham' 'ham' 'ham']



```python
from sklearn.metrics import classification_report
```


```python
print (classification_report(messages["label"], all_predictions))
```

                 precision    recall  f1-score   support

            ham       0.98      1.00      0.99      4825
           spam       1.00      0.85      0.92       747

    avg / total       0.98      0.98      0.98      5572



Not bad! but as I did not train/test the model, it is not clear if it is overfitted and the model just learn its way or for the contrary, we have a pretty good model to predict ham/Spam. Because of that I am going to repeat the model

# Train Test split


```python
from sklearn.model_selection import train_test_split
```


```python
msg_train, msg_test, label_train, label_test = train_test_split(messages["message"],
                                                               messages["label"], test_size = 0.3)
```


```python
print(len(msg_train), len(msg_test), len(msg_train) + len(msg_test) )
```

    3900 1672 5572


# Create a pipeline


```python
from sklearn.pipeline import Pipeline

pipeline = Pipeline([
    ('bow', CountVectorizer(analyzer=text_process)),  # strings to token integer counts
    ('tfidf', TfidfTransformer()),  # integer counts to weighted TF-IDF scores
    ('classifier', MultinomialNB()),  # train on TF-IDF vectors w/ Naive Bayes classifier
])
```


```python
pipeline.fit(msg_train,label_train)
```

```python
predictions = pipeline.predict(msg_test)
```


```python
print(classification_report(predictions,label_test))
```

                 precision    recall  f1-score   support

            ham       1.00      0.96      0.98      1527
           spam       0.71      1.00      0.83       145

    avg / total       0.98      0.97      0.97      1672




```python

```

Done!
