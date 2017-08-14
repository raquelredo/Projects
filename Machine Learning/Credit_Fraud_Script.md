---
title: "Credit Card Fault detection"
layout: post
excerpt: "Are we able to predict credit card fraud in online transactions?
Anonymized credit card transactions labeled as fraudulent or genuine. Anonymization has been achieved performing Principal Component Analysis. 492 frauds out of 284,807 transactions.

-   Features: 30
-   Observations: 284,807
-   Tuples: 8,544,210

**Challenges:** Imbalanced data | Understanding PCA"
tags: [R, dplyr, ggplot2, unbalanced data, fraud, logistic, tree, AUC, kaggle]
header:
  teaser: fraud_cc.png
categories: portfolio
link:
share: true
comments: false
date: 13-08-2017
---
## Dataset
Anonymized credit card transactions labelled as fraudulent or genuine.
Dataset can be downloaded from Kaggle site in the following [link. ][4e2f2e50]

  [4e2f2e50]: https://www.kaggle.com/dalpozz/creditcardfraud/downloads/creditcard.csv.zip "dataset"

## Description
The datasets contains transactions made by credit cards in September 2013 by European cardholders. This dataset presents transactions that occurred in two days, where we have 492 frauds out of 284,807 transactions. The dataset is highly unbalanced, the positive class (frauds) account for 0.172% of all transactions.

It contains only numerical input variables which are the result of a PCA transformation. Unfortunately, due to confidentiality issues, they cannot provide the original features and more background information about the data. Features V1, V2, ... V28 are the principal components obtained with PCA, the only features which have not been transformed with PCA are 'Time' and 'Amount'. Feature 'Time' contains the seconds elapsed between each transaction and the first transaction in the dataset. The feature 'Amount' is the transaction Amount, this feature can be used for example-dependant cost-sensitive learning. Feature 'Class' is the response variable and it takes value 1 in case of fraud and 0 otherwise.

Given the class imbalance ratio, we recommend measuring the accuracy using the Area Under the Precision-Recall Curve (AUPRC). Confusion matrix accuracy is not meaningful for unbalanced classification.

