# # To save all my old functions in case i need to come back to them
# comp = True
# def getHTML():
#     pass

# def GROSSMONT():
#     if comp:
#             num_scores_per_school = 22
#             schoolScores = [contentScores[i:i+num_scores_per_school] for i in range(0, len(contentScores), num_scores_per_school)]
#             schoolRanks = [contentRanks[i:i+num_scores_per_school] for i in range(0, len(contentRanks), num_scores_per_school)]
#             modifiedSchoolScores = []
#             modifiedSchoolRanks = []

#             for scores in schoolScores:
#                 scores.insert(21, 0)
#                 modifiedSchoolScores.append(scores)

#             for ranks in schoolRanks:
#                 ranks.insert(21, '')
#                 modifiedSchoolRanks.append(ranks)

#             return modifiedSchoolScores, modifiedSchoolRanks, headers, locations, comp, month, day, szn, locationsAreListed
















# def findDivision(school_name):

#     soup = getHTML("https://csbc.compsuite.io/groups")
#     link = None
#     for a_tag in soup.find_all('a'):
#         if school_name.lower() in a_tag.text.lower():
#             link = a_tag['href']
#             break
#     if link is not None:
#         base_url = "https://csbc.compsuite.io"
#         full_url = base_url + link
#         soup = getHTML(full_url)
#         # Find the <div> tag containing "Division xA" text
#         division_tag = None
#         for div_tag in soup.find_all('div'):
#             if 'Division' in div_tag.text and div_tag.text.endswith('A'):
#                 division_tag = div_tag
#                 break

#         if division_tag is not None:
#             info = division_tag.text.strip()
#             return info.split(' ')[1]

#     # If the school or division info is not found, return None or handle the error accordingly
#     return None      

# def parseScoresAndRanksForSchool(schoolName, df):
#     # if season:
#     #     filtered_df = df[(df['school'] == schoolName) & (df['season'] == season)]
#     # else:
#     filtered_df = df[df['school']== schoolName]
#     scoresList = filtered_df['scores'].tolist()
#     scoresList = [parseScoresAndRanks(score_str) for score_str in scoresList]
#     scoresArray = np.array(scoresList, dtype=float)
#     ranksList = filtered_df['ranks'].tolist()
#     ranksList = [parseScoresAndRanks(ranks_str) for ranks_str in ranksList]
#     ranksArray = np.array(ranksList, dtype=float)
#     return scoresArray, ranksArray

# def getAvgScoresAndRanksPerSchool(schoolName, df):
#     mean_scores = np.mean(parseScoresAndRanksForSchool(schoolName, df)[0], axis=0)
#     mean_ranks = np.mean(parseScoresAndRanksForSchool(schoolName, df)[1], axis=0)

#     return mean_scores, mean_ranks

# def getAvgScoresAndRanksForDivision(division, df):
#     filtered_df = df[df['division'] == division]
#     scoresList = filtered_df['scores'].tolist()
#     scoresList = [score_str.strip("[]").replace("'", "").split() for score_str in scoresList]
#     scoresArray = np.array(scoresList, dtype=float)
#     mean_scores = np.mean(scoresArray, axis=0)

#     ranksList = filtered_df['ranks'].tolist()
#     ranksList = [ranks_str.strip("[]").replace("'", "").split() for ranks_str in ranksList]
#     max_len = max(len(rank) for rank in ranksList)
#     ranksList = [rank + ['0'] * (max_len - len(rank)) for rank in ranksList]
#     ranksArray = np.array(ranksList, dtype=float)
#     mean_ranks = np.mean(ranksArray, axis=0)

#     return mean_scores, mean_ranks


# def dataAnalysis(school, division, df):
#     division_avg_scores = getAvgScoresAndRanksForDivision(division, df)[0]
#     school_avg_scores = getAvgScoresAndRanksPerSchool(school, df)[0]

#     x = np.arange(division_avg_scores.shape[0])
#     width = 0.45  # Width of the bars

#     fig, ax = plt.subplots()
#     division_bars = ax.bar(x - width/2, division_avg_scores, width, color = '#DD517F', label=f'Division {division}')
#     school_bars = ax.bar(x + width/2, school_avg_scores, width, color='#461E52', label= school)

#     ax.set_xlabel('Category')
#     ax.set_ylabel('Average Score')

#     labels = ['MusicPerf Ens', 'MusicPerf Ind', 'MusicPerf SubTotal', 'VisualPerf Ens', 'VisualPerf Ind', 'VisualPerf Subtotal', 'Performance Total', 'GE Music CE', 'GE Music PE', 'GE Music Subtotal', 'GE Visual CE', 'GE Visual PE', 'GE Visual Subtotal', 'GE Total', 'Perc Cont', 'Perc Ach', 'Perc Total', 'Perc ScaledTotal', 'Guard Cont', 'Guard Ach', 'Guard Total', 'Guard ScaledTotal', 'Sub Total', 'Timing/Penalties', 'Total']

#     ax.set_xticks(x)
#     ax.set_xticklabels(labels, rotation=90)
#     ax.legend()

#     # Label the division bars
#     for bar in division_bars:
#         height = bar.get_height()
#         ax.annotate(f'{height:.2f}', xy=(bar.get_x() + bar.get_width() / 2, height), xytext=(0,3),
#                     textcoords="offset points", ha='center', va='bottom',color = '#DD517F', rotation = 90)

#     # Label the school bars
#     for bar in school_bars:
#         height = bar.get_height()
#         ax.annotate(f'{height:.2f}', xy=(bar.get_x() + bar.get_width() / 2, height), xytext=(0,3),
#                     textcoords="offset points", ha='center', va='bottom', color='#461E52', rotation = 90)
#     plt.title('Average Scores Comparison')
#     plt.tight_layout()
#     plt.show()

