HR Analytics
================

Load libraries
==============

``` r
library(ggplot2)
library(corrplot)#Correlation matrix
library(cluster)
library(fpc)# for cluster
library(caret)
library(dplyr)
library(pROC)
```

Import
======

``` r
hr <- read.csv("HR_comma_sep.csv")
```

``` r
head(hr)
```

    ##   satisfaction_level last_evaluation number_project average_montly_hours
    ## 1               0.38            0.53              2                  157
    ## 2               0.80            0.86              5                  262
    ## 3               0.11            0.88              7                  272
    ## 4               0.72            0.87              5                  223
    ## 5               0.37            0.52              2                  159
    ## 6               0.41            0.50              2                  153
    ##   time_spend_company Work_accident left promotion_last_5years sales salary
    ## 1                  3             0    1                     0 sales    low
    ## 2                  6             0    1                     0 sales medium
    ## 3                  4             0    1                     0 sales medium
    ## 4                  5             0    1                     0 sales    low
    ## 5                  3             0    1                     0 sales    low
    ## 6                  3             0    1                     0 sales    low

Pre-processing
==============

``` r
hr$left <- as.factor(hr$left)
hr$Work_accident <- as.factor(hr$Work_accident)
hr$promotion_last_5years <- as.factor(hr$promotion_last_5years)
colnames(hr)[4] <- "average_monthly_hours"
colnames(hr)[9] <- "department"
```

``` r
range <- apply(hr, 2, range)
```

Is it balanced?

``` r
round(table(hr$left)/nrow(hr)*100, 2)
```

    ## 
    ##     0     1 
    ## 76.19 23.81

No problem concerning data imbalance.

Salary strings should follow an increasing order:

``` r
list <- c("low", "medium", "high")
hr$salary <- factor(hr$salary, levels = list)
str(hr$salary)
```

    ##  Factor w/ 3 levels "low","medium",..: 1 2 2 1 1 1 1 1 1 1 ...

plot histograms

``` r
variables <- colnames(hr)[1:5]
for (i in seq_along(variables)) {
  n <- ggplot(data=hr, aes_string(x=variables[i]))
  h <- geom_histogram(bins = 50, alpha=0.3, aes(y=..density.., fill=left))
  d <- stat_density(geom="line",aes(color=left)) # no geom_density because it leaves a baseline
  print(n+h+d)
  ggsave(n+h+d, filename=paste("plot_", variables[i], ".png", sep=""))
  dev.off()
}
```
Histograms and density plots are stored in the wd. I will load one here to show its shape.
![](HR_analytics_files/figure-markdown_github/plot_average_monthly_hours.png)



Normalization
=============

``` r
hr_n <- apply(hr[,1:5], 2, scale)
```

Variance-Near Zero Variance
===========================

``` r
nzv <- nearZeroVar(hr, saveMetrics = TRUE)
nzv
```

    ##                       freqRatio percentUnique zeroVar   nzv
    ## satisfaction_level     1.068657    0.61337422   FALSE FALSE
    ## last_evaluation        1.014164    0.43336222   FALSE FALSE
    ## number_project         1.076449    0.04000267   FALSE FALSE
    ## average_monthly_hours  1.000000    1.43342890   FALSE FALSE
    ## time_spend_company     1.986128    0.05333689   FALSE FALSE
    ## Work_accident          5.915168    0.01333422   FALSE FALSE
    ## left                   3.200224    0.01333422   FALSE FALSE
    ## promotion_last_5years 46.018809    0.01333422   FALSE  TRUE
    ## department             1.522059    0.06667111   FALSE FALSE
    ## salary                 1.134967    0.02000133   FALSE FALSE

Modelling
=========

First step is building our training and testing datasets.

Some preprocessing was left

``` r
hr <- mutate(hr, left = ifelse(left == "0", "No", "Yes"))
```

Dividing the data into training/test con 0.7/0.3:

``` r
set.seed(123)
index <- createDataPartition(hr$left, p = 0.7, list=F)
TrSet <- hr[index, ] 
TeSet <- hr[-index,]
table(TrSet$left)
```

    ## 
    ##   No  Yes 
    ## 8000 2500

``` r
ctrl0 <- trainControl(method = "cv", 
                      number = 10,
                      summaryFunction = twoClassSummary,
                      classProbs = T,
                      allowParallel = T)
```

``` r
t0 <- proc.time()
model_Lgm01 <- caret::train(left ~.,
                     data = TrSet,
                     method="glm", 
                     family= binomial(link = "logit"),
                     trControl = ctrl0)
tf <- proc.time() - t0
tf
```

    ##    user  system elapsed 
    ##    3.39    0.14    3.53

