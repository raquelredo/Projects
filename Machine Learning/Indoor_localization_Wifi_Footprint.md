---
title: "Indoor localization through Wi fi footprint"
layout: post
excerpt:  "GPS are not working properly indoors. But, is it possible to locate a person according Wi fi footprint?
-   Features: 529
-   Observations: 19,937
-   Tuples: 10,546,673

**Challenges:** Reduce data set for downloading time computation | Indoor localization"
tags: [R, PCA, feature reduction, model evaluation, C50, adaboost, random forest, cross validation]
header:
  teaser: wifi.png
link:
share: true
categories: portfolio
---
# Data Set

The Dataset can be easily download from the UCI MAchine Learning Repository in here: <http://archive.ics.uci.edu/ml/datasets/UJIIndoorLoc>

## Source

Donors/Contact Joaquín Torres-Sospedra jtorres +@+ uji.es Raul Montoliu montoliu +@+ uji.es Adolfo Martínez-Usó admarus +@+ upv.es Joaquín Huerta huerta +@+ uji.es UJI - Institute of New Imaging Technologies, Universitat Jaume I, Avda. Vicente Sos Baynat S/N, 12071, Castellón, Spain. UPV - Departamento de Sistemas Informáticos y Computación, Universitat Politècnica de València, Valencia, Spain.

Creators Joaquín Torres-Sospedra, Raul Montoliu, Adolfo Martínez-Usó, Tomar J. Arnau, Joan P. Avariento, Mauri Benedito-Bordonau, Joaquín Huerta, Yasmina Andreu, óscar Belmonte, Vicent Castelló, Irene Garcia-Martí, Diego Gargallo, Carlos Gonzalez, Nadal Francisco, Josep López, Ruben Martínez, Roberto Mediero, Javier Ortells, Nacho Piqueras, Ianisse Quizán, David Rambla, Luis E. Rodríguez, Eva Salvador Balaguer, Ana Sanchís, Carlos Serra, and Sergi Trilles.

## Data Set Information

Many real world applications need to know the localization of a user in the world to provide their services. Therefore, automatic user localization has been a hot research topic in the last years. Automatic user localization consists of estimating the position of the user (latitude, longitude and altitude) by using an electronic device, usually a mobile phone. Outdoor localization problem can be solved very accurately thanks to the inclusion of GPS sensors into the mobile devices. However, indoor localization is still an open problem mainly due to the loss of GPS signal in indoor environments. Although, there are some indoor positioning technologies and methodologies, this database is focused on WLAN fingerprint-based ones (also know as WiFi Fingerprinting).

Although there are many papers in the literature trying to solve the indoor localization problem using a WLAN fingerprint-based method, there still exists one important drawback in this field which is the lack of a common database for comparison purposes. So, UJIIndoorLoc database is presented to overcome this gap. We expect that the proposed database will become the reference database to compare different indoor localization methodologies based on WiFi fingerprinting.

The UJIIndoorLoc database covers three buildings of Universitat Jaume I with 4 or more floors and almost 110.000m2. It can be used for classification, e.g. actual building and floor identification, or regression, e.g. actual longitude and latitude estimation. It was created in 2013 by means of more than 20 different users and 25 Android devices. The database consists of 19937 training/reference records (trainingData.csv file) and 1111 validation/test records (validationData.csv file).

The 529 attributes contain the WiFi fingerprint, the coordinates where it was taken, and other useful information.

Each WiFi fingerprint can be characterized by the detected Wireless Access Points (WAPs) and the corresponding Received Signal Strength Intensity (RSSI). The intensity values are represented as negative integer values ranging -104dBm (extremely poor signal) to 0dbM. The positive value 100 is used to denote when a WAP was not detected. During the database creation, 520 different WAPs were detected. Thus, the WiFi fingerprint is composed by 520 intensity values.

Then the coordinates (latitude, longitude, floor) and Building ID are provided as the attributes to be predicted.

Additional information has been provided.

The particular space (offices, labs, etc.) and the relative position (inside/outside the space) where the capture was taken have been recorded. Outside means that the capture was taken in front of the door of the space.

Information about who (user), how (android device & version) and when (timestamp) WiFi capture was taken is also recorded.

## Description

Attribute Information:

**Attribute 001 (WAP001):** Intensity value for WAP001. Negative integer values from -104 to 0 and +100. Positive value 100 used if WAP001 was not detected. (....)

**Attribute 520 (WAP520):** Intensity value for WAP520. Negative integer values from -104 to 0 and +100. Positive value 100 used if WAP520 was not detected.

