from selenium import webdriver
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re
import requests
from urllib.parse import urljoin
import matplotlib.pyplot as plt
from scipy.stats import percentileofscore
url = "https://recaps.competitionsuite.com/2cda9f44-30fd-4bf7-b68a-d4dcf88155e0.htm"
def getHTML(url):
    # Set up the web driver (in this case, we're using Chrome)
    driver = webdriver.Chrome()

    # Load the page
    driver.get(url)

    # Wait for the page to fully render
    driver.implicitly_wait(10)

    # Extract the HTML from the fully rendered page
    html = driver.page_source

    # Clean up the HTML with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Close the web driver
    driver.quit()

    return soup
def compFilter(tag):
    return tag.name == 'div' and tag.get('style') == 'text-align: center; font-weight: bold; font-size: 18px; max-width: 750px; white-space: normal'
def dateSzn(tag):
    return tag.name == 'div' and tag.get('style') == 'text-align: center; font-style: italic; font-size: 12px; margin-top: 5px;'
def findDateSznMonth(soup):
    dateAndSzn = soup.find_all(dateSzn)
    dateSznFinal = [element.text for element in dateAndSzn if any(char.isdigit() for char in element.text)]
    month, day = dateSznFinal[0].split(',')[1].split(' ')[1:]
    szn = dateSznFinal[0].split(',')[2][1:]

    return month, day, szn
def getInfo(soup):
    contentScores = [score.text.strip() for score in soup.find_all('td', class_ ='content score')]
    contentRanks = [rank.text.strip() for rank in soup.find_all('td', class_ ='content rank')]
    headersAndLocation = [header.text.strip() for header in soup.find_all('td', class_ = 'content topBorder rightBorderDouble')]
    headers = headersAndLocation[::2]
    locations = headersAndLocation[1::2]
    print(type(contentScores))
    print(contentScores)
    # schoolScores = [contentScores[i:i+25] for i in range(0, len(contentScores), 25)]
    # schoolRanks = [contentRanks[i:i+25] for i in range(0, len(contentRanks), 25)]
    # the next couple of lines are modified for the funky formate in CSBC 2021. uncomment the abvoe lines and comment out the below to restore to new format
    schoolScores = [contentScores[i:i+23] for i in range(0, len(contentScores), 23)]
    schoolRanks = [contentRanks[i:i+23] for i in range(0, len(contentRanks), 23)]
    
    modifiedSchoolScores = []
    modifiedSchoolRanks = []

    for scores in schoolScores:
        scores.insert(17, str(float(scores[16]) / 10))
        scores.insert(21, str(float(scores[20]) / 10))
        modifiedSchoolScores.append(scores)

    for ranks in schoolRanks:
        ranks.insert(17, ranks[16])
        ranks.insert(21, ranks[20])
        modifiedSchoolRanks.append(ranks)
    compLabel = soup.find(compFilter)
    comp = compLabel.text
    month, day, szn = findDateSznMonth(soup)

    #return schoolScores, schoolRanks, headers, locations, comp, month, day, szn
    return modifiedSchoolScores, modifiedSchoolRanks, headers, locations, comp, month, day, szn
def findDivision(school_name):
    soup = getHTML("https://csbc.compsuite.io/groups")
    link = None
    for a_tag in soup.find_all('a'):
        if school_name.lower() in a_tag.text.lower():
            link = a_tag['href']
            break
    if link is not None:
        base_url = "https://csbc.compsuite.io"
        full_url = base_url + link
        soup = getHTML(full_url)
        # Find the <div> tag containing "Division xA" text
        division_tag = None
        for div_tag in soup.find_all('div'):
            if 'Division' in div_tag.text and div_tag.text.endswith('A'):
                division_tag = div_tag
                break

        if division_tag is not None:
            info = division_tag.text.strip()
            return info.split(' ')[1]

    # If the school or division info is not found, return None or handle the error accordingly
    return None        
def createSchoolDicts(schoolScores, schoolRanks, headers, locations, comp, month, day, szn):
    listDicts = {}
    for school in headers:
        idx = headers.index(school)
        stats = {
            'scores': np.array(schoolScores[idx]),
            'ranks': np.array(schoolRanks[idx]),
            'location': locations[idx],
            'comp': comp,
            'month': month,
            'dayOfMonth': day,
            'season': szn,
            'division': findDivision(school)
        }
        listDicts[school] = stats

    return listDicts
