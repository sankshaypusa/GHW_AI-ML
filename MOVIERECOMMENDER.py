

import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns 
import plotly_express as px 
import warnings
import collections
warnings.filterwarnings("ignore")
from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.metrics.pairwise import cosine_similarity

data = pd.read_csv('/Users/sankshay/Downloads/netflix_titles.csv')
data.head ()

net_movie = data.loc[data.type=='Movie',:].reset_index ()
net_movie.title = net_movie.title.str.lower ()
net_movie['index'] = net_movie.index
net_movie.head()

#fliter tv shows data from the data set
tv_shows = data.loc [data['type'] == 'TV Show'].reset_index()
tv_shows.title = tv_shows.title.str.lower()
tv_shows['index']=tv_shows.index
tv_shows

data.duplicated().sum()
tv_shows.duplicated().sum()

#getting index of tv_shows
index=tv_shows.index
number_of_rows_tv=len(index)

#getting index of net_movie

index=net_movie.index
number_of_rows_movies=len(index)

#comparing number of tv shows and movies

color=['y','r']
label='TV Shows','Movies'
sizes=[number_of_rows_tv,number_of_rows_movies]
explode=(0.1,0)
fig1,ax1=plt.subplots()
ax1.pie(sizes,explode=explode,labels=label,colors=color,autopct='%2.2f%%',shadow=True,startangle=120)
ax1.axis('equal')
plt.show()

newdata=net_movie
new=newdata.groupby("listed_in").count ()
category=new.sort_values(by='index',ascending = False).head(10)
net_movie.columns


#selecting features
features = ['director', 'cast', 'country', 'description', 'listed_in']


#so we’ll gonna select a few features and create a column in a data frame that combines all the selected features into one string:
for feature in features:
    net_movie[feature] = net_movie[feature].fillna('')
def combine_features(row):
    return row['director'] +" "+row['cast']+" "+row["country"]+" "+row["description"]+" "+row["listed_in"]
net_movie["combined_features"] = net_movie.apply(combine_features, axis=1)
print ("Combine Feature:", net_movie["combined_features"])

#create count matrix from this new combine column
cv = CountVectorizer()
count_matrix = cv.fit_transform(net_movie ["combined_features"])
cosine_sim = cosine_similarity(count_matrix)
# After getting the similarity between the content we just need to print the

#get index of the movie from the title
def title_from_index(index):
    return net_movie[net_movie.index == index]["title"].values[0]
def title_from_index(df, index):
    return df[df.index == index]["title"].values[0]
def index_from_title(df, title):
    return df[df.title == title]["index"].values[0]

#get the list of similar movies in descending order of similarity score 
def selectmovie(movie_user_likes):
    try:
        movie_user_likes = movie_user_likes.lower()
        movie_index = index_from_title(net_movie, movie_user_likes)
        similar_movies = list(enumerate (cosine_sim [movie_index]))
        sorted_similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)[1:]
        i=0
        print("Top 5 similar movies to " +movie_user_likes+" are: \n")
        for element in sorted_similar_movies:
            print(title_from_index(net_movie, element [0]))
            i=i+1 
            if i>=5:
                break
    except:
        print('Movie not found on Netflix')
#print the title of top 5 similar movies
selectmovie ('automata')