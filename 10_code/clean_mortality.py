# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd


# %%
df_list=[]
for y in range(2003,2016):
    df_tmp=pd.read_csv('../00_source/'+str(y)+'.csv')
    df_list.append(df_tmp)


# %%
df_all = pd.concat(df_list)
df_all= df_all[df_all['Drug/Alcohol Induced Cause Code'].str[0].isin(['D'])]
df=df_all[df_all['Deaths'] !='Missing']
df=df[['State','County','Year','Deaths']]
df=df[df["State"].str.contains("AK")==False]


# %%
df=df.groupby(['State','County','Year']).sum()
df=df.reset_index()


# %%
df.to_parquet("../20_intermediate_files/df_clean_mortality.parquet", engine="fastparquet")

# %% [markdown]
# ### Check the data

# %%
df['Deaths']=df['Deaths'].astype(float).astype(int)


# %%
df['Deaths'].max()


# %%
import altair as alt


# %%
fig=alt.Chart(df).mark_point(size=5).encode(x=alt.X("Year", scale=alt.Scale(zero=False)),
y=alt.Y('Deaths'))
alt.data_transformers.enable('data_server')
fig.display()
#It can be seen from the graph that there are no extreme data


# %%
test=df.groupby(['State','County','Year']).count()
(test['Deaths']>1).any()
#to make sure there is only one value of death per state-county for each year.


# %%
df['Year']=df['Year'].astype(int)
(df['Year']>2015).any()
(df['Year']<2003).any()
# make sure all the years are between 2003-2015