#data = createSchoolDicts(schoolScores, schoolRanks, headers, locations, comp, month, day, szn)
#df = pd.DataFrame.from_dict(data).T
#df.to_csv('csbcData.csv', index=True)

urls = ['https://recaps.competitionsuite.com/4b57b394-4733-4ce1-b228-e6cb0d77aa34.htm','https://recaps.competitionsuite.com/c937b83c-6c33-425f-94c2-fb9ebc69c27f.htm','https://recaps.competitionsuite.com/0e7526aa-665d-4684-ad3b-227b0989504b.htm','https://recaps.competitionsuite.com/ce9d2def-789f-48f4-bd63-02e41ca50907.htm','https://recaps.competitionsuite.com/15e3ae6c-eaf3-4a5f-948d-4a58c42ee17d.htm','https://recaps.competitionsuite.com/a710bb36-d400-417e-a92c-c8a9d3a5b931.htm','https://recaps.competitionsuite.com/a7ee52a0-d3f1-42e0-a283-87db425b23bb.htm','https://recaps.competitionsuite.com/e768de25-1e79-4579-becf-bb4a1236d5e2.htm','https://recaps.competitionsuite.com/7a02ab6e-7fde-473b-8f0b-8c3913b3137f.htm','https://recaps.competitionsuite.com/331fdf07-e6d7-4d3e-b0d4-fbe46892bcdb.htm','https://recaps.competitionsuite.com/d2eb9a15-dee8-4625-bd69-7dac7833d086.htm','https://recaps.competitionsuite.com/1d71df67-cbd8-4be8-bc46-68b098de7869.htm','https://recaps.competitionsuite.com/29f5862a-785a-4c6c-a6dc-770d05f999ad.htm','https://recaps.competitionsuite.com/fa57a668-3268-41b3-b352-65d3f0536f3c.htm','https://recaps.competitionsuite.com/f67ad4b7-ebf6-418d-9f4b-932479987f6a.htm','https://recaps.competitionsuite.com/96b54e79-bf9a-47f8-aad7-f8ccda9892dd.htm','https://recaps.competitionsuite.com/2142aa69-b08c-4193-8892-b567dbaf3b5f.htm','https://recaps.competitionsuite.com/cc849f9d-1256-42b5-b308-8092f5c12982.htm','https://recaps.competitionsuite.com/2bb6c25b-6fcc-4090-a8d2-7593d3d9d6e1.htm','https://recaps.competitionsuite.com/ad547192-810a-49d6-be7e-937671844f75.htm','https://recaps.competitionsuite.com/cbd8d983-32ab-4eea-a8a1-b5ec26b5424f.htm','https://recaps.competitionsuite.com/4e6a73d7-0dec-48c1-babf-abc89231e865.htm','https://recaps.competitionsuite.com/a8dfdde8-34ad-4552-8010-0684d930c5c9.htm','https://recaps.competitionsuite.com/6b129b9e-42f5-47be-912e-cb9f744b344a.htm','https://recaps.competitionsuite.com/6cd04f7a-ff22-4894-9409-c06d4dde63e4.htm','https://recaps.competitionsuite.com/5ec6f9e5-08f1-42ed-b013-c689a4fae009.htm','https://recaps.competitionsuite.com/9da0cc7e-4719-4466-8e4b-799531570a0a.htm']

def doEverything(url):
    
    soup = getHTML(url)
    schoolScores, schoolRanks, headers, locations, comp, month, day, szn = getInfo(soup)
    data = createSchoolDicts(schoolScores, schoolRanks, headers, locations, comp, month, day, szn)
    df = pd.DataFrame.from_dict(data).T
    #df.to_csv('csbcData.csv', mode = 'a', index=True)
    # df.to_csv('csbcData2019.csv', mode = 'a', index=True)
    df.to_csv('csbcData2019.csv', index=True)

for url in urls:
    doEverything(url)


df2023 = pd.read_csv('csbcData.csv')
def parseScoresAndRanks(numArray):
    listNums = numArray.strip("[]").replace("'", "").split()
    return listNums

