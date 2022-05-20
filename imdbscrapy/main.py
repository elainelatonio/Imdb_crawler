import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# define the font size for plot text
SMALL_SIZE = 8
MEDIUM_SIZE = 10
BIG_SIZE = 12

plt.rc('font', size=SMALL_SIZE)
plt.rc('axes', titlesize=SMALL_SIZE)
plt.rc('axes', labelsize=SMALL_SIZE)
plt.rc('xtick', labelsize=SMALL_SIZE)
plt.rc('ytick', labelsize=SMALL_SIZE)
plt.rc('legend', fontsize=SMALL_SIZE)
plt.rc('figure', titlesize=BIG_SIZE)

# import crawled IMDB Top250 data as dataframe
data = pd.read_csv('IMDBTop250_v2.csv').set_index('rank')

# clean up data to fill blanks in awards with 0
data['awards_wins'] = data['awards_wins'].fillna(0)
data['awards_nominations'] = data['awards_nominations'].fillna(0)

# checking the data
print(data.info())          # should have 250 items
print(data.isnull().sum())  # check for columns with null values
print(data.describe())


# Analyzing correlation of rating vs quantifiable factors
# Create a figure for subplots
fig1, axs = plt.subplots(2, 2, figsize=(9,7))
fig1.suptitle('Correlations with IMDB Rating')

# correlation of rating and number of votes
print(data['rating'].corr(data['votes']))
axs[0,0].scatter(x='votes', y='rating', data=data, color="blue")
axs[0,0].set_ylabel("Rating")
axs[0,0].set_xlabel("Number of votes")

# correlation of rating and runtime
print(data['rating'].corr(data['runtime_mins']))
axs[0,1].scatter(x='runtime_mins', y='rating', data=data, color="green")
axs[0,1].set_ylabel("Rating")
axs[0,1].set_xlabel("Runtime (mins)")

# correlation of rating and wins
print(data['rating'].corr(data['awards_wins']))
axs[1,0].scatter(x='awards_wins', y='rating', data=data, color="red")
axs[1,0].set_ylabel("Rating")
axs[1,0].set_xlabel("No. of awards won")

# correlation of rating and gross box office
data.gross_worldwide_usd = pd.to_numeric(data.gross_worldwide_usd.str.replace(',',''))
print(data['rating'].corr(data['gross_worldwide_usd']))
axs[1,1].scatter(x='gross_worldwide_usd', y='rating', data=data, color="orange")
axs[1,1].set_ylabel("Rating")
axs[1,1].set_xlabel("Gross box office (worldwide, USD m)")

# Look at average ratings per genre, release year, country of origin
# Create a figure2 for subplotes

fig2, axs = plt.subplots(1,3, figsize=(15,3))
fig2.suptitle('Average IMDB Ratings per Genre, Year of Release, and Origin')

# average rating per year
avgrate_per_year = data.groupby('year').agg({'rating':[np.mean]})
avgrate_per_year.plot(title='Average IMDB rating per year of release',legend=False, ax=axs[0])

# average rating per genre, multiple-genre movies are considered in each of their genres
genres = (data.genre.str.split(',', expand=True).stack().to_frame(name='genre'))
genres.index = genres.index.droplevel(1)
avg_per_genre = genres.join(data['rating']).groupby('genre').mean()
avg_per_genre.plot(kind='bar', ylim=(data['rating'].min(),avg_per_genre['rating'].max()),
                                                          title='Average IMDB rating per genre', ax=axs[1])

# average rating per country, multiple-origin movies are considered under each of their countries
countries = (data.origin.str.split(',', expand=True).stack().to_frame(name='origin'))
countries.index = countries.index.droplevel(1)
avg_per_origin = countries.join(data['rating']).groupby('origin').mean()
avg_per_origin.plot(kind='bar', ylim=(data['rating'].min(),avg_per_origin['rating'].max()),
                                                         title='Average IMDB rating per country of origin', ax=axs[2])
fig2.tight_layout()

plt.show()

