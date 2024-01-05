#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Supress Warnings

import warnings
warnings.filterwarnings('ignore')


# In[2]:


# Import the numpy and pandas packages

import numpy as np
import pandas as pd


# * Imported and read the movie database. Store it in a variable called `movies`

# In[3]:


movies = pd.read_csv('movie_data.csv')
movies


# * Inspect the dataframe's columns, shapes & variable types 

# In[4]:


movies.shape


# In[5]:


type(movies)


# In[6]:


movies.info()


# * Statistical summary of the dataframe 

# In[7]:


movies.describe()


# #### insights from the statistics

# In[8]:


#average duration
avg_duration= movies['duration'].mean().round(2)
avg_duration


# In[9]:


movies.head()


# In[10]:


# details of  movie , which has the highest imdb score

highest_imdb_score = movies[movies['imdb_score']==max(movies['imdb_score'])]
highest_imdb_score


# #### Cleaning the Data

# In[11]:


# The total number of null values in each column of the dataset
movies.isnull().sum()


# In[12]:


#The percentage of null values in each column, rounded up to two decimal places
round(movies.isnull().sum()*100/len(movies),2)


# In[ ]:





# #### Dropping the unnecessary columns

# In[13]:


movies = movies.drop(['color', 
                     'director_facebook_likes', 
                     'actor_3_facebook_likes', 
                     'actor_1_facebook_likes', 
                     'cast_total_facebook_likes', 
                     'actor_2_facebook_likes', 
                     'duration', 
                     'facenumber_in_poster', 
                     'content_rating', 
                     'country', 
                     'movie_imdb_link', 
                     'aspect_ratio',
                     'plot_keywords',
                     'actor_2_name',
                     'actor_3_name'], 
                      axis = 1)
movies


# In[14]:


#checking for the duplicates and  droping all the duplicate rows except the first instance
movies.drop_duplicates(subset=None , keep='first',inplace = True)


# In[15]:


movies.duplicated().sum()


# In[16]:


#The first line will discard all the rows with null values in the column gross and 
#keep only the rows with non-null values in the original dataset
movies=movies[~np.isnan(movies['gross'])]
movies=movies[~np.isnan(movies['budget'])]
movies
#The second line will discard all the rows with null values in the column budget and 
#keep only the rows with non-null values in the original dataset


# In[ ]:





# #### keeping the column which has less than 5 null values

# In[17]:


#This code will calculate the total null values in each columns
#Then it will only keep the columns in which the total null values are less than 5
#Basically the code is discarding all the columns which have more than 5 null values
movies = movies[movies.isnull().sum(axis=1) <= 5]
movies


# In[18]:


#Replacing null value in all the rows in the column language , with the value English

movies['language'].describe()
movies.loc[pd.isnull(movies['language']), ['language']] = 'English'
movies


#  #####  Converting  units of gross and budget to millions for all movies in the dataset.

# In[19]:


# Write your code here
movies['gross'] = movies['gross']/1000000
movies['budget'] = movies['budget']/1000000
movies


#   ####  10 movies with the highest profit.

# In[20]:


#creating a new column for profit
movies['profit'] = movies['gross'] - movies['budget']

#sorting the dataset by profit in descending order
top_movies_profit = movies.sort_values(by='profit',ascending = False)

#getting the top 10 movies with highest profit
top_movies_profit = top_movies_profit.iloc[:10]


# In[21]:


top_movies_profit


#   #####   top 10 movies (based on IMDb ratings) with a minimum of 25,000 ratings 

# In[22]:


#1. Filter the movies with number of ratings >= 25000
#2. Sort the filtered movies by imdb score in descending order
#3. Get the top 10 movies from the top 10 rows of the sorted movies


# In[23]:


#Step 1
top_movies_rating = movies[movies['num_voted_users'] >= 25000]
#Step 2
top_movies_rating=top_movies_rating.sort_values(by='imdb_score',ascending=False)
#Step 3
top_movies_rating[['movie_title']].head(10)


#  ##### Names of  the top 5 directors based on IMDb ratings with a minimum of 5 movies 

# In[24]:


#1. Getting the average IMDb score of all directors
#2. Get the count of movies for each director
#3. From this, filter the directors who have directed at least 5 movies
#4. From these filtered directors, get the top 5 directors based on IMDb rating


# In[25]:


#Step 1
top_movie_director =pd.DataFrame(movies.groupby('director_name')['imdb_score'].mean())
#Step 2
top_movie_director['Movies_count'] = movies['director_name'].value_counts().sort_index()
#Step 3
top_movie_director = top_movie_director[top_movie_director['Movies_count'] >=5]
#Step 4
top_movie_director = top_movie_director.sort_values(by='imdb_score',ascending=False)
#Final playlist
top_movie_director.head(5)


#  ##### The most popular genre of movies by highest average rating

# In[26]:


#1. Preprocessing - Getting the primary genre of each movie

#2. Get average rating of the movies by imdb_score

#3. Get the most popular genre with the highest average rating (imdb_score)


# In[27]:


#Step1 : Preprocessing
movies['genres'] = movies['genres']
movies['genres'] = movies['genres'].str.split('|')
movies['primary_genres'] = movies['genres'].apply(lambda x: x[0])
movies['primary_genres']


# In[65]:


top_genres_movies = pd.DataFrame(movies.groupby('primary_genres')['imdb_score'].mean())


# In[67]:


top_genres_movies=top_genres_movies.sort_values(by='imdb_score',ascending=False)


# In[68]:


top_genres_movies=top_genres_movies.iloc[:1]


# In[69]:


top_genres_movies


#   #####  the most popular genre of movies (by total gross) 

# In[70]:


popular_genres_according_to_gross = pd.DataFrame(movies.groupby('primary_genres')['gross'].sum().sort_values(ascending=False))


# In[34]:


popular_genres_according_to_gross.head(1)