**Attribute 521** (Longitude): Longitude. Negative real values from -7695.9387549299299000 to -7299.786516730871000

**Attribute 522** (Latitude): Latitude. Positive real values from 4864745.7450159714 to 4865017.3646842018.

**Attribute 523** (Floor): Altitude in floors inside the building. Integer values from 0 to 4.

**Attribute 524** (BuildingID): ID to identify the building. Measures were taken in three different buildings. Categorical integer values from 0 to 2.

**Attribute 525** (SpaceID): Internal ID number to identify the Space (office, corridor, classroom) where the capture was taken. Categorical integer values.

**Attribute 526** (RelativePosition): Relative position with respect to the Space (1 - Inside, 2 - Outside in Front of the door). Categorical integer values.

**Attribute 527** (UserID): User identifier (see below). Categorical integer values.

**Attribute 528** (PhoneID): Android device identifier (see below). Categorical integer values.

**Attribute 529** (Timestamp): UNIX Time when the capture was taken. Integer value.

------------------------------------------------------------------------

| UserID      | Anonymized user Height (cm) |
|-------------|-----------------------------|
| 0 USER0000  | (Validation User)N/A        |
| 1 USER0001  | 170                         |
| 2 USER0002  | 176                         |
| 3 USER0003  | 172                         |
| 4 USER0004  | 174                         |
| 5 USER0005  | 184                         |
| 6 USER0006  | 180                         |
| 7 USER0007  | 160                         |
| 8 USER0008  | 176                         |
| 9 USER0009  | 177                         |
| 10 USER0010 | 186                         |
| 11 USER0011 | 176                         |
| 12 USER0012 | 158                         |
| 13 USER0013 | 174                         |
| 14 USER0014 | 173                         |
| 15 USER0015 | 174                         |
| 16 USER0016 | 171                         |
| 17 USER0017 | 166                         |
| 18 USER0018 | 162                         |

| PhoneID | Android Device     | Android Ver. | UserID   |
|---------|--------------------|--------------|----------|
| 0       | Celkon A27         | 4.0.4(6577)  | 0        |
| 1       | GT-I8160           | 2.3.6        | 8        |
| 2       | GT-I8160           | 4.1.2        | 0        |
| 3       | GT-I9100           | 4.0.4        | 5        |
| 4       | GT-I9300           | 4.1.2        | 0        |
| 5       | GT-I9505           | 4.2.2        | 0        |
| 6       | GT-S5360           | 2.3.6        | 7        |
| 7       | GT-S6500           | 2.3.6        | 14       |
| 8       | Galaxy Nexus       | 4.2.2        | 10       |
| 9       | Galaxy Nexus       | 4.3          | 0        |
| 10      | HTC Desire HD      | 2.3.5        | 18       |
| 11      | HTC One            | 4.1.2        | 15       |
| 12      | HTC One            | 4.2.2        | 0        |
| 13      | HTC Wildfire S     | 2.3.5        | 0,11     |
| 14      | LT22i              | 4.0.4        | 0,1,9,16 |
| 15      | LT22i              | 4.1.2        | 0        |
| 16      | LT26i              | 4.0.4        | 3        |
| 17      | M1005D             | 4.0.4        | 13       |
| 18      | MT11i              | 2.3.4        | 4        |
| 19      | Nexus              | 4 4.2.2      | 6        |
| 20      | Nexus              | 4 4.3        | 0        |
| 21      | Nexus S            | 4.1.2        | 0        |
| 22      | Orange Monte Carlo | 2.3.5        | 17       |
| 23      | Transformer TF101  | 4.0.3        | 2        |
| 24      | bq Curie           | 4.1.1        | 12       |


# Analysis

Longitude, latitude, and altitude are the only values I need in order to locate someone.The main purpose is to be able to locate a person in building in order to show him his position on a map and be able to give some instructions to move inside the building.

## Import files


``` r
library(readr)
trainingData <- read.csv("trainingData.csv",
                         check.names=TRUE)
validationData <- read.csv("validationData.csv",
                           check.names=TRUE)
```

# PART 1: DATA EXPLORATION

## Descriptive analysis

Some stats to look into

