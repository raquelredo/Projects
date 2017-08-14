---
title: "Lending Club"
layout: post
excerpt:  "Credit Scoring project.

-   Features: 18
-   Observations: 9,578
-   Tuples: 172,404

**Challenges:** ML with Python"
tags: [python, scoring, pandas, numpy]
header:
  teaser: scoring.jpg
link:
share: true
categories: portfolio
---

For this project I will be exploring a public available data from [LendingClub.com](https://www.lendingclub.com/).
LendingClub is a peer to peer lending platform connecting people who need money (the borrower) with people who have the money (investors). As an investor I would want to invest in people who showed a profile of having a high probability of paying me back. I am going to create a model that will help me to predict this.
I am going to use data from 2007 to 2010 and be trying to classify and predict whether or not the borrower paid back their loan in full.
I already saved a dataset with NaN treated.


```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline
```
# Read the data


```python
loans = pd.read_csv("inputs/loan_data.csv")
```


```python
loans.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 9578 entries, 0 to 9577
    Data columns (total 14 columns):
    credit.policy        9578 non-null int64
    purpose              9578 non-null object
    int.rate             9578 non-null float64
    installment          9578 non-null float64
    log.annual.inc       9578 non-null float64
    dti                  9578 non-null float64
    fico                 9578 non-null int64
    days.with.cr.line    9578 non-null float64
    revol.bal            9578 non-null int64
    revol.util           9578 non-null float64
    inq.last.6mths       9578 non-null int64
    delinq.2yrs          9578 non-null int64
    pub.rec              9578 non-null int64
    not.fully.paid       9578 non-null int64
    dtypes: float64(6), int64(7), object(1)
    memory usage: 1.0+ MB



```python
loans.describe()
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
      <th>credit.policy</th>
      <th>int.rate</th>
      <th>installment</th>
      <th>log.annual.inc</th>
      <th>dti</th>
      <th>fico</th>
      <th>days.with.cr.line</th>
      <th>revol.bal</th>
      <th>revol.util</th>
      <th>inq.last.6mths</th>
      <th>delinq.2yrs</th>
      <th>pub.rec</th>
      <th>not.fully.paid</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>9578.000000</td>
      <td>9578.000000</td>
      <td>9578.000000</td>
      <td>9578.000000</td>
      <td>9578.000000</td>
      <td>9578.000000</td>
      <td>9578.000000</td>
      <td>9.578000e+03</td>
      <td>9578.000000</td>
      <td>9578.000000</td>
      <td>9578.000000</td>
      <td>9578.000000</td>
      <td>9578.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>0.804970</td>
      <td>0.122640</td>
      <td>319.089413</td>
      <td>10.932117</td>
      <td>12.606679</td>
      <td>710.846314</td>
      <td>4560.767197</td>
      <td>1.691396e+04</td>
      <td>46.799236</td>
      <td>1.577469</td>
      <td>0.163708</td>
      <td>0.062122</td>
      <td>0.160054</td>
    </tr>
    <tr>
      <th>std</th>
      <td>0.396245</td>
      <td>0.026847</td>
      <td>207.071301</td>
      <td>0.614813</td>
      <td>6.883970</td>
      <td>37.970537</td>
      <td>2496.930377</td>
      <td>3.375619e+04</td>
      <td>29.014417</td>
      <td>2.200245</td>
      <td>0.546215</td>
      <td>0.262126</td>
      <td>0.366676</td>
    </tr>
    <tr>
      <th>min</th>
      <td>0.000000</td>
      <td>0.060000</td>
      <td>15.670000</td>
      <td>7.547502</td>
      <td>0.000000</td>
      <td>612.000000</td>
      <td>178.958333</td>
      <td>0.000000e+00</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>1.000000</td>
      <td>0.103900</td>
      <td>163.770000</td>
      <td>10.558414</td>
      <td>7.212500</td>
      <td>682.000000</td>
      <td>2820.000000</td>
      <td>3.187000e+03</td>
      <td>22.600000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>1.000000</td>
      <td>0.122100</td>
      <td>268.950000</td>
      <td>10.928884</td>
      <td>12.665000</td>
      <td>707.000000</td>
      <td>4139.958333</td>
      <td>8.596000e+03</td>
      <td>46.300000</td>
      <td>1.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>1.000000</td>
      <td>0.140700</td>
      <td>432.762500</td>
      <td>11.291293</td>
      <td>17.950000</td>
      <td>737.000000</td>
      <td>5730.000000</td>
      <td>1.824950e+04</td>
      <td>70.900000</td>
      <td>2.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>max</th>
      <td>1.000000</td>
      <td>0.216400</td>
      <td>940.140000</td>
      <td>14.528354</td>
      <td>29.960000</td>
      <td>827.000000</td>
      <td>17639.958330</td>
      <td>1.207359e+06</td>
      <td>119.000000</td>
      <td>33.000000</td>
      <td>13.000000</td>
      <td>5.000000</td>
      <td>1.000000</td>
    </tr>
  </tbody>
</table>
</div>


```python
loans.head(5)
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
      <th>credit.policy</th>
      <th>purpose</th>
      <th>int.rate</th>
      <th>installment</th>
      <th>log.annual.inc</th>
      <th>dti</th>
      <th>fico</th>
      <th>days.with.cr.line</th>
      <th>revol.bal</th>
      <th>revol.util</th>
      <th>inq.last.6mths</th>
      <th>delinq.2yrs</th>
      <th>pub.rec</th>
      <th>not.fully.paid</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>debt_consolidation</td>
      <td>0.1189</td>
      <td>829.10</td>
      <td>11.350407</td>
      <td>19.48</td>
      <td>737</td>
      <td>5639.958333</td>
      <td>28854</td>
      <td>52.1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>credit_card</td>
      <td>0.1071</td>
      <td>228.22</td>
      <td>11.082143</td>
      <td>14.29</td>
      <td>707</td>
      <td>2760.000000</td>
      <td>33623</td>
      <td>76.7</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1</td>
      <td>debt_consolidation</td>
      <td>0.1357</td>
      <td>366.86</td>
      <td>10.373491</td>
      <td>11.63</td>
      <td>682</td>
      <td>4710.000000</td>
      <td>3511</td>
      <td>25.6</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1</td>
      <td>debt_consolidation</td>
      <td>0.1008</td>
      <td>162.34</td>
      <td>11.350407</td>
      <td>8.10</td>
      <td>712</td>
      <td>2699.958333</td>
      <td>33667</td>
      <td>73.2</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1</td>
      <td>credit_card</td>
      <td>0.1426</td>
      <td>102.92</td>
      <td>11.299732</td>
      <td>14.97</td>
      <td>667</td>
      <td>4066.000000</td>
      <td>4740</td>
      <td>39.5</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>


# Exploratory Data Analysis

I will, first create some histograms of FICO distributions.

A FICO score is a type of credit score created by the Fair Isaac Corporation. Lenders use borrowers' FICO scores along with other details on borrowers' credit reports to assess credit risk and determine whether to extend credit. FICO scores take into account various factors in five areas to determine credit worthiness: payment history, current level of indebtedness, types of credit used, length of credit history and new credit accounts.

Read more: FICO Score http://www.investopedia.com/terms/f/ficoscore.asp#ixzz4lBW0yxF0


```python
plt.figure(figsize = (10, 6)) #Canvas
loans[loans["credit.policy"]==1]["fico"].hist(alpha = 0.5, color = "blue", bins = 30, label = "Credit Policy 1")
loans[loans["credit.policy"]==0]["fico"].hist(alpha = 0.5, color = "red", bins = 30, label = "Credit Policy 0")
```

![](/Lendingclub_project_9_1.png)


Now, I will do similar for `not.fully.paid`column


```python
plt.figure(figsize = (10, 6)) #Canvas
loans[loans["not.fully.paid"]==1]["fico"].hist(alpha = 0.5, color = "blue", bins = 30, label = "Not fully paid 1")
loans[loans["not.fully.paid"]==0]["fico"].hist(alpha = 0.5, color = "red", bins = 30, label = "Not fully paid 0")
```


![](/Lendingclub_project_11_1.png)


Let's talk about countplots


```python
plt.figure(figsize = (11, 7))
sns.countplot(x = "purpose", hue = "not.fully.paid", data = loans, palette = "Set1")
```

![](/Lendingclub_project_13_1.png)

Let's see the trend between FICO score and interest rate.

```python
sns.jointplot( x= "fico", y = "int.rate", data = loans, color = "purple")
```


![](/Lendingclub_project_15_1.png)


```python
plt.figure(figsize = (11,7))
sns.lmplot( y = "int.rate", x = "fico", data = loans, hue = "credit.policy", col = "not.fully.paid", palette = "Set1")
```

![](/Lendingclub_project_16_2.png)


# Setting up the Data


```python
loans.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 9578 entries, 0 to 9577
    Data columns (total 14 columns):
    credit.policy        9578 non-null int64
    purpose              9578 non-null object
    int.rate             9578 non-null float64
    installment          9578 non-null float64
    log.annual.inc       9578 non-null float64
    dti                  9578 non-null float64
    fico                 9578 non-null int64
    days.with.cr.line    9578 non-null float64
    revol.bal            9578 non-null int64
    revol.util           9578 non-null float64
    inq.last.6mths       9578 non-null int64
    delinq.2yrs          9578 non-null int64
    pub.rec              9578 non-null int64
    not.fully.paid       9578 non-null int64
    dtypes: float64(6), int64(7), object(1)
    memory usage: 1.0+ MB


The `purpose`column is categorical. We need to apply some transformation so sklearn would be able to understand them.


```python
cat_feat = ["purpose"] #to create a list of categorical values
```


```python
final_data = pd.get_dummies(loans, columns = cat_feat, drop_first = True)
```


```python
final_data.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 9578 entries, 0 to 9577
    Data columns (total 19 columns):
    credit.policy                 9578 non-null int64
    int.rate                      9578 non-null float64
    installment                   9578 non-null float64
    log.annual.inc                9578 non-null float64
    dti                           9578 non-null float64
    fico                          9578 non-null int64
    days.with.cr.line             9578 non-null float64
    revol.bal                     9578 non-null int64
    revol.util                    9578 non-null float64
    inq.last.6mths                9578 non-null int64
    delinq.2yrs                   9578 non-null int64
    pub.rec                       9578 non-null int64
    not.fully.paid                9578 non-null int64
    purpose_credit_card           9578 non-null uint8
    purpose_debt_consolidation    9578 non-null uint8
    purpose_educational           9578 non-null uint8
    purpose_home_improvement      9578 non-null uint8
    purpose_major_purchase        9578 non-null uint8
    purpose_small_business        9578 non-null uint8
    dtypes: float64(6), int64(7), uint8(6)
    memory usage: 1.0 MB


# Split


```python
from sklearn.model_selection import train_test_split
X = final_data.drop("not.fully.paid", axis = 1) #all features bu<t the one to predict
y = final_data["not.fully.paid"] #value to predict
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.30, random_state = 123)
```

# Training a Decision Tree Model


```python
from sklearn.tree import DecisionTreeClassifier
```

Create an instance of DecisionTreeClassifier() called dtree and fit it to the training data.


```python
dtree = DecisionTreeClassifier()
```


```python
dtree.fit(X_train, y_train)
```


    DecisionTreeClassifier(class_weight=None, criterion='gini', max_depth=None,
                max_features=None, max_leaf_nodes=None,
                min_impurity_split=1e-07, min_samples_leaf=1,
                min_samples_split=2, min_weight_fraction_leaf=0.0,
                presort=False, random_state=None, splitter='best')



Predictions and Evaluation of Decision Tree¶
Create predictions from the test set and create a classification report and a confusion matrix.


```python
predictions = dtree.predict(X_test)
```


```python
from sklearn.metrics import classification_report,confusion_matrix
```


```python
print(classification_report(y_test,predictions))
```

                 precision    recall  f1-score   support

              0       0.85      0.84      0.84      2394
              1       0.24      0.26      0.25       480

    avg / total       0.75      0.74      0.74      2874



# Training the Random Forest model
Now its time to train our model!
Create an instance of the RandomForestClassifier class and fit it to our training data from the previous step.


```python
from sklearn.ensemble import RandomForestClassifier
```


```python
rfc = RandomForestClassifier(n_estimators=600)
```


```python
rfc.fit(X_train,y_train)
```




    RandomForestClassifier(bootstrap=True, class_weight=None, criterion='gini',
                max_depth=None, max_features='auto', max_leaf_nodes=None,
                min_impurity_split=1e-07, min_samples_leaf=1,
                min_samples_split=2, min_weight_fraction_leaf=0.0,
                n_estimators=600, n_jobs=1, oob_score=False, random_state=None,
                verbose=0, warm_start=False)



# Predictions and Evaluation
Let's predict off the y_test values and evaluate the model.
Predict the class of not.fully.paid for the X_test data.


```python
predictions = rfc.predict(X_test)
```

Now create a classification report from the results.


```python
from sklearn.metrics import classification_report,confusion_matrix
```


```python
print(classification_report(y_test,predictions))
```

                 precision    recall  f1-score   support

              0       0.84      1.00      0.91      2394
              1       0.75      0.03      0.05       480

    avg / total       0.82      0.84      0.77      2874



Show the Confusion Matrix for the predictions.


```python
print(confusion_matrix(y_test,predictions))
```

    [[2390    4]
     [ 468   12]]
