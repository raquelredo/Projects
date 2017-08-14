---
title: "Titanic: Machine Learning from Disaster"
layout: post
excerpt:  "The sinking of the RMS Titanic is one of the most infamous shipwrecks in history. Can we build a model to predict chances of survival?
It is my job to predict if a passenger survived the sinking of the Titanic or not.

-   Features: 11
-   Observations: 891
-   Tuples: 10,692

**Challenges:** Missing values Treatment | Working with text"
header:
  teaser: Titanic.jpg
link:
tags: [R, survival prediction, titanic, kaggle, tree, knn, c5.0, logistic regression, missing data, inference, feature engineering]
share: true
categories: portfolio
---


## Dataset

-   test set can be downloaded from [here](https://www.kaggle.com/c/titanic/download/test.csv)
-   train set can be downloaded from [here] (https://www.kaggle.com/c/titanic/download/train.csv)

## Description

The sinking of the RMS Titanic is one of the most infamous shipwrecks in history. On April 15, 1912, during her maiden voyage, the Titanic sank after colliding with an iceberg, killing 1502 out of 2224 passengers and crew. This sensational tragedy shocked the international community and led to better safety regulations for ships.

One of the reasons that the shipwreck led to such loss of life was that there were not enough lifeboats for the passengers and crew. Although there was some element of luck involved in surviving the sinking, some groups of people were more likely to survive than others, such as women, children, and the upper-class.

In this challenge, we ask you to complete the analysis of what sorts of people were likely to survive. In particular, we ask you to apply the tools of machine learning to predict which passengers survived the tragedy.

<table style="width:62%;">
<colgroup>
<col width="8%" />
<col width="15%" />
<col width="38%" />
</colgroup>
<thead>
<tr class="header">
<th>Variable</th>
<th>Definition</th>
<th>Key</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>survival</td>
<td>Survival</td>
<td>0 = No, 1 = Yes</td>
</tr>
<tr class="even">
<td>pclass</td>
<td>Ticket class</td>
<td>1 = 1st, 2 = 2nd, 3 = 3rd</td>
</tr>
<tr class="odd">
<td>sex</td>
<td>Sex</td>
</tr>
<tr class="even">
<td>Age</td>
<td>Age in years</td>
</tr>
<tr class="odd">
<td>sibsp</td>
<td># of siblings / spouses aboard the Titanic</td>
</tr>
<tr class="even">
<td>parch</td>
<td># of parents / children aboard the Titanic</td>
</tr>
<tr class="odd">
<td>ticket</td>
<td>Ticket number</td>
</tr>
<tr class="even">
<td>fare</td>
<td>Passenger fare</td>
</tr>
<tr class="odd">
<td>cabin</td>
<td>Cabin number</td>
</tr>
<tr class="even">
<td>embarked</td>
<td>Port of Embarkation</td>
<td>C = Cherbourg, Q = Queenstown, S = Southampton</td>
</tr>
</tbody>
</table>

## Variable Notes

-   pclass: A proxy for socio-economic status (SES) 1st = Upper 2nd = Middle 3rd = Lower

-   age: Age is fractional if less than 1. If the age is estimated, is it in the form of xx.5

-   sibsp: The dataset defines family relations in this way... Sibling = brother, sister, stepbrother, stepsister Spouse = husband, wife (mistresses and fiancés were ignored)

-   parch: The dataset defines family relations in this way... Parent = mother, father Child = daughter, son, stepdaughter, stepson Some children travelled only with a nanny, therefore parch=0 for them.

### Analysis
Libraries needed to run the script:

``` r
library(corrplot) #for correlation matrix
library(gsubfn)#for preprocessing
library(caret)#for prediction
library(dplyr)#for mutate
library(kknn)
library(C50)
```

Importing the files:

``` r
train <- read.csv("train.csv", na.strings = c("NA", "NULL", ""))
test <- read.csv("test.csv", na.strings = c("NA", "NULL", ""))
head(train)
```

    ##   PassengerId Survived Pclass
    ## 1           1        0      3
    ## 2           2        1      1
    ## 3           3        1      3
    ## 4           4        1      1
    ## 5           5        0      3
    ## 6           6        0      3
    ##                                                  Name    Sex Age SibSp
    ## 1                             Braund, Mr. Owen Harris   male  22     1
    ## 2 Cumings, Mrs. John Bradley (Florence Briggs Thayer) female  38     1
    ## 3                              Heikkinen, Miss. Laina female  26     0
    ## 4        Futrelle, Mrs. Jacques Heath (Lily May Peel) female  35     1
    ## 5                            Allen, Mr. William Henry   male  35     0
    ## 6                                    Moran, Mr. James   male  NA     0
    ##   Parch           Ticket    Fare Cabin Embarked
    ## 1     0        A/5 21171  7.2500  <NA>        S
    ## 2     0         PC 17599 71.2833   C85        C
    ## 3     0 STON/O2. 3101282  7.9250  <NA>        S
    ## 4     0           113803 53.1000  C123        S
    ## 5     0           373450  8.0500  <NA>        S
    ## 6     0           330877  8.4583  <NA>        Q

``` r
str(train)
```

    ## 'data.frame':    891 obs. of  12 variables:
    ##  $ PassengerId: int  1 2 3 4 5 6 7 8 9 10 ...
    ##  $ Survived   : int  0 1 1 1 0 0 0 0 1 1 ...
    ##  $ Pclass     : int  3 1 3 1 3 3 1 3 3 2 ...
    ##  $ Name       : Factor w/ 891 levels "Abbing, Mr. Anthony",..: 109 191 358 277 16 559 520 629 417 581 ...
    ##  $ Sex        : Factor w/ 2 levels "female","male": 2 1 1 1 2 2 2 2 1 1 ...
    ##  $ Age        : num  22 38 26 35 35 NA 54 2 27 14 ...
    ##  $ SibSp      : int  1 1 0 1 0 0 0 3 0 1 ...
    ##  $ Parch      : int  0 0 0 0 0 0 0 1 2 0 ...
    ##  $ Ticket     : Factor w/ 681 levels "110152","110413",..: 524 597 670 50 473 276 86 396 345 133 ...
    ##  $ Fare       : num  7.25 71.28 7.92 53.1 8.05 ...
    ##  $ Cabin      : Factor w/ 147 levels "A10","A14","A16",..: NA 82 NA 56 NA NA 130 NA NA NA ...
    ##  $ Embarked   : Factor w/ 3 levels "C","Q","S": 3 1 3 3 3 2 3 3 3 1 ...

``` r
colnames(train)
```

    ##  [1] "PassengerId" "Survived"    "Pclass"      "Name"        "Sex"
    ##  [6] "Age"         "SibSp"       "Parch"       "Ticket"      "Fare"
    ## [11] "Cabin"       "Embarked"

``` r
colnames(test)
```

    ##  [1] "PassengerId" "Pclass"      "Name"        "Sex"         "Age"
    ##  [6] "SibSp"       "Parch"       "Ticket"      "Fare"        "Cabin"
    ## [11] "Embarked"

``` r
test <-  mutate(test, Survived = NA)#add column Survived
```

# Preprocessing

### Sex

Convert Sex attribute to boolean

``` r
train$male <- as.integer(ifelse(train$Sex == "male", 1, 0))
train$Sex <- NULL
```

### Survived

Transform to factor:

``` r
train$Survived <- as.factor(train$Survived)
```

### Missing values

First I will take a look in where are the missing values

``` r
library(Amelia)
missmap(train)
```

![](/Titanic-unnamed-chunk-8-1.png)

``` r
missmap(test)
```

![](/Titanic-unnamed-chunk-8-2.png)

``` r
is.na(train$Age)#index of MV
```

    ##   [1] FALSE FALSE FALSE FALSE FALSE  TRUE FALSE FALSE FALSE FALSE FALSE
    ##  [12] FALSE FALSE FALSE FALSE FALSE FALSE  TRUE FALSE  TRUE FALSE FALSE
    ##  [23] FALSE FALSE FALSE FALSE  TRUE FALSE  TRUE  TRUE FALSE  TRUE  TRUE
    ##  [34] FALSE FALSE FALSE  TRUE FALSE FALSE FALSE FALSE FALSE  TRUE FALSE
    ##  [45] FALSE  TRUE  TRUE  TRUE  TRUE FALSE FALSE FALSE FALSE FALSE FALSE
    ##  [56]  TRUE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE  TRUE  TRUE
    ##  [67] FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE  TRUE
    ##  [78]  TRUE FALSE FALSE FALSE FALSE  TRUE FALSE FALSE FALSE FALSE  TRUE
    ##  [89] FALSE FALSE FALSE FALSE FALSE FALSE FALSE  TRUE FALSE FALSE FALSE
    ## [100] FALSE FALSE  TRUE FALSE FALSE FALSE FALSE FALSE  TRUE FALSE  TRUE
    ## [111] FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE
    ## [122]  TRUE FALSE FALSE FALSE FALSE  TRUE FALSE  TRUE FALSE FALSE FALSE
    ## [133] FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE  TRUE FALSE FALSE
    ## [144] FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE
    ## [155]  TRUE FALSE FALSE FALSE  TRUE  TRUE FALSE FALSE FALSE FALSE FALSE
    ## [166] FALSE  TRUE FALSE  TRUE FALSE FALSE FALSE FALSE FALSE FALSE FALSE
    ## [177]  TRUE FALSE FALSE FALSE  TRUE  TRUE FALSE FALSE FALSE  TRUE  TRUE
    ## [188] FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE  TRUE FALSE
    ## [199]  TRUE FALSE FALSE  TRUE FALSE FALSE FALSE FALSE FALSE FALSE FALSE
    ## [210] FALSE FALSE FALSE FALSE FALSE  TRUE FALSE FALSE FALSE FALSE FALSE
    ## [221] FALSE FALSE FALSE  TRUE FALSE FALSE FALSE FALSE FALSE  TRUE FALSE
    ## [232] FALSE FALSE FALSE FALSE  TRUE FALSE FALSE FALSE FALSE  TRUE  TRUE
    ## [243] FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE  TRUE FALSE FALSE
    ## [254] FALSE FALSE FALSE  TRUE FALSE FALSE FALSE  TRUE FALSE FALSE FALSE
    ## [265]  TRUE FALSE FALSE FALSE FALSE FALSE  TRUE FALSE FALSE FALSE  TRUE
    ## [276] FALSE FALSE  TRUE FALSE FALSE FALSE FALSE FALSE FALSE  TRUE FALSE
    ## [287] FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE  TRUE FALSE
    ## [298] FALSE  TRUE FALSE  TRUE  TRUE FALSE  TRUE  TRUE FALSE  TRUE FALSE
    ## [309] FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE
    ## [320] FALSE FALSE FALSE FALSE FALSE  TRUE FALSE FALSE FALSE FALSE FALSE
    ## [331]  TRUE FALSE FALSE FALSE  TRUE  TRUE FALSE FALSE FALSE FALSE FALSE
    ## [342] FALSE FALSE FALSE FALSE FALSE FALSE  TRUE FALSE FALSE FALSE  TRUE
    ## [353] FALSE FALSE  TRUE FALSE FALSE FALSE  TRUE  TRUE FALSE FALSE FALSE
    ## [364] FALSE  TRUE FALSE FALSE  TRUE  TRUE FALSE FALSE FALSE FALSE FALSE
    ## [375] FALSE  TRUE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE  TRUE
    ## [386] FALSE FALSE FALSE  TRUE FALSE FALSE FALSE FALSE FALSE FALSE FALSE
    ## [397] FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE
    ## [408] FALSE FALSE  TRUE  TRUE  TRUE FALSE  TRUE FALSE  TRUE FALSE FALSE
    ## [419] FALSE FALSE  TRUE FALSE FALSE FALSE FALSE  TRUE FALSE FALSE  TRUE
    ## [430] FALSE FALSE  TRUE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE
    ## [441] FALSE FALSE FALSE FALSE  TRUE FALSE FALSE FALSE FALSE FALSE FALSE
    ## [452]  TRUE FALSE FALSE  TRUE FALSE FALSE  TRUE FALSE  TRUE FALSE FALSE
    ## [463] FALSE FALSE  TRUE FALSE  TRUE FALSE  TRUE FALSE  TRUE FALSE FALSE
    ## [474] FALSE FALSE  TRUE FALSE FALSE FALSE FALSE FALSE  TRUE FALSE FALSE
    ## [485] FALSE  TRUE FALSE FALSE FALSE FALSE  TRUE FALSE FALSE FALSE FALSE
    ## [496]  TRUE FALSE  TRUE FALSE FALSE FALSE FALSE  TRUE FALSE FALSE FALSE
    ## [507] FALSE  TRUE FALSE FALSE FALSE  TRUE FALSE FALSE FALSE FALSE FALSE
    ## [518]  TRUE FALSE FALSE FALSE FALSE  TRUE FALSE  TRUE FALSE FALSE  TRUE
    ## [529] FALSE FALSE FALSE  TRUE FALSE  TRUE FALSE FALSE FALSE FALSE  TRUE
    ## [540] FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE  TRUE FALSE FALSE
    ## [551] FALSE FALSE  TRUE FALSE FALSE FALSE FALSE  TRUE FALSE FALSE  TRUE
    ## [562] FALSE FALSE  TRUE  TRUE FALSE FALSE FALSE  TRUE FALSE FALSE FALSE
    ## [573] FALSE  TRUE FALSE FALSE FALSE FALSE  TRUE FALSE FALSE FALSE FALSE
    ## [584] FALSE  TRUE FALSE FALSE FALSE FALSE  TRUE FALSE FALSE FALSE  TRUE
    ## [595] FALSE FALSE  TRUE FALSE  TRUE FALSE FALSE  TRUE  TRUE FALSE FALSE
    ## [606] FALSE FALSE FALSE FALSE FALSE FALSE  TRUE  TRUE  TRUE FALSE FALSE
    ## [617] FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE
    ## [628] FALSE FALSE  TRUE FALSE FALSE FALSE  TRUE FALSE FALSE FALSE FALSE
    ## [639] FALSE  TRUE FALSE FALSE FALSE  TRUE FALSE FALSE FALSE FALSE  TRUE
    ## [650] FALSE  TRUE FALSE FALSE  TRUE FALSE FALSE  TRUE FALSE FALSE FALSE
    ## [661] FALSE FALSE FALSE FALSE FALSE FALSE FALSE  TRUE FALSE  TRUE FALSE
    ## [672] FALSE FALSE FALSE  TRUE FALSE FALSE FALSE FALSE FALSE  TRUE FALSE
    ## [683] FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE  TRUE
    ## [694] FALSE FALSE FALSE FALSE  TRUE FALSE FALSE FALSE FALSE FALSE FALSE
    ## [705] FALSE FALSE FALSE FALSE FALSE  TRUE FALSE  TRUE FALSE FALSE FALSE
    ## [716] FALSE FALSE FALSE  TRUE FALSE FALSE FALSE FALSE FALSE FALSE FALSE
    ## [727] FALSE  TRUE FALSE FALSE FALSE FALSE  TRUE FALSE FALSE FALSE FALSE
    ## [738] FALSE  TRUE  TRUE  TRUE FALSE FALSE FALSE FALSE FALSE FALSE FALSE
    ## [749] FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE
    ## [760] FALSE  TRUE FALSE FALSE FALSE FALSE FALSE  TRUE FALSE  TRUE FALSE
    ## [771] FALSE FALSE FALSE  TRUE FALSE FALSE  TRUE FALSE  TRUE FALSE FALSE
    ## [782] FALSE FALSE  TRUE FALSE FALSE FALSE FALSE FALSE FALSE  TRUE FALSE
    ## [793]  TRUE  TRUE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE
    ## [804] FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE
    ## [815] FALSE  TRUE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE
    ## [826]  TRUE  TRUE FALSE  TRUE FALSE FALSE FALSE  TRUE FALSE FALSE FALSE
    ## [837] FALSE  TRUE FALSE  TRUE FALSE FALSE FALSE FALSE FALSE FALSE  TRUE
    ## [848] FALSE FALSE  TRUE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE
    ## [859] FALSE  TRUE FALSE FALSE FALSE  TRUE FALSE FALSE FALSE FALSE  TRUE
    ## [870] FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE  TRUE FALSE
    ## [881] FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE  TRUE FALSE FALSE

``` r
sum(is.na(train$Age) == TRUE) #177
```

    ## [1] 177

``` r
sum(is.na(train$Age) == TRUE)/length(train$Age)#in%  0.1986532
```

    ## [1] 0.1986532

### Embarked

``` r
table(train$Embarked, useNA = "always")
```

    ##
    ##    C    Q    S <NA>
    ##  168   77  644    2

I will assign the value to the port with more passengers, *Southampton*

``` r
train$Embarked[which(is.na(train$Embarked))] <- "S"
```

### Age

We are going to check the titles in the Name feature. We assume that in those years people had similar styles of life, meaning people got married or had children at similar ages.

``` r
train$Name <- as.character(train$Name)
table_words <- table(unlist(strsplit(train$Name, "\\s+")))
sort(table_words [grep("\\.", names(table_words))], decreasing = TRUE)
```

    ##
    ##       Mr.     Miss.      Mrs.   Master.       Dr.      Rev.      Col.
    ##       517       182       125        40         7         6         2
    ##    Major.     Mlle.     Capt. Countess.      Don. Jonkheer.        L.
    ##         2         2         1         1         1         1         1
    ##     Lady.      Mme.       Ms.      Sir.
    ##         1         1         1         1

We need to find, first, the missing values that need to be filled up.

``` r
library(stringr)
tab <- cbind(train$Age, str_match(train$Name, "[a-zA-Z]+\\."))
table(tab[is.na(tab[,1]),2])
```

    ##
    ##     Dr. Master.   Miss.     Mr.    Mrs.
    ##       1       4      36     119      17

For the title containing a missing values, I will impute the mean of the value for each title group;

``` r
mean_mr <- mean(train$Age[grepl(" Mr\\.", train$Name) & !is.na(train$Age)])
mean_mrs <- mean(train$Age[grepl(" Mrs\\.", train$Name) & !is.na(train$Age)])
mean_dr <- mean(train$Age[grepl(" Dr\\.", train$Name) & !is.na(train$Age)])
mean_miss <- mean(train$Age[grepl(" Miss\\.", train$Name) & !is.na(train$Age)])
mean_master <- mean(train$Age[grepl(" Master\\.", train$Name) & !is.na(train$Age)])
mean_ms <- mean(train$Age[grepl(" Ms\\.", train$Name) & !is.na(train$Age)])
```

and impute the missing value with the mean of its group.

``` r
train$Age[grepl(" Mr\\.", train$Name) &
                 is.na(train$Age)] = mean_mr
train$Age[grepl(" Mrs\\.", train$Name) &
                 is.na(train$Age)] =  mean_mrs
train$Age[grepl(" Dr\\.", train$Name) &
                            is.na(train$Age)] = mean_dr
train$Age[grepl(" Miss\\.", train$Name) &
                              is.na(train$Age)] = mean_miss
train$Age[grepl(" Master\\.", train$Name) &
                                is.na(train$Age)] = mean_master
```

### Other features

Some of the variables, intuitively, does not have anything to do with survival rate.

``` r
train$Name <- NULL
train$Ticket <- NULL
train$Cabin <- NULL
train$Fare <- NULL
```

## Data Visualization

### Survival frequency

``` r
library(ggplot2)
ggplot(train, aes(x = Survived, y=..count.., fill = Survived)) +
  geom_bar()
```

![](/Titanic-unnamed-chunk-17-1.png)

### Survival by age bins

``` r
ggplot(data=train, aes(x=Age))+
  geom_histogram(bins = 25, aes(y=..density..,
                                            fill = Survived))
```

![](/Titanic-unnamed-chunk-18-1.png)

``` r
boxplot(train$Age ~ train$Survived, main= "Passenger survival by age",
        xlab = "Survived", ylab = "Age")
```

![](/Titanic-unnamed-chunk-19-1.png)

Does `Gender` as anything to do with survival?

``` r
table(train$Pclass, train$male)
```

    ##
    ##       0   1
    ##   1  94 122
    ##   2  76 108
    ##   3 144 347

``` r
ggplot(train, aes(x=male, fill=Survived)) + geom_bar()
```

![](/Titanic-unnamed-chunk-21-1.png)

Number of family members on board

``` r
ggplot(train, aes(x=SibSp, fill=Survived)) + geom_bar()
```

![](/Titanic-unnamed-chunk-22-1.png)

``` r
ggplot(train, aes(x=Parch, fill=Survived)) + geom_bar()
```

![](/Titanic-unnamed-chunk-23-1.png)

### Transforming Age to bins

I will group people in four different bins according to their age:

``` r
train_child <- train$Survived[train$Age < 13]
length(train_child[which(train_child == 1)])/length(train_child)
```

    ## [1] 0.5753425

``` r
train_youth <- train$Survived[train$Age >= 15 & train$Age <25]
length(train_youth[which(train_youth == 1)])/length(train_youth)
```

    ## [1] 0.4025424

``` r
train_adult <- train$Survived[train$Age >= 25 & train$Age < 65]
length(train_adult[which(train_adult == 1)])/length(train_adult)
```

    ## [1] 0.3540925

``` r
train_senior <- train$Survived[train$Age >= 65]
length(train_senior[which(train_senior == 1)])/length(train_senior)
```

    ## [1] 0.09090909

### Scale & Transform some variables

``` r
train$Embarked <- gsub("C", "1", train$Embarked)
train$Embarked <- gsub("Q", "2", train$Embarked)
train$Embarked <- gsub("S", "3", train$Embarked)
train$Embarked <- as.integer(train$Embarked)
```

``` r
range(train$Age, na.rm = TRUE)
```

    ## [1]  0.42 80.00

``` r
range(test$Age, na.rm = TRUE)
```

    ## [1]  0.17 76.00

We will consider the minimum and maximun age value for scaling both datasets.

``` r
min <- 0.17
max <- 80
scale_t <- function(x) {
  return( (x -min) / (max -min) )
}
train$Age_s <- sapply(train$Age, scale_t)
train$Age <-NULL
```

for other variables scaling is much straigtforward:

``` r
normal <- function(x) {
  (x-min(x))/(max(x)-min(x))
}

train$Pclass_s <- normal(train$Pclass)
train$SibSp_s <- normal(train$SibSp)
train$Embarked_s <- normal(train$Embarked)
train$Parch_s <- normal(train$Parch)
#
train$Pclass <- NULL
train$SibSp <- NULL
train$Embarked <- NULL
train$Parch <- NULL
```

``` r
ctrl <- trainControl(method = "cv",
                     number = 10,
                     summaryFunction = twoClassSummary,
                     classProb = T,
                     allowParallel = T)
```

## Building the model

``` r
##First some mutation
train <- mutate(train, Survived = ifelse(Survived == 1,
                                         "survived", "perished"))
#### Dividing the data into training/test con 0.7/0.3
set.seed(123)
train <- as.data.frame(train)
index <- createDataPartition(unlist(train$Survived), p = 0.7, list=F)
train_1 <- train[index, ]
train_2 <- train[-index,]
table(train_1$Survived)#it is balanced!
```

    ##
    ## perished survived
    ##      385      240

### Knn

``` r
#train_2 <- as.matrix(train_2)
model_knn <- caret::train(Survived~.-PassengerId,
                   train_1,
                   method = "kknn",
                   trControl = ctrl,
                   metric= "kappa")
model_knn
```

    ## k-Nearest Neighbors
    ##
    ## 625 samples
    ##   7 predictor
    ##   2 classes: 'perished', 'survived'
    ##
    ## No pre-processing
    ## Resampling: Cross-Validated (10 fold)
    ## Summary of sample sizes: 563, 562, 562, 562, 563, 563, ...
    ## Resampling results across tuning parameters:
    ##
    ##   kmax  ROC        Sens       Spec
    ##   5     0.8195892  0.8548583  0.6958333
    ##   7     0.8206590  0.8729420  0.6833333
    ##   9     0.8335217  0.8730094  0.6791667
    ##
    ## Tuning parameter 'distance' was held constant at a value of 2
    ##
    ## Tuning parameter 'kernel' was held constant at a value of optimal
    ## ROC was used to select the optimal model using  the largest value.
    ## The final values used for the model were kmax = 9, distance = 2 and
    ##  kernel = optimal.

### Tree

``` r
model_tree <- train(unlist(Survived)~.-PassengerId ,
             train_1,
             method = 'C5.0',
             trControl = ctrl,
             metric= "kappa",
             na.action  = na.pass)
model_tree
```

    ## C5.0
    ##
    ## 625 samples
    ##   7 predictor
    ##   2 classes: 'perished', 'survived'
    ##
    ## No pre-processing
    ## Resampling: Cross-Validated (10 fold)
    ## Summary of sample sizes: 563, 562, 562, 562, 562, 563, ...
    ## Resampling results across tuning parameters:
    ##
    ##   model  winnow  trials  ROC        Sens       Spec
    ##   rules  FALSE    1      0.8108946  0.9094467  0.6541667
    ##   rules  FALSE   10      0.8595971  0.8939271  0.6791667
    ##   rules  FALSE   20      0.8616341  0.9170040  0.6833333
    ##   rules   TRUE    1      0.8088282  0.9043860  0.6625000
    ##   rules   TRUE   10      0.8636794  0.9042510  0.6875000
    ##   rules   TRUE   20      0.8668269  0.9118084  0.7083333
    ##   tree   FALSE    1      0.8190030  0.9068151  0.6541667
    ##   tree   FALSE   10      0.8610338  0.9171390  0.6791667
    ##   tree   FALSE   20      0.8626518  0.9223347  0.6708333
    ##   tree    TRUE    1      0.8208699  0.9043860  0.6625000
    ##   tree    TRUE   10      0.8644638  0.9196356  0.6875000
    ##   tree    TRUE   20      0.8655575  0.9170715  0.6916667
    ##
    ## ROC was used to select the optimal model using  the largest value.
    ## The final values used for the model were trials = 20, model = rules
    ##  and winnow = TRUE.

### Logistic regression

``` r
model_log <- train(Survived ~.-PassengerId,
             train_1,
             method="glm",
             family= binomial(link = "logit"),
             trControl = ctrl,
             metric = "Kappa",
             na.action  = na.pass)
model_log
```

    ## Generalized Linear Model
    ##
    ## 625 samples
    ##   7 predictor
    ##   2 classes: 'perished', 'survived'
    ##
    ## No pre-processing
    ## Resampling: Cross-Validated (10 fold)
    ## Summary of sample sizes: 563, 562, 562, 563, 563, 562, ...
    ## Resampling results:
    ##
    ##   ROC       Sens       Spec
    ##   0.851476  0.8568826  0.6958333

### Making Predictions

``` r
pred_kknn <- predict(model_knn, train_2)
pred_log <-  predict(model_log, train_2)
pred_tree <- predict(model_tree, train_2)
```

``` r
confusionMatrix(pred_kknn, train_2$Survived)
```

    ## Confusion Matrix and Statistics
    ##
    ##           Reference
    ## Prediction perished survived
    ##   perished      143       35
    ##   survived       21       67
    ##
    ##                Accuracy : 0.7895
    ##                  95% CI : (0.7355, 0.8369)
    ##     No Information Rate : 0.6165
    ##     P-Value [Acc > NIR] : 1.118e-09
    ##
    ##                   Kappa : 0.5429
    ##  Mcnemar's Test P-Value : 0.08235
    ##
    ##             Sensitivity : 0.8720
    ##             Specificity : 0.6569
    ##          Pos Pred Value : 0.8034
    ##          Neg Pred Value : 0.7614
    ##              Prevalence : 0.6165
    ##          Detection Rate : 0.5376
    ##    Detection Prevalence : 0.6692
    ##       Balanced Accuracy : 0.7644
    ##
    ##        'Positive' Class : perished
    ##

``` r
confusionMatrix(pred_log, train_2$Survived)
```

    ## Confusion Matrix and Statistics
    ##
    ##           Reference
    ## Prediction perished survived
    ##   perished      142       30
    ##   survived       22       72
    ##
    ##                Accuracy : 0.8045
    ##                  95% CI : (0.7517, 0.8504)
    ##     No Information Rate : 0.6165
    ##     P-Value [Acc > NIR] : 3.037e-11
    ##
    ##                   Kappa : 0.5803
    ##  Mcnemar's Test P-Value : 0.3317
    ##
    ##             Sensitivity : 0.8659
    ##             Specificity : 0.7059
    ##          Pos Pred Value : 0.8256
    ##          Neg Pred Value : 0.7660
    ##              Prevalence : 0.6165
    ##          Detection Rate : 0.5338
    ##    Detection Prevalence : 0.6466
    ##       Balanced Accuracy : 0.7859
    ##
    ##        'Positive' Class : perished
    ##

``` r
confusionMatrix(pred_tree, train_2$Survived)
```

    ## Confusion Matrix and Statistics
    ##
    ##           Reference
    ## Prediction perished survived
    ##   perished      153       35
    ##   survived       11       67
    ##
    ##                Accuracy : 0.8271
    ##                  95% CI : (0.7762, 0.8705)
    ##     No Information Rate : 0.6165
    ##     P-Value [Acc > NIR] : 6.692e-14
    ##
    ##                   Kappa : 0.6172
    ##  Mcnemar's Test P-Value : 0.000696
    ##
    ##             Sensitivity : 0.9329
    ##             Specificity : 0.6569
    ##          Pos Pred Value : 0.8138
    ##          Neg Pred Value : 0.8590
    ##              Prevalence : 0.6165
    ##          Detection Rate : 0.5752
    ##    Detection Prevalence : 0.7068
    ##       Balanced Accuracy : 0.7949
    ##
    ##        'Positive' Class : perished
    ##

### Results for `train_2`predictions


``` r
results <- cbind(kknn = paste(pred_kknn),
                 tree = paste(pred_tree),
                 log = paste(pred_log))
```

tranform again to binary values:

``` r
col_p <- function(x){
  ifelse(x=="perished", 0, 1)
}

results <- apply(results, 2, col_p)
```

I am going to count the results according to the different algorithms and then, build a result matrix with the prediction that most ocurrs.

``` r
#results <- as.data.frame(results)
survival <- rowSums(results)
survival <- as.data.frame(survival)
survival$perish <- 3-survival[,1]
results2 <- ifelse(survival$survival>survival$perish, 1, 0)
```

``` r
train_2$Survived <- ifelse(train_2$Survived=="survived", 1, 0)
confusionMatrix(results2, train_2$Survived)
```

    ## Confusion Matrix and Statistics
    ##
    ##           Reference
    ## Prediction   0   1
    ##          0 148  34
    ##          1  16  68
    ##
    ##                Accuracy : 0.812
    ##                  95% CI : (0.7598, 0.8571)
    ##     No Information Rate : 0.6165
    ##     P-Value [Acc > NIR] : 4.357e-12
    ##
    ##                   Kappa : 0.5887
    ##  Mcnemar's Test P-Value : 0.01621
    ##
    ##             Sensitivity : 0.9024
    ##             Specificity : 0.6667
    ##          Pos Pred Value : 0.8132
    ##          Neg Pred Value : 0.8095
    ##              Prevalence : 0.6165
    ##          Detection Rate : 0.5564
    ##    Detection Prevalence : 0.6842
    ##       Balanced Accuracy : 0.7846
    ##
    ##        'Positive' Class : 0
    ##

The result can not beat the Tree prediction. So, this is the model we will use to predict the value in the test set.

## Mirroring the preprocess with the validation test Set.


``` r
test$male <- as.integer(ifelse(test$Sex == "male", 1, 0))
test$Sex <- NULL
test$Embarked[which(is.na(test$Embarked))] <- "S"
test$Age[grepl(" Mr\\.", test$Name) &
                 is.na(test$Age)] = mean_mr
test$Age[grepl(" Mrs\\.", test$Name) &
                 is.na(test$Age)] =  mean_mrs
test$Age[grepl(" Dr\\.", test$Name) &
                            is.na(test$Age)] = mean_dr
test$Age[grepl(" Miss\\.", test$Name) &
                              is.na(test$Age)] = mean_miss
test$Age[grepl(" Master\\.", test$Name) &
                                is.na(test$Age)] = mean_master
test$Age[grepl(" Ms\\.", test$Name) &
                                is.na(test$Age)] = mean_ms
#
test$Name <- NULL
test$Ticket <- NULL
test$Cabin <- NULL
test_child <- test$Survived[test$Age < 13]
test_youth <- test$Survived[test$Age >= 15 & test$Age <25]
test_adult <- test$Survived[test$Age >= 25 & test$Age < 65]
test_senior <- test$Survived[test$Age >= 65]
test$Embarked <- gsub("C", "1", test$Embarked)
test$Embarked <- gsub("Q", "2", test$Embarked)
test$Embarked <- gsub("S", "3", test$Embarked)
test$Embarked <- as.integer(test$Embarked)
test$Age_s <- sapply(test$Age, scale_t)
test$Age <- NULL
test$Pclass_s <- normal(test$Pclass)
test$SibSp_s <- normal(test$SibSp)
test$Embarked_s <- normal(test$Embarked)
test$Parch_s <- normal(test$Parch)
#
test$Pclass <- NULL
test$SibSp <- NULL
test$Embarked <- NULL
test$Parch <- NULL
```

and make the prediction:

``` r
pred_s <- predict(model_tree, test)
pred_s <- ifelse(pred_s=="survived", 1, 0)
pred_s <- as.data.frame(pred_s)
pred_s$PassengerId <- test$PassengerId
pred_s <- pred_s[,c(2,1)]
colnames(pred_s) <- c("PassengerId","Survived")
```
## Save file
Finally, I will write file for submission:

``` r
write.csv(pred_s, "pred_s.csv", row.names = FALSE)
```
