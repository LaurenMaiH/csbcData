from selenium import webdriver
from selenium.webdriver.chrome.service import Service
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
    chromedriver_path = r"C:/Users/lauri/OneDrive/Documents/ChromeDrivers/chrome-win64/chromedriver.exe"

    # Create a Service object
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service)
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
    if "2023" in text:
        return False
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

def doEverything(url):
    
    soup = getHTML(url)
    for division in findDivision(soup):
        schoolScores, schoolRanks, headers, locations, comp, month, day, szn, locationsAreListed = getInfo(soup, division)
        data = createSchoolDicts(schoolScores, schoolRanks, headers, locations, comp, month, day, szn, division, locationsAreListed)
        df = pd.DataFrame.from_dict(data, orient='index')
        if os.path.isfile('csbcData2023.csv'):
            df.to_csv('csbcData2023.csv', mode = 'a', index=False, header = False)
        else:
            df.to_csv('csbcData2023.csv', index=False)

urls2023 = ['https://recaps.competitionsuite.com/338440d8-9750-48d6-a5dc-da64f75709b4.htm', 'https://recaps.competitionsuite.com/a782f8dc-0465-4209-b86e-bf1d9cdaa63f.htm', 'https://recaps.competitionsuite.com/4fd45950-384f-4374-8def-794adc1e7e68.htm', 'https://recaps.competitionsuite.com/f3cf62bf-13c4-4882-9183-d7244feb8baf.htm', 'https://recaps.competitionsuite.com/5fc05728-5cb6-4860-96c6-5cb40851d2a8.htm', 'https://recaps.competitionsuite.com/7872d8f9-eb81-464e-8e02-8eb787a8012c.htm', 'https://recaps.competitionsuite.com/09f386f8-7930-405c-baf6-0f514da0848a.htm', 'https://recaps.competitionsuite.com/9f2e6491-ce55-4933-a0d0-5be8744c1119.htm', 'https://recaps.competitionsuite.com/dbc8f2fa-5016-4817-94f8-c0937e83bb0a.htm', 'https://recaps.competitionsuite.com/35ed987e-53c5-4842-a6e3-4a22e50b8676.htm', 'https://recaps.competitionsuite.com/f5124063-fa3a-4c58-80b0-41685774e4de.htm', 'https://recaps.competitionsuite.com/6b1f9e7e-9556-4741-a8df-29ad3fd970ea.htm', 'https://recaps.competitionsuite.com/25852766-eaa2-4e66-b204-8a75249f5697.htm', 'https://recaps.competitionsuite.com/815a5bc6-59dd-479f-b1a8-6e0ad288100d.htm', 'https://recaps.competitionsuite.com/bf328c58-4ed1-4737-8b97-888b5faa33bd.htm', 'https://recaps.competitionsuite.com/bac76732-1351-4e15-b2a7-762a1752a6be.htm', 'https://recaps.competitionsuite.com/20877e4f-bcca-4741-9c70-b31a1e3d3180.htm', 'https://recaps.competitionsuite.com/be2cbdad-2adc-4302-b501-f9464c8c32c6.htm', 'https://recaps.competitionsuite.com/551fc5e8-6045-4058-96bc-d46b1a314076.htm', 'https://recaps.competitionsuite.com/71c7367d-e912-43e6-b9ca-969833f0ddea.htm', 'https://recaps.competitionsuite.com/b22562d4-b4f9-4ab2-bf28-5f9009d701f1.htm', 'https://recaps.competitionsuite.com/e696413d-be37-4cd7-a146-c11b0f3121f7.htm', 'https://recaps.competitionsuite.com/13f9024e-3b20-4f57-8b89-aaea84f11f18.htm', 'https://recaps.competitionsuite.com/09fac2fb-4238-4ae0-9d8b-66bc7266f155.htm', 'https://recaps.competitionsuite.com/3b5a6d67-a74c-4da8-b946-31ff2c4a1470.htm', 'https://recaps.competitionsuite.com/5609aebb-b479-487d-9351-a21ee649c542.htm', 'https://recaps.competitionsuite.com/fa21c263-9d6a-4c3d-b45f-8928b0234dfb.htm', 'https://recaps.competitionsuite.com/fff413ac-f51e-4b04-a0e5-a636e2db92e9.htm', 'https://recaps.competitionsuite.com/1487fe84-490a-4404-9ccb-207969c713dc.htm', 'https://recaps.competitionsuite.com/7db895b7-0f1e-4104-8555-5d6191f8697e.htm', 'https://recaps.competitionsuite.com/0fe21763-7abd-4b3d-a7bf-a87ff9da67b1.htm', 'https://recaps.competitionsuite.com/7877e199-5979-421a-8db9-0dae80283de1.htm']
urls2021= ['https://recaps.competitionsuite.com/f5857673-6380-422b-8471-cea7cd2e5b55.htm', 'https://recaps.competitionsuite.com/7ad58ffb-db14-4c6a-991b-b04210613c02.htm', 'https://recaps.competitionsuite.com/31f07290-b6c8-4df0-82c3-875e2186b3fc.htm', 'https://recaps.competitionsuite.com/c7df6848-d9d9-4d69-aece-36c93b6c5003.htm', 'https://recaps.competitionsuite.com/b1ff8463-0f06-456e-830b-686de4093a3c.htm', 'https://recaps.competitionsuite.com/48ca6831-859f-4f39-8f40-ac4d847e0aa0.htm', 'https://recaps.competitionsuite.com/c121ee96-6dd5-4342-9599-5bff22a23b46.htm', 'https://recaps.competitionsuite.com/845557ce-dc84-4a25-b4b8-95793abca6e9.htm', 'https://recaps.competitionsuite.com/9f546ff0-89cb-4dfa-9799-565314c629d1.htm', 'https://recaps.competitionsuite.com/c2e6b7a1-c56d-4839-b3e6-02e568d2cc96.htm', 'https://recaps.competitionsuite.com/35ddfcbc-e84d-4b41-a704-dee2a275d596.htm', 'https://recaps.competitionsuite.com/8aa4d197-f8e0-4daf-8390-fe793f2d5d1c.htm', 'https://recaps.competitionsuite.com/72edbad5-6fbc-472c-b377-2d1d8b9e6538.htm', 'https://recaps.competitionsuite.com/d5e19e63-c68c-4002-a7a8-9f971fae0c66.htm', 'https://recaps.competitionsuite.com/625e8afb-99cb-49cb-bebe-f207b20f9e4a.htm', 'https://recaps.competitionsuite.com/891938a1-0456-4e2c-9136-52a859ca9570.htm', 'https://recaps.competitionsuite.com/68aede15-fa6b-4937-a555-cd3f9f63f38b.htm', 'https://recaps.competitionsuite.com/d8e2ea0a-fa48-4f57-b7c3-b29d52b09840.htm', 'https://recaps.competitionsuite.com/836d8bf2-956b-4ad5-a41c-da184cfca6ef.htm', 'https://recaps.competitionsuite.com/42651f85-779a-4290-9130-c49775af163d.htm', 'https://recaps.competitionsuite.com/66e2e967-37cf-49cc-aacb-4138b82d1f44.htm', 'https://recaps.competitionsuite.com/e75b2f44-5162-40e5-9856-c71e641b17dd.htm', 'https://recaps.competitionsuite.com/d5221904-a3aa-4aab-83b5-1b9360c55805.htm', 'https://recaps.competitionsuite.com/a1581e9a-cafb-4fbe-aa8f-6f64d5c951f1.htm', 'https://recaps.competitionsuite.com/f795951c-760b-4e8e-8c92-98ebd4edb092.htm', 'https://recaps.competitionsuite.com/05868879-8b45-4ef6-be25-5ca5536a71d3.htm', 'https://recaps.competitionsuite.com/0c994b24-eba8-4b62-9145-30438c6b07bc.htm', 'https://recaps.competitionsuite.com/b50e85fd-8b08-4666-893f-c6985e9fe54c.htm', 'https://recaps.competitionsuite.com/abb8978d-4b0a-41fd-99f1-906e4602d063.htm', 'https://recaps.competitionsuite.com/e13fb282-59fd-4871-a67f-87d825538de4.htm']
urls2022 = ['https://recaps.competitionsuite.com/2bf4c34f-4eae-4ac1-9a0c-b29ff8c429d6.htm', 'https://recaps.competitionsuite.com/2cda9f44-30fd-4bf7-b68a-d4dcf88155e0.htm', 'https://recaps.competitionsuite.com/d3749b61-3f2e-47f9-82d4-e3be345ee388.htm', 'https://recaps.competitionsuite.com/4dfb6cec-1345-43e5-b243-870af94fe9c5.htm', 'https://recaps.competitionsuite.com/986cdf29-2112-49d7-9696-032b5960e5a4.htm', 'https://recaps.competitionsuite.com/98793bbc-b569-4fd5-ab0d-0aa0142c4aa9.htm', 'https://recaps.competitionsuite.com/b97ff93d-8885-4ad5-b272-33bac8e0c1f1.htm', 'https://recaps.competitionsuite.com/e52a7e9d-ef14-4d4e-999c-af021d8b4840.htm', 'https://recaps.competitionsuite.com/8777d3b4-9bee-4bb4-9b88-57bfc573c793.htm', 'https://recaps.competitionsuite.com/714f33e9-12e8-447f-bb3f-b5eb9044ff55.htm', 'https://recaps.competitionsuite.com/0e5ea311-8137-4ad7-8046-8a88e0edb191.htm', 'https://recaps.competitionsuite.com/f80efb8e-0b7c-48be-abc4-8a0b2e7b8565.htm', 'https://recaps.competitionsuite.com/8a6dcd63-a11c-44b7-be6e-e895fd2e4304.htm', 'https://recaps.competitionsuite.com/9bf24f5c-b692-4a01-a54a-21db55bc6278.htm', 'https://recaps.competitionsuite.com/45b4cf01-555d-475a-a466-49a06ea8aff1.htm', 'https://recaps.competitionsuite.com/f17b07b9-1b2d-42e4-b036-6368dcb2c894.htm', 'https://recaps.competitionsuite.com/247c1360-86be-4604-b3e6-62d4a9335bf8.htm', 'https://recaps.competitionsuite.com/3f674eb1-2bce-45d8-8975-33a994648e6d.htm', 'https://recaps.competitionsuite.com/bbb56d9a-4334-43d4-a9a1-665b162f6585.htm', 'https://recaps.competitionsuite.com/f058b506-6091-462d-892b-95283bcd2bc4.htm', 'https://recaps.competitionsuite.com/b04bca39-9640-4468-b328-f64036c8d20f.htm', 'https://recaps.competitionsuite.com/faf83bac-e8ef-4204-845a-d4b3236e5205.htm', 'https://recaps.competitionsuite.com/759fa5b2-71de-4d5d-b84c-8cc8a13598a4.htm', 'https://recaps.competitionsuite.com/433fbf09-e697-4149-a7fc-221234c9477a.htm', 'https://recaps.competitionsuite.com/16603d93-bf22-47a8-8d7b-53404785419d.htm', 'https://recaps.competitionsuite.com/5c29ba54-6040-47d2-a3a8-c0a6689c0fa5.htm', 'https://recaps.competitionsuite.com/409e1a97-73b7-4b8c-ab08-f785d4fa5032.htm', 'https://recaps.competitionsuite.com/cdd37fd8-f4d9-4826-b80e-b20118fdabf9.htm', 'https://recaps.competitionsuite.com/810b0731-895c-4631-ae12-7c20306a1487.htm']


