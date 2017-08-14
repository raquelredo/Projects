---
title: "Market Basket Analysis"
layout: post
excerpt:  "Which products are more alike to be bought together?
The main purpose is to analyze the Basket composition from purchase tickets to study how consumers buy products together. This analysis might the foundation base for a cluster customer analysis or a product system recommendation.

-   Type: list of lists
-   Observations: 9835 ticket lists

**Challenges:** Association Analysis per se"
header:
  teaser: market-basket-analysis.jpg
link:
tags: [R, MBA, asociation rules, set, support, confidence, lift]
share: true
categories: portfolio
---

### Dataset

The dataset is a list of a list. It contains 9,835 grocery purchased tickets. Each line on the file represents one ticket. Items are labelled and separated by a comma. Style is:

-   citrus fruit,semi-finished bread,margarine,ready soups
-   tropical fruit,yogurt,coffee
-   whole milk
-   pip fruit,yogurt,cream cheese ,meat spreads
-   other vegetables,whole milk,condensed milk,long life bakery product

The main purpose is to make association rules for products frequently bought together. Why?
The results can be used in **brick and mortar** to store products with affinity next to each other in order to improve the customer experience. Marketing campaigns can also be a useful method to increase revenues.
As per online channels, deliver targeted marketing is one of the main benefits as well as drive recommendation engines.

### Analysis
Libraries needed

``` r
library(arules)
library(arulesViz)#for visualization
```

In this data set each line/receipt represents a transaction with items that were purchased. Each line is called a transaction and each column in a row represents an item.

Let's start by importing the file.

``` r
groceries <- read.transactions("groceries.csv", sep = ",")
groceries
```

    ## transactions in sparse format with
    ##  9835 transactions (rows) and
    ##  169 items (columns)

after the importing, I will perform some basic data exploration.

``` r
summary(groceries)
```

    ## transactions as itemMatrix in sparse format with
    ##  9835 rows (elements/itemsets/transactions) and
    ##  169 columns (items) and a density of 0.02609146
    ##
    ## most frequent items:
    ##       whole milk other vegetables       rolls/buns             soda
    ##             2513             1903             1809             1715
    ##           yogurt          (Other)
    ##             1372            34055
    ##
    ## element (itemset/transaction) length distribution:
    ## sizes
    ##    1    2    3    4    5    6    7    8    9   10   11   12   13   14   15
    ## 2159 1643 1299 1005  855  645  545  438  350  246  182  117   78   77   55
    ##   16   17   18   19   20   21   22   23   24   26   27   28   29   32
    ##   46   29   14   14    9   11    4    6    1    1    1    1    3    1
    ##
    ##    Min. 1st Qu.  Median    Mean 3rd Qu.    Max.
    ##   1.000   2.000   3.000   4.409   6.000  32.000
    ##
    ## includes extended item information - examples:
    ##             labels
    ## 1 abrasive cleaner
    ## 2 artif. sweetener
    ## 3   baby cosmetics

``` r
inspect (groceries[1:5])
```

    ##     items
    ## [1] {citrus fruit,
    ##      margarine,
    ##      ready soups,
    ##      semi-finished bread}
    ## [2] {coffee,
    ##      tropical fruit,
    ##      yogurt}
    ## [3] {whole milk}
    ## [4] {cream cheese,
    ##      meat spreads,
    ##      pip fruit,
    ##      yogurt}
    ## [5] {condensed milk,
    ##      long life bakery product,
    ##      other vegetables,
    ##      whole milk}

``` r
itemFrequency(groceries[,1:3])
```

    ## abrasive cleaner artif. sweetener   baby cosmetics
    ##     0.0035587189     0.0032536858     0.0006100661

I will call **item** to a product purchased in each cart. And **item set**, is products occurring together.

In association analysis there are 3 main concepts to work with:

1. **Support:** The fraction of which our item set occurs in our data set.
2. **Confidence:** probability that a rule is correct for a new transaction with items on the left.
3. **Lift:** The ratio by which by the confidence of a rule exceeds the expected confidence.

## Data visualization


Items at least with 10% support.

``` r
itemFrequencyPlot(groceries, support = 0.1)
```

![](/MBA-unnamed-chunk-7-1.png)

Frequency Plot for the top 20 items

``` r
itemFrequencyPlot(groceries, topN = 20)
```

![](/MBA-unnamed-chunk-8-1.png)

It is also possible to visualize the entire Sparse Matrix:

``` r
image(groceries[1:5])
```

