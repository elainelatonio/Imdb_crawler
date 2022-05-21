import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logging


class ImdbAnalysis:
    # define the font size for plot text
    plt.rc('font', size=8)
    plt.rc('axes', titlesize=8)
    plt.rc('axes', labelsize=7)
    plt.rc('xtick', labelsize=7)
    plt.rc('ytick', labelsize=7)
    plt.rc('legend', fontsize=8)
    plt.rc('figure', titlesize=10)

    def __init__(self, filename):
        # initialize analysis by getting file output of the spider, create a pandas dataframe
        self.data = pd.read_csv(filename).set_index('rank')
        # set logging level for imported module and create custom logger to view data and analysis info
        logging.getLogger('matplotlib').setLevel(logging.WARNING)
        self.logger = logging.getLogger('analysis')
        logging.getLogger('analysis').setLevel(logging.INFO)
        # clean and check data
        self.clean_data()
        self.check_data()

    # clean the data and convert to number format to allow calculations
    def clean_data(self):
        self.data['awards_wins'] = self.data['awards_wins'].fillna(0)
        self.data['awards_nominations'] = self.data['awards_nominations'].fillna(0)
        self.data.gross_worldwide_usd = pd.to_numeric(self.data.gross_worldwide_usd.str.replace(',', ''))

    def check_data(self):
        self.data.info()  # show column names, count of non-null and data type
        self.logger.warning(self.data.isnull().sum())  # check if any field has null values after cleaning the data

    # show as graphical representation the correlations and average ratings
    def show_graphs(self):
        # Look at scatter plot of rating versus quantifiable factors
        # Create a figure for subplots
        self.fig1, axs = plt.subplots(2, 2, figsize=(7.6, 7))
        self.fig1.suptitle('Correlations with IMDB Rating')

        # correlation of rating and votes
        self.logger.info('Rating vs votes: %f ', self.data['rating'].corr(self.data['votes']))
        axs[0, 0].scatter(x='votes', y='rating', data=self.data, color="blue")
        axs[0, 0].set_ylabel("Rating")
        axs[0, 0].set_xlabel("Number of votes (mn)")
        axs[0, 0].set_title("Rating vs Votes")

        # correlation of rating and runtime
        self.logger.info('Rating vs Runtime: %f ', self.data['rating'].corr(self.data['runtime_mins']))
        axs[0, 1].scatter(x='runtime_mins', y='rating', data=self.data, color="green")
        axs[0, 1].set_ylabel("Rating")
        axs[0, 1].set_xlabel("Runtime (mins)")
        axs[0, 1].set_title("Rating vs Runtime")

        # correlation of rating and wins
        self.logger.info('Rating vs Awards: %f ', self.data['rating'].corr(self.data['awards_wins']))
        axs[1, 0].scatter(x='awards_wins', y='rating', data=self.data, color="red")
        axs[1, 0].set_ylabel("Rating")
        axs[1, 0].set_xlabel("No. of awards won")
        axs[1, 0].set_title("Rating vs Awards")

        # correlation of rating and gross box office
        last_10y = self.data[self.data['year'] > 2011]
        self.logger.info('Rating vs Gross Worldwide: %f ', last_10y['rating'].corr(last_10y['gross_worldwide_usd']))
        axs[1, 1].scatter(x='gross_worldwide_usd', y='rating', data=last_10y, color="orange")
        axs[1, 1].set_ylabel("Rating")
        axs[1, 1].set_title("Rating vs Gross Worldwide (for movies in last 10 years)")
        axs[1, 1].set_xlabel("Gross box office (worldwide, USD bn)")

        self.fig1.tight_layout()

        # Look at average ratings per genre, release year, country of origin
        # Create a figure2 for subplots
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


if __name__ == "__main__":
    top250 = ImdbAnalysis('IMDBTop250.csv')
    top250.show_graphs()
