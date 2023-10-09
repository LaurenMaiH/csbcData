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

def parseScoresAndRanks(numArray):
    listNums = numArray.strip("[]").replace("'", "").split()
    return listNums



def explodecolumn(df, columnName):
    if columnName == "scores":
        scorelabels = ['MPES', 'MPIS', 'MPSTS', 'VPES', 'VPIS', 'VPSTS', 'PTS', 'GEMCES', 'GEMPES', 'GEMSTS', 'GEVCES', 'GEVPES', 'GEVSTS', 'GETS', 'PCS', 'PAS', 'PTS', 'PSTS', 'GCS', 'GAS', 'GTS', 'GSTS', 'STS', 'T/P', 'TotalScore']

        for idx, col in enumerate(df['scores']):
        # Create a dictionary with new column names and values from the array
            scoreArray = parseScoresAndRanks(col)
            scoreArray = [float(i) for i in scoreArray]
            scoreDict = {scorelabels[i]: [scoreArray[i]] for i in range(len(scoreArray))}
            if idx ==0:
                scoreDF = pd.DataFrame.from_dict(scoreDict)
            else:
                scoreDF = scoreDF.append(scoreDict, ignore_index = True)

            result_df = pd.concat([df, scoreDF], axis=1)
            result_df.drop('scores', axis=1, inplace=True)
            result_df.to_csv("csbcData2019.csv", index=False)
    elif columnName == "ranks":
        ranklabels = ['MPER', 'MPIR', 'MPSTR', 'VPER', 'VPIR', 'VPSTR', 'PTR', 'GEMCER', 'GEMPER', 'GEMSTR', 'GEVCER', 'GEVPER', 'GEVSTR', 'GETR', 'PCR', 'PAR', 'PTR', 'PSTR', 'GCR', 'GAR', 'GTR', 'GSTR', 'STR', 'T/P_rank', 'TotalRank']

        for idx, col in enumerate(df['ranks']):
        # Create a dictionary with new column names and values from the array
            rankArray = parseScoresAndRanks(col)
            rankArray = [float(i) for i in rankArray]
            rankDict = {ranklabels[i]: [rankArray[i]] for i in range(len(rankArray))}
            if idx ==0:
                rankDF = pd.DataFrame.from_dict(rankDict)
            else:
                rankDF = rankDF.append(rankDict, ignore_index = True)

            result_df = pd.concat([df, rankDF], axis=1)
            result_df.drop('ranks', axis=1, inplace=True)
            result_df.to_csv("csbcData2022.csv", index=False)
            
    
def fixDivisionError(dataframe):
    finals_dataframe = dataframe[dataframe['division'].str.contains('Finals')]

    for school in finals_dataframe['school'].unique():
        finals_indices = finals_dataframe[finals_dataframe['school'] == school].index
        non_finals_row = dataframe[(dataframe['school'] == school) & ~dataframe['division'].str.contains('Finals')]


        non_finals_division = non_finals_row.iloc[0]['division']
        dataframe.loc[finals_indices, 'division'] = non_finals_division
    dataframe.to_csv("INPUT CSV HERE", index=False)


def getSchoolsBeatUs(df, school):
    filteredDataFrame = df[df['school'] == school]
    comps = filteredDataFrame['comp'].unique()
    print(comps)
    for comp in comps:
        compDF = df[df['comp'] == comp]

    """
    for comp in comps:
        comparisonRanks = comp[comp['school'] == 'Scripps Ranch HS Varsity']['ranks'].values
        comparisonScores = comp[comp['school'] == 'Scripps Ranch HS Varsity']['scores'].values
        
        for index, row in comp.iterrows():
            schoolRow = row['ranks']
            schoolName = row['school']
            categories = {
                0: 'Equipment Vocab', 
                1: 'Movement Vocab', 
                2: 'Design Composition',
                3: 'GE Rep 1', 
                4: 'GE Rep 2'
            }
            competition = row['comp']
            for i in range(len(schoolRow)):
                if np.any(schoolRow[i] < comparisonRanks[0][i]):
                    enemyScore = row['scores'][i]
                    ourScore = comparisonScores[0][i]
                    defeatMargin = str(enemyScore - ourScore)
                    print(f'At the competition {competition}, SRHS was beat by {schoolName} in {categories[i]}. The margin of defeat was {defeatMargin} ({enemyScore} - {ourScore} = {defeatMargin})')
"""

# dfUsed = pd.read_csv('csbcData2022.csv')
# infoSchool = 'Scripps Ranch High School'
# div = dfUsed.loc[dfUsed['school'] ==  infoSchool, 'division'].iloc[2]
# Scripps = printInfo(infoSchool, div, dfUsed)
# Scripps.lineGraph()
# Scripps.printPercentiles()
# Scripps.printRanks()
# print(div)






