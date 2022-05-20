import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logging

logging.getLogger('matplotlib').setLevel(logging.WARNING)

class ImdbAnalysis:
    # define the font size for plot text
    plt.rc('font', size=8)
    plt.rc('axes', titlesize=7)
    plt.rc('axes', labelsize=8)
    plt.rc('xtick', labelsize=7)
    plt.rc('ytick', labelsize=7)
    plt.rc('legend', fontsize=8)
    plt.rc('figure', titlesize=10)

    def __init__(self):
        self.data = pd.read_csv('IMDBTop250.csv').set_index('rank')
        self.data['awards_wins'] = self.data['awards_wins'].fillna(0)
        self.data['awards_nominations'] = self.data['awards_nominations'].fillna(0)

    def check_data(self):
        print(self.data.info())  # should have 250 items
        print(self.data.isnull().sum())  # check for columns with null values
        print(self.data.describe())

    def get_correlations(self):
        print(self.data['rating'].corr(self.data['votes']))
        print(self.data['rating'].corr(self.data['runtime_mins']))
        print(self.data['rating'].corr(self.data['awards_wins']))
        print(self.data['rating'].corr(self.data['gross_worldwide_usd']))

    def show_graphs(self):
        self.fig1, axs = plt.subplots(2, 2, figsize=(7.6, 7))
        self.fig1.suptitle('Correlations with IMDB Rating')

        # correlation of rating and votes
        axs[0, 0].scatter(x='votes', y='rating', data=self.data, color="blue")
        axs[0, 0].set_ylabel("Rating")
        axs[0, 0].set_xlabel("Number of votes (mn)")

        # correlation of rating and runtime
        axs[0, 1].scatter(x='runtime_mins', y='rating', data=self.data, color="green")
        axs[0, 1].set_ylabel("Rating")
        axs[0, 1].set_xlabel("Runtime (mins)")

        # correlation of rating and wins
        axs[1, 0].scatter(x='awards_wins', y='rating', data=self.data, color="red")
        axs[1, 0].set_ylabel("Rating")
        axs[1, 0].set_xlabel("No. of awards won")

        # correlation of rating and gross box office
        self.data.gross_worldwide_usd = pd.to_numeric(self.data.gross_worldwide_usd.str.replace(',', ''))
        axs[1, 1].scatter(x='gross_worldwide_usd', y='rating', data=self.data, color="orange")
        axs[1, 1].set_ylabel("Rating")
        axs[1, 1].set_xlabel("Gross box office (worldwide, USD bn)")

        # Look at average ratings per genre, release year, country of origin
        # Create a figure2 for subplotes

        self.fig2, axs = plt.subplots(1, 3, figsize=(15, 3))
        self.fig2.suptitle('Average IMDB Ratings per Genre, Year of Release, and Origin')

        # average rating per year
        avgrate_per_year = self.data.groupby('year').agg({'rating': [np.mean]})
        avgrate_per_year.plot(title='Average IMDB rating per year of release', legend=False, ax=axs[0])

        # average rating per genre, multiple-genre movies are considered in each of their genres
        genres = (self.data.genre.str.split(',', expand=True).stack().to_frame(name='genre'))
        genres.index = genres.index.droplevel(1)
        avg_per_genre = genres.join(self.data['rating']).groupby('genre').mean()
        avg_per_genre.plot(kind='bar', ylim=(self.data['rating'].min(), avg_per_genre['rating'].max()),
                           title='Average IMDB rating per genre', ax=axs[1])

        # average rating per country, multiple-origin movies are considered under each of their countries
        countries = (self.data.origin.str.split(',', expand=True).stack().to_frame(name='origin'))
        countries.index = countries.index.droplevel(1)
        avg_per_origin = countries.join(self.data['rating']).groupby('origin').mean()
        avg_per_origin.plot(kind='bar', ylim=(self.data['rating'].min(), avg_per_origin['rating'].max()),
                            title='Average IMDB rating per country of origin', ax=axs[2])
        self.fig2.tight_layout()

        plt.show()
