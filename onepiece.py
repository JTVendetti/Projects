import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

import warnings
warnings.filterwarnings("ignore")

plt.rcParams['figure.figsize'] = (10, 9)
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.style'] = "oblique"

data = pd.read_csv("../input/one-piece-arcs/OnePieceArcs.csv")

df = pd.DataFrame(data)
df.dtypes
df.head(5)

df['Arc'] = df['Arc'].astype('str')
df.dtypes

max_episode = df['TotalEpisodes'].max()
df[df['TotalEpisodes'] == max_episode]

dfwano = df[df['Arc'].str.match('Wano')]
dfwano

wanoTotalChapters = sum(dfwano['TotalChapters'])
wanoTotalPages = sum(dfwano['TotalPages'])
wanoMangaPercent = "{:.1f}".format(wanoTotalChapters/sum(data['TotalChapters'])*100)+"%"

wanoTotalEpisode = sum(dfwano['TotalEpisodes'])
wanoTotalMinutes = sum(dfwano['TotalMinutes(avg 24)'])
wanoAnimePercent = "{:.1f}".format(wanoTotalEpisode/sum(data['TotalEpisodes'])*100)+"%"

df.lock[len(df.index)] = ['Wano', 909,wanoTotalChapters,wanoTotalPages,wanoMangaPercent,890,wanoTotalEpisode,wanoTotalMinutes,wanoAnimePercent]

dfwanofix = df[df['Arc'] == 'Wano']
dfwanofix

df.drop(dfwano.index, axis=0, inplace=True)
max_episode = df['TotalEpisodes'].max()
df[df['TotalEpisodes'] == max_episode]

