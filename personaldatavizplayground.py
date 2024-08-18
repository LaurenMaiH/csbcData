import sys

sys.dont_write_bytecode = True
import seaborn as sns
import streamlit as st
import matplotlib

matplotlib.use('TkAgg')  # Replace 'TkAgg' with the backend of your choice

# matplotlib.use('agg')  # Use the Qt5Agg backend

import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy import stats

month_rank_mapping = {
        'January': 1,
        'February': 2,
        'March': 3,
        'April': 4,
        'May': 5,
        'June': 6,
        'July': 7,
        'August': 8,
        'September': 9,
        'October': 10,
        'November': 11,
        'December': 12
    }
#change lineGraph to find division champion instead of defaulting to Great Oak

def createViolinPlot(df, ex = "division", why = "TotalScore"):
    yr = str(df.loc[0]["season"])
    sns.violinplot(x = ex, y = why, data = df).set(title = "Distribution of " + why + " in " + yr)
    plt.show()

def compareAvgSchoolScoresToAvgDivisionScores(school, df):
    division = df.loc[df['school'] == school].iloc[0]["division"]

    div_df = df[df['division'] == division]
    division_avg = div_df.drop(['season', 'dayOfMonth'], axis=1).mean(numeric_only=True)
    div_avg_scores = division_avg.iloc[:24]
    div_avg_ranks = division_avg.iloc[25:]

    school_df = div_df[div_df['school'] == school]
    school_avg = school_df.drop(['season', 'dayOfMonth'], axis=1).mean(numeric_only=True)
    school_avg_scores = school_avg.iloc[:24]
    school_avg_ranks = school_avg.iloc[25:]

    # Create an array of x-axis positions for the bars
    x = range(len(div_avg_scores))

    width = 0.35  # Width of the bars

    fig, ax = plt.subplots()

    division_bars = ax.bar(x, div_avg_scores, width, color='#DD517F', label=f'{division}')
    school_bars = ax.bar([i + width for i in x], school_avg_scores, width, color='#461E52', label=school)

    ax.set_xlabel('Category')
    ax.set_ylabel('Average Score')

    labels = ['MusicPerf Ens', 'MusicPerf Ind', 'MusicPerf SubTotal', 'VisualPerf Ens', 'VisualPerf Ind', 'VisualPerf Subtotal', 'Performance Total', 'GE Music CE', 'GE Music PE', 'GE Music Subtotal', 'GE Visual CE', 'GE Visual PE', 'GE Visual Subtotal', 'GE Total', 'Perc Cont', 'Perc Ach', 'Perc ScaledTotal', 'Perc Total', 'Guard Cont', 'Guard Ach', 'Guard Total', 'Guard ScaledTotal', 'Sub Total', 'Timing/Penalties', 'Total']

    ax.set_xticks([i + width / 2 for i in x])
    ax.set_xticklabels(labels, rotation=90)
    ax.legend()

    # Label the division bars
    for bar in division_bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}', xy=(bar.get_x() + bar.get_width() / 2, height), xytext=(0, 3),
                    textcoords="offset points", ha='center', va='bottom', color='#DD517F', rotation=90)

    # Label the school bars
    for bar in school_bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}', xy=(bar.get_x() + bar.get_width() / 2, height), xytext=(0, 3),
                    textcoords="offset points", ha='center', va='bottom', color='#461E52', rotation=90)

    plt.title('Average Scores Comparison')
    plt.tight_layout()

    plt.show() # instead of plt.show()