def parseScoresAndRanksForSchool(schoolName, df):
    # if season:
    #     filtered_df = df[(df['school'] == schoolName) & (df['season'] == season)]
    # else:
    filtered_df = df[df['school']== schoolName]
    scoresList = filtered_df['scores'].tolist()
    scoresList = [parseScoresAndRanks(score_str) for score_str in scoresList]
    scoresArray = np.array(scoresList, dtype=float)
    ranksList = filtered_df['ranks'].tolist()
    ranksList = [parseScoresAndRanks(ranks_str) for ranks_str in ranksList]
    ranksArray = np.array(ranksList, dtype=float)
    return scoresArray, ranksArray

def getAvgScoresAndRanksPerSchool(schoolName, df):
    mean_scores = np.mean(parseScoresAndRanksForSchool(schoolName, df)[0], axis=0)
    mean_ranks = np.mean(parseScoresAndRanksForSchool(schoolName, df)[1], axis=0)

    return mean_scores, mean_ranks

def getAvgScoresAndRanksForDivision(division, df):
    filtered_df = df[df['division'] == division]
    scoresList = filtered_df['scores'].tolist()
    scoresList = [score_str.strip("[]").replace("'", "").split() for score_str in scoresList]
    scoresArray = np.array(scoresList, dtype=float)
    mean_scores = np.mean(scoresArray, axis=0)

    ranksList = filtered_df['ranks'].tolist()
    ranksList = [ranks_str.strip("[]").replace("'", "").split() for ranks_str in ranksList]
    max_len = max(len(rank) for rank in ranksList)
    ranksList = [rank + ['0'] * (max_len - len(rank)) for rank in ranksList]
    ranksArray = np.array(ranksList, dtype=float)
    mean_ranks = np.mean(ranksArray, axis=0)

    return mean_scores, mean_ranks


def dataAnalysis(school, division, df):
    division_avg_scores = getAvgScoresAndRanksForDivision(division, df)[0]
    school_avg_scores = getAvgScoresAndRanksPerSchool(school, df)[0]

    x = np.arange(division_avg_scores.shape[0])
    width = 0.45  # Width of the bars

    fig, ax = plt.subplots()
    division_bars = ax.bar(x - width/2, division_avg_scores, width, color = '#DD517F', label=f'Division {division}')
    school_bars = ax.bar(x + width/2, school_avg_scores, width, color='#461E52', label= school)

    ax.set_xlabel('Category')
    ax.set_ylabel('Average Score')

    labels = ['MusicPerf Ens', 'MusicPerf Ind', 'MusicPerf SubTotal', 'VisualPerf Ens', 'VisualPerf Ind', 'VisualPerf Subtotal', 'Performance Total', 'GE Music CE', 'GE Music PE', 'GE Music Subtotal', 'GE Visual CE', 'GE Visual PE', 'GE Visual Subtotal', 'GE Total', 'Perc Cont', 'Perc Ach', 'Perc Total', 'Perc ScaledTotal', 'Guard Cont', 'Guard Ach', 'Guard Total', 'Guard ScaledTotal', 'Sub Total', 'Timing/Penalties', 'Total']

    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=90)
    ax.legend()

    # Label the division bars
    for bar in division_bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}', xy=(bar.get_x() + bar.get_width() / 2, height), xytext=(0,3),
                    textcoords="offset points", ha='center', va='bottom',color = '#DD517F', rotation = 90)

    # Label the school bars
    for bar in school_bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}', xy=(bar.get_x() + bar.get_width() / 2, height), xytext=(0,3),
                    textcoords="offset points", ha='center', va='bottom', color='#461E52', rotation = 90)
    plt.title('Average Scores Comparison')
    plt.tight_layout()
    plt.show()

    percentile_ranks = [percentileofscore(division_avg_scores, score) for score in school_avg_scores]
    return percentile_ranks, labels

def findCompetitors(school, division, df):
        filtered_df = df[df['school'] == school]
        competitions = filtered_df['comp'].unique()
        competitor_df = df[df['comp'].isin(competitions)]
        allCompetitors = competitor_df['school'].unique()
        target_scores = np.array(parseScoresAndRanks(filtered_df['scores'].iloc[0]), dtype=float)
        target_ranks = np.array(parseScoresAndRanks(filtered_df['ranks'].iloc[0]), dtype=float)
        similarityScores = []
        for idx, row in competitor_df.iterrows():
            scores = np.array(parseScoresAndRanks(row['scores']), dtype=float)
            ranks = np.array(parseScoresAndRanks(row['ranks']), dtype=float)
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
            if score[0] not in added_schools:
                closestCompetitors.append(score[0])
                added_schools.add(score[0])
                if len(closestCompetitors) >= num_competitors:
                    break

        print(f'The closest competitors of {school} are: {closestCompetitors}')
        return closestCompetitors