# for url in urls2023:
#      doEverything(url)

def parseScoresAndRanks(numArray):
    listNums = numArray.strip("[]").replace("'", "").split()
    return listNums




def explodecolumn(df, columnName):
    if columnName == "scores":
       #problem line scorelabels = ['MPES', 'MPIS', 'MPSTS', 'VPES', 'VPIS', 'VPSTS', 'PTS', 'GEMCES', 'GEMPES', 'GEMSTS', 'GEVCES', 'GEVPES', 'GEVSTS', 'GETS', 'PCS', 'PAS', 'PTS', 'PSTS', 'GCS', 'GAS', 'GTS', 'GSTS', 'STS', 'T/P', 'TotalScore']
        scorelabels = ['MPES', 'MPIS', 'MPSTS', 'VPES', 'VPIS', 'VPSTS', 'PerfTS', 'GEMCES', 'GEMPES', 'GEMSTS', 'GEVCES', 'GEVPES', 'GEVSTS', 'GETS', 'PCS', 'PAS', 'PTS', 'PSTS', 'GCS', 'GAS', 'GTS', 'GSTS', 'STS', 'T/P', 'TotalScore']
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
            result_df.to_csv("csbcData2023.csv", index=False)
    elif columnName == "ranks":
        ranklabels = ['MPER', 'MPIR', 'MPSTR', 'VPER', 'VPIR', 'VPSTR', 'PerfTR', 'GEMCER', 'GEMPER', 'GEMSTR', 'GEVCER', 'GEVPER', 'GEVSTR', 'GETR', 'PCR', 'PAR', 'PTR', 'PSTR', 'GCR', 'GAR', 'GTR', 'GSTR', 'STR', 'TotalRank']

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
            result_df.to_csv("csbcData2023.csv", index=False)
            
    
def fixDivisionError(dataframe):
    finals_dataframe = dataframe[dataframe['division'].str.contains('Finals')]

    for school in finals_dataframe['school'].unique():
        finals_indices = finals_dataframe[finals_dataframe['school'] == school].index
        non_finals_row = dataframe[(dataframe['school'] == school) & ~dataframe['division'].str.contains('Finals')]


        non_finals_division = non_finals_row.iloc[0]['division']
        dataframe.loc[finals_indices, 'division'] = non_finals_division
    dataframe.to_csv("csbcData2023.csv", index=False)


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



