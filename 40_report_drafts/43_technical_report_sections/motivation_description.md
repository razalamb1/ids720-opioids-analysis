###The motivation for the project:

Social policies play an essential role in regulating people's lives and the development of society. The motivation for this project is to 
quantify the impact of state policy changes in comparison to places where such policy changes didn't take place, to determine whether 
and to what extent these policies have addressed the current problems, and whether the policy chages can inform the development of more 
effective policies in the future. The context of this project is the increase in drug addiction and prescription opioid overdose deaths 
in the US in the past two decades. In this project, we'll measure the effect of a series of policy changes designed to limit abuse of 
prescription opioid drugs and mortality from drug overdoses. Three policies we will be focusing on were effective in Florida, Texas, 
and Washington in 2010, 2007 and 2012, respectively. 


###The motivation for the research design being used:

The research design that we're implementing should show us if the policy changes in Florida, Texas, and Washington affected the number of deaths related to 
opioid abuse and the number of prescription opioids shipped into the state. Therefore, the motivation for the research design is to establish a causal 
relationship between policy change and opioid abuse parameters. We will achieve this by using two strategiesin tandem: pre-post comparison and 
difference-in-difference analysis. Pre-post comparison will show us what opioid abuse parameters look like beforeand after the policy change. 
In difference-in-difference analysis, we will compare the pre and post-periods in policy state of interest to a control group 
with no policy change. This analysis will eliminate the causal effects of changes other than the policy change that could lead us to misinterpretating 
the result. 

###Details of the data used and how different datasets have been related to one another:

Three datasets that were used in the analysis were 1) all opioid prescription drug shipments in the US from 2006-2012 (from US Drug Enforcement Agency, 
requested by Washington Post), 2) mortality due to drug and non-drug-related causes in the US from 2003-2015 (from US Vital Statistics records), and 
3) Population and population estimates for each us county from 2003-2015 (from US Census). The opioid shipment data had detailed information for 
each transaction that happened, including buyer/reporter, drug type/dose, date. From these, we kept transaction date, buyer state/county/zip, drug code/name,
the total active weight of drug, dosage unit, drug morphine equivalent, and dose strength in milligrams. We decided to use total active weight in grams
(CALC_BASE_WT_IN_GM) to represent opioid shipment for each transaction. We grouped the selected columns by transaction year, buyer country, and 
CALC_BASE_WT_IN_GM to get the final data frame. For the mortality dataset, we read data for each year in separate excel sheets. We subsetted data 
for Drug/Alcohol-related deaths in category D. We grouped data by State, County, Year, and summed occurrences in these groups. For the population data,
we used data from US Census in 2000 and 2010. We constructed a data frame with population count for years available and population estimates for the 
remaining years from 2003-2015. The final data frame had state, county, year, population columns. After cleaning three datasets, we merged population 
dataframe to both mortality and opioid shipment. We performed a 1:1 outer merge of population and mortality datasets on state, county, and year.
Counts that did not have observations for 13 years did not seem worthy of being added to this discussion, while those that had values in some years,
we kept them and filled the remaining nulls with 0s. We also performed a 1:1 outer merge between populations and shipment datasets on state, county, year.
We dropped non-mainland regions and filled in nulls with 0s. Once wehad the two merged datasets, we subsetted both for each policy state and others. 
We also added an indicator variable showing if the observation was pre or post-policy and normalized data by population. These final datasets were 
used for analysis.


###Summary statistics for your data:

Data Statistics for Florida, Mortality :
|       |Deaths,total |   deaths_per_100k |
|:------|------------:|------------------:|
| count | 871         |         871       |
| mean  |  37.4263    |          14.6665  |
| std   |  63.4655    |           4.64608 |
| min   |   0.0863859 |           3.90227 |
| 25%   |   0.40555   |          12.5642  |
| 50%   |  11         |          14.5381  |
| 75%   |  40.5       |          16.3985  |
| max   | 326         |          40.8222  |

Data Statistics for Washington, Mortality :
|       |Deaths,total |   deaths_per_100k |
|:------|------------:|------------------:|
| count | 507         |          507      |
| mean  |  20.4532    |           13.4558 |
| std   |  48.3154    |            3.335  |
| min   |   0.0232961 |            4.2504 |
| 25%   |   0.274741  |           12.0201 |
| 50%   |   0.814898  |           13.6818 |
| 75%   |  16         |           14.3425 |
| max   | 309         |           30.685  |

