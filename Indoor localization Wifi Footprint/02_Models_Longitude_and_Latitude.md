Longitude and Latitude Modelling
================

PART 2 : MODELS FOR LONGITUDE & LATITUDE
========================================

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

Data Preparation
================

First I will split the data for Latitude and Longitud

``` r
c <- as.numeric(ncol(training))
Classes <- training[,c(1:c)]
#Classes & Features
LO <- as.data.frame(training[,c(1:(c-6),(c-5))]) 
LA <- as.data.frame(training[,c(1:(c-6),(c-4))]) 
LO2 <- validation[,c(1:(c-6),(c-5))]
LA2 <- validation[,c(1:(c-6),(c-4))]
```

Create Partition
================

``` r
#Longitude - create data partition####
set.seed(601)
trainIndex5 <- createDataPartition(y = LO$LO, 
                                   p = .70, 
                                   list = FALSE) 
LOTrain <- as.data.frame(LO[trainIndex5,])
LOTest <-  as.data.frame(LO[-trainIndex5,])
LO2Train <- as.data.frame(LO2[trainIndex5,])
LO2Test  <- as.data.frame(LO2[-trainIndex5,])

#Latitude - create data partition####
set.seed(601)
trainIndex6 <- createDataPartition(y = LA$LA, 
                                   p = .70, 
                                   list = FALSE) 
LATrain <- as.data.frame(LA[trainIndex6,])
LATest <-  as.data.frame(LA[-trainIndex6,])
```

Control for Training
====================

Create Control Cross Validation

``` r
ctrl <- trainControl(method = "repeatedcv",
                     repeats = 3, 
                     summaryFunction = multiClassSummary)
ctrl1 <- trainControl(method = "repeatedcv",
                      summaryFunction = multiClassSummary,
                      repeats = 3)
ctrlS <- trainControl(method = "repeatedcv",
                      repeats = 3,
                       classProbs = TRUE)
ctrl2 <- trainControl(method = "repeatedcv",
                      summaryFunction = twoClassSummary,
                      repeats = 3,
                      classProbs = TRUE)
```

Building the Model
==================

Create train & Test Set

``` r
train <- as.data.frame(LOTrain[,])
test <- as.data.frame(LOTest[,])
trainPredictors <- as.data.frame(LOTrain[,1:92])
```

``` r
#train <- sample_n(train, 1000)#uncomment if needed a smaller sample
```

¬¬¬¬¬¬¬¬¬¬¬¬¬LONGITUDE¬¬¬¬¬¬¬¬¬¬¬¬¬
===================================

1.Longitude - Nearest neighbour
-------------------------------

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

2.Longitude - Random Forest
---------------------------

