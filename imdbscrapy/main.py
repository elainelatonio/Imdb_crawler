import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

data = pd.read_csv('IMDBTop250.csv')

#print(data.head(10))
#print(data.shape)
#print(data.isnull().sum())
#print(data.describe())

top10_len=data.nlargest(10,'rating')[['title','rating']].set_index('title')
print(top10_len)
sns.barplot(x='rating',y=top10_len.index,data=top10_len)
plt.show()
#sns.barplot(x="year",y="rating",data=data)
#plt.show()