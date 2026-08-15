# CSBCDATA

**Competition analytics for California State Band Championships (CSBC) marching band and color guard programs.**

CSBCDATA scrapes, cleans, and analyzes scoring data from the California State Band Championships circuit, turning raw tournament results into season summaries, progress charts, competitor analysis, and category-level strengths and weaknesses. Built during my sophomore summer of high school -- Summer 2023 -- this project represents my first foray into data analysis / visualization. Let it be known: codebase is **profoundly** chopped. Beyond belief. But I like to keep it up as a reminder of where I started out. Maybe someday I'll get around to cleaning it up.


## why this exists

Marching band and color guard programs generate a surprising amount of data every season — scores and ranks across a dozen judged categories, competitor lineups, tournament sites, week-over-week progress. But it lives scattered across a scoring website, in a format built for reading one sheet at a time, not for seeing a season as a whole.

CSBCDATA started as a personal tool to answer questions my program couldn't easily answer. Eventually, it grew into a web application other CSBC directors could use. Our performances generate the data, the data informs the next rehearsal, and the next performance generates better data.

## what it does

- **Season summaries** — five-number statistical summaries of a school's scores across the season
- **Progress tracking** — line charts of total score over time, plotted against a school's closest competitors
- **Competitor analysis** — automatically identifies a school's five closest competitors based on similarity across scores and ranks, weighted toward same-division rivals
- **Category comparison** — bar charts comparing a school's average scores against its division average, category by category
- **Head-to-head comparison** — side-by-side average-score comparison between any two schools
- **Percentile ranking** — where a school sits within its division on each judged category
- **Distribution views** — violin plots showing how scores are distributed across divisions

All of it maps to the CSBC judging rubric: music performance (ensemble / individual), visual performance, general effect (music and visual), percussion, color guard, and timing/penalties.


## tech stack

- **Python**
- **Streamlit** — interactive web app front end
- **pandas** / **NumPy** — data wrangling and numeric work
- **SciPy** — percentile and statistical calculations
- **Matplotlib** / **Seaborn** — charts and plots
- A custom web scraper that dynamically loads the CSBC score site and pulls results to local storage


## how it works

**Scraping → cleaning → analysis** is the pipeline.

1. **Scrape.** A scraper dynamically loads the CSBC scores site and pulls tournament results to disk.
2. **Clean & structure.** Raw score sheets are parsed into a tidy table: one row per school per competition, with columns for each judged sub-category, plus metadata (division, competition, date, season).
3. **Analyze & visualize.** The Streamlit app loads that table and exposes the analysis functions above through an interactive interface.

A couple of the more interesting pieces:

- **Closest-competitor detection** measures similarity between schools in score-and-rank feature space (Euclidean distance, inverted into a similarity score), then applies a bonus weight to schools in the same division so that division rivals surface first.
- **Percentile ranking** computes each school's season-average per category, then scores it against the distribution of all schools in its division.


## getting started (at your own peril)

```bash
# 1. Clone the repo
git clone https://github.com/LaurenMaiH/csbcData.git
cd csbcData

# 2. (Recommended) create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run webVersion1.py
```

If you don't have a `requirements.txt` yet, this covers the imports:

```
streamlit
pandas
numpy
scipy
matplotlib
seaborn
```


## data notes

CSBCDATA works with publicly posted competition results (school names and judged scores). No private or personally identifying information is involved.


## status & roadmap

This project began as a self-taught high school build. It's here as a bit of a fossil, really.

Things I'd improve given time:

- Replace hardcoded school/column references with configuration and named lookups
- Normalize/standardize features before the competitor-similarity calculation so high-magnitude categories don't dominate
- Add tests around the data-parsing and column-mapping logic
- Docstrings and type hints throughout