labels = ['MusicPerf Ens', 'MusicPerf Ind', 'MusicPerf SubTotal', 'VisualPerf Ens', 'VisualPerf Ind', 'VisualPerf Subtotal', 'Performance Total', 'GE Music CE', 'GE Music PE', 'GE Music Subtotal', 'GE Visual CE', 'GE Visual PE', 'GE Visual Subtotal', 'GE Total', 'Perc Cont', 'Perc Ach', 'Perc Total', 'Perc ScaledTotal', 'Guard Cont', 'Guard Ach', 'Guard Total', 'Guard ScaledTotal', 'Sub Total', 'Timing/Penalties', 'Total']
class printInfo:
    def __init__(self, school, division, df):
        self.school = school
        self.division = division
        self.df  = df
        # if season == "All Time":
        #     self.season = None
        # else:
        #     self.season = season

    def lineGraph(self):
        competitorsAndTarget = findCompetitors(self.school, self.division, self.df)
        competitorsAndTarget.append('The Spirit of Great Oak')
        # Plot lines for each school
        for targschool in competitorsAndTarget:
            # Filter the DataFrame for the current school
            school_df = self.df[self.df['school'] == targschool].copy()  # Make a copy of the filtered DataFrame

            # Combine separate date columns into a single column
            school_df['date'] = pd.to_datetime(school_df['month'].astype(str) + ' ' + school_df['dayOfMonth'].astype(str) + ', ' + school_df['season'].astype(str), format='%B %d, %Y')

            # Sort the DataFrame by date
            school_df = school_df.sort_values('date')

            # Extract the competitions, dates, and scores
            competitions = school_df['comp'].tolist()
            dates = school_df['date'].tolist()
            scores = [scores[-1] for scores in school_df['scores'].apply(parseScoresAndRanks).tolist()]

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
        plt.show()

    
    def printPercentiles(self):
        percentile_ranks, labels = dataAnalysis(self.school, self.division, self.df)
        labelsModified = ['MusicPerf Ens', 'MusicPerf Ind', 'MusicPerf SubTotal', 'VisualPerf Ens', 'VisualPerf Ind', 'VisualPerf Subtotal', 'Performance Total', 'GE Music CE', 'GE Music PE', 'GE Music Subtotal', 'GE Visual CE', 'GE Visual PE', 'GE Visual Subtotal', 'GE Total', 'Perc Cont', 'Perc Ach', 'Perc Total', 'Perc ScaledTotal', 'Guard Cont', 'Guard Ach', 'Guard Total', 'Guard ScaledTotal', 'Sub Total', 'Total']
        percentile_ranks_modified = [percentile_ranks[labels.index(label)] for label in labelsModified]
    
        print(percentile_ranks_modified)
        for label, rank in zip(labelsModified, percentile_ranks_modified):
            if label in ['MusicPerf Ens', 'MusicPerf Ind', 'VisualPerf Ens', 'VisualPerf Ind', 'Performance Total', 'GE Music CE', 'GE Music PE', 'GE Visual CE', 'GE Visual PE', 'Perc Cont', 'Perc Ach', 'Perc Total', 'Guard Cont', 'Guard Ach', 'Guard Total', 'Total']:
                print(f'{label}: {rank}th percentile')
    def printRanks(self):
        ranks = getAvgScoresAndRanksPerSchool(self.school, self.df)[1]
        labelsModified = [label for label in labels if label != 'Timing/Penalties']
        for label in labelsModified:
            idx = labelsModified.index(label)
            print(f'{label}: {ranks[idx]}')

# interestSchool = 'Grand Terrace High School'
# div = df.loc[df['school'] == interestSchool, 'division'].iloc[0]
# info = printInfo(interestSchool, div, "All Time")
# print(div)
# info.printPercentiles()
# info.printRanks()



# infoSchool = 'Scripps Ranch High School'
# div = '5A'
# dfUsed = pd.read_csv('csbcData2021.csv')
# Scripps = printInfo(infoSchool, div, dfUsed)
# Scripps.lineGraph()
# Scripps.printPercentiles()
# Scripps.printRanks()

