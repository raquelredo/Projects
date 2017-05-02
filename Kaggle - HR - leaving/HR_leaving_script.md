HR predicting leaving
================

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

Removing feature 4 as it changes the scale of the boxplot

``` r
boxplot(hr[,-4])
```

![](HR_leaving_script_files/figure-markdown_github/unnamed-chunk-6-1.png) Salary strings should follow an increasing order:

``` r
list <- c("low", "medium", "high")
hr$salary <- factor(hr$salary, levels = list)
str(hr$salary)
```

    ##  Factor w/ 3 levels "low","medium",..: 1 2 2 1 1 1 1 1 1 1 ...
