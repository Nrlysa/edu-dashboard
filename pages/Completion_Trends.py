import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Completion Trends", layout="wide")
st.title("1. District School Completion Trends")

df_comp = pd.read_csv("completion_school_district_cleaned_final.csv")
df_district = df_comp[df_comp["area_level"] == "District"]

selected_state = st.selectbox("Select State:", sorted(df_district["state"].unique()))
filtered_df = df_district[df_district["state"] == selected_state]

trend_df = filtered_df.groupby(["year", "stage"])["completion"].mean().reset_index()

fig = px.line(
    trend_df,
    x="year",
    y="completion",
    color="stage",
    markers=True,
    title=f"Average Completion Rate by Stage in {selected_state}"
)
fig.update_xaxes(dtick=1)
st.plotly_chart(fig, use_container_width=True)
