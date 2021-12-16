## Analysis Methodology
We have opioid shipment data for Florida only and opioid overdose death data for Florida, Washington, and Texas. As such, the measured metrics are shipment and overdose death for Florida and only overdose death for Washington and Texas. To investigate the effect of opioid drug prescription regulations on the volume of opioid shipment and drug overdose deaths, we employed two methodologies.  First, we compared the metrics before and after the regulations went into effect in each state. Next, we performed difference-in-difference analyses to account for nation-wide factors that might have influenced the values of the metrics so that we can more accurately quantify the effect of the regulation changes.

### Pre-Post Comparison
To investigate the effect of opioid drug prescription regulations on volume of opioids prescribed and drug overdose deaths, we employed two methodologies. First, we compared the metrics before and after the regulations went into effect in each state. Next, we performed difference-in-difference analyses to account for nation-wide factors that might have influenced the values of the metrics so that we can more accurately quantify the effect of the regulation changes.

#### Analysis Time Periods
The pre-period of each analysis includes all years before the regulation took effect in the state. The year that the regulation took effect and onwards are the post-period. Each of the three states we investigated implemented regulations in different years. In addition, the opioid shipment and drug overdose death data sets we used cover different time periods. As such, the pre- and post-periods for each analysis is different. 

We have laid out the pre- and post-periods for each analysis below to clarify the time periods of each analysis.

| State      	| Analysis              	| Regulation Date 	| Pre-Period  	| Post-Period 	|
|------------	|-----------------------	|-----------------	|-------------	|-------------	|
| Florida    	| Opioid Shipment       	| February, 2010  	| 2006 - 2009 	| 2010 - 2012 	|
| Florida    	| Opioid Overdose Death 	| February, 2010  	| 2003 - 2009 	| 2010 - 2015 	|
| Texas      	| Opioid Overdose Death 	| January, 2007   	| 2003 - 2006 	| 2007 - 2015 	|
| Washington 	| Opioid Overdose Death 	| January, 2012   	| 2003 - 2011 	| 2012 - 2015 	|

#### Methodology
For each analysis, we created an indicator variable that would mark whether each observation was from the pre-period or the post-period. We then ran linear regressions for the pre-period and the post-period separately, using year as the independent variable and the metric of interest of the analysis (shipment or overdose death) as the dependent variable. We also calculated the 95% confidence interval for each regression.

To visualize the effect of regulation, we plotted the regression line and the confidence band of the pre-period and those of the post-period on the same plot. In each plot, the x-axis represents year and the y-axis represents the metric of interest.

Opioid shipment and overdose death had been increasing the Florida, Texas, and Washington before the regulations took effect. As such, if opioid regulations did have a positive effect on opioid prescriptions or overdose death, we’d expect the post-period regression line to have a smaller slope than the pre-period regression line. If the slopes in the post-period and the pre-period are similar, then the regulations likely did not have a meaningful impact. 

### Difference-in-Difference
The pre-post comparison method described above is an easy and straightforward way to visualize the effect of regulation of opioid. However, it is difficult to attribute the changes of pre- vs post-period slopes to the regulations because the pre-post comparison method does not account for potential confounders.

To overcome this limitation, we next employed a difference-in-difference method, in which we compared the counties in Florida, Texas, and Washington to similar counties. To make things easier, we’ll refer to counties in Florida, Texas, and Washington each as a “test group”, and the group of similar counties selected for each test group the “control group”. For each test group, we selected a control group comprised of similar counties. The selection method is described below.

#### Control Group Selection
To ensure that the difference-in-difference methodology measures the effect of regulations instead of effects of confounders, we’d need to find control counties that are as similar to the test group as possible. Most importantly, we have to ensure that the control group has a similar pre-period slope as the test group. To achieve this, we used the below process to select control counties for each test group.

1.	Calculate the pre-period slope of the measured metric (shipment / mortality) for counties in the test group and counties in the rest of the country
2.	Calculate the pre-period average population of counties in the test group and counties in the rest of the country
3.	For each county in the test group, select 2 counties in the control group whose pre-period slope is the most similar to that of the test county
4.	If there are ties, narrow down to 2 counties whose pre-period average population is the most similar to the that of the test county
5.	Draw with replacement

Following the process above, we selected 2 similar counties for each county in the three test groups. Counties were first selected based on pre-period slope of the measured metric. There were many counties in the test groups whose pre-period slope was 0 – for those counties, we selected control counties whose pre-period slope was also 0 and who had similar population as the test county.

We drew with replacement so that if a particular county was selected as the control multiple times, then we’d give the county a higher weight in the control group accordingly.

#### Time Period
The pre- and post-period of each analysis is the same as the time periods listed out in the table under the previous section. For each analysis, we used the same time periods for the test group and the control group.

#### Methodology
Similar to the pre-post comparison analysis, we created an indicator variable to mark whether an observation was from the pre-period or the post-period. In each analysis, we ran four regressions, one each for the test and control groups in the pre- and post-periods. We then plotted the regression lines and as well as the confidence bands using 95% confidence level.

We plotted each analysis in a separate plot. On each plot, there are 4 lines – test group in the pre-period, test group in the post-period, control group in the pre-period, and control group in the post-period. To distinguish the test group from the control group, we applied different colors for each group. If we had performed the control selection appropriately, we’d expect to see similar slopes for the regression lines of the test group and the control group in the pre-period. If the regulation had a meaningful impact on opioid shipment or overdose death, then we’d expect the slope of the test group in the post-period to decrease while the slope of the control group in the post-period remains constant or decreases by a smaller magnitude.