``` r
Stats1 <- data.frame(
  Min = apply(trainingData, 2, min), # minimum
  Q1 = apply(trainingData, 2, quantile, 1/4), # First quartile
  Med = apply(trainingData, 2, median), # median
  Mean = apply(trainingData, 2, mean), # mean
  Q3 = apply(trainingData, 2, quantile, 3/4), # Third quartile
  Max = apply(trainingData, 2, max) # Maximum
)
head(Stats1,5)
```

    ##        Min  Q1 Med      Mean  Q3 Max
    ## WAP001 -97 100 100  99.82364 100 100
    ## WAP002 -90 100 100  99.82094 100 100
    ## WAP003 100 100 100 100.00000 100 100
    ## WAP004 100 100 100 100.00000 100 100
    ## WAP005 -97 100 100  99.61373 100 100

``` r
Stats2 <- data.frame(
  Min = apply(validationData, 2, min), # minimum
  Q1 = apply(validationData, 2, quantile, 1/4), # First quartile
  Med = apply(validationData, 2, median), # median
  Mean = apply(validationData, 2, mean), # mean
  Q3 = apply(validationData, 2, quantile, 3/4), # Third quartile
  Max = apply(validationData, 2, max) # Maximum
)
```

There are some features that, by common sense, will not be useful for our prediction.

``` r
trainingData$TIMESTAMP <- NULL
trainingData$USERID <- NULL
trainingData$PHONEID <- NULL
#
validationData$TIMESTAMP <- NULL
validationData$USERID <- NULL
validationData$PHONEID <- NULL
```

I am going to create a only-features data frame with only the WAP values.

``` r
trainingData1 <- trainingData[,1:520]
trainingData1 <- apply(trainingData1, 2, as.numeric)
trainingData2 <- trainingData[,521:526]
#
validationData1 <- validationData[,1:520]
validationData1 <- apply(validationData1, 2, as.numeric)
validationData2 <- validationData[,521:526]
```

NearZeroVar
===========

Values with Variance near zero are only introducing noise in our model, therefore they are also not useful for our model.

``` r
library(stats)
library(caret)
nzv <- nearZeroVar(trainingData1,
                   saveMetrics = TRUE)
head(nzv,5)
```

    ##        freqRatio percentUnique zeroVar  nzv
    ## WAP001  2489.875     0.0300948   FALSE TRUE
    ## WAP002  1991.800     0.0150474   FALSE TRUE
    ## WAP003     0.000     0.0050158    TRUE TRUE
    ## WAP004     0.000     0.0050158    TRUE TRUE
    ## WAP005  1421.214     0.0501580   FALSE TRUE

how many Wap features do we have?

``` r
dim(trainingData1)
```

    ## [1] 19937   520

I am going to use the value from the WAPS with Null values (=100 in our data set) as a cut-off value.

``` r
x <- 0.0100316  #that is the value of the variance from which we will discriminate.
```

``` r
dim(nzv[nzv$percentUnique > x,])
```

    ## [1] 428   4

I select the WAPs that fulfill the requirement.

``` r
colz <- c(rownames(nzv[nzv$percentUnique > x,]))
```

and then eliminate them in both data sets:

``` r
new_trainingData1 <-
  as.data.frame(trainingData1[,colz])
new_validationData1 <-
  as.data.frame(validationData1[,colz])
remove(x)
remove(colz)
remove(nzv)
```

I will check if both data sets had the same transformation:

``` r
all.equal(colnames(new_trainingData1),
          colnames(new_validationData1))#TRUE
```

    ## [1] TRUE

``` r
dim(new_trainingData1)#428 columns
```

    ## [1] 19937   428

``` r
dim(new_validationData1)#428 colums
```

    ## [1] 1111  428

Scaling
=======

I apply the following function -min/max-min

``` r
normalize <- function(x) { return( (x +104) / (0 + 104) ) }
```

``` r
pmatrix1 <- as.data.frame(apply(new_trainingData1,
                                2,
                                normalize))
pmatrix2 <- as.data.frame(apply(new_validationData1,
                                2, normalize))
```

#Feature Reduction (with PCA)


Considering the data frame has many features, I want to reduce the number of them. I also need to check the correlation between them in order to remove the columns that give the same information. The reason is that it will impact wrongly in our model. One way to do both things is applying the Principle component Analysis.