#     percentile_ranks = [percentileofscore(division_avg_scores, score) for score in school_avg_scores]
#     return percentile_ranks, labels

# def findCompetitors(school, division, df):
#         filtered_df = df[df['school'] == school]
#         competitions = filtered_df['comp'].unique()
#         competitor_df = df[df['comp'].isin(competitions)]
#         allCompetitors = competitor_df['school'].unique()
#         target_scores = np.array(parseScoresAndRanks(filtered_df['scores'].iloc[0]), dtype=float)
#         target_ranks = np.array(parseScoresAndRanks(filtered_df['ranks'].iloc[0]), dtype=float)
#         similarityScores = []
#         for idx, row in competitor_df.iterrows():
#             scores = np.array(parseScoresAndRanks(row['scores']), dtype=float)
#             ranks = np.array(parseScoresAndRanks(row['ranks']), dtype=float)
#             scoreSimilarity = 1 / (1 + np.linalg.norm(target_scores - scores))
#             rankSimilarity = 1 / (1 + np.linalg.norm(target_ranks - ranks))
#             total_similarity = scoreSimilarity + rankSimilarity
#             similarityScores.append((row['school'], total_similarity))
#         similarityScores.sort(key=lambda x: x[1], reverse=True)

#         #weights = [(score[0], score[1] + 0.25) for score in similarityScores if df.loc[df['school'] == score[0], 'division'].values[0] == df.loc[df['school'] == school, 'division'].values[0]]
#         weights = [(score[0], score[1] + 0.25) for score in similarityScores if df.loc[df['school'] == score[0], 'division'].values[0] == division]

#         weights.sort(key=lambda x: x[1], reverse=True)
#         num_competitors = 5
#         closestCompetitors = []
#         added_schools = set()
#         for score in weights:
#             if score[0] not in added_schools:
#                 closestCompetitors.append(score[0])
#                 added_schools.add(score[0])
#                 if len(closestCompetitors) >= num_competitors:
#                     break

#         print(f'The closest competitors of {school} are: {closestCompetitors}')
#         return closestCompetitors


# class printInfo:
#     def __init__(self, school, division, df):
#         self.school = school
#         self.division = division
#         self.df  = df
#         # if season == "All Time":
#         #     self.season = None
#         # else:
#         #     self.season = season

#     def lineGraph(self):
#         competitorsAndTarget = findCompetitors(self.school, self.division, self.df)
#         competitorsAndTarget.append('The Spirit of Great Oak')

#         for targschool in competitorsAndTarget:

#             school_df = self.df[self.df['school'] == targschool].copy()  # Make a copy of the filtered DataFrame


#             school_df['date'] = pd.to_datetime(school_df['month'].astype(str) + ' ' + school_df['dayOfMonth'].astype(str) + ', ' + school_df['season'].astype(str), format='%B %d, %Y')


#             school_df = school_df.sort_values('date')

#             competitions = school_df['comp'].tolist()
#             dates = school_df['date'].tolist()
#             scores = [scores[-1] for scores in school_df['scores'].apply(parseScoresAndRanks).tolist()]

#             # Sort scores and dates together based on dates
#             sorted_indices = np.argsort(dates)
#             sorted_dates = np.array(dates)[sorted_indices]
#             sorted_scores = np.array(scores)[sorted_indices]

#             # Plot the line for the school
#             plt.plot(sorted_dates, sorted_scores.astype(float), marker='o', label=targschool)

#         # Set labels and title
#         plt.xlabel('Date')
#         plt.ylabel('Scores')
#         plt.title('Total Scores Over Time')
#         plt.xticks(rotation=45)

#         # Add legend
#         plt.legend()

#         # Display the graph
#         plt.tight_layout()
#         plt.show()

    
#     def printPercentiles(self):
#         percentile_ranks, labels = dataAnalysis(self.school, self.division, self.df)
#         labelsModified = ['MusicPerf Ens', 'MusicPerf Ind', 'MusicPerf SubTotal', 'VisualPerf Ens', 'VisualPerf Ind', 'VisualPerf Subtotal', 'Performance Total', 'GE Music CE', 'GE Music PE', 'GE Music Subtotal', 'GE Visual CE', 'GE Visual PE', 'GE Visual Subtotal', 'GE Total', 'Perc Cont', 'Perc Ach', 'Perc Total', 'Perc ScaledTotal', 'Guard Cont', 'Guard Ach', 'Guard Total', 'Guard ScaledTotal', 'Sub Total', 'Total']
#         percentile_ranks_modified = [percentile_ranks[labels.index(label)] for label in labelsModified]
    

#         for label, rank in zip(labelsModified, percentile_ranks_modified):
#             if label in ['MusicPerf Ens', 'MusicPerf Ind', 'VisualPerf Ens', 'VisualPerf Ind', 'Performance Total', 'GE Music CE', 'GE Music PE', 'GE Visual CE', 'GE Visual PE', 'Perc Cont', 'Perc Ach', 'Perc Total', 'Guard Cont', 'Guard Ach', 'Guard Total', 'Total']:
#                 print(f'{label}: {rank}th percentile')
#     def printRanks(self):
#         ranks = getAvgScoresAndRanksPerSchool(self.school, self.df)[1]
#         labelsModified = [label for label in labels if label != 'Timing/Penalties']
#         for label in labelsModified:
#             idx = labelsModified.index(label)
#             print(f'{label}: {ranks[idx]}')