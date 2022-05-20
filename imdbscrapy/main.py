import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

data = pd.read_csv('IMDBTop250_v2.csv')

#print(data.head(10))
#print(data.shape)
#print(data.isnull().sum())
#print(data.describe())

#top10_len=data.nlargest(10,'rating')[['title','rating']].set_index('title')
#print(top10_len)
#sns.barplot(x='rating',y=top10_len.index,data=top10_len)
#plt.show()
#sns.barplot(x="year",y="rating",data=data)
#plt.show()


data.rating = pd.to_numeric(data.rating, errors='coerce')
avgrate_per_year = data.groupby('year').agg({'rating':[np.mean]})

avgrate_per_year.plot(figsize=(6,4), title='Average IMDB rating per year of release')

avgrate_per_year.plot(figsize=(9,5), title='Average IMDB rating per year of release')

plt.show()