The dataset has been collected and analysed during a research collaboration of Worldline and [the Machine Learning Group ][3c08bc65] of ULB (Université Libre de Bruxelles) on big data mining and fraud detection. More details on current and past projects on related topics are available on [ http://mlg.ulb.ac.be/BruFence](http://mlg.ulb.ac.be/BruFence) and [http://mlg.ulb.ac.be/ARTML](http://mlg.ulb.ac.be/ARTML)

  [3c08bc65]: (http://mlg.ulb.ac.be) "The Machine Learning Group"

Please cite: Andrea Dal Pozzolo, Olivier Caelen, Reid A. Johnson and Gianluca Bontempi. Calibrating Probability with Undersampling for Unbalanced Classification. In Symposium on Computational Intelligence and Data Mining (CIDM), IEEE, 2015
Database released under Open Database License, individual contents under Database Contents License.

 Feature | Description | Type
-------- | --------------------------------------------- | ---------
Time  | Seconds Elapsed from first transaction | Numeric
V1 to V28  | Anonymized information with PCA applied | Numeric
Amount | Transaction Amount | Numeric
Class | The actual classification classes (boolean 0 or 1) | Numeric

I will start loading the libraries needed:

``` r
library(dplyr) # To use filter
library(caret)
library(ggplot2)
library(MLmetrics) # To compute AUC
library(e1071) #for cotrl1
library(unbalanced) #handle imbalanced class
library(tidyr)
library(Amelia) # library to search for Missing Values (MV)
library(corrplot) #for correlation matrix
library(C50) # for model tree prediction
```

Then, let's load the data:

``` r
data <- read.csv(file = "creditcard.csv", na.strings = c("NA","NULL",""))
head(data)
```

    ##   Time         V1          V2        V3         V4          V5          V6
    ## 1    0 -1.3598071 -0.07278117 2.5363467  1.3781552 -0.33832077  0.46238778
    ## 2    0  1.1918571  0.26615071 0.1664801  0.4481541  0.06001765 -0.08236081
    ## 3    1 -1.3583541 -1.34016307 1.7732093  0.3797796 -0.50319813  1.80049938
    ## 4    1 -0.9662717 -0.18522601 1.7929933 -0.8632913 -0.01030888  1.24720317
    ## 5    2 -1.1582331  0.87773675 1.5487178  0.4030339 -0.40719338  0.09592146
    ## 6    2 -0.4259659  0.96052304 1.1411093 -0.1682521  0.42098688 -0.02972755
    ##            V7          V8         V9         V10        V11         V12
    ## 1  0.23959855  0.09869790  0.3637870  0.09079417 -0.5515995 -0.61780086
    ## 2 -0.07880298  0.08510165 -0.2554251 -0.16697441  1.6127267  1.06523531
    ## 3  0.79146096  0.24767579 -1.5146543  0.20764287  0.6245015  0.06608369
    ## 4  0.23760894  0.37743587 -1.3870241 -0.05495192 -0.2264873  0.17822823
    ## 5  0.59294075 -0.27053268  0.8177393  0.75307443 -0.8228429  0.53819555
    ## 6  0.47620095  0.26031433 -0.5686714 -0.37140720  1.3412620  0.35989384
    ##          V13        V14        V15        V16         V17         V18
    ## 1 -0.9913898 -0.3111694  1.4681770 -0.4704005  0.20797124  0.02579058
    ## 2  0.4890950 -0.1437723  0.6355581  0.4639170 -0.11480466 -0.18336127
    ## 3  0.7172927 -0.1659459  2.3458649 -2.8900832  1.10996938 -0.12135931
    ## 4  0.5077569 -0.2879237 -0.6314181 -1.0596472 -0.68409279  1.96577500
    ## 5  1.3458516 -1.1196698  0.1751211 -0.4514492 -0.23703324 -0.03819479
    ## 6 -0.3580907 -0.1371337  0.5176168  0.4017259 -0.05813282  0.06865315
    ##           V19         V20          V21          V22         V23
    ## 1  0.40399296  0.25141210 -0.018306778  0.277837576 -0.11047391
    ## 2 -0.14578304 -0.06908314 -0.225775248 -0.638671953  0.10128802
    ## 3 -2.26185710  0.52497973  0.247998153  0.771679402  0.90941226
    ## 4 -1.23262197 -0.20803778 -0.108300452  0.005273597 -0.19032052
    ## 5  0.80348692  0.40854236 -0.009430697  0.798278495 -0.13745808
    ## 6 -0.03319379  0.08496767 -0.208253515 -0.559824796 -0.02639767
    ##           V24        V25        V26          V27         V28 Amount Class
    ## 1  0.06692807  0.1285394 -0.1891148  0.133558377 -0.02105305 149.62     0
    ## 2 -0.33984648  0.1671704  0.1258945 -0.008983099  0.01472417   2.69     0
    ## 3 -0.68928096 -0.3276418 -0.1390966 -0.055352794 -0.05975184 378.66     0
    ## 4 -1.17557533  0.6473760 -0.2219288  0.062722849  0.06145763 123.50     0
    ## 5  0.14126698 -0.2060096  0.5022922  0.219422230  0.21515315  69.99     0
    ## 6 -0.37142658 -0.2327938  0.1059148  0.253844225  0.08108026   3.67     0

## Missing Data
The first thing I like to know is if there are missing values in my dataset. I love Amelia package as it gives me the answer pretty quickly.

``` r
missmap(data)
```

![](/CF-Missing%20V-1.png)

Class should be a factor, not a type number.

``` r
# Changing Class type to factor
data$Class <- as.factor(data$Class)
str(data$Class)
```

    ##  Factor w/ 2 levels "0","1": 1 1 1 1 1 1 1 1 1 1 ...

The dataset information already warns about the unbalanced values of the class. Let's take a look!

``` r
# Frequency table (in%)
round(table(data$Class)/nrow(data)*100, 2)
```

    ##
    ##     0     1
    ## 99.83  0.17

# Correlation
PCA process already solves the problem for correlation between the V columns. I want to check if between Time and Amount exists correlation.

``` r
m <- cor(data[c("Time", "Amount")])
corrplot(m, method = "square", type = "lower")
```

![](/CF-correlation-1.png) We can keep both variables if we need them.

# Data visualization

## Pre-preprocess

For DATA visualization I will keep the original data frame Principal Component Analysis (PCA) shows the transformed original values finding a linear correlation between them. The final transformed featured are ordered from explaining most of the variance to explaining less to the variance. In other words and in short, our new columns are ordered from most important to less important.

As new features, are less and less important we want to reduce the "noise" introduced by the less important values. As a rule of a thumb variables explaining 80% of the variance can make a better model. I want to find how many features I should pick to build my models.

``` r
variance <- as.vector(apply(data[2:29], 2, var))
p_var <- variance / sum(variance)*100
cs <- as.vector(cumsum(p_var))
cs
```

    ##  [1]  12.48376  21.35670  28.83764  35.36078  41.55983  47.33542  52.31527
    ##  [8]  56.95697  60.88447  64.74233  68.13248  71.38124  74.60451  77.59459
    ## [15]  80.32076  82.81921  85.16652  87.45255  89.60882  91.54273  93.29832
    ## [22]  95.01199  96.28087  97.47445  98.35865  99.11533  99.64547 100.00000

So, the first 15 components will give us enough information to build a good model.

``` r
# We now change the "0" and "1" in Class because it will give problems later.
data_n <- mutate(data_n, Class = ifelse(Class == "0", "No", "Yes"))
```

## Histograms
These function will give us all the histograms in a clic:

``` r
# Some plots with ggplot
variables <- colnames(data_n)[2:16]

for (i in seq_along(variables)) {
  n <- ggplot(data=data_n, aes_string(x=variables[i]))
  h <- geom_histogram(bins = 50, alpha=0.3, aes(y=..density.., fill=Class))
  d <- stat_density(geom="line",aes(color=Class)) # no geom_density because it leaves a baseline
  print(n+h+d)
  ggsave(n+h+d, filename=paste("plot_", variables[i], ".png", sep=""))
  dev.off()
}
```
All plots are saved in my working directory. But let's show one of them.

![](\CF-plot_V11.png)

# Building the model

First step is building our training and testing datasets.

``` r
#### Dividing the data into training/test with 0.7/0.3
set.seed(123)
index <- createDataPartition(data_n$Class, p = 0.7, list=F)
TrSet <- data_n[index, ]
TrSet <- mutate(TrSet, Class = ifelse(Class == "Yes", 1, 0))#we neet TrSet as 0-1 for oversampling
TeSet <- data_n[-index,]
table(TrSet$Class)
```

    ##
    ##      0      1
    ## 199021    345

``` r
table(TeSet$Class)
```

    ##
    ##    No   Yes
    ## 85294   147

## Oversampling
We want to use Logistic regression and model trees as both are best methods for binary Class predictions. However, these methods will treat as "noise" values that occur less frequently. One way to solve this situation is oversampling the minority class. Oversampling Fraud cases up to 25% percent will give us more balance to the variable to predict without introducing too many repeated records.

``` r
#oversampling to improve prediction because imbalanced class
set.seed(1234)
output<-as.factor(TrSet$Class)
input<-as.vector(TrSet[ ,-18])
data1 <- ubOver(X = input, Y= output, k= 185)
TrSet <- data.frame(data1$X, Class= data1$Y)

# We now change the "0" and "1" in Class because it will give problems later.
TrSet <- mutate(TrSet, Class = ifelse(Class == "0", "No", "Yes"))
```

let's check the transformation...

``` r
#New data % frequency table
round(table(TrSet$Class)/nrow(TrSet)*100, 2)
```

    ##
    ##    No   Yes
    ## 75.72 24.28

## Logistic Regresion

I will Create my tunning parameters, 10 folder Cross Validation, and `my_metric` to choose model (AUC).

``` r
ctrl0 <- trainControl(method = "cv",
                      number = 10,
                      summaryFunction = twoClassSummary,
                      classProbs = T,
                      allowParallel = T)
my_metric = "AUC"
```

**with 15 PCA's features**


``` r
t0 <- proc.time()
model_Lgm01 <- caret::train(Class ~.-Time -Amount,
                     data = TrSet,
                     method="glm",
                     family= binomial(link = "logit"),
                     metric = my_metric,
                     trControl = ctrl0)
tf <- proc.time() - t0
tf
```

    ##    user  system elapsed
    ##   81.88    9.80   98.15

``` r
model_Lgm01
```

    ## Generalized Linear Model
    ##
    ## 262846 samples
    ##     17 predictor
    ##      2 classes: 'No', 'Yes'
    ##
    ## No pre-processing
    ## Resampling: Cross-Validated (10 fold)
    ## Summary of sample sizes: 236562, 236561, 236562, 236561, 236562, 236561, ...
    ## Resampling results:
    ##
    ##   ROC        Sens       Spec
    ##   0.9840832  0.9915034  0.8933178

**with 10 PCA's features**


``` r
t0 <- proc.time()
model_Lgm02 <- caret::train(Class ~ +V1+V2+V3+V4+V5+V6+V7+V8+V9+V10,
                     data = TrSet,
                     method="glm",
                     family= binomial(link = "logit"),
                     metric = my_metric,
                     trControl = ctrl0)
tf <- proc.time() - t0
tf
```

    ##    user  system elapsed
    ##   57.04    8.83   71.26

``` r
model_Lgm02
```

    ## Generalized Linear Model
    ##
    ## 262846 samples
    ##     10 predictor
    ##      2 classes: 'No', 'Yes'
    ##
    ## No pre-processing
    ## Resampling: Cross-Validated (10 fold)
    ## Summary of sample sizes: 236562, 236560, 236561, 236561, 236562, 236562, ...
    ## Resampling results:
    ##
    ##   ROC        Sens       Spec
    ##   0.9726635  0.9899156  0.8672308

**With all the features**

``` r
t0 <- proc.time()
model_Lgm03 <- caret::train(Class ~. ,
                     data = TrSet,
                     method = "glm",
                     family = binomial(link = "logit"),
                     metric = my_metric,
                     trControl = ctrl0)
tf <- proc.time() - t0
tf
```

    ##    user  system elapsed
    ##   72.03   10.31   84.51

``` r
model_Lgm03
```

    ## Generalized Linear Model
    ##
    ## 262846 samples
    ##     17 predictor
    ##      2 classes: 'No', 'Yes'
    ##
    ## No pre-processing
    ## Resampling: Cross-Validated (10 fold)
    ## Summary of sample sizes: 236561, 236561, 236561, 236561, 236562, 236562, ...
    ## Resampling results:
    ##
    ##   ROC        Sens       Spec
    ##   0.9856594  0.9908251  0.8933178

**Predictions with our logistic models**

``` r
pred_Lgm01 <- predict(model_Lgm01, TeSet)
pred_Lgm02 <- predict(model_Lgm02, TeSet)
pred_Lgm03 <- predict(model_Lgm03, TeSet)
```

## Trees

**with 15 PCA's features**

``` r
t0 <- proc.time()
model_t01 <- caret::train(Class ~. -Time -Amount,
                     data = TrSet,
                     method = "C5.0",
                     metric = my_metric,
                     trControl = ctrl0)
tf <- proc.time() - t0
tf
```

    ##     user   system  elapsed
    ## 10244.86    21.33 10383.34

``` r
model_t01
```

    ## C5.0
    ##
    ## 262846 samples
    ##     17 predictor
    ##      2 classes: 'No', 'Yes'
    ##
    ## No pre-processing
    ## Resampling: Cross-Validated (10 fold)
    ## Summary of sample sizes: 236561, 236562, 236562, 236561, 236562, 236560, ...
    ## Resampling results across tuning parameters:
    ##
    ##   model  winnow  trials  ROC        Sens       Spec
    ##   rules  FALSE    1      0.9996447  0.9990554  1
    ##   rules  FALSE   10      0.9999734  0.9998292  1
    ##   rules  FALSE   20      0.9999885  0.9998191  1
    ##   rules   TRUE    1      0.9996447  0.9990554  1
    ##   rules   TRUE   10      0.9999734  0.9998292  1
    ##   rules   TRUE   20      0.9999885  0.9998191  1
    ##   tree   FALSE    1      0.9997734  0.9990855  1
    ##   tree   FALSE   10      0.9999721  0.9998040  1
    ##   tree   FALSE   20      0.9999732  0.9998342  1
    ##   tree    TRUE    1      0.9997734  0.9990855  1
    ##   tree    TRUE   10      0.9999721  0.9998040  1
    ##   tree    TRUE   20      0.9999732  0.9998342  1
    ##
    ## ROC was used to select the optimal model using  the largest value.
    ## The final values used for the model were trials = 20, model = rules
    ##  and winnow = TRUE.

**with 10 PCA's features**

``` r
t0 <- proc.time()
model_t02 <- caret::train(Class ~ +V1+V2+V3+V4+V5+V6+V7+V8+V9+V10,
                     data = TrSet,
                     method = "C5.0",
                     metric = my_metric,
                     trControl = ctrl0)
tf <- proc.time() - t0
tf
```

    ##    user  system elapsed
    ## 8208.00   11.79 8275.13

``` r
model_t02
```

    ## C5.0
    ##
    ## 262846 samples
    ##     10 predictor
    ##      2 classes: 'No', 'Yes'
    ##
    ## No pre-processing
    ## Resampling: Cross-Validated (10 fold)
    ## Summary of sample sizes: 236561, 236561, 236562, 236562, 236560, 236562, ...
    ## Resampling results across tuning parameters:
    ##
    ##   model  winnow  trials  ROC        Sens       Spec
    ##   rules  FALSE    1      0.9996510  0.9990353  1
    ##   rules  FALSE   10      0.9999787  0.9998342  1
    ##   rules  FALSE   20      0.9999808  0.9998392  1
    ##   rules   TRUE    1      0.9996510  0.9990353  1
    ##   rules   TRUE   10      0.9999787  0.9998342  1
    ##   rules   TRUE   20      0.9999808  0.9998392  1
    ##   tree   FALSE    1      0.9997651  0.9988845  1
    ##   tree   FALSE   10      0.9999801  0.9997588  1
    ##   tree   FALSE   20      0.9999829  0.9997789  1
    ##   tree    TRUE    1      0.9997651  0.9988845  1
    ##   tree    TRUE   10      0.9999801  0.9997588  1
    ##   tree    TRUE   20      0.9999829  0.9997789  1
    ##
    ## ROC was used to select the optimal model using  the largest value.
    ## The final values used for the model were trials = 20, model = tree
    ##  and winnow = TRUE.

**with all features**

``` r
t0 <- proc.time()
model_t03 <- caret::train(Class ~. ,
                     data = TrSet,
                     method = "C5.0",
                     metric = my_metric,
                     trControl = ctrl0)
tf <- proc.time() - t0
tf
```

    ##     user   system  elapsed
    ## 10376.58    17.27 10464.56

``` r
model_t03
```

    ## C5.0
    ##
    ## 262846 samples
    ##     17 predictor
    ##      2 classes: 'No', 'Yes'
    ##
    ## No pre-processing
    ## Resampling: Cross-Validated (10 fold)
    ## Summary of sample sizes: 236562, 236561, 236562, 236561, 236561, 236562, ...
    ## Resampling results across tuning parameters:
    ##
    ##   model  winnow  trials  ROC        Sens       Spec
    ##   rules  FALSE    1      0.9997420  0.9991207  1
    ##   rules  FALSE   10      0.9999803  0.9998744  1
    ##   rules  FALSE   20      0.9999802  0.9998593  1
    ##   rules   TRUE    1      0.9997487  0.9991257  1
    ##   rules   TRUE   10      0.9999803  0.9998844  1
    ##   rules   TRUE   20      0.9999802  0.9998744  1
    ##   tree   FALSE    1      0.9997685  0.9990704  1
    ##   tree   FALSE   10      0.9999767  0.9997638  1
    ##   tree   FALSE   20      0.9999819  0.9998442  1
    ##   tree    TRUE    1      0.9997699  0.9990755  1
    ##   tree    TRUE   10      0.9999767  0.9997689  1
    ##   tree    TRUE   20      0.9999819  0.9998241  1
    ##
    ## ROC was used to select the optimal model using  the largest value.
    ## The final values used for the model were trials = 20, model = tree
    ##  and winnow = TRUE.

**Predictions with our Tree models**

``` r
pred_t01 <- predict(model_t01, TeSet)
pred_t02 <- predict(model_t02, TeSet)
pred_t03 <- predict(model_t03, TeSet)
```

## Results from all models

``` r
results <- cbind(real = TeSet$Class,
                 lgm01 = paste(pred_Lgm01),
                 lgm02 = paste(pred_Lgm02),
                 lgm03 = paste(pred_Lgm03),
                 t01 = paste(pred_t01),
                 t02 = paste(pred_t02),
                 t03 = paste(pred_t03))
head(results)
```

    ##      real lgm01 lgm02 lgm03 t01  t02  t03
    ## [1,] "No" "No"  "No"  "No"  "No" "No" "No"
    ## [2,] "No" "No"  "No"  "No"  "No" "No" "No"
    ## [3,] "No" "No"  "No"  "No"  "No" "No" "No"
    ## [4,] "No" "No"  "No"  "No"  "No" "No" "No"
    ## [5,] "No" "No"  "No"  "No"  "No" "No" "No"
    ## [6,] "No" "No"  "No"  "No"  "No" "No" "No"

## Some Metrics

AUC


``` r
auc_lgm01 <- ModelMetrics::auc(TeSet$Class, pred_Lgm01)
auc_lgm02 <- ModelMetrics::auc(TeSet$Class, pred_Lgm02)
auc_lgm03 <- ModelMetrics::auc(TeSet$Class, pred_Lgm03)
auc_t01 <- ModelMetrics::auc(TeSet$Class, pred_t01)
auc_t02 <- ModelMetrics::auc(TeSet$Class, pred_t02)
auc_t03 <- ModelMetrics::auc(TeSet$Class, pred_t03)
AUC <- cbind(auc_lgm01,auc_lgm02,auc_lgm03, auc_t01, auc_t02, auc_t03)
AUC
```

    ##      auc_lgm01 auc_lgm02 auc_lgm03   auc_t01   auc_t02   auc_t03
    ## [1,] 0.9274297 0.9264917 0.9304852 0.9046974 0.8876613 0.9047091

Our best metric is for `auc_lgm03`, which is a logistic regression that uses PCA from 1 to 15 as well as Time and Amount. Training Set has been oversampled in order to reduce bias occurred by unbalanced fraud class.

**Confusion Matrix:**

``` r
confusionMatrix(results[,4], results[,1])
```

    ## Confusion Matrix and Statistics
    ##
    ##           Reference
    ## Prediction    No   Yes
    ##        No  84460    19
    ##        Yes   834   128
    ##
    ##                Accuracy : 0.99
    ##                  95% CI : (0.9893, 0.9907)
    ##     No Information Rate : 0.9983
    ##     P-Value [Acc > NIR] : 1
    ##
    ##                   Kappa : 0.2285
    ##  Mcnemar's Test P-Value : <0.0000000000000002
    ##
    ##             Sensitivity : 0.9902
    ##             Specificity : 0.8707
    ##          Pos Pred Value : 0.9998
    ##          Neg Pred Value : 0.1331
    ##              Prevalence : 0.9983
    ##          Detection Rate : 0.9885
    ##    Detection Prevalence : 0.9887
    ##       Balanced Accuracy : 0.9305
    ##
    ##        'Positive' Class : No
    ##


``` r
write.csv(pred_Lgm03, "prediction.csv")
```


It is not a bad model to start with. Looking at the results of the confusion matrix we can say that although our model is quite good in general (Accuracy is 0.99), we need some improvement for the False Positives. We have 834 of the cases in which our prediction is fraud when it is not. That might be inconvenient if the business implements some restriction over this kind of transaction.