![](/MBA-unnamed-chunk-9-1.png)

``` r
image(sample(groceries, 100))
```

![](/MBA-unnamed-chunk-9-2.png)

# Building the Model


We are now ready to mine some rules! + We set the minimum support to 0.006. + We set the minimum confidence of 0.25. + We set the minimum to 2 items.

``` r
apriori(groceries)#Mine frequent itemsets
```

    ## Apriori
    ##
    ## Parameter specification:
    ##  confidence minval smax arem  aval originalSupport maxtime support minlen
    ##         0.8    0.1    1 none FALSE            TRUE       5     0.1      1
    ##  maxlen target   ext
    ##      10  rules FALSE
    ##
    ## Algorithmic control:
    ##  filter tree heap memopt load sort verbose
    ##     0.1 TRUE TRUE  FALSE TRUE    2    TRUE
    ##
    ## Absolute minimum support count: 983
    ##
    ## set item appearances ...[0 item(s)] done [0.00s].
    ## set transactions ...[169 item(s), 9835 transaction(s)] done [0.00s].
    ## sorting and recoding items ... [8 item(s)] done [0.00s].
    ## creating transaction tree ... done [0.00s].
    ## checking subsets of size 1 2 done [0.00s].
    ## writing ... [0 rule(s)] done [0.00s].
    ## creating S4 object  ... done [0.00s].

    ## set of 0 rules

``` r
# Get the rules
rules <- apriori(groceries, parameter = list(supp = 0.006,
                                             conf = 0.25,
                                             minlen = 2))
```

    ## Apriori
    ##
    ## Parameter specification:
    ##  confidence minval smax arem  aval originalSupport maxtime support minlen
    ##        0.25    0.1    1 none FALSE            TRUE       5   0.006      2
    ##  maxlen target   ext
    ##      10  rules FALSE
    ##
    ## Algorithmic control:
    ##  filter tree heap memopt load sort verbose
    ##     0.1 TRUE TRUE  FALSE TRUE    2    TRUE
    ##
    ## Absolute minimum support count: 59
    ##
    ## set item appearances ...[0 item(s)] done [0.00s].
    ## set transactions ...[169 item(s), 9835 transaction(s)] done [0.00s].
    ## sorting and recoding items ... [109 item(s)] done [0.00s].
    ## creating transaction tree ... done [0.00s].
    ## checking subsets of size 1 2 3 4 done [0.00s].
    ## writing ... [463 rule(s)] done [0.00s].
    ## creating S4 object  ... done [0.00s].

``` r
summary(rules)
```

    ## set of 463 rules
    ##
    ## rule length distribution (lhs + rhs):sizes
    ##   2   3   4
    ## 150 297  16
    ##
    ##    Min. 1st Qu.  Median    Mean 3rd Qu.    Max.
    ##   2.000   2.000   3.000   2.711   3.000   4.000
    ##
    ## summary of quality measures:
    ##     support           confidence          lift
    ##  Min.   :0.006101   Min.   :0.2500   Min.   :0.9932
    ##  1st Qu.:0.007117   1st Qu.:0.2971   1st Qu.:1.6229
    ##  Median :0.008744   Median :0.3554   Median :1.9332
    ##  Mean   :0.011539   Mean   :0.3786   Mean   :2.0351
    ##  3rd Qu.:0.012303   3rd Qu.:0.4495   3rd Qu.:2.3565
    ##  Max.   :0.074835   Max.   :0.6600   Max.   :3.9565
    ##
    ## mining info:
    ##       data ntransactions support confidence
    ##  groceries          9835   0.006       0.25

## Evaluating model performance

The size of the rule is calculated as the total of both Left-hand side (LHS) and right-hand side of the rule (RHS).

``` r
inspect(rules[1:5])
```

    ##     lhs             rhs                support     confidence lift
    ## [1] {pot plants} => {whole milk}       0.006914082 0.4000000  1.565460
    ## [2] {pasta}      => {whole milk}       0.006100661 0.4054054  1.586614
    ## [3] {herbs}      => {root vegetables}  0.007015760 0.4312500  3.956477
    ## [4] {herbs}      => {other vegetables} 0.007727504 0.4750000  2.454874
    ## [5] {herbs}      => {whole milk}       0.007727504 0.4750000  1.858983

Sorting the set of the association Rule by lift