``` r
library(FactoMineR)
library(doParallel)#to squeeze my computer

registerDoParallel(core = 4)
princ <- prcomp(pmatrix1, scale=FALSE, center = FALSE)
head(princ, 10)
```

    ## $sdev
    ##   [1] 3.913694e+01 2.633500e+00 1.614418e+00 1.535428e+00 1.507737e+00
    ##   [6] 1.345620e+00 1.333864e+00 1.227014e+00 1.086523e+00 1.033271e+00
    ##    (...)

    ##
    ## $rotation
    ##                PC1           PC2           PC3           PC4           PC5 (...)
    ## WAP001 -0.05007236 -4.485729e-03  1.453957e-03  1.434506e-03 -0.0049701130
    ## WAP002 -0.05007215 -4.598461e-03  3.379632e-03  1.624848e-04 -0.0022121978
    ## WAP005 -0.05002200 -2.816786e-03  1.398534e-03 -2.747780e-04 -0.0037291724
    ## WAP006 -0.04940410 -1.009230e-02 -1.330434e-02  2.217957e-03  0.0081471708
    ## WAP007 -0.04881923 -2.361195e-02  6.659241e-02 -2.742223e-02  0.0336694821
    ## (...)
    ## $center
    ## [1] FALSE
    ##
    ## $scale
    ## [1] FALSE
    ##
    ## $x
    ##                PC1          PC2           PC3           PC4           PC5 (...)
    ##     [1,] -39.13904  2.145305354  1.414171e+00 -0.5326860655 -2.853106e-01
    ##     [2,] -39.22598  2.062387110  1.304850e+00 -0.5031498311 -2.385503e-01
    ##     [3,] -39.27975  1.927227491  1.336221e+00 -0.4058264979  4.048748e-02
    ##     [4,] -39.22547  2.136748296  1.300703e+00 -0.5447649753  2.185814e-01
    ##     [5,] -40.53580  1.354093581  4.022594e-01 -0.1105455692 -1.983623e-01
    ##     [6,] -39.28550  2.042570199  8.911077e-01 -0.3462115565 -2.178086e-01
    ##     [7,] -39.10092  2.029787586  1.487316e+00 -0.4474948292 -8.749077e-02
    ##    (...)

## Screeplot
``` r
screeplot(princ,npcs = 80)
```

![](/Wf-unnamed-chunk-17-1.png) \# Variance Let's start plotting it.

``` r
plot(princ, xlab = "var")
```

![](/Wf-Variance-1.png) How much of the Total Variance explains each component?

``` r
variance <- princ$sdev^2/sum(princ$sdev^2)*100
plot(variance, type = "line", col = "red")
```

![](/Wf-unnamed-chunk-18-1.png) As a rule of a thumb features explaining 80% of the variance are enough to build a good model. In our new data set our 92 first PCA's fulfill that requirement.

As I mention before I need to apply the same transformation to my validation set.

``` r
pmatrix1 <- as.matrix(pmatrix1)
pmatrix2 <- as.matrix(pmatrix2)
```

``` r
rotation <- princ$rotation
brandnew_trainingData1 <- pmatrix1 %*% rotation
brandnew_validationData1 <- pmatrix2 %*% rotation
```

Did I do it right?

``` r
all.equal(brandnew_trainingData1, princ$x)
```

    ## [1] TRUE

I am going to create a new data set with the selected components. I will also rename my classes for better typing.

``` r
colnames(trainingData2) <-  c("LO", "LA", "FL", "BU", "SP", "RP")
colnames(validationData2) <- c("LO", "LA", "FL", "BU", "SP", "RP")
comp <- 92
new_trainingSet <-
  as.data.frame(cbind(brandnew_trainingData1[,1:comp],
                      trainingData2))
#
new_validationSet <-
  as.data.frame(cbind(brandnew_validationData1[,1:comp],
                      validationData2))
```

# Save the new data


I am going to save this new files so I can use lattet without running all the script.

``` r
write.csv(new_trainingSet, "new_training.csv",
          row.names = FALSE)
write.csv(new_validationSet, "new_validation.csv",
          row.names = FALSE)
```

## Data Visualization


``` r
library(ggplot2)
```

## Plot 1- Building ID


``` r
ggplot(trainingData, aes(LONGITUDE,
                         LATITUDE),
       colour = BUILDINGID) +
  ggtitle("Building ID - Vs Longitud $Latitude") +
  geom_hex() +
  theme(legend.position = "bottom")
```

![](/Wf-Building%20ID-1.png)