``` r
model_Lgm01
```

    ## Generalized Linear Model 
    ## 
    ## 10500 samples
    ##     9 predictor
    ##     2 classes: 'No', 'Yes' 
    ## 
    ## No pre-processing
    ## Resampling: Cross-Validated (10 fold) 
    ## Summary of sample sizes: 9450, 9450, 9450, 9450, 9450, 9450, ... 
    ## Resampling results:
    ## 
    ##   ROC        Sens    Spec  
    ##   0.8220355  0.9285  0.3636

``` r
t0 <- proc.time()
model_Lgm02 <- caret::train(left ~.-promotion_last_5years,
                     data = TrSet,
                     method="glm", 
                     family= binomial(link = "logit"),
                     trControl = ctrl0)
tf <- proc.time() - t0
tf
```

    ##    user  system elapsed 
    ##    3.03    0.03    3.06

``` r
model_Lgm02
```

    ## Generalized Linear Model 
    ## 
    ## 10500 samples
    ##     9 predictor
    ##     2 classes: 'No', 'Yes' 
    ## 
    ## No pre-processing
    ## Resampling: Cross-Validated (10 fold) 
    ## Summary of sample sizes: 9450, 9450, 9450, 9450, 9450, 9450, ... 
    ## Resampling results:
    ## 
    ##   ROC       Sens     Spec  
    ##   0.821493  0.92975  0.3592

Tree
====

``` r
t0 <- proc.time()
model_t01 <- caret::train(left ~.,
                     data = TrSet,
                     method="C5.0", 
                     trControl = ctrl0)
tf <- proc.time() - t0
tf
```

    ##    user  system elapsed 
    ##  129.36    0.09  129.91

``` r
model_t01
```

    ## C5.0 
    ## 
    ## 10500 samples
    ##     9 predictor
    ##     2 classes: 'No', 'Yes' 
    ## 
    ## No pre-processing
    ## Resampling: Cross-Validated (10 fold) 
    ## Summary of sample sizes: 9450, 9450, 9450, 9450, 9450, 9450, ... 
    ## Resampling results across tuning parameters:
    ## 
    ##   model  winnow  trials  ROC        Sens      Spec  
    ##   rules  FALSE    1      0.9600597  0.995250  0.9196
    ##   rules  FALSE   10      0.9903612  0.994000  0.9396
    ##   rules  FALSE   20      0.9911250  0.996500  0.9380
    ##   rules   TRUE    1      0.9604063  0.995250  0.9188
    ##   rules   TRUE   10      0.9896705  0.994750  0.9364
    ##   rules   TRUE   20      0.9912220  0.996500  0.9364
    ##   tree   FALSE    1      0.9750663  0.994750  0.9224
    ##   tree   FALSE   10      0.9902305  0.993500  0.9352
    ##   tree   FALSE   20      0.9915232  0.996500  0.9328
    ##   tree    TRUE    1      0.9749853  0.995375  0.9212
    ##   tree    TRUE   10      0.9901515  0.994875  0.9368
    ##   tree    TRUE   20      0.9907405  0.996375  0.9352
    ## 
    ## ROC was used to select the optimal model using  the largest value.
    ## The final values used for the model were trials = 20, model = tree
    ##  and winnow = FALSE.

``` r
t0 <- proc.time()
model_t02 <- caret::train(left ~.-promotion_last_5years,
                     data = TrSet,
                     method="C5.0", 
                     trControl = ctrl0)
tf <- proc.time() - t0
tf
```

    ##    user  system elapsed 
    ##  128.12    0.14  129.31

``` r
model_t02
```

    ## C5.0 
    ## 
    ## 10500 samples
    ##     9 predictor
    ##     2 classes: 'No', 'Yes' 
    ## 
    ## No pre-processing
    ## Resampling: Cross-Validated (10 fold) 
    ## Summary of sample sizes: 9450, 9450, 9450, 9450, 9450, 9450, ... 
    ## Resampling results across tuning parameters:
    ## 
    ##   model  winnow  trials  ROC        Sens      Spec  
    ##   rules  FALSE    1      0.9617780  0.995375  0.9208
    ##   rules  FALSE   10      0.9901092  0.993625  0.9372
    ##   rules  FALSE   20      0.9916105  0.995875  0.9332
    ##   rules   TRUE    1      0.9601232  0.995875  0.9192
    ##   rules   TRUE   10      0.9896788  0.993375  0.9360
    ##   rules   TRUE   20      0.9910350  0.995875  0.9324
    ##   tree   FALSE    1      0.9752555  0.995875  0.9224
    ##   tree   FALSE   10      0.9904705  0.994250  0.9320
    ##   tree   FALSE   20      0.9914545  0.996000  0.9332
    ##   tree    TRUE    1      0.9749845  0.996250  0.9208
    ##   tree    TRUE   10      0.9901102  0.994125  0.9364
    ##   tree    TRUE   20      0.9907550  0.995875  0.9316
    ## 
    ## ROC was used to select the optimal model using  the largest value.
    ## The final values used for the model were trials = 20, model = rules
    ##  and winnow = FALSE.