def findCompetitorsCompCentric(school, df):
        division = df.loc[df['school'] == school].iloc[0]["division"]
        school_df = df[df['school'] == school]
        competitions = school_df['comp'].unique()
        competitor_df = df[df['comp'].isin(competitions)]
        allCompetitors = competitor_df['school'].unique()
        school_avg = school_df.drop(['season', 'dayOfMonth'], axis=1).mean(numeric_only=True)
        target_scores = school_avg.iloc[:24]
        target_ranks = school_avg.iloc[25:]
        similarityScores = []
        numericColumns = competitor_df.select_dtypes(include = np.number).drop(["dayOfMonth", "season"], axis = 1).columns.tolist()
        scoreCols = numericColumns[:24]
        rankCols = numericColumns[25:]

        for idx, row in competitor_df.iterrows():
            scores = row[scoreCols]
            ranks = row[rankCols]

            scoreSimilarity = 1 / (1 + np.linalg.norm(target_scores - scores))
            rankSimilarity = 1 / (1 + np.linalg.norm(target_ranks - ranks))
            total_similarity = scoreSimilarity + rankSimilarity
            similarityScores.append((row['school'], total_similarity))
        similarityScores.sort(key=lambda x: x[1], reverse=True)

        #weights = [(score[0], score[1] + 0.25) for score in similarityScores if df.loc[df['school'] == score[0], 'division'].values[0] == df.loc[df['school'] == school, 'division'].values[0]]
        weights = [(score[0], score[1] + 0.25) for score in similarityScores if df.loc[df['school'] == score[0], 'division'].values[0] == division]

        weights.sort(key=lambda x: x[1], reverse=True)
        num_competitors = 5
        closestCompetitors = []
        added_schools = set()
        for score in weights:
            if score[0] not in added_schools and score[0] != school:
                closestCompetitors.append(score[0])
                added_schools.add(score[0])
                if len(closestCompetitors) >= num_competitors:
                    break

        # print(f'The closest competitors of {school} are: {closestCompetitors}')
        return closestCompetitors

def lineGraph(school, df):
        division = df.loc[df['school'] == school].iloc[0]["division"]
        competitorsAndTarget = findCompetitorsCompCentric(school,  df)
        if "Cesar E. Chavez High School Titan Band" not in competitorsAndTarget:
            competitorsAndTarget.append("Cesar E. Chavez High School Titan Band")
        if school not in competitorsAndTarget:
             competitorsAndTarget.append(school)
        lineFig = plt.figure(figsize=(10, 6))
        for targschool in competitorsAndTarget:

            school_df = df[df['school'] == targschool].copy()  # Make a copy of the filtered DataFrame


            school_df['date'] = pd.to_datetime(school_df['month'].astype(str) + ' ' + school_df['dayOfMonth'].astype(str) + ', ' + school_df['season'].astype(str), format='%B %d, %Y')


            school_df = school_df.sort_values('date')

            competitions = school_df['comp'].tolist()
            dates = school_df['date'].tolist()
            # scores = [scores[-1] for scores in school_df['scores'].apply(parseScoresAndRanks).tolist()]
            scores = [score for score in school_df['TotalScore']]
            

            # Sort scores and dates together based on dates
            sorted_indices = np.argsort(dates)
            sorted_dates = np.array(dates)[sorted_indices]
            sorted_scores = np.array(scores)[sorted_indices]

            # Plot the line for the school
            plt.plot(sorted_dates, sorted_scores.astype(float), marker='o', label=targschool)

        # Set labels and title
        plt.xlabel('Date')
        plt.ylabel('Scores')
        plt.title('Total Scores Over Time')
        plt.xticks(rotation=45)

        # Add legend
        plt.legend()

        # Display the graph
        plt.tight_layout()
        plt.show()# instead of plt.show()

def calculatePercentiles(school, df, return_type = "dictionary"):
    division = df.loc[df['school'] == school].iloc[0]["division"]
    categories = df.select_dtypes(include=np.number).drop(["dayOfMonth", "season"], axis=1).columns.tolist()
    categories.append('school')

    # Calculate percentiles for each category within the division
    filtered_df = df[df['division'] == division][categories]

    
    school_avg = filtered_df[filtered_df['school']==school].mean(numeric_only=True)

    mean_scores_df = filtered_df.groupby('school').mean()
    percentiles = []

    # print(school_avg['TotalRank'])

    categories.pop(-1)
   
    for col in categories:
         percentile = stats.percentileofscore(mean_scores_df[col], school_avg[col], kind = 'strict')
         percentiles.append(percentile)

    if return_type == "dictionary":
        pcntl_dict = {col:perc for col, perc in zip(categories, percentiles)}
        return pcntl_dict
    if return_type == "arr":
         return percentiles
         
def averageSchoolScoresAndRanks(school, df, rType = "default"):
    school_df = df[df['school'] == school]
    school_avg = school_df.drop(['season', 'dayOfMonth'], axis=1).mean(numeric_only=True)
    school_avg_scores = school_avg.iloc[:24]
    school_avg_ranks = school_avg.iloc[25:]
    if rType == "default":
        return school_avg_ranks, school_avg_scores
    elif rType == "both":
        return school_avg
    
