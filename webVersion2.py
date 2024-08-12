import streamlit as st
import dataviz
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="CSBC Stats",
    page_icon="🎺",
    layout = "wide"

)

def main():
    st.title("CSBC Stats")
    
    year = st.selectbox("Select the year", ["2019", "2021", "2022", "2023"])
    
    dfUsed = pd.read_csv(f"csbcData{year}.csv")
    
    school_selected = st.selectbox("Select the school", pd.unique(dfUsed['school']))
    
    tab1, tab2, tab3 = st.tabs(["📈 Line Chart", "🗃 Bar Graph", "Averages"])
    
    with tab1:
        st.subheader(f"{school_selected} Compared to Closest Competitors, {year}")
        dataviz.lineGraph(school_selected, dfUsed)
        competitors = dataviz.findCompetitors(school_selected, dfUsed)
        st.markdown(f"#### __{school_selected}'s__ closest competitors are: {', '.join(competitors)}")

    with tab2:
        st.subheader(f"{school_selected} Averages Compared to Division Averages, {year}")
        dataviz.compareAvgSchoolScoresToAvgDivisionScores(school_selected, dfUsed)
    with tab3:
        st.subheader(f"Metrics for {school_selected}, {year}")
        cols = dfUsed.select_dtypes(include=np.number).drop(["dayOfMonth", "season"], axis=1).columns.tolist()
        cat = st.selectbox("Select category", cols)
        idxCol = cols.index(cat)
        yearAvgValue = dataviz.getAvgs(school_selected, dfUsed)[idxCol]
        _delta_ = getMetricDelta(year, school_selected, dfUsed, idxCol, yearAvgValue)

        st.metric(cat, yearAvgValue, delta= _delta_)

def findDataFrameOneYearBehind(year):
    if year != "2021" and year != "2019":
        lastYear = str(int(year)-1)
    else:
        lastYear = "2019"
    lastYearDF=  pd.read_csv(f"csbcData{lastYear}.csv")
    return lastYearDF
def getMetricDelta(yr, school, df, idxCol, yearAvgValue):
    lastYear = findDataFrameOneYearBehind(yr)
    lastYearAvgValue = dataviz.getAvgs(school, lastYear)[idxCol]

    return yearAvgValue-lastYearAvgValue

if __name__ == "__main__":
    main()


