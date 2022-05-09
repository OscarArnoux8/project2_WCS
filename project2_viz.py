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

col1, col2, col3 = st.columns([1,1,1]) # Center our image
with col1:
  st.write("")
with col2:
  st.image('bobine.jpg')
with col3:
  st.write("")

st.markdown("<h1 style='text-align: center;'>JAO analytics : Analyses et recommandations</h1>", unsafe_allow_html=True)
st.write('# Le résultat de nos analyses sur l\'industrie du film')

st.subheader('Les outils utilisés')
st.write("IMDb")
col1, col2, col3, col4, col5, col6, col7 = st.columns([1 for i in range(7)])
with col1:
    st.image('IMDB_Logo_2016.svg.png', width=60)
with col2:
    st.write('A Name')
'''
st.write("Python")
col1, mid, col2 = st.columns([1,1,20])
with col1:
    st.image('', width=60)
with col2:
    st.write('A Name')
   
st.write("Streamlit")
col1, mid, col2 = st.columns([1,1,20])
with col1:
    st.image('row_2_col_1.jpg', width=60)
with col2:
    st.write('A Name')
    
st.write("Scikit-Learn")
col1, mid, col2 = st.columns([1,1,20])
with col1:
    st.image('row_2_col_1.jpg', width=60)
with col2:
    st.write('A Name')
    
st.write("Matplotlib")
col1, mid, col2 = st.columns([1,1,20])
with col1:
    st.image('row_2_col_1.jpg', width=60)
with col2:
    st.write('A Name')
    
st.write("Numpy")
col1, mid, col2 = st.columns([1,1,20])
with col1:
    st.image('row_2_col_1.jpg', width=60)
with col2:
    st.write('A Name')

st.write("Pandas")
col1, mid, col2 = st.columns([1,1,20])
with col1:
    st.image('row_2_col_1.jpg', width=60)
with col2:
    st.write('A Name')
'''

st.write('# Notre base de donnée :')
st.write('Nous avons utilisé la base de donnée IMDb, contenant sept tables avec la structure suivante :')

coltab, colpie = st.columns([1,1])

with coltab:
  st.table(pd.DataFrame(np.array([['name','11 531 349'],['title','8 824 341'],['akas','31 569 218'],
                       ['crew','31 569 218'],['episode','6 615 976'],['principals','49 736 924'],
                       ['ratings','1 230 633']]),
                     columns = ['Nom','Lignes']))
with colpie:
  st.markdown("<h2 style='text-align: center;'>Pourcentage de films extraits de la base</h2>", unsafe_allow_html=True)
  fig, ax = plt.subplots(figsize=(3,3))
  ax = plt.pie(x=[605284-22560,22560],labels=['96,3%','3,7%'],explode=[0,0.1])
  st.pyplot(fig)
  
st.write(''' En réalité, la base de donnée contient 605 284 films.
   Nous avons réduit la base de donnée à 22560 films, soit 3,7% du total.
   Les filtres sont les suivants :
   Seuls des films vous seront proposés, tout public, avec plus de 1000 votes et une note supérieure à 4/10 sur le site IMDb.
   Nous avons décidé de n'inclure que les films qui ont été diffusé en France.
   L'algorithme est limité aux films entre 80 et 210 minutes. 
   Nous pensons que ce format est plus adapté à votre cinéma.
   ''')
         
row1_space1, row_1_1, row1_space2, row_1_2 = st.columns((.1, 1, .1, 1))

with row_1_1, _lock:
  st.subheader('Evolution du nombre de votes par film dans le temps')
  fig1,ax1 = plt.subplots() # First graph : lineplot, movies by year (maybe try with sns/px ?)
  ax1 = imdb.groupby(imdb.startYear)['numVotes'].mean().plot()
  plt.xlabel('Date')
  plt.ylabel('Votes')
  st.pyplot(fig1)