def getAvgs(school, df, ntype = "sandr"):
     if(ntype == "s"):
        return averageSchoolScoresAndRanks(school, df)[1]
     elif(ntype == "r"):
        return averageSchoolScoresAndRanks(school, df)[0]
     else:
        return averageSchoolScoresAndRanks(school, df, "both")

def compareSchooltoSchoolAvgs(school1, school2, df1, df2):
    division1 = df1.loc[df1['school'] == school1].iloc[0]["division"]
    division2 = df2.loc[df2['school'] == school2].iloc[0]["division"]
    # div_df1 = df1[df1['division'] == division1]
    # div_df2 = df2[df2['division'] == division2]

    school1_df = df1[df1['school'] == school1]
    school1_avg = school1_df.drop(['season', 'dayOfMonth', 'GSTS', 'PSTS'], axis=1).mean(numeric_only=True)
    school1_avg_scores = school1_avg.iloc[:23]
    # school1_avg_ranks = school1_avg.iloc[25:]

    school2_df = df2[df2['school'] == school2]

    school2_avg = school2_df.drop(['season', 'dayOfMonth', 'GSTS', 'PSTS'], axis=1).mean(numeric_only=True)
    school2_avg_scores = school2_avg.iloc[:23]
    # school2_avg_ranks = school2_avg.iloc[25:]
    labels = ['MusicPerf Ens', 'MusicPerf Ind', 'MusicPerf SubTotal', 'VisualPerf Ens', 'VisualPerf Ind', 'VisualPerf Subtotal', 'Performance Total', 'GE Music CE', 'GE Music PE', 'GE Music Subtotal', 'GE Visual CE', 'GE Visual PE', 'GE Visual Subtotal', 'GE Total', 'Perc Cont', 'Perc Ach', 'Perc ScaledTotal', 'Guard Cont', 'Guard Ach', 'Guard Total', 'Sub Total', 'Timing/Penalties', 'Total']

    # Create an array of x-axis positions for the bars
    x = range(len(school2_avg_scores))
    print(school2_avg_scores)

    width = 0.35  # Width of the bars

    fig, ax = plt.subplots()

    school1_bars = ax.bar(x, school1_avg_scores, width, color='#00bbf3', label=f'{school1}') #usd to be division
    school2_bars = ax.bar([i + width for i in x], school2_avg_scores, width, color='#f3d165', label=school2)

    ax.set_xlabel('Category')
    ax.set_ylabel('Average Score')


    ax.set_xticks([i + width / 2 for i in x]) 
    ax.set_xticklabels(labels, rotation=90)
    ax.legend()

    # Label the division bars
    for bar in school1_bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}', xy=(bar.get_x() + bar.get_width() / 2, height), xytext=(0, 3),
                    textcoords="offset points", ha='center', va='bottom', color='#00bbf3', rotation=90)

    # Label the school bars
    for bar in school2_bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}', xy=(bar.get_x() + bar.get_width() / 2, height), xytext=(0, 3),
                    textcoords="offset points", ha='center', va='bottom', color='#f3d165', rotation=90)

    plt.title('Average Scores Comparison')
    plt.tight_layout()
    plt.show() # instead of plt.show()

def getScoreBoardBasedonAvgScoreInEachCategory(df, division, num, cols = ['MPES', 'MPIS', 'VPES', 'VPIS', 'VPSTS', 'PSTS', 'GEMCES', 'GEMPES', 'GEVCES', 'GEVPES', 'GETS', 'PCS', 'PAS', 'PSTS', 'GCS', 'GAS', 'GTS', 'TotalScore']):

    filtered = df[df['division'] == division]
    filtered = filtered.groupby('school', as_index = False).mean()

    for col in cols:
        if "R" in col:
            colDF = filtered[['school', col]].sort_values(by= col)
            print(colDF.head(n = num).to_string(index=False))
        else: 
            colDF = filtered[['school', col]].sort_values(by= col, ascending=False)
            print(colDF.head(n = num).to_string(index=False))

