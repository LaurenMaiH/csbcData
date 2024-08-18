import streamlit as st
import dataviz
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="CSBC DATA",
    page_icon="🎺",
    layout = "wide"

)

uiCols = ['MusicPerf Ens Score', 'MusicPerf Ind Score', 'MusicPerf SubTotal Score', 'VisualPerf Ens Score', 'VisualPerf Ind Score', 'VisualPerf Subtotal Score', 'Performance Total Score', 'GE Music CE Score', 'GE Music PE Score', 'GE Music Subtotal Score', 'GE Visual CE Score', 'GE Visual PE Score', 'GE Visual Subtotal Score', 'GE Total Score', 'Perc Cont Score', 'Perc Ach Score', 'PercTotal Score', 'Perc ScaledTotal Score', 'Guard Cont Score', 'Guard Ach Score', 'Guard Total Score', 'Guard ScaledTotal Score', 'Sub Total Score', 'Timing/Penalties', 'Total Score', 'MusicPerf Ens Rank', 'MusicPerf Ind Rank', 'MusicPerf SubTotal Rank', 'VisualPerf Ens Rank', 'VisualPerf Ind Rank', 'VisualPerf Subtotal Rank', 'Performance Total Rank', 'GE Music CE Rank', 'GE Music PE Rank', 'GE Music Subtotal Rank', 'GE Visual CE Rank', 'GE Visual PE Rank', 'GE Visual Subtotal Rank', 'GE Total Rank', 'Perc Cont Rank', 'Perc Ach Rank', 'PercTotal Rank', 'Perc ScaledTotal Rank', 'Guard Cont Rank', 'Guard Ach Rank', 'Guard Total Rank', 'Guard ScaledTotal Rank', 'Sub Total Rank', 'Total Rank']

def main():
    st.title("CSBC DATA")
    
    year = st.selectbox("Select year", ["2021", "2022", "2023"])
    
    dfUsed = pd.read_csv(f"csbcData{year}.csv")
    
    school_selected = st.selectbox("Select school", pd.unique(dfUsed['school']))
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Line Chart", "📊 Bar Chart", "📅 Year-to-Year Averages", "📋 Season Stat Summary", "⭐ Custom Data"])
    
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
        uiCat = st.selectbox("Select category", uiCols)
        uiCatIdx = uiCols.index(uiCat)
        cat = cols[uiCatIdx]
        idxCol = cols.index(cat)
   
        yearAvgValue = dataviz.getAvgs(school_selected, dfUsed).iloc[idxCol]
        _delta_ = getMetricDelta(year, school_selected, dfUsed, idxCol, yearAvgValue)
        st.metric(cat, yearAvgValue, delta= _delta_)

        st.write("*note that 2021 is the earliest year that CSBC Stats has recorded, so the change in average score from 2019 is not calculated and defaults to zero.")
    with tab4:
        st.subheader(f"{year} CSBC Season Stat Summary")
        filtered = dfUsed[dfUsed["school"] == "Scripps Ranch High School"]
        keep = filtered.columns[:32]
        filtered = filtered[keep].select_dtypes(include='number').drop(columns = ['MPSTS','VPSTS','GEMSTS','GEVSTS','GETS','PSTS','GSTS','T/P', 'dayOfMonth', 'season'])
        numeric_values = filtered.values.flatten()

        mean_val = round(numeric_values.mean(), 2)
        median_val = pd.Series(numeric_values).median()
        std = round(pd.Series(numeric_values).std(), 2)
        st.metric("Mean Score", mean_val) #0 is placeholder value
        st.metric("Median Score", median_val)
        st.metric("Standard Deviation", std)

        st.write("These metrics are calculated with all of a school's scores in every relevant numeric category for every competition it participated in for the duration of the season. Subtotals, scaled totals, and timing/penalties are excluded because they are not scored in the same range.")
    with tab5:
        st.title("Want More?")
        st.header("Unlock Insights With Customized CSBC Stats Reports")

        st.write("""
        The free stats on CSBC Stats provide a broad overview, but every director has unique data needs. Custom data reports, on the other hand, are made to provide tailored insights that can address your specific questions and goals. For just $35, you can receive a comprehensive report that includes five fully customizable sections.        """)

        st.subheader("🛠️ What's Possible With Custom Sections?")
        st.write("""
                 \n
                  \n
Pretty much anything you can think of! Some examples of custom work I’ve done before:
- **School-to-School Comparison**: Compare the averages of two schools side-by-side in a bar graph. Similar to the 📊 **Bar Chart** tab, but focused on school-to-school average comparisons instead of school-to-division. This visual tool is an excellent way to see how you measure up against your competitors.

- **Scoreboard**: Stay updated on your standings in any category. View the complete leaderboard for any category at any point during the season.

- **Tailored Competitor Analysis Algorithm**: Identify the schools to focus on using a custom algorithm designed to pinpoint your primary competitors (those you frequently compete against), strongest competitors (those dominating the division), and similar competitors (schools that score similarly to yours and are your main rivals).
        
And much more, tailored to your specific questions and needs.
                 """)

        st.subheader("🔍 How it Works:")
        st.write("""
                 \n
                  \n
1. **Initial Contact**: Reach out to me via email or form.
2. **Consultation**: Iron out and define your specific needs and goals for the custom data report. 
3. **Report Generation**: I get to work generating your custom report. Timeframe may vary, as the scope and complexity of the request varies from report to report. 
4. **Delivery**: I send the completed report directly to you. 
        """)

        st.subheader("💵 Pricing")
        st.write("""
                 \n
                  \n
        **Base Report (5 Sections)**: \$35 
                \n
        **Additional Sections**: $10         

        """)


        st.subheader("🚀 Get Started")
        st.write("""
       Ready to transform your CSBC Stats into actionable insights? Contact me at laurenhenderson265@gmail.com and let’s talk.
        """)




    st.write("\n")
    st.divider()
    st.write("CSBC Stats is constantly improving! Please report any issues [here](https://forms.gle/jySUDsGwNeoS3DZJ7).")
    st.write("☕ Made and maintained by Lauren Henderson. If you found this site useful, please consider supporting me wtih [a delicious coffee](https://ko-fi.com/laurenhenderson265).")
    st.write("⭐ If you're interested in obtaining my data, or a personalized, custom data report, visit the Custom Data tab. Thanks for your time!")
def findDataFrameOneYearBehind(year):
    if year != "2021":
        lastYear = str(int(year)-1)
    else:
        lastYear = "2021"
    lastYearDF=  pd.read_csv(f"csbcData{lastYear}.csv")
    return lastYearDF
def getMetricDelta(yr, school, df, idxCol, yearAvgValue):
    lastYear = findDataFrameOneYearBehind(yr)
    lastYearAvgValue = dataviz.getAvgs(school, lastYear).iloc[idxCol]

    return yearAvgValue-lastYearAvgValue

if __name__ == "__main__":
    main()


