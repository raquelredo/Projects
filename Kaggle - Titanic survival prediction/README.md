Titanic: Machine Learning from Disaster
================

Dataset
=======

-   test set can be downloaded from : <https://www.kaggle.com/c/titanic/download/test.csv>
-   train set can be downloaded from: <https://www.kaggle.com/c/titanic/download/train.csv>

Description
===========

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

Variable Notes
==============

-   pclass: A proxy for socio-economic status (SES) 1st = Upper 2nd = Middle 3rd = Lower

-   age: Age is fractional if less than 1. If the age is estimated, is it in the form of xx.5

-   sibsp: The dataset defines family relations in this way... Sibling = brother, sister, stepbrother, stepsister Spouse = husband, wife (mistresses and fiancés were ignored)

-   parch: The dataset defines family relations in this way... Parent = mother, father Child = daughter, son, stepdaughter, stepson Some children travelled only with a nanny, therefore parch=0 for them.