knn
===

``` r
t0 <- proc.time()
model_knn01 <- caret::train(left ~.,
                     data = TrSet,
                     method="kknn", 
                     trControl = ctrl0)
tf <- proc.time() - t0
tf
```

    ##    user  system elapsed 
    ##  152.50    0.33  153.99

``` r
model_t02
```

    ## C5.0 
    ## 
    ## 10500 samples
    ##     9 predictor
    ##     2 classes: 'No', 'Yes' 
    ## 
    ## No pre-processing
    ## Resampling: Cross-Validated (10 fold) 
    ## Summary of sample sizes: 9450, 9450, 9450, 9450, 9450, 9450, ... 
    ## Resampling results across tuning parameters:
    ## 
    ##   model  winnow  trials  ROC        Sens      Spec  
    ##   rules  FALSE    1      0.9617780  0.995375  0.9208
    ##   rules  FALSE   10      0.9901092  0.993625  0.9372
    ##   rules  FALSE   20      0.9916105  0.995875  0.9332
    ##   rules   TRUE    1      0.9601232  0.995875  0.9192
    ##   rules   TRUE   10      0.9896788  0.993375  0.9360
    ##   rules   TRUE   20      0.9910350  0.995875  0.9324
    ##   tree   FALSE    1      0.9752555  0.995875  0.9224
    ##   tree   FALSE   10      0.9904705  0.994250  0.9320
    ##   tree   FALSE   20      0.9914545  0.996000  0.9332
    ##   tree    TRUE    1      0.9749845  0.996250  0.9208
    ##   tree    TRUE   10      0.9901102  0.994125  0.9364
    ##   tree    TRUE   20      0.9907550  0.995875  0.9316
    ## 
    ## ROC was used to select the optimal model using  the largest value.
    ## The final values used for the model were trials = 20, model = rules
    ##  and winnow = FALSE.

Now I am just being curious. I sant to see if I can make clusters between employees.

Plotting the clusters
=====================

``` r
set.seed(123)
cluster <- kmeans(hr[,1:5], 5)
```

``` r
cluster$centers
```

    ##   satisfaction_level last_evaluation number_project average_monthly_hours
    ## 1          0.6620474       0.7745434       4.155719              246.3246
    ## 2          0.5584399       0.6296165       3.126794              138.6828
    ## 3          0.4880803       0.7838100       4.692458              275.8521
    ## 4          0.6821828       0.7384727       3.874557              212.1733
    ## 5          0.6486514       0.6996636       3.637535              173.8953
    ##   time_spend_company
    ## 1           3.691125
    ## 2           3.346204
    ## 3           3.872674
    ## 4           3.471651
    ## 5           3.275385

``` r
plotcluster(hr[,1:5], cluster$cluster)
```

![](HR_analytics_files/figure-markdown_github/unnamed-chunk-27-1.png)

``` r
clusplot(hr[,1:5], cluster$cluster, color=TRUE, shade=TRUE, 
         labels=2, lines=0)
```

![](HR_analytics_files/figure-markdown_github/unnamed-chunk-28-1.png)

It seems that I cannot find clear clusters, right?

Plot tree
=========

``` r
pred_lgm01 <- predict(model_Lgm01, TeSet)
pred_lgm02 <- predict(model_Lgm02, TeSet)
pred_t01 <- predict(model_t01, TeSet)
pred_t02 <- predict(model_t02, TeSet)
pred_knn01 <- predict(model_knn01, TeSet)
```

``` r
met_lgm01 <- pROC::roc(TeSet$left, as.numeric(pred_lgm01))
met_lgm02 <- pROC::roc(TeSet$left, as.numeric(pred_lgm02))
met_t01 <- pROC::roc(TeSet$left, as.numeric(pred_t01))
met_t02 <- pROC::roc(TeSet$left, as.numeric(pred_t02))
met_knn01 <- pROC::roc(TeSet$left, as.numeric(pred_knn01))
```

``` r
AUC <- cbind(met_lgm01$auc,met_lgm02$auc, 
             met_t01$auc, met_t02$auc, met_knn01$auc)
AUC
```

    ##           [,1]     [,2]      [,3]     [,4]      [,5]
    ## [1,] 0.6424874 0.640562 0.9744987 0.975491 0.9696578

Best AUC is from model\_t02