with row_1_2, _lock:
  st.subheader('Sorties par décennie')
  fig2,ax2 = plt.subplots() # Seventh graph, amount of movies by decade
  ax2 = imdb.groupby((imdb['startYear']//10)*10)['tconst'].count().plot(kind='barh')
  plt.ylabel('Décennie')
  plt.xlabel('Nombre de films')
  st.pyplot(fig2)
  
row2_space1, row_2_1, row2_space2, row_2_2,row2_space3, row_2_3 = st.columns((.1, 1, .1, 1, .1, 1))

with row_2_1, _lock:
  st.subheader('Evolution de la durée des films au fil des années')
  fig3,ax3 = plt.subplots() # Third graph, variation of the length of movies overtime (decades as x)
  ax3 = sns.lineplot(data=imdb,x='startYear',y='runtimeMinutes')
  plt.xlabel('Date')
  plt.ylabel('Durée (minutes)')
  st.pyplot(fig3)

with row_2_2, _lock:
  st.subheader('Notes en fonction de la durée des films')
  fig4,ax4 = plt.subplots() # Second graph, averageRating by length of movies
  ax4 = sns.lineplot(data=imdb,x='runtimeMinutes',y='averageRating')
  plt.xlabel('Durée (minutes)')
  plt.ylabel('Note moyenne')
  st.pyplot(fig4)

with row_2_3, _lock:
  st.subheader('Evolution de la Moyenne des notes dans le temps')
  fig5,ax5 = plt.subplots() # Fourth graph, average rating overtime
  ax5 = sns.lineplot(data=imdb,x='startYear',y='averageRating')
  plt.xlabel('Date')
  plt.ylabel('Note moyenne')
  st.pyplot(fig5)

row3_space1, row_3_1, row3_space2, row_3_2 = st.columns((.1, 1, .1, 1))

with row_3_1, _lock:
  st.subheader('Les dix films avec le plus de votes')
  plus_notes = imdb.numVotes.sort_values(ascending=False).head(10) # Our top 10 movies by number of votes, as a table
  titres = np.array([imdb.title.iloc[plus_notes.index[i]] for i in range(10)])
  votes = np.array([imdb.numVotes.iloc[plus_notes.index[i]] for i in range(10)])
  plus_notes = pd.DataFrame([{titres[x]:str(votes[x]) for x in range(10)}]).T 
  st.table(plus_notes.rename(columns={0:'Nombre de votes'}))

with row_3_2, _lock:
  st.subheader('Les dix films avec la meilleure note moyenne')
  mieux_notes = imdb.averageRating.sort_values(ascending=False).head(10) # Our top 10 movies by average rating, as a table
  titres_notes = np.array([imdb.title.iloc[mieux_notes.index[i]] for i in range(10)])
  notes = np.array([imdb.averageRating.iloc[mieux_notes.index[i]] for i in range(10)])
  mieux_notes = pd.DataFrame([{titres_notes[x]:str(notes[x])[0:3] for x in range(10)}]).T 
  st.table(mieux_notes.rename(columns={0:'Note moyenne'}))

row4_space1, row_4_1, row4_space2, row_4_2 = st.columns((.1, 1, .1, 1))

with row_4_1, _lock:
  st.subheader('Nombre de films par genre')
  fig5,ax5 = plt.subplots() # Fifth graph, amount of movies for each genre
  ax5= people.genres.str.get_dummies(',').sum().sort_values(ascending=True).tail(15).plot(kind='barh')
  plt.ylabel('Genre')
  plt.xlabel('Nombre de films')
  st.pyplot(fig5)

# Add graph with multiple genres

'''
# This is the fifth row, maybe add a graph with evolution of gender repartition ?
fig6,ax6 = plt.subplots() # Sixth graph, repartition by sex : percentage of actresses and actors
ax6 = round(people.category.value_counts(normalize=True)*100,1).plot(kind='bar')
plt.ylabel('Pourcentage')
plt.xticks(ticks = [0,1],labels=['acteurs','actrices'])
ax6.bar_label(ax6.containers[0], label_type='edge')
plt.title('Répartition par sexe')
st.pyplot(fig6)
'''

row6_space1, row_6_1, row6_space2, row_6_2 = st.columns((.1, 1, .1, 1))

with row_6_1, _lock:
  st.subheader('Top 5 des actrices, par nombre de films')
  top_actresses = pd.DataFrame(people.query('category=="actress"').primaryName.value_counts().head()) # Table of the 5 most prolific actresses
  st.dataframe(top_actresses.rename(columns={'primaryName':'Actrices'}))
  
with row_6_2, _lock:
  st.subheader('Top 5 des acteurs, par nombre de films')
  top_actors = pd.DataFrame(people.query('category=="actor"').primaryName.value_counts().head()) # Table of the 5 most prolific actors
  st.dataframe(top_actors.rename(columns={'primaryName':'Acteurs'}))

st.write(f'''
    <a target="_self" href="https://share.streamlit.io/pilouliz/movie_reco/main/app.py">
        <button>
            Nos recommandations
        </button>
    </a>
    ''',
    unsafe_allow_html=True
        )

   