``` r
inspect(sort(rules, by ="lift")[1:5])
```

    ##     lhs                   rhs                      support confidence     lift
    ## [1] {herbs}            => {root vegetables}    0.007015760  0.4312500 3.956477
    ## [2] {berries}          => {whipped/sour cream} 0.009049314  0.2721713 3.796886
    ## [3] {other vegetables,
    ##      tropical fruit,
    ##      whole milk}       => {root vegetables}    0.007015760  0.4107143 3.768074
    ## [4] {beef,
    ##      other vegetables} => {root vegetables}    0.007930859  0.4020619 3.688692
    ## [5] {other vegetables,
    ##      tropical fruit}   => {pip fruit}          0.009456024  0.2634561 3.482649

## Targeting Items

I am going to subset to see if a particular item is purchased along with others.

There are two types of targets we might be interested in that are illustrated with some examples: + What are customers likely to buy after buying "blueberries" + What are customers likely to buy before buying "whole milk"" + What are customers likely to buy if they purchase "yogurt" and "blueberries"?

``` r
berryrules <- subset(rules, items %in% "berries")
inspect((berryrules))
```

    ##     lhs          rhs                  support     confidence lift
    ## [1] {berries} => {whipped/sour cream} 0.009049314 0.2721713  3.796886
    ## [2] {berries} => {yogurt}             0.010574479 0.3180428  2.279848
    ## [3] {berries} => {other vegetables}   0.010269446 0.3088685  1.596280
    ## [4] {berries} => {whole milk}         0.011794611 0.3547401  1.388328

Interesting, it seems people buy berries to consume mostly for breakfast time. Mixing them with milk (maybe as a shake) or with yoghurt or cream.

Now, the second question can also be answered.

``` r
milkrules<-apriori(data=groceries, parameter=list(supp=0.001,conf = 0.08),
               appearance = list(default="lhs",rhs="whole milk"),
               control = list(verbose=F))
milkrules<-sort(rules, decreasing=TRUE,by="confidence")
inspect(milkrules[1:5])
```

    ##     lhs                            rhs          support     confidence
    ## [1] {butter,whipped/sour cream} => {whole milk} 0.006710727 0.6600000
    ## [2] {butter,yogurt}             => {whole milk} 0.009354347 0.6388889
    ## [3] {butter,root vegetables}    => {whole milk} 0.008235892 0.6377953
    ## [4] {curd,tropical fruit}       => {whole milk} 0.006507372 0.6336634
    ## [5] {butter,tropical fruit}     => {whole milk} 0.006202339 0.6224490
    ##     lift
    ## [1] 2.583008
    ## [2] 2.500387
    ## [3] 2.496107
    ## [4] 2.479936
    ## [5] 2.436047

and mixing queries...

``` r
rules2 <- subset(rules, items %in% c("berries", "yogurt"))
inspect(rules2[1:10])
```

    ##      lhs                rhs                  support     confidence
    ## [1]  {cat food}      => {yogurt}             0.006202339 0.2663755
    ## [2]  {hard cheese}   => {yogurt}             0.006405694 0.2614108
    ## [3]  {butter milk}   => {yogurt}             0.008540925 0.3054545
    ## [4]  {ham}           => {yogurt}             0.006710727 0.2578125
    ## [5]  {sliced cheese} => {yogurt}             0.008032537 0.3278008
    ## [6]  {berries}       => {whipped/sour cream} 0.009049314 0.2721713
    ## [7]  {berries}       => {yogurt}             0.010574479 0.3180428
    ## [8]  {berries}       => {other vegetables}   0.010269446 0.3088685
    ## [9]  {berries}       => {whole milk}         0.011794611 0.3547401
    ## [10] {dessert}       => {yogurt}             0.009862735 0.2657534
    ##      lift
    ## [1]  1.909478
    ## [2]  1.873889
    ## [3]  2.189610
    ## [4]  1.848095
    ## [5]  2.349797
    ## [6]  3.796886
    ## [7]  2.279848
    ## [8]  1.596280
    ## [9]  1.388328
    ## [10] 1.905018

Except for the cat-food item, the other products seem to be purchased also for breakfast time.

# Visualization


``` r
plot(rules,method="graph",interactive=TRUE,shading=NA)
```
![](/MBA-unnamed-chunk-19-1.png)

## Save rules

I will, finally, convert the rules as data frame in order to view it in the R studio viewer and will save in a csv for extensive analysing purposes.

``` r
rules_df <- as(rules, "data.frame")
write(rules, file = "groceryrules.csv",
      sep = ",",
      quote =TRUE,
      row.names = FALSE)
```