I can see the shapes of the buldings. Also I can recognise when looking in Google map, which building is. It is part of the University Campus from [Universitat Jaume I](https://www.google.es/maps/place/Universitat+Jaume+I/@39.9929222,-0.0676806,17z/data>=!4m5!3m4!1s0xd5ffe0fca9b5147:0x1368bf53b3a7fb3f!8m2!3d39.9945711!4d-0.0689003?hl=es) ,in Castelló, Spain. Not surprisingly, is the University in which attend this data set owners. The plot shows the coherence of the data collected. It seems there is no mistake in its collection.

I have drawn its shape on the map.

![](/Wf-gmap.png)

## Plot 2 - Relative Position

``` r
ggplot(trainingData, aes(LONGITUDE,
                         LATITUDE)) +
  geom_point(colour = trainingData$RELATIVEPOSITION) +
  ggtitle("Relative Position")
```

![](/Wf-Relative%20Position-1.png)

## Plot 3 - Space Id


With this plot I want to know if the Space ID is shared with other buildings or is an unique name across buildings.

``` r
ggplot(trainingData, aes(as.character(BUILDINGID),
                         as.character(SPACEID))) +
    geom_point()+
    xlab("BUILDING #")+
    ylab("SPACE ID")+
    ggtitle("Space ID vs Building")
```

![](/Wf-Plot%203%20-%20Space%20Id-1.png) Space is not unique!

## Plot 4 - Longitude, latitude and Floor


``` r
library(scatterplot3d)
scatterplot3d( x= trainingData$LATITUDE,
               y= trainingData$LONGITUDE,
               z = trainingData$FLOOR,
               type = "p",
               color = trainingData$SPACEID,
               pch = 20)
```

![](/Wf-Longitude,%20latitude%20and%20Floor-1.png)

## Basic Exploration


## Missing values


``` r
library(Amelia)
missmap(trainingData)#there is no missing values
```

![](/Wf-Missing%20values-1.png)

``` r
missmap(validationData)#there is no missing values
```

![](/Wf-Missing%20values-2.png)

## Plot 5 - Correlation Matrices


``` r
library(GGally)
corr1 <- cor(trainingData1)
corr2 <- trainingData2[,]
ggcorr(corr1, label = TRUE)
```

![](/Wf-Correlation%20Matrices-1.png)

there are so many features that we are not able to see correlation between them.

``` r
ggcorr(corr2, label = TRUE)
```

![](/Wf-Correlation%20Matrices2-1.png)

``` r
library(corrplot)
corrplot(corr1, method = "square", type ="upper")
```

![](/Wf-Correlation%20Matrices3-1.png)

``` r
#
ggpairs(corr2)
```

![](/Wf-Correlation%20Matrices3-2.png)

``` r
library(psych)
pairs.panels(trainingData2)
```

![](/Wf-panel-1.png)

# Visualizing PCA


## Plot 6 - % of the Variance


With PCA we decided that 92 components were explaining most of the variance. Now we can see it in a plot.

``` r
library(factoextra)
fviz_eig(princ, addlabels = TRUE,
         linecolor = "chocolate1",
         barfill="white",
         barcolor ="darkblue")
```

![](/Wf-perc.%20of%20the%20Variance-1.png)

## Plot 7 - Factor map PCA colored


``` r
fviz_pca_var(princ, col.var="cos2") +
  scale_color_gradient2(low="white",
                        mid="blue",
                        high="red",
                        midpoint=0.5) + theme_minimal()
```

![](/Wf-Factor%20map%20PCA%20colored-1.png)

## Plot 8 - Eigenvalue


``` r
fviz_eig(princ, choice = "eigenvalue",
         addlabels=TRUE)
```

![](/Wf-Eigenvalue-1.png)

# PART 2: MODELS FOR LONGITUDE & LATITUDE & ALTITUDE(FLOOR)


I will clean my environment and just recover the preprocessed files

``` r
rm(list = setdiff(ls(), lsf.str()))
```

Libraries Needed

``` r
library(readr)
library(ggplot2)#graphs
library(caret)#ML
library(mlbench)
library(doParallel)
library(PerformanceAnalytics)
library(dplyr)#for preprocessing data
library(kknn)#ML
library(ModelMetrics)#for the metrics
library(randomForest)#ML
library(e1071)#ML
library(foreach)
library(MLmetrics)
registerDoParallel(cores = 8)#to speed up process
```

``` r
R_MAX_MEM_SIZE <- memory.limit(size = 40000)#Increase memory limit
```

Reading the files

``` r
training <- read.csv("new_training.csv",
                     sep=",", as.is = TRUE)
validation <- read.csv("new_validation.csv",
                       sep=",", as.is = TRUE)
```

## Data Preparation

I will remove classes that I will not need anymore.

``` r
training$RP <- NULL
training$SP <- NULL
training$BU <- NULL
#
validation$RP <- NULL
validation$SP <- NULL
validation$BU <- NULL
```

First I will split the data for each different class.

``` r
c <- as.numeric(ncol(training))
Classes <- training[,c(1:c)]
#Classes & Features
LO <- as.data.frame(training[,c(1:(c-3),(c-2))])
LA <- as.data.frame(training[,c(1:(c-3),(c-1))])
FL <- as.data.frame(training[,c(1:(c-3),(c))])
LO2 <- validation[,c(1:(c-3),(c-2))]
LA2 <- validation[,c(1:(c-3),(c-1))]
FL2 <- validation[,c(1:(c-3),(c))]
```

## Create Partition

``` r
#Longitude - create data partition####
set.seed(601)
trainIndex5 <- createDataPartition(y = LO$LO,
                                   p = .70,
                                   list = FALSE)
LOTrain <- as.data.frame(LO[trainIndex5,])
LOTest <-  as.data.frame(LO[-trainIndex5,])

#Latitude - create data partition####
set.seed(601)
trainIndex6 <- createDataPartition(y = LA$LA,
                                   p = .70,
                                   list = FALSE)
LATrain <- as.data.frame(LA[trainIndex6,])
LATest <-  as.data.frame(LA[-trainIndex6,])

#Altitude(Floor) - create data partition####
set.seed(601)
trainIndex7 <- createDataPartition(y = FL$FL,
                                   p = .70,
                                   list = FALSE)
FLTrain <- as.data.frame(FL[trainIndex7,])
FLTest <-  as.data.frame(FL[-trainIndex7,])
```

## Control for Training


Create Control Cross Validation

``` r
ctrl <- trainControl(method = "repeatedcv",
                     repeats = 3,
                     summaryFunction = multiClassSummary)
ctrl1 <- trainControl(method = "repeatedcv",
                      summaryFunction = multiClassSummary,
                      repeats = 3)
ctrlk <- trainControl(method = "cv",
                      number = 10,
                      summaryFunction = multiClassSummary,
                      classProbs = TRUE,
                      allowParallel = T)
ctrlS <- trainControl(method = "repeatedcv",
                      repeats = 3,
                      classProbs = TRUE)
ctrl2 <- trainControl(method = "repeatedcv",
                      summaryFunction = twoClassSummary,
                      repeats = 3,
                      classProbs = TRUE)
```

# Building the Model

Create train & test Set

``` r
train <- as.data.frame(LOTrain[,])
test <- as.data.frame(LOTest[,])
#trainPredictors <- as.data.frame(LOTrain[,1:92])
```

``` r
#train <- sample_n(train, 1000)#uncomment if needed a smaller sample
```

# LONGITUDE


## 1.Longitude - Nearest neighbour


``` r
library(kknn)
set.seed(601)
tkkn_LO <- system.time(
  kknn_LO <- train.kknn(LO~.,
                        data = train,
                        trControl = ctrl,
                        method = "kknn",
                        method = "optimal",
                        kmax = 5)
)
#to save the model
save(kknn_LO, file = "ModelLongitudeKNN.rda")
#
#prediction
kknn_LO_predic <- predict(kknn_LO, LOTest)
#@Capture metrics####
kknn_LO_Summary <- capture.output(kknn_LO)
cat("Summary", kknn_LO_Summary,
    file = "summary of kknn_LO.txt",
    sep = "\n",
    append = TRUE)
kknn_LO
```

    ##
    ## Call:
    ## train.kknn(formula = LO ~ ., data = train, kmax = 5, trControl = ctrl,     method = "kknn", method = "optimal")
    ##
    ## Type of response variable: continuous
    ## minimal mean absolute error: 3.479484
    ## Minimal mean squared error: 86.37815
    ## Best kernel: optimal
    ## Best k: 4

## 2.Longitude - Random Forest

``` r
train <- as.matrix(train[,])
test <- as.matrix(test[,])
#
library(randomForest)
library(e1071)
library(foreach)
set.seed(601)
trf_LO <- system.time(
rf_LO <- randomForest(LO~.,
                      data = train,
                      method ='rf',
                      trControl = ctrl,
                      importance = TRUE,
                      ntree= 500,
                      maximize =TRUE
)
)
#save the model####
save(rf_LO, file = "ModelLongitudeRF.rda")
#
#@prediction with the modelo####
rf_LO_predic <- predict(rf_LO, LOTest, level = .95)
#@CAPTURE metrics####
rf_LO_Summary <- capture.output(rf_LO)
cat("Summary", rf_LO_Summary,
  file = "summary of rf_LO.txt",
  sep = "\n",
  append = TRUE)
rf_LO
```

    ##
    ## Call:
    ##  randomForest(formula = LO ~ ., data = train, method = "rf", trControl = ctrl,      importance = TRUE, ntree = 500, maximize = TRUE)
    ##                Type of random forest: regression
    ##                      Number of trees: 500
    ## No. of variables tried at each split: 30
    ##
    ##           Mean of squared residuals: 96.35986
    ##                     % Var explained: 99.37

## 3.Longitude - SVM

``` r
train <- as.data.frame(train)
test <- as.data.frame(test)
library(e1071)
set.seed(601)
tsvm_LO <- system.time(
  svm_LO <- svm(LO ~ ., data = train,
                trControl = ctrl,
                preProc = c("center", "scale")
  )
)
#@saving the model####
save(svm_LO, file = "ModelLongitudSVM.rda")
#
#@prediccion del modelo####
svm_LO_predic <- predict(svm_LO, LOTest, level = .95)
#@CAPTURE Metrics of the model####
svm_LO_Summary <- capture.output(svm_LO)
cat("Summary", svm_LO_Summary,
    file = "summary of svm_LO.txt",
    sep = "\n",
    append = TRUE)
svm_LO
```

    ##
    ## Call:
    ## svm(formula = LO ~ ., data = train, trControl = ctrl, preProc = c("center",
    ##     "scale"))
    ##
    ##
    ## Parameters:
    ##    SVM-Type:  eps-regression
    ##  SVM-Kernel:  radial
    ##        cost:  1
    ##       gamma:  0.01086957
    ##     epsilon:  0.1
    ##
    ##
    ## Number of Support Vectors:  2968

# LATITUDE


Load data

``` r
train <- as.data.frame(LATrain[,])
test <- as.data.frame(LATest[,])
trainPredictors <- as.data.frame(LATrain[,1:92])

#train <- sample_n(train, 1000)#uncomment when needed
```

## 1.Latitude - Nearest neighbour


``` r
library(kknn)
set.seed(601)
tkkn_LA <- system.time(
kknn_LA <- train.kknn(LA~.,
                      data = train,
                      trControl = ctrl,
                      method = "kknn",
                      method = "optimal",
                      kmax = 5)
)
#@guardar el modelo####
save(kknn_LA, file = "ModelLatitudeKNN.rda")
#
#@prediccion del modelo####
kknn_LA_predic <- predict(kknn_LA, LATest)
#@CAPTURAR Metrica del modelo####
kknn_LA_Summary <- capture.output(kknn_LA)
cat("Summary", kknn_LA_Summary,
  file = "summary of kknn_LA.txt",
  sep = "\n",
  append = TRUE)
kknn_LA
```

    ##
    ## Call:
    ## train.kknn(formula = LA ~ ., data = train, kmax = 5, trControl = ctrl,     method = "kknn", method = "optimal")
    ##
    ## Type of response variable: continuous
    ## minimal mean absolute error: 2.897793
    ## Minimal mean squared error: 51.76575
    ## Best kernel: optimal
    ## Best k: 5

## 2.Latitude - Random Forest


``` r
train <- as.matrix(train[,])
test <- as.matrix(test[,])
#
library(randomForest)
library(e1071)
library(foreach)
set.seed(601)
trf_LA <- system.time(
rf_LA <- randomForest(LA~.,
                      data = train,
                      method ='rf',
                      trControl = ctrl,
                      importance = TRUE,
                      ntree= 500,
                      maximize =TRUE
)
)
#save the model####
save(rf_LA, file = "ModelLatitudeRF.rda")
#
#@prediction with the modelo####
rf_LA_predic <- predict(rf_LA, LATest, level = .95)
#@CAPTURE metrics####
rf_LA_Summary <- capture.output(rf_LA)
cat("Summary", rf_LA_Summary,
  file = "summary of rf_LA.txt",
  sep = "\n",
  append = TRUE)
rf_LA
```

    ##
    ## Call:
    ##  randomForest(formula = LA ~ ., data = train, method = "rf", trControl = ctrl,      importance = TRUE, ntree = 500, maximize = TRUE)
    ##                Type of random forest: regression
    ##                      Number of trees: 500
    ## No. of variables tried at each split: 30
    ##
    ##           Mean of squared residuals: 56.78588
    ##                     % Var explained: 98.73

``` r
#train <- as.data.frame(train[,])
#test <- as.data.frame(test[,])
```

## 3.Latitude - SVM

``` r
        library(e1071)
        set.seed(601)
        tsvm_LA <- system.time(
          svm_LA <- svm(LA~.,
                        data = train,
                        trControl = ctrl,
                        preProc = c("center", "scale")
          )
        )
        #@saving the model####
        save(svm_LA, file = "ModelLatitudeSVM.rda")
        #
        #@prediction with the model####
        svm_LA_predic <- predict(svm_LA, LATest, level = .95)
        #@CAPTURE Metrics of the model LA####
        svm_LA_Summary <- capture.output(svm_LA)
        cat("Summary", svm_LA_Summary,
            file = "summary of svm_LA.txt",
            sep = "\n",
            append = TRUE)
kknn_LA
```

    ##
    ## Call:
    ## train.kknn(formula = LA ~ ., data = train, kmax = 5, trControl = ctrl,     method = "kknn", method = "optimal")
    ##
    ## Type of response variable: continuous
    ## minimal mean absolute error: 2.897793
    ## Minimal mean squared error: 51.76575
    ## Best kernel: optimal
    ## Best k: 5

# ALTITUDE


This is a classification problem.

``` r
train <- as.data.frame(FLTrain[,])
test <- as.data.frame(FLTest[,])
trainPredictors <- as.data.frame(FLTrain[,1:92])
```

I am going to change the legend for `Floor` as follow: Floor \#0: A Floor \#1: B Floor \#2: C Floor \#3: D Floor \#4: E

``` r
test <- test %>% mutate(FL = ifelse(FL =="0", "A",
                                    ifelse(FL =="1", "B",
                                           ifelse(FL =="2", "c",
                                                  ifelse(FL =="3", "D",
                                                         ifelse(FL =="4", "E", " "))))))
#
train <- train %>% mutate(FL = ifelse(FL =="0", "A",
                                    ifelse(FL =="1", "B",
                                           ifelse(FL =="2", "c",
                                                  ifelse(FL =="3", "D",
                                                         ifelse(FL =="4", "E", " "))))))
```

## 1.Floor - Random Forest


``` r
#
#test <- as.matrix(test)
#train <- as.matrix(train)
#
metric <- "Accuracy"
#
set.seed(601)
tRF_FL <- system.time(
  RF_FL <- caret::train(FL~.,
                 train,
                 method = "rf",
                 trControl = ctrl,
                 tune.randomForest="best.foo")
)
#
#@save the model####
save(RF_FL, file = "RF_FL.rda")
#
#@prediction with the model####
RF_FL_predic <- predict(RF_FL, FLTest, level = .95)
#@CAPTURE Metrics of the model####
RF_FL_Summary <- capture.output(RF_FL)
cat("Summary",RF_FL_Summary,
    file = "summary of RF_FL.txt",
    sep = "\n",
    append =TRUE)
#
RF_FL
```
## 2.Floor - C50
``` r
library(C50)
test <- as.data.frame(test)
train <- as.data.frame(train)
#train$FL <- as.factor(train$FL)
set.seed(601)
tc50_FL <- system.time(
  c50_FL <- caret::train(FL~. ,
                  data = train,
                  method = "C5.0",
                  trControl = c(ctrlk, noGlobalPruning = TRUE)
  )
)
#@saving the model####
save(c50_FL, file = "ModelFloorC50.rda")
#prediction with the model####
c50_FL_predic <- predict(c50_FL, FLTest, level = .95, type = "raw")
#
c50_FL
```
    ## Random Forest
    ##
    ## 13958 samples
    ##    92 predictor
    ##     5 classes: 'A', 'B', 'c', 'D', 'E'
    ##
    ## No pre-processing
    ## Resampling: Cross-Validated (10 fold, repeated 3 times)
    ## Summary of sample sizes: 12563, 12563, 12562, 12561, 12560, 12562, ...
    ## Resampling results across tuning parameters:
    ##
    ##   mtry  Accuracy   Kappa      Mean_F1    Mean_Sensitivity
    ##    2    0.9634133  0.9525659  0.9591979  0.9502713
    ##   47    0.9590199  0.9469298  0.9590057  0.9550289
    ##   92    0.9449296  0.9286685  0.9446636  0.9400118
    ##   Mean_Specificity  Mean_Pos_Pred_Value  Mean_Neg_Pred_Value
    ##   0.9903396         0.9702534            0.9908029
    ##   0.9892615         0.9635392            0.9894662
    ##   0.9855808         0.9500972            0.9858397
    ##   Mean_Detection_Rate  Mean_Balanced_Accuracy
    ##   0.1926827            0.9703055
    ##   0.1918040            0.9721452
    ##   0.1889859            0.9627963
    ##
    ## Accuracy was used to select the optimal model using  the largest value.
    ## The final value used for the model was mtry = 2.