Data Statistics for Texas, Mortality :
|       |   Deaths,total |   deaths_per_100k |
|:------|---------------:|------------------:|
| count | 3302           |        3302       |
| mean  |    7.09966     |          10.2316  |
| std   |   34.9609      |           2.24658 |
| min   |    0.000454319 |           1.43812 |
| 25%   |    0.0676432   |           9.36017 |
| 50%   |    0.18248     |           9.95264 |
| 75%   |    0.496975    |          10.6828  |
| max   |  528           |          42.7442  |

Data Statistics for Florida, Annual Opioid Shipment :
|       |shipment,total |   shipment_per_resident |
|:------|--------------:|------------------------:|
| count | 469           |                 469     |
| mean  |   2.26374e+08 |                 640.032 |
| std   |   4.41328e+08 |                 385.64  |
| min   |   0           |                   0     |
| 25%   |   1.24526e+07 |                 356.089 |
| 50%   |   6.77975e+07 |                 572.974 |
| 75%   |   2.22017e+08 |                 816.735 |
| max   |   3.43323e+09 |                2582.39  |

Data Statistics for Washington, Annual Opioid Shipment :
|       |shipment,total |   shipment_per_resident |
|:------|--------------:|------------------------:|
| count | 273           |                 273     |
| mean  |   7.62184e+07 |                 467.972 |
| std   |   1.39873e+08 |                 197.039 |
| min   |   1.03975e+06 |                 137.011 |
| 25%   |   9.268e+06   |                 319.47  |
| 50%   |   2.48922e+07 |                 416.167 |
| 75%   |   6.43875e+07 |                 581.359 |
| max   |   7.86435e+08 |                1082.66  |

Data Statistics for Texas, Annual Opioid Shipment :
|       | shipment,total |   shipment_per_resident |
|:------|---------------:|------------------------:|
| count | 1778           |                1778     |
| mean  |    3.0085e+07  |                 260.959 |
| std   |    1.18823e+08 |                 185.31  |
| min   |    0           |                   0     |
| 25%   |    1.08372e+06 |                 128.189 |
| 50%   |    4.29198e+06 |                 240.878 |
| 75%   |    1.78259e+07 |                 373.066 |
| max   |    1.82396e+09 |                1247.6   |

Data Statistics for Florida, Monthly Shipment :
|       | shipment,total |   shipment_per_resident |
|:------|---------------:|------------------------:|
| count | 5628           |               5628      |
| mean  |    1.88645e+07 |                 53.336  |
| std   |    3.73027e+07 |                 33.1503 |
| min   |    0           |                  0      |
| 25%   |    1.03512e+06 |                 29.2221 |
| 50%   |    5.70403e+06 |                 47.17   |
| 75%   |    1.79521e+07 |                 68.2473 |
| max   |    3.95105e+08 |                293.004  |

Data Statistics for Texas, Monthly Shipment :
|       |   shipment,total |   shipment_per_resident |
|:------|-----------------:|------------------------:|
| count |  21336           |              21336      |
| mean  |      2.50708e+06 |                 21.7466 |
| std   |      9.93162e+06 |                 15.8343 |
| min   |      0           |                  0      |
| 25%   |  86500           |                 10.2439 |
| 50%   | 361263           |                 20.1635 |
| 75%   |      1.49206e+06 |                 30.9853 |
| max   |      1.81066e+08 |                157.198  |

Data Statistics for Washington, Monthly Shipment :
|       |   shipment,total |   shipment_per_resident |
|:------|-----------------:|------------------------:|
| count |   3276           |              3276       |
| mean  |      6.35154e+06 |                38.9976  |
| std   |      1.16649e+07 |                16.9282  |
| min   |  40750           |                 8.33754 |
| 25%   | 727212           |                26.3117  |
| 50%   |      2.10206e+06 |                34.9091  |
| 75%   |      5.47547e+06 |                48.2707  |
| max   |      7.15086e+07 |               110.665   |


Data Statistics for the County Population Dataset : 
|       |       population |
|:------|-----------------:|
| count |  40853           |
| mean  |  97386.9         |
| std   | 312310           |
| min   |     55           |
| 25%   |  11061           |
| 50%   |  25580           |
| 75%   |  65964           |
| max   |      1.00854e+07 |





