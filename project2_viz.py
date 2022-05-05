import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import pickle
sns.set()

imdb = pd.read_csv('./imdb.csv')
people = pd.read_csv('./people.csv.gz')

st.title('Visualisations et indicateurs')
st.write('Le résultat de nos analyses sur l\'industrie du film')

fig1,ax1 = plt.subplots()
ax1 = imdb.groupby(imdb.startYear)['numVotes'].mean().plot()
plt.title('Evolution du nombre de votes par film dans le temps')
plt.xlabel('Date')
plt.ylabel('Votes')
st.pyplot(fig1)

fig2,ax2 = plt.subplots()
ax2 = sns.lineplot(data=imdb,x='runtimeMinutes',y='averageRating')
plt.title('Notes en fonction de la durée des films')
plt.xlabel('Durée (minutes)')
plt.ylabel('Note moyenne')
st.pyplot(fig2)

fig3,ax3 = plt.subplots()
ax3 = sns.lineplot(data=imdb,x='startYear',y='runtimeMinutes')
plt.title('Evolution de la durée des films au fil des années')
plt.xlabel('Date')
plt.ylabel('Durée (minutes)')
st.pyplot(fig3)

fig4,ax4 = plt.subplots()
ax4 = sns.lineplot(data=imdb,x='startYear',y='averageRating')
plt.title('Evolution de la Moyenne des notes dans le temps')
plt.xlabel('Date')
plt.ylabel('Note moyenne')
st.pyplot(fig4)

plus_notes = imdb.numVotes.sort_values(ascending=False).head(10)
titres = np.array([imdb.title.iloc[plus_notes.index[i]] for i in range(10)])
votes = np.array([imdb.numVotes.iloc[plus_notes.index[i]] for i in range(10)])
plus_notes = pd.DataFrame([{titres[x]:str(votes[x]) for x in range(10)}]).T 
st.write(plus_notes.rename(columns={0:'Nombre de votes'}))

mieux_notes = imdb.averageRating.sort_values(ascending=False).head(10)
titres_notes = np.array([imdb.title.iloc[mieux_notes.index[i]] for i in range(10)])
notes = np.array([imdb.averageRating.iloc[mieux_notes.index[i]] for i in range(10)])
mieux_notes = pd.DataFrame([{titres_notes[x]:str(notes[x])[0:3] for x in range(10)}]).T 
st.write(mieux_notes.rename(columns={0:'Note moyenne'}))
