import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
sns.set()

imdb = pd.read_csv('./imdb.csv')
#people = pd.read_csv('./people.csv.gz')

st.title('Visualisations et indicateurs')
st.write('Le résultat de nos analyses sur l\'industrie du film')

fig1 = imdb.groupby(imdb.startYear)['numVotes'].mean().plot()
plt.title('Evolution de la Moyenne des votes dans le temps')
plt.xlabel('Date')
plt.ylabel('Votes')

st.pyplot(fig1)

fig2 = sns.lineplot(data=imdb,x='runtimeMinutes',y='averageRating')
plt.title('Notes en fonction de la durée des films')
plt.xlabel('Durée (minutes)')
plt.ylabel('Note moyenne')

st.pyplot(fig2)
