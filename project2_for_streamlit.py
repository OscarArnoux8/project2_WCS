import pandas as pd
import numpy as np
from IPython.display import display
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors import kneighbors_graph
from IPython.display import Image, HTML
import streamlit as st

st.set_page_config(layout="wide")
st.write('''
Vous avez aimé un film ?
Nous trouverons votre bonheur
''')

st.title('Recommandation de films')

imdb = pd.read_csv('imdb.csv')
tmdb = pd.read_csv('movies_additional_data.csv') # Additional dataset for pictures etc

X = imdb[['isAdult', 'startYear', 'runtimeMinutes',
       'averageRating', 'numVotes', 'Action', 'Adventure',
       'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama',
       'Family', 'Fantasy', 'History', 'Horror', 'Music', 'Musical', 'Mystery',
       'News', 'Romance', 'Sci-Fi', 'Sport', 'Thriller', 'War', 'Western']]

scale = StandardScaler().fit(X) 
X_scaled = scale.transform(X)

x_scaled = pd.DataFrame(X_scaled, columns=X.columns)

x_scaled.numVotes = x_scaled.numVotes * 0.8
x_scaled.startYear = x_scaled.startYear * 1.5
x_scaled.iloc[:,5:] = x_scaled.iloc[:,5:] * 1.5
x_scaled.averageRating = x_scaled.averageRating * 1.5

distanceKNN = NearestNeighbors(n_neighbors=6).fit(X_scaled)

try:
    predict = distanceKNN.kneighbors(X_scaled[imdb.title.str.lower() == input().lower()]) #Mettre le input en regex
    stop = 0
except ValueError:
    st.write("Le film n'est pas dans la séléction.")
    stop = 1

newFilm = pd.DataFrame(columns = imdb.columns) 
for i in range(6):
    if stop == 1: break
    newFilm = newFilm.append(imdb.iloc[predict[1][0][i],:])
    if i !=0 : st.write(np.array(newFilm.title)[i]) # Affiche que le nom des films
#newFilm[1:] #Debug
'''
image = pd.merge(newFilm,tmdb,how='left',on='tconst')

fig = plt.figure(figsize=(16, 10))
rows = 2
columns = 3
compteur = 1
for number in range(6):
    try:
        Image = urllib.request.urlopen(image.poster_url[number]) # Getting our picture from url
        fig.add_subplot(rows, columns, compteur) # Preparing subplots for better display
        arr = np.asarray(bytearray(Image.read()), dtype=np.uint8) # Creating an array of the picture
        img = cv2.imdecode(arr, -1) # Converting the array in image
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        plt.imshow(img) # Displaying
        cv2.waitKey(0) # Time before displaying
        plt.title(image.title[number]) # Assigning titles
        plt.axis('off') # Removing borders between sub-arrays
        compteur += 1
    except:
        print('Pas d\'affiche disponible pour',image.title[number]) # Handling error if the picture is not in the database
'''