def getScoreBoardFromMostRecentScores(df, division, num, cols=['MPES', 'MPIS', 'VPES', 'VPIS', 'VPSTS', 'PSTS', 'GEMCES', 'GEMPES', 'GEVCES', 'GEVPES', 'GETS', 'PCS', 'PAS', 'PSTS', 'GCS', 'GAS', 'GTS', 'TotalScore']):
    # Define a mapping from month names to numeric ranks
    month_rank_mapping = {
        'January': 1,
        'February': 2,
        'March': 3,
        'April': 4,
        'May': 5,
        'June': 6,
        'July': 7,
        'August': 8,
        'September': 9,
        'October': 10,
        'November': 11,
        'December': 12
    }

    # Convert the 'month' column to numeric ranks
    df['month_rank'] = df['month'].map(month_rank_mapping)

    filtered_df = df[df['division'].isin(division)]
    filtered_df = filtered_df.sort_values(by=['month_rank', 'dayOfMonth'], ascending=False).groupby('school').first().reset_index()

    for col in cols:
        if "R" in col:
            colDF = filtered_df[['school', col]].sort_values(by=col)
            print(colDF.head(n=num).to_string(index=False))
        else:
            colDF = filtered_df[['school', col]].sort_values(by=col, ascending=False)
            print(colDF.head(n=num).to_string(index=False))

def findCompetitorsDivisionCentric(school, df):
    division = df.loc[df['school'] == school].iloc[0]["division"]
    school_df = df[df['school'] == school]
    div_df = df[df['division'] == division]
    school_avg = school_df.drop(['season', 'dayOfMonth'], axis=1).mean(numeric_only=True)
    target_scores = school_avg.iloc[:24]
    target_ranks = school_avg.iloc[25:]
    similarityScores = []
    numericColumns = div_df.select_dtypes(include = np.number).drop(["dayOfMonth", "season"], axis = 1).columns.tolist()
    scoreCols = numericColumns[:24]
    rankCols = numericColumns[25:]

    for idx, row in div_df.iterrows():
        scores = row[scoreCols]
        ranks = row[rankCols]

        scoreSimilarity = 1 / (1 + np.linalg.norm(target_scores - scores))
        rankSimilarity = 1 / (1 + np.linalg.norm(target_ranks - ranks))
        total_similarity = scoreSimilarity + rankSimilarity
        similarityScores.append((row['school'], total_similarity))
    similarityScores.sort(key=lambda x: x[1], reverse=True)

    #weights = [(score[0], score[1] + 0.25) for score in similarityScores if df.loc[df['school'] == score[0], 'division'].values[0] == df.loc[df['school'] == school, 'division'].values[0]]
    weights = [(score[0], score[1] + 0.25) for score in similarityScores if df.loc[df['school'] == score[0], 'division'].values[0] == division]

    weights.sort(key=lambda x: x[1], reverse=True)
    num_competitors = 5
    closestCompetitors = []
    added_schools = set()
    for score in weights:
        if score[0] not in added_schools and score[0] != school:
            closestCompetitors.append(score[0])
            added_schools.add(score[0])
            if len(closestCompetitors) >= num_competitors:
                break

        # print(f'The closest competitors of {school} are: {closestCompetitors}')
    return closestCompetitors


def compareSchooltoSchoolFinals(school1, school2, df1, df2):
    school1_df = df1[df1['school'] == school1]
    school1_df['month_rank'] = school1_df['month'].map(month_rank_mapping)
    school1_df = school1_df.sort_values(by=['month_rank', 'dayOfMonth'], ascending=False).head(1).reset_index(drop = True).drop(['season', 'dayOfMonth', 'GSTS', 'PSTS'], axis=1)
    school1_latest = school1_df.iloc[:23]
    # school1_avg_ranks = school1_avg.iloc[25:]

    school2_df = df2[df2['school'] == school2]

    school2_df['month_rank'] = school2_df['month'].map(month_rank_mapping)
    school2_df = school2_df.sort_values(by=['month_rank', 'dayOfMonth'], ascending=False).head(1).reset_index(drop = True).drop(['season', 'dayOfMonth', 'GSTS', 'PSTS'], axis=1)
    school2_latest = school2_df.iloc[:23]
    print(school2_latest)
    


dfUsed = pd.read_csv('csbcData2023.csv')
dfUsed2 = pd.read_csv('csbcData2022.csv')
s = "Scripps Ranch High School"

# print(dfUsed1.columns)
# print(len(dfUsed1.columns))

getScoreBoardFromMostRecentScores(dfUsed, "Division 5A", ['TotalScore'])