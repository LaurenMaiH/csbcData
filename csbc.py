from selenium import webdriver
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from urllib.parse import urljoin
import matplotlib.pyplot as plt
import os.path
from scipy.stats import percentileofscore

labels = ['MusicPerf Ens', 'MusicPerf Ind', 'MusicPerf SubTotal', 'VisualPerf Ens', 'VisualPerf Ind', 'VisualPerf Subtotal', 'Performance Total', 'GE Music CE', 'GE Music PE', 'GE Music Subtotal', 'GE Visual CE', 'GE Visual PE', 'GE Visual Subtotal', 'GE Total', 'Perc Cont', 'Perc Ach', 'Perc Total', 'Perc ScaledTotal', 'Guard Cont', 'Guard Ach', 'Guard Total', 'Guard ScaledTotal', 'Sub Total', 'Timing/Penalties', 'Total']



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
def getInfo(soup, division_name):
    division_tbody = soup.find('td', attrs={'style': 'text-align: center; padding: 2px; font-weight: bold; font-size: 14px;'}, string=division_name).find_parent('tbody')
    contentScores = [score.text.strip() for score in division_tbody.find_all('td', class_='content score')]
    contentRanks = [rank.text.strip() for rank in division_tbody.find_all('td', class_='content rank')]
    headersAndLocation = [header.text.strip() for header in division_tbody.find_all('td', class_ = 'content topBorder rightBorderDouble')]
    locationsAreListed = hasLocation(soup)
    if locationsAreListed:
        headers = headersAndLocation[::2]
        locations = headersAndLocation[1::2]
    else:
        headers = headersAndLocation
        locations = 'LNF'
    compLabel = soup.find(compFilter)
    comp = compLabel.text
    month, day, szn = findDateSznMonth(soup)
    num_scores_per_school = 25 if len(contentScores) % 25 == 0 else 23

        

    try:
        schoolScores = [contentScores[i:i+num_scores_per_school] for i in range(0, len(contentScores), num_scores_per_school)]
        schoolRanks = [contentRanks[i:i+num_scores_per_school] for i in range(0, len(contentRanks), num_scores_per_school)]
    except ValueError:
        print("Error: Unable to parse scores and ranks.")
        return None

    if num_scores_per_school == 23:
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

        return modifiedSchoolScores, modifiedSchoolRanks, headers, locations, comp, month, day, szn, locationsAreListed
    else:
        return schoolScores, schoolRanks, headers, locations, comp, month, day, szn, locationsAreListed
def findDivision(soup):
    divs = soup.find_all('td', attrs={'style': 'text-align: center; padding: 2px; font-weight: bold; font-size: 14px;'})
    divText = [div.text for div in divs]
    for div in divText:
        try:
            div.split(' ')[1]
        except IndexError:
            div = div
    return divText
def hasLocation(soup):
    text = soup.get_text()
    if ", CA" in text:
        return True
    else:
        return False

def createSchoolDicts(schoolScores, schoolRanks, headers, locations, comp, month, day, szn, division, locationsAreListed):
    listDicts = {}
    print(headers)
    for school in headers:
        idx = headers.index(school)
        stats = {
            'school': school,
            'scores': np.array(schoolScores[idx]),
            'ranks': np.array(schoolRanks[idx]),
            'comp': comp,
            'month': month,
            'dayOfMonth': day,
            'season': szn,
            'division': division
        }

        
        if locationsAreListed:
            stats['location'] = locations[idx]
        else:
            stats['location'] = "LNL"

        listDicts[school] = stats
    

    return listDicts
#data = createSchoolDicts(schoolScores, schoolRanks, headers, locations, comp, month, day, szn)
#df = pd.DataFrame.from_dict(data).T
#df.to_csv('csbcData.csv', index=True)

# soup = getHTML('https://recaps.competitionsuite.com/c284b34d-6d37-4819-a119-2053fdd951ba.htm')
# print(hasLocation(soup))

