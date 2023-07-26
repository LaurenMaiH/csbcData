# To save all my old functions in case i need to come back to them
comp = True
def getHTML():
    pass

def GROSSMONT():
    if comp:
            num_scores_per_school = 22
            schoolScores = [contentScores[i:i+num_scores_per_school] for i in range(0, len(contentScores), num_scores_per_school)]
            schoolRanks = [contentRanks[i:i+num_scores_per_school] for i in range(0, len(contentRanks), num_scores_per_school)]
            modifiedSchoolScores = []
            modifiedSchoolRanks = []

            for scores in schoolScores:
                scores.insert(21, 0)
                modifiedSchoolScores.append(scores)

            for ranks in schoolRanks:
                ranks.insert(21, '')
                modifiedSchoolRanks.append(ranks)

            return modifiedSchoolScores, modifiedSchoolRanks, headers, locations, comp, month, day, szn, locationsAreListed
















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