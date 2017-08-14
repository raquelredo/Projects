---
title: "911 Data Exploration"
layout: post
excerpt: "Using some Python data exploration libraries.
The intention here is just Explore the Dataset. Put in action some Data visualization libraries and tools.

-   Features: 9
-   Observations: 205,580
-   Tuples: 1,850,220

**Challenges:** Work with different visualization tools | work with Python"
tags: [python, seaborn, matplotlib, numpy, pandas]
categories: portfolio
header:
  teaser: call-center.png
link:
share: true
comments: false
---

This kernel is about some data exploration with plots on the Dataset 911 Emergency Calls. I  am using it to practice some Python visualization skills learned from Jose Portilla's Python course at [Udemy][9295e9ed], as well as a show window for newbies on Python. Let's start!

  [9295e9ed]: https://www.udemy.com/courses/ "Udemy"

```python
import numpy as np #for numerical operations
import pandas as pd #for working with dataframes
import matplotlib.pyplot as plt #for data visualization
import seaborn as sns #for data visualization
%matplotlib inline
#to be able to show plots in this jupyter notebook
```
```python
df = pd.read_csv("../input/911.csv") #import dataframe to this kernel
```
Checking the basic information:

```python
df.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 205580 entries, 0 to 205579
    Data columns (total 9 columns):
    lat          205580 non-null float64
    lng          205580 non-null float64
    desc         205580 non-null object
    zip          180597 non-null float64
    title        205580 non-null object
    timeStamp    205580 non-null object
    twp          205506 non-null object
    addr         205580 non-null object
    e            205580 non-null int64
    dtypes: float64(3), int64(1), object(5)
    memory usage: 14.1+ MB

```python
df.head()
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
      <th>lat</th>
      <th>lng</th>
      <th>desc</th>
      <th>zip</th>
      <th>title</th>
      <th>timeStamp</th>
      <th>twp</th>
      <th>addr</th>
      <th>e</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>40.297876</td>
      <td>-75.581294</td>
      <td>REINDEER CT &amp; DEAD END;  NEW HANOVER; Station ...</td>
      <td>19525.0</td>
      <td>EMS: BACK PAINS/INJURY</td>
      <td>2015-12-10 17:10:52</td>
      <td>NEW HANOVER</td>
      <td>REINDEER CT &amp; DEAD END</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>40.258061</td>
      <td>-75.264680</td>
      <td>BRIAR PATH &amp; WHITEMARSH LN;  HATFIELD TOWNSHIP...</td>
      <td>19446.0</td>
      <td>EMS: DIABETIC EMERGENCY</td>
      <td>2015-12-10 17:29:21</td>
      <td>HATFIELD TOWNSHIP</td>
      <td>BRIAR PATH &amp; WHITEMARSH LN</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>40.121182</td>
      <td>-75.351975</td>
      <td>HAWS AVE; NORRISTOWN; 2015-12-10 @ 14:39:21-St...</td>
      <td>19401.0</td>
      <td>Fire: GAS-ODOR/LEAK</td>
      <td>2015-12-10 14:39:21</td>
      <td>NORRISTOWN</td>
      <td>HAWS AVE</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>40.116153</td>
      <td>-75.343513</td>
      <td>AIRY ST &amp; SWEDE ST;  NORRISTOWN; Station 308A;...</td>
      <td>19401.0</td>
      <td>EMS: CARDIAC EMERGENCY</td>
      <td>2015-12-10 16:47:36</td>
      <td>NORRISTOWN</td>
      <td>AIRY ST &amp; SWEDE ST</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>40.251492</td>
      <td>-75.603350</td>
      <td>CHERRYWOOD CT &amp; DEAD END;  LOWER POTTSGROVE; S...</td>
      <td>NaN</td>
      <td>EMS: DIZZINESS</td>
      <td>2015-12-10 16:56:52</td>
      <td>LOWER POTTSGROVE</td>
      <td>CHERRYWOOD CT &amp; DEAD END</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>

Basic Exploration:

1. Top zipcodes for 911 calls?
2. Top 5 townships for 911 calls?
3. how many unique title codes are?

```python
df["zip"].value_counts().head(5)
```

    19401.0    14234
    19464.0    13859
    19403.0    10372
    19446.0     9910
    19406.0     6777
    Name: zip, dtype: int64

```python
df["twp"].value_counts().head(5)
```
    LOWER MERION    17646
    ABINGTON        12570
    NORRISTOWN      11892
    UPPER MERION    10699
    CHELTENHAM       9461
    Name: twp, dtype: int64

