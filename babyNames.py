

# load the file


import pandas as pd

import numpy as np

import matplotlib as plt

names1880 = pd.read_csv('/Volumes/Vy\'s/PYTHON/pydata-book-2nd-edition/datasets/babynames/yob1881.txt',names=['name','sex','births'])

names1880.groupby('sex').births.sum()


years = range(1880,2010)


pieces = []

columns = ['name','sex','births']


# combine multiple tables as one

for year in years:
    
    
    path = '/Volumes/Vy\'s/PYTHON/pydata-book-2nd-edition/datasets/babynames/yob' + str(year) +'.txt'
    
    frame = pd.read_csv(path,names=columns)
    
    frame['year'] = year
    
    pieces.append(frame)
    
    # concatenate everything into a single DataFrame
    
    
    names = pd.concat(pieces,ignore_index=True)
    
    
total_births = names.pivot_table('births',index=['year'],columns=['sex'],aggfunc=sum)
    
total_births.tail() #show last 5


total_births.plot(title='Total births by sex and year')  #plot , index on the x-axis 


def add_prop(group):
    #integer division floors
    
    births = group.births.astype(float)
    
    group['prop']= births/births.sum()
    
    return group


names = names.groupby(['year','sex']).apply(add_prop)


def get_top1000(group):
    return group.sort_index(by='births', ascending = False)[:1000]

grouped = names.groupby(['year','sex'])

top1000 = grouped.apply(get_top1000)

boys = top1000[top1000.sex =='M']

girls = top1000[top1000.sex =='F']

total_births = top1000.pivot_table('births',index=['year'],columns ='name',aggfunc=sum)

subset = total_births[['John','Mary','Harry','Marilyn']]

subset.plot(subplots=True,figsize= (12,10),grid=False,title="Number of births per year")

table = top1000.pivot_table('prop',index = ['year'],columns = 'sex',aggfunc=sum)

table.plot(title= 'Sum of table1000.prop by year and sex',yticks=np.linspace(0,1.2,13),xticks=range(1800,2020,10))

df = boys[boys.year == 1900]


prop_cumsum = df.sort_index(by= ['prop'],ascending = False).prop.cumsum()

prop_cumsum.searchsorted(0.5) + 1 #since array is 0 indexed. adding 1 to the result


def get_quantile_count(group, q = 0.5):
    
    group = group.sort_index(by = 'prop', ascending = False)
    
    return group.prop.cumsum().searchsorted(q) + 1

diversity = top1000.groupby(['year','sex']).apply(get_quantile_count)

diversity = diversity.unstack('sex')

diversity.head()

diversity.plot(title = "number of popular names in top 50%")

#extract last letter from names



last_letters = list(map(lambda x: x[-1],names.name)) # create a list

last_letters = names.name.map(lambda x: x[-1]) # create a data frame 


# pitvot table last letters




names = names.assign(last_letters=last_letters.values)

table =  names.pivot_table('births',index=['last_letters'],columns=['sex','year'],aggfunc=sum)

subtable = table.reindex(columns = [1910,1960,2009], level = 'year')


subtable.head()

letter_prop = subtable/subtable.sum().astype(float)

fig, axes = plt.pyplot.subplots(2,1,figsize = (10,8))

letter_prop['M'].plot(kind='bar', rot = 0, ax = axes[0],title = 'Male',legend = True)

letter_prop['F'].plot(kind='bar', rot = 0, ax = axes[0],title = 'Female',legend = True)


letter_prop = table/table.sum().astype(float)


dny_ts = letter_prop.ix[['d','n','y'],'M'].T


dny_ts.head()

dny_ts.plot()

all_names = top1000.name.unique()

mask = np.array(['lesl' in x.lower() for x in all_names])

lesley_like = all_names[mask] #imagine this is a function for now where mask is a independent variable

filtered = top1000[top1000.name.isin(lesley_like)]

filtered.groupby('name').births.sum()

table = filtered.pivot_table('births',index=['year'],columns=['sex'],aggfunc = sum)

table = table.div(table.sum(1),axis = 0)


table.plot(style = {'M':'k-','F':'k--'})
