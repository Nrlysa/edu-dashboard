import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="School Density", layout="wide")
st.title("2. Institutional Density & Sector Reliance")

df_schools = pd.read_excel("dataset_schools_cleaned (1).xlsx")

selected_area = st.multiselect(
    "Filter by Area:",
    options=sorted(df_schools["Area"].dropna().unique()),
    default=sorted(df_schools["Area"].dropna().unique())[:5]
)

filtered_schools = df_schools[df_schools["Area"].isin(selected_area)]
grouped = filtered_schools.groupby(["Level", "Status"]).size().reset_index(name="School Count")

fig = px.bar(
    grouped,
    x="Level",
    y="School Count",
    color="Status",
    barmode="group",
    title="Public vs. Private School Distribution by Education Level"
)
st.plotly_chart(fig, use_container_width=True)