```python
df["title"].nunique()
```
    125

## Creating new features
In the title feature we have the reason/department , the values are as example similar to ``EMS: DIABETIC EMERGENCY``
I will create a new column splitting by the value Reason `EMS`

```python
df["Reason"] = df["title"].apply(lambda title: title.split(":")[0])
```

```python
df["Reason"].head(10)
```


    0        EMS
    1        EMS
    2       Fire
    3        EMS
    4        EMS
    5        EMS
    6        EMS
    7        EMS
    8        EMS
    9    Traffic
    Name: Reason, dtype: object


Which is the most common reason for calling 911?

```python
df["Reason"].value_counts()
```

    EMS        102623
    Traffic     72404
    Fire        30553
    Name: Reason, dtype: int64


plotting

```python
sns.countplot( x= "Reason", data = df, palette = "viridis")
```





![](/Data%20Exploration_16_1.png)


Ther is no doubt that the biggest numbers are for calls `EMS` (Emergency Medical Service), followed by `traffic` and more far away for `Fire reasons`


```python
type(df["timeStamp"].iloc[0])
```

    str


```python
df["timeStamp"] = pd.to_datetime(df["timeStamp"])
df["timeStamp"].iloc[0]
```

    Timestamp('2015-12-10 17:10:52')


I will create new columns for slicing by the time attribute.


```python
df["Hour"] = df["timeStamp"].apply(lambda time: time.hour)
df["Month"] = df["timeStamp"].apply(lambda time: time.month)
df["Day of the Week"] = df["timeStamp"].apply(lambda time: time.dayofweek)
```


```python
df["Day of the Week"].head(10)
```


    0    3
    1    3
    2    3
    3    3
    4    3
    5    3
    6    3
    7    3
    8    3
    9    3
    Name: Day of the Week, dtype: int64



I will assign this integer numbers for day of the week to the corresponding names of the weekdays.


```python
dmap = {0:"Mon", 1:"Tue", 2:"Wed", 3:"Thu", 4:"Fri", 5:"Sat", 6:"Sun"} #create the map dictionary
df["Day of the Week"] = df["Day of the Week"].map(dmap)
```

Now I will plot a countplot of the new column, `Day of the Week`, with hue based off the `Reason` Column


```python
sns.countplot(x = "Day of the Week", data = df, hue = "Reason", palette = "viridis")
#I need to relocate the legend that by default is drawn in the midlle of the graph
plt.legend(bbox_to_anchor = (1.05, 1), loc = 2,  borderaxespad = 0.)
```


![](/Data%20Exploration_26_1.png)


We do have much more stability on count numbers if we look within the week days. A bit difference is seen in `Traffic`calls value. Not surprisingly Saturday and Sundays there is a valley on the number of calls. Is it because weekends people are much more relaxed and have better driving? is it because there are fewer cars on the street?

Now, I'll do the same by month.


```python
sns.countplot(x = "Month", data = df, hue = "Reason", palette = "viridis")
#I need to relocate the legend that by default is drawn in the midlle of the graph
plt.legend(bbox_to_anchor = (1.05, 1), loc = 2,  borderaxespad = 0.)
```


![](/Data%20Exploration_29_1.png)


It seems that colder months are more sensible in `EMS` ocurrences as well as the other reasons.

Create a new column `Date` that contains the date from the `timeStamp` column


```python
df["Date"] = df["timeStamp"].apply(lambda t: t.date())
df["Date"].head(5)
```

    0    2015-12-10
    1    2015-12-10
    2    2015-12-10
    3    2015-12-10
    4    2015-12-10
    Name: Date, dtype: object



now, I will group from this `Date` columns


```python
df.groupby("Date").count()["twp"].plot()
plt.tight_layout()
```

![](Data%20Exploration_34_0.png)


the same, but now separating each `Reason`:


```python
df[df["Reason"]== "Traffic"].groupby("Date").count()["twp"].plot()
plt.title("Traffic")
plt.tight_layout()
```

![](/Data%20Exploration_36_0.png)


```python
df[df["Reason"]== "Fire"].groupby("Date").count()["twp"].plot()
plt.title("Fire")
plt.tight_layout()
```

![](/Data%20Exploration_37_0.png)


```python
df[df["Reason"]== "EMS"].groupby("Date").count()["twp"].plot()
plt.title("EMS")
plt.tight_layout()
```


![](/Data%20Exploration_38_0.png)


