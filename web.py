import streamlit as st
import dataviz
import pandas as pd

st.set_page_config(
    page_title="CSBC Stats",
    page_icon="🎺",

)

def main():
    st.title("CSBC Stats")
    
    year = st.selectbox("Select the year", ["2019", "2021", "2022"])
    
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


if __name__ == "__main__":
    main()


