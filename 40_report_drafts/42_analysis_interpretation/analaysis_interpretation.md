## Analysis Interpretation

### Pre-Post Analysis

Initially, we conducted our pre-post analysis, simply looking at the trend in either opioid prescription shipments or opioid overdoses in states with a policy change, before and after that policy change. Therefore, four relevant graphs were generated: opioid shipments in Florida, and opioid overdoses in Florida, Texas, and Washington, individually. These graphs visually demonstrate whether or not there was a change in the trend of opioid shipments or mortality per year before and after the state's policy change. First off, included are both opioid shipments per capita and mortality per capita before and after a significant policy change in 2010.

<p float="left">
<img src="../30_results/prepost_Florida_mortality.png" width="330" height="180" />
<img src="../30_results/prepost_Florida_shipment.png" width="330" height="180" />
</p>

Interestingly, we can see that there is a clear increasing trend in both opioid shipments and opioid mortality prior to 2010, after which this trend is reversed. However, as visualized by the 95% confidence bands, there is greater uncertainty (i.e. more spread) in the mortality data. This is likely due to the fact that the vast majority of counties have less than 10 opioid mortality deaths per year, which are unreportable, and represented as zeros in our dataset. Overall, from these graphs, we can assert relatively confidently that there was a change in the trend of opioid shipments per capita in Florida after the policy change, and mortality also appears to display a different trend, but we are less confident, due to the larger error bands.

Next, displayed are opioid mortality trends in Texas and Washington, again, before and after policy changes.

<p float="left">
<img src="../30_results/prepost_Texas_mortality.png" width="330" height="180" />
<img src="../30_results/prepost_Washington_mortality.png" width="330" height="180" />
</p>

Visibly, the results here are not as clear. In Texas, there is a step increasing trend in mortality before the policy change (2007), and a much flatter trend subsequently. While the evidence is not clear enough to say there is a reversal in the trend, the increase is at least dampened. In Washington, on the other hand, there is visibly very limited evidence that the trend in opioid mortality was altered at all after the policy change. While the confidence band is wide, the trend itself is nearly identical.

### Difference-in-Difference Analysis

While the trends above are an important part of the story, the pre-post analysis does not take into account any other confounders that could be happening at a national level, also influencing either opioid shipments or mortality. To account for any potential greater trends that could muddy the interpretation of our results, we also conducted a difference-in-difference analysis (methodology for selecting control states discused in the XX section). As previously, there are the same four graphs, but in this case, the graphs also include the selected control counties before and after the policy change. Below are graphs for Florida, for both mortality and shipment data. The pre-post lines representing Florida are exactly the same as above, but these graphs also contain the selected control counties. Interestingly, the control counties demonstrate that the increasing trend in opioid mortality exhibited before the policy change actually steepens afterwards. This directly supports the previous conclusion from the pre-post analysis, and even strengthens it. For Florida's opioid shipment data, the opposite is true. The control states show that the trend in shipments actually is decreasing outside of Florida, but the reversal of the trend in Florida is still much stronger than that exhibited in the control states.

<p float="left">
<img src="../30_results/Florida_mortality.png" width="330" height="180" />
<img src="../30_results/Florida_shipment.png" width="330" height="180" />
</p>

Similarly, below are the graphs for mortality in Texas and Washington. For Texas, the change in the increasing trend previous to the policy change is much more visible when compared with the control. However, in Washington's graph, interestingly, we see an excelleration in the increases of opioid mortality in the control states. Contrary to our initial pre-post analysis, this suggests that while the trend before and after the policy change in Washington is similar, there actual may be a treatment effect due to overall increases in similar states to Washington. However, this interpretation is similarly limited by the width of the confidence bands, which suggest the data may have a wide spread, and we are not very confident about the direction of the trend.

<p float="left">
<img src="../30_results/Texas_mortality.png" width="330" height="180" />
<img src="../30_results/Washington_mortality.png" width="330" height="180" />
</p>

## Conclusion