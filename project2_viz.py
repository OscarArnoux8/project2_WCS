import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import RendererAgg
import matplotlib
from matplotlib.figure import Figure
import plotly.express as px
import seaborn as sns
sns.set_style("whitegrid") # Setting the background grid

imdb = pd.read_csv('./imdb.csv') # Reading csv, replace by pickle if necessary
people = pd.read_csv('./people.csv') # Our table with actors/actresses 
# Keep in mind : tables can change. We should be able to always display our graphs no matter the mergers we apply

matplotlib.use("agg") # This manages backend
_lock = RendererAgg.lock

st.set_page_config(layout="wide")

st.markdown("<h1 style='text-align: center; color: black;'>Visualisatons et indicateurs</h1>", unsafe_allow_html=True)
st.write('# Le résultat de nos analyses sur l\'industrie du film')

st.image('bobine.jpg',width=150)

row1_space1, row_1_1, row1_space2, row_1_2 = st.columns((.1, 1, .1, 1))

with row_1_1, _lock:
  fig1,ax1 = plt.subplots() # First graph : lineplot, movies by year (maybe try with sns/px ?)
  ax1 = imdb.groupby(imdb.startYear)['numVotes'].mean().plot()
  plt.title('Evolution du nombre de votes par film dans le temps')
  plt.xlabel('Date')
  plt.ylabel('Votes')
  st.pyplot(fig1)

with row_1_2, _lock:
  fig2,ax2 = plt.subplots() # Seventh graph, amount of movies by decade
  ax2 = imdb.groupby((imdb['startYear']//10)*10)['tconst'].count().plot(kind='barh')
  plt.ylabel('Décennie')
  plt.xlabel('Nombre de films')
  plt.title('Sorties par décennie')
  st.pyplot(fig2)
  
row2_space1, row_2_1, row2_space2, row_2_2,row2_space3, row_2_3 = st.columns((.1, 1, .1, 1, .1, 1))

with row_2_1, _lock:
  fig3,ax3 = plt.subplots() # Third graph, variation of the length of movies overtime (decades as x)
  ax3 = sns.lineplot(data=imdb,x='startYear',y='runtimeMinutes')
  plt.title('Evolution de la durée des films au fil des années')
  plt.xlabel('Date')
  plt.ylabel('Durée (minutes)')
  st.pyplot(fig3)

with row_2_2, _lock:
  fig4,ax4 = plt.subplots() # Second graph, averageRating by length of movies
  ax4 = sns.lineplot(data=imdb,x='runtimeMinutes',y='averageRating')
  plt.title('Notes en fonction de la durée des films')
  plt.xlabel('Durée (minutes)')
  plt.ylabel('Note moyenne')
  st.pyplot(fig4)

with row_2_3, _lock:
  fig5,ax5 = plt.subplots() # Fourth graph, average rating overtime
  ax5 = sns.lineplot(data=imdb,x='startYear',y='averageRating')
  plt.title('Evolution de la Moyenne des notes dans le temps')
  plt.xlabel('Date')
  plt.ylabel('Note moyenne')
  st.pyplot(fig5)

row3_space1, row_3_1, row3_space2, row_3_2 = st.columns((.1, 1, .1, 1))

with row_3_1, _lock:
  plus_notes = imdb.numVotes.sort_values(ascending=False).head(10) # Our top 10 movies by number of votes, as a table
  titres = np.array([imdb.title.iloc[plus_notes.index[i]] for i in range(10)])
  votes = np.array([imdb.numVotes.iloc[plus_notes.index[i]] for i in range(10)])
  plus_notes = pd.DataFrame([{titres[x]:str(votes[x]) for x in range(10)}]).T 
  st.table(plus_notes.rename(columns={0:'Nombre de votes'}))

with row_3_2, _lock:
  mieux_notes = imdb.averageRating.sort_values(ascending=False).head(10) # Our top 10 movies by average rating, as a table
  titres_notes = np.array([imdb.title.iloc[mieux_notes.index[i]] for i in range(10)])
  notes = np.array([imdb.averageRating.iloc[mieux_notes.index[i]] for i in range(10)])
  mieux_notes = pd.DataFrame([{titres_notes[x]:str(notes[x])[0:3] for x in range(10)}]).T 
  st.table(mieux_notes.rename(columns={0:'Note moyenne'}))

row4_space1, row_4_1, row4_space2, row_4_2 = st.columns((.1, 1, .1, 1))

with row_4_1, _lock:
  fig5,ax5 = plt.subplots() # Fifth graph, amount of movies for each genre
  ax5= people.genres.str.get_dummies(',').sum().sort_values(ascending=True).tail(15).plot(kind='barh')
  plt.ylabel('Genre')
  plt.xlabel('Nombre de films')
  plt.title('Films par genre')
  st.pyplot(fig5)

# Add graph with multiple genres

# This is the fifth row, maybe add a graph with evolution of gender repartition ?
fig6,ax6 = plt.subplots() # Sixth graph, repartition by sex : percentage of actresses and actors
ax6 = round(people.category.value_counts(normalize=True)*100,1).plot(kind='bar')
plt.ylabel('Pourcentage')
plt.xticks(ticks = [0,1],labels=['acteurs','actrices'])
ax6.bar_label(ax6.containers[0], label_type='edge')
plt.title('Répartition par sexe')
st.pyplot(fig6)

row6_space1, row_6_1, row6_space2, row_6_2 = st.columns((.1, 1, .1, 1))

with row_6_1, _lock:
  top_actors = pd.DataFrame(people.query('category=="actor"').primaryName.value_counts().head()) # Table of the 5 most prolific actors
  st.dataframe(top_actors.rename(columns={'primaryName':'Acteurs'}))
  
with row_6_2, _lock:
  top_actresses = pd.DataFrame(people.query('category=="actress"').primaryName.value_counts().head()) # Table of the 5 most prolific actresses
  st.dataframe(top_actresses.rename(columns={'primaryName':'Actrices'}))