## Heat maps Time!

I love Heat maps for analysing values along with time series. At the end our brain is used to wath time events in the form of a calendar week, month or year. Once the data is correctly displayed for us to interpret we can easily find unusual or explainable patterns.
For heat maps we need to reshape a bit the data frame. I need the columns to be hours and the `Index` to become the `Day of the Week`.


```python
dayHour = df.groupby(by = ["Day of the Week", "Hour"]).count()["Reason"].unstack()
dayHour.head(7)
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
      <th>Hour</th>
      <th>0</th>
      <th>1</th>
      <th>2</th>
      <th>3</th>
      <th>4</th>
      <th>5</th>
      <th>6</th>
      <th>7</th>
      <th>8</th>
      <th>9</th>
      <th>...</th>
      <th>14</th>
      <th>15</th>
      <th>16</th>
      <th>17</th>
      <th>18</th>
      <th>19</th>
      <th>20</th>
      <th>21</th>
      <th>22</th>
      <th>23</th>
    </tr>
    <tr>
      <th>Day of the Week</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Fri</th>
      <td>554</td>
      <td>493</td>
      <td>448</td>
      <td>414</td>
      <td>379</td>
      <td>466</td>
      <td>859</td>
      <td>1350</td>
      <td>1572</td>
      <td>1610</td>
      <td>...</td>
      <td>1889</td>
      <td>2070</td>
      <td>2142</td>
      <td>2146</td>
      <td>1647</td>
      <td>1544</td>
      <td>1364</td>
      <td>1184</td>
      <td>1105</td>
      <td>875</td>
    </tr>
    <tr>
      <th>Mon</th>
      <td>561</td>
      <td>442</td>
      <td>429</td>
      <td>379</td>
      <td>433</td>
      <td>541</td>
      <td>858</td>
      <td>1385</td>
      <td>1777</td>
      <td>1747</td>
      <td>...</td>
      <td>1763</td>
      <td>1956</td>
      <td>1983</td>
      <td>2015</td>
      <td>1735</td>
      <td>1421</td>
      <td>1207</td>
      <td>950</td>
      <td>838</td>
      <td>641</td>
    </tr>
    <tr>
      <th>Sat</th>
      <td>743</td>
      <td>622</td>
      <td>534</td>
      <td>509</td>
      <td>490</td>
      <td>482</td>
      <td>581</td>
      <td>778</td>
      <td>1018</td>
      <td>1344</td>
      <td>...</td>
      <td>1656</td>
      <td>1632</td>
      <td>1634</td>
      <td>1585</td>
      <td>1547</td>
      <td>1484</td>
      <td>1234</td>
      <td>1135</td>
      <td>1027</td>
      <td>968</td>
    </tr>
    <tr>
      <th>Sun</th>
      <td>745</td>
      <td>660</td>
      <td>640</td>
      <td>534</td>
      <td>458</td>
      <td>468</td>
      <td>562</td>
      <td>738</td>
      <td>928</td>
      <td>1223</td>
      <td>...</td>
      <td>1452</td>
      <td>1395</td>
      <td>1371</td>
      <td>1481</td>
      <td>1421</td>
      <td>1302</td>
      <td>1091</td>
      <td>979</td>
      <td>766</td>
      <td>685</td>
    </tr>
    <tr>
      <th>Thu</th>
      <td>564</td>
      <td>413</td>
      <td>466</td>
      <td>365</td>
      <td>357</td>
      <td>512</td>
      <td>893</td>
      <td>1451</td>
      <td>1682</td>
      <td>1757</td>
      <td>...</td>
      <td>1838</td>
      <td>1998</td>
      <td>1959</td>
      <td>2162</td>
      <td>1741</td>
      <td>1438</td>
      <td>1277</td>
      <td>1122</td>
      <td>887</td>
      <td>705</td>
    </tr>
    <tr>
      <th>Tue</th>
      <td>555</td>
      <td>461</td>
      <td>417</td>
      <td>373</td>
      <td>398</td>
      <td>495</td>
      <td>866</td>
      <td>1421</td>
      <td>1787</td>
      <td>1786</td>
      <td>...</td>
      <td>1879</td>
      <td>1946</td>
      <td>2157</td>
      <td>2072</td>
      <td>1824</td>
      <td>1437</td>
      <td>1265</td>
      <td>1062</td>
      <td>828</td>
      <td>617</td>
    </tr>
    <tr>
      <th>Wed</th>
      <td>524</td>
      <td>461</td>
      <td>391</td>
      <td>421</td>
      <td>337</td>
      <td>508</td>
      <td>898</td>
      <td>1479</td>
      <td>1694</td>
      <td>1717</td>
      <td>...</td>
      <td>1858</td>
      <td>1940</td>
      <td>2089</td>
      <td>2093</td>
      <td>1780</td>
      <td>1433</td>
      <td>1324</td>
      <td>1104</td>
      <td>883</td>
      <td>670</td>
    </tr>
  </tbody>
</table>
<p>7 rows × 24 columns</p>
</div>


```python
plt.figure(figsize = (12,6)) #canvas size
sns.heatmap(dayHour, cmap = "viridis")
```

![](/Data%20Exploration_42_1.png)


As we can observe daylight hours are more usual to have 911 calls than night time. Quite an intuitive answer, as at those hours much more people is awake, therefore there is much more chance of some event occurrence than other hours with most people is resting at home.

Now I will create a cluster map using this DataFrame.


```python
sns.clustermap(dayHour, cmap = "viridis")
```

![](/Data%20Exploration_45_2.png)


now, I will repeat but using the `Month` as the column


```python
dayMonth = df.groupby(by = ["Day of the Week", "Month"]).count()["Reason"].unstack()
dayMonth.head(7)
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
      <th>Month</th>
      <th>1</th>
      <th>2</th>
      <th>3</th>
      <th>4</th>
      <th>5</th>
      <th>6</th>
      <th>7</th>
      <th>8</th>
      <th>9</th>
      <th>10</th>
      <th>11</th>
      <th>12</th>
    </tr>
    <tr>
      <th>Day of the Week</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Fri</th>
      <td>3527</td>
      <td>3171</td>
      <td>3532</td>
      <td>3574</td>
      <td>3278</td>
      <td>1647</td>
      <td>2042</td>
      <td>1740</td>
      <td>2195</td>
      <td>1901</td>
      <td>1699</td>
      <td>3116</td>
    </tr>
    <tr>
      <th>Mon</th>
      <td>3706</td>
      <td>3552</td>
      <td>3103</td>
      <td>3088</td>
      <td>3351</td>
      <td>1609</td>
      <td>1685</td>
      <td>1865</td>
      <td>1552</td>
      <td>2042</td>
      <td>1682</td>
      <td>2777</td>
    </tr>
    <tr>
      <th>Sat</th>
      <td>3527</td>
      <td>2871</td>
      <td>2539</td>
      <td>3490</td>
      <td>2764</td>
      <td>1376</td>
      <td>1691</td>
      <td>1423</td>
      <td>1406</td>
      <td>1935</td>
      <td>1516</td>
      <td>2975</td>
    </tr>
    <tr>
      <th>Sun</th>
      <td>3470</td>
      <td>2339</td>
      <td>2229</td>
      <td>3026</td>
      <td>2580</td>
      <td>1329</td>
      <td>1667</td>
      <td>1360</td>
      <td>1235</td>
      <td>1757</td>
      <td>1281</td>
      <td>2177</td>
    </tr>
    <tr>
      <th>Thu</th>
      <td>3182</td>
      <td>3189</td>
      <td>3909</td>
      <td>3097</td>
      <td>3289</td>
      <td>2055</td>
      <td>1642</td>
      <td>1579</td>
      <td>2165</td>
      <td>1625</td>
      <td>1630</td>
      <td>3264</td>
    </tr>
    <tr>
      <th>Tue</th>
      <td>3953</td>
      <td>3160</td>
      <td>3529</td>
      <td>3065</td>
      <td>3579</td>
      <td>1671</td>
      <td>1650</td>
      <td>1993</td>
      <td>1559</td>
      <td>1542</td>
      <td>2193</td>
      <td>2933</td>
    </tr>
    <tr>
      <th>Wed</th>
      <td>3336</td>
      <td>3381</td>
      <td>3902</td>
      <td>3003</td>
      <td>3225</td>
      <td>2045</td>
      <td>1711</td>
      <td>1944</td>
      <td>1557</td>
      <td>1700</td>
      <td>2090</td>
      <td>2836</td>
    </tr>
  </tbody>
</table>
</div>




```python
plt.figure(figsize = (12,6)) #canvas size
sns.heatmap(dayMonth, cmap = "viridis")
```

![](/Data%20Exploration_48_1.png)


```python
sns.clustermap(dayMonth, cmap = "viridis")
```


![](/Data%20Exploration_49_2.png)