# urls2022 = ['https://recaps.competitionsuite.com/2bf4c34f-4eae-4ac1-9a0c-b29ff8c429d6.htm', 'https://recaps.competitionsuite.com/2cda9f44-30fd-4bf7-b68a-d4dcf88155e0.htm', 'https://recaps.competitionsuite.com/d3749b61-3f2e-47f9-82d4-e3be345ee388.htm', 'https://recaps.competitionsuite.com/4dfb6cec-1345-43e5-b243-870af94fe9c5.htm', 'https://recaps.competitionsuite.com/986cdf29-2112-49d7-9696-032b5960e5a4.htm', 'https://recaps.competitionsuite.com/98793bbc-b569-4fd5-ab0d-0aa0142c4aa9.htm', 'https://recaps.competitionsuite.com/b97ff93d-8885-4ad5-b272-33bac8e0c1f1.htm', 'https://recaps.competitionsuite.com/e52a7e9d-ef14-4d4e-999c-af021d8b4840.htm', 'https://recaps.competitionsuite.com/8777d3b4-9bee-4bb4-9b88-57bfc573c793.htm', 'https://recaps.competitionsuite.com/714f33e9-12e8-447f-bb3f-b5eb9044ff55.htm', 'https://recaps.competitionsuite.com/0e5ea311-8137-4ad7-8046-8a88e0edb191.htm', 'https://recaps.competitionsuite.com/f80efb8e-0b7c-48be-abc4-8a0b2e7b8565.htm', 'https://recaps.competitionsuite.com/8a6dcd63-a11c-44b7-be6e-e895fd2e4304.htm', 'https://recaps.competitionsuite.com/9bf24f5c-b692-4a01-a54a-21db55bc6278.htm', 'https://recaps.competitionsuite.com/45b4cf01-555d-475a-a466-49a06ea8aff1.htm', 'https://recaps.competitionsuite.com/f17b07b9-1b2d-42e4-b036-6368dcb2c894.htm', 'https://recaps.competitionsuite.com/247c1360-86be-4604-b3e6-62d4a9335bf8.htm', 'https://recaps.competitionsuite.com/3f674eb1-2bce-45d8-8975-33a994648e6d.htm', 'https://recaps.competitionsuite.com/bbb56d9a-4334-43d4-a9a1-665b162f6585.htm', 'https://recaps.competitionsuite.com/f058b506-6091-462d-892b-95283bcd2bc4.htm', 'https://recaps.competitionsuite.com/b04bca39-9640-4468-b328-f64036c8d20f.htm', 'https://recaps.competitionsuite.com/faf83bac-e8ef-4204-845a-d4b3236e5205.htm', 'https://recaps.competitionsuite.com/759fa5b2-71de-4d5d-b84c-8cc8a13598a4.htm', 'https://recaps.competitionsuite.com/433fbf09-e697-4149-a7fc-221234c9477a.htm', 'https://recaps.competitionsuite.com/16603d93-bf22-47a8-8d7b-53404785419d.htm', 'https://recaps.competitionsuite.com/5c29ba54-6040-47d2-a3a8-c0a6689c0fa5.htm', 'https://recaps.competitionsuite.com/409e1a97-73b7-4b8c-ab08-f785d4fa5032.htm', 'https://recaps.competitionsuite.com/cdd37fd8-f4d9-4826-b80e-b20118fdabf9.htm', 'https://recaps.competitionsuite.com/810b0731-895c-4631-ae12-7c20306a1487.htm']
def doEverything(url):
    
    soup = getHTML(url)
    for division in findDivision(soup):
        schoolScores, schoolRanks, headers, locations, comp, month, day, szn, locationsAreListed = getInfo(soup, division)
        data = createSchoolDicts(schoolScores, schoolRanks, headers, locations, comp, month, day, szn, division, locationsAreListed)
        df = pd.DataFrame.from_dict(data, orient='index')
        if os.path.isfile('csbcData2022.csv'):
            df.to_csv('csbcData2022.csv', mode = 'a', index=False, header = False)
        else:
            df.to_csv('csbcData2022.csv', index=False)



# for url in urls2022:
#     doEverything(url)

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

        for targschool in competitorsAndTarget:

            school_df = self.df[self.df['school'] == targschool].copy()  # Make a copy of the filtered DataFrame


            school_df['date'] = pd.to_datetime(school_df['month'].astype(str) + ' ' + school_df['dayOfMonth'].astype(str) + ', ' + school_df['season'].astype(str), format='%B %d, %Y')


            school_df = school_df.sort_values('date')

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
# div = 'Division 5A'
# dfUsed = pd.read_csv('csbcData2021.csv')
# Scripps = printInfo(infoSchool, div, dfUsed)
# Scripps.lineGraph()
# Scripps.printPercentiles()
# Scripps.printRanks()