``` r
train <- as.matrix(train[,])
        test <- as.matrix(test[,])
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
#save the model
save(rf_LO, file = "ModelLatitudeRF.rda")
#
#predicton
rf_LO_predic <- predict(rf_LO, LOTest, level = .95)
#capture metrics
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

3.Latitude - SVM
----------------

``` r
train <- as.data.frame(train)
test <- as.data.frame(test)
library(e1071)
set.seed(601)
tsvm_LO <- system.time(
  svm_LO <- svm(LO~.,
                 data = train,
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

¬¬¬¬¬¬¬¬¬¬¬¬¬LATITUDE¬¬¬¬¬¬¬¬¬¬¬¬¬
==================================

Load data

``` r
library(dplyr)
train <- as.data.frame(LATrain[,])
test <- as.data.frame(LATest[,])
trainPredictors <- as.data.frame(LATrain[,1:92])
        
#train <- sample_n(train, 1000)#uncomment when needed
```

1..Latitude - Nearest neighbour
===============================

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

2.Latitude - Random Forest
==========================

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
train <- as.data.frame(train[,])
test <- as.data.frame(test[,])
```

3.Latitude - SVM
================

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

¬¬¬¬¬¬¬¬¬¬¬¬¬PREDICTIONS¬¬¬¬¬¬¬¬¬¬¬¬¬
=====================================

``` r
LatitudePred <- matrix()
LatitudePred$Real <- LATest$LA
```

    ## Warning in LatitudePred$Real <- LATest$LA: Realizando coercion de LHD a una
    ## lista

``` r
LatitudePred$RandomForest <- rf_LA_predic
LatitudePred$SVM <- svm_LA_predic
LatitudePred$KNN <- kknn_LA_predic
LatitudePred$NA. <- NULL
LatitudePred<- as.data.frame(LatitudePred)

write.csv(LatitudePred, "Predictions_LA.csv")
#
LongitudePred<- matrix()
LongitudePred$Real <- LOTest$LO
```

    ## Warning in LongitudePred$Real <- LOTest$LO: Realizando coercion de LHD a
    ## una lista

``` r
LongitudePred$RandomForest <- rf_LO_predic 
LongitudePred$SVM <- svm_LO_predic
LongitudePred$KNN <- kknn_LO_predic
LongitudePred$NA. <- NULL
LongitudePred<- as.data.frame(LongitudePred)
```

``` r
write.csv(LongitudePred, "Predictions_LO.csv")
```

¬¬¬¬¬¬¬¬¬¬¬¬¬METRICS¬¬¬¬¬¬¬¬¬¬¬¬¬
---------------------------------

LONGITUDE
=========

``` r
library(MLmetrics)

#Random Forest
RF_R_LO <- R2_Score(LongitudePred$Real, LongitudePred$RandomForest)
RF_MAE_LO <- MAE(LongitudePred$Real, LongitudePred$RandomForest)
RF_RAE <- RAE(LongitudePred$Real, LongitudePred$RandomForest)
RF_Gini <- Gini(LongitudePred$Real, LongitudePred$RandomForest)
RF_MedianAE <- MedianAE(LongitudePred$Real, LongitudePred$RandomForest)
RF_MAPE <- MAPE(LongitudePred$Real, LongitudePred$RandomForest)

RF <- as.data.frame(cbind(RF_R_LO, RF_MAE_LO, 
                          RF_RAE,RF_Gini, RF_MedianAE, RF_MAPE))
#Kknn
KNN_R_LO <- R2_Score(LongitudePred$Real, LongitudePred$KNN)
KNN_MAE_LO <- MAE(LongitudePred$Real, LongitudePred$KNN)
KNN_RAE <- RAE(LongitudePred$Real, LongitudePred$KNN)
KNN_Gini <- Gini(LongitudePred$Real, LongitudePred$KNN)
KNN_MedianAE <- MedianAE(LongitudePred$Real, LongitudePred$KNN)
KNN_MAPE <- MAPE(LongitudePred$Real, LongitudePred$KNN)

KNN <- as.data.frame(cbind(KNN_R_LO, KNN_MAE_LO, 
                          KNN_RAE,KNN_Gini, KNN_MedianAE, KNN_MAPE))
#SVM
SVM_R_LO <- R2_Score(LongitudePred$Real, LongitudePred$SVM)
SVM_MAE_LO <- MAE(LongitudePred$Real, LongitudePred$SVM)
SVM_RAE <- RAE(LongitudePred$Real, LongitudePred$SVM)
SVM_Gini <- Gini(LongitudePred$Real, LongitudePred$SVM)
SVM_MedianAE <- MedianAE(LongitudePred$Real, LongitudePred$SVM)
SVM_MAPE <- MAPE(LongitudePred$Real, LongitudePred$SVM)

SVM <- as.data.frame(cbind(SVM_R_LO, SVM_MAE_LO, 
                           SVM_RAE,SVM_Gini, SVM_MedianAE, SVM_MAPE))
LONGITUDE <- vector()

LONGITUDE$SVM <- c(SVM_R_LO,SVM_MAE_LO,SVM_RAE,SVM_Gini,
                       SVM_MedianAE,SVM_MAPE)
LONGITUDE <- as.data.frame(LONGITUDE)
LONGITUDE$KNN <- c(KNN_R_LO,KNN_MAE_LO,KNN_RAE,KNN_Gini,
                   KNN_MedianAE,KNN_MAPE)
LONGITUDE$RF <- c(RF_R_LO,RF_MAE_LO,RF_RAE,RF_Gini,
                   KNN_MedianAE,KNN_MAPE)

LONGITUDE <- as.data.frame(t(LONGITUDE))
colnames(LONGITUDE)<- c("R2", "MAE", "RAE",
                        "Gini", "MedianAE", 
                        "MAPE")
write.csv(LONGITUDE,"LONGITUDE.CSV")
View(LONGITUDE)
```

LATITUDE
========

``` r
#Random Forest
RF_R_LA <- R2_Score(LatitudePred$Real, LatitudePred$RandomForest)
RF_MAE_LA <- MAE(LatitudePred$Real, LatitudePred$RandomForest)
RF_RAE <- RAE(LatitudePred$Real, LatitudePred$RandomForest)
RF_Gini <- Gini(LatitudePred$Real, LatitudePred$RandomForest)
RF_MedianAE <- MedianAE(LatitudePred$Real, LatitudePred$RandomForest)
RF_MAPE <- MAPE(LatitudePred$Real, LatitudePred$RandomForest)

RF <- as.data.frame(cbind(RF_R_LA, RF_MAE_LA, 
                          RF_RAE,RF_Gini, RF_MedianAE, RF_MAPE))
#Kknn
KNN_R_LA <- R2_Score(LatitudePred$Real, LatitudePred$KNN)
KNN_MAE_LA <- MAE(LatitudePred$Real, LatitudePred$KNN)
KNN_RAE <- RAE(LatitudePred$Real, LatitudePred$KNN)
KNN_Gini <- Gini(LatitudePred$Real, LatitudePred$KNN)
KNN_MedianAE <- MedianAE(LatitudePred$Real, LatitudePred$KNN)
KNN_MAPE <- MAPE(LatitudePred$Real, LatitudePred$KNN)

KNN <- as.data.frame(cbind(KNN_R_LA, KNN_MAE_LA, 
                           KNN_RAE,KNN_Gini, KNN_MedianAE, KNN_MAPE))
#SVM
SVM_R_LA <- R2_Score(LatitudePred$Real, LatitudePred$SVM)
SVM_MAE_LA <- MAE(LatitudePred$Real, LatitudePred$SVM)
SVM_RAE <- RAE(LatitudePred$Real, LatitudePred$SVM)
SVM_Gini <- Gini(LatitudePred$Real, LatitudePred$SVM)
SVM_MedianAE <- MedianAE(LatitudePred$Real, LatitudePred$SVM)
SVM_MAPE <- MAPE(LatitudePred$Real, LatitudePred$SVM)

SVM <- as.data.frame(cbind(SVM_R_LA, SVM_MAE_LA, 
                           SVM_RAE,SVM_Gini, SVM_MedianAE, SVM_MAPE))
LATITUDE <- vector()

LATITUDE$SVM <- c(SVM_R_LA,SVM_MAE_LA,SVM_RAE,SVM_Gini,
                   SVM_MedianAE,SVM_MAPE)
```

    ## Warning in LATITUDE$SVM <- c(SVM_R_LA, SVM_MAE_LA, SVM_RAE, SVM_Gini,
    ## SVM_MedianAE, : Realizando coercion de LHD a una lista

``` r
LATITUDE <- as.data.frame(LATITUDE)
LATITUDE$KNN <- c(KNN_R_LA,KNN_MAE_LA,KNN_RAE,KNN_Gini,
                   KNN_MedianAE,KNN_MAPE)
LATITUDE$RF <- c(RF_R_LA,RF_MAE_LA,RF_RAE,RF_Gini,
                  KNN_MedianAE,KNN_MAPE)

LATITUDE <- as.data.frame(t(LATITUDE))
colnames(LATITUDE)<- c("R2", "MAE", "RAE",
                        "Gini", "MedianAE", 
                        "MAPE")
write.csv(LATITUDE,"LATITUDE.CSV")
View(LATITUDE)
```
