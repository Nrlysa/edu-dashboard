import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="School Density", layout="wide")
st.title("2. Institutional Density & Public vs. Private Reliance")

@st.cache_data
def load_schools_data():
    return pd.read_excel("dataset_schools_cleaned (1).xlsx")

df_schools = load_schools_data()
all_areas = sorted(df_schools["Area"].dropna().unique())

selected_areas = st.multiselect(
    "Tapis Mengikut Kawasan (Area):",
    options=all_areas,
    default=all_areas[:5]
)

filtered_schools = df_schools[df_schools["Area"].isin(selected_areas)]
grouped = filtered_schools.groupby(["Level", "Status"]).size().reset_index(name="School Count")

fig = px.bar(
    grouped,
    x="Level",
    y="School Count",
    color="Status",
    barmode="group",
    labels={"Level": "School Level", "School Count": "Number of Schools", "Status": "Sector"},
    title="Distribution of Public vs. Private Schools by Level of Education"
)
st.plotly_chart(fig, use_container_width=True)
