import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Completion Trends", layout="wide")
st.title("1. District School Completion Trends (2021–2025)")

@st.cache_data
def load_completion_data():
    df = pd.read_csv("completion_school_district_cleaned_final.csv")
    return df[df["area_level"] == "District"]

df_district = load_completion_data()

selected_state = st.selectbox(
    "Pilih Negeri (State):",
    options=sorted(df_district["state"].dropna().unique())
)

filtered_df = df_district[df_district["state"] == selected_state]
trend_df = filtered_df.groupby(["year", "stage"], as_index=False)["completion"].mean()

fig = px.line(
    trend_df,
    x="year",
    y="completion",
    color="stage",
    markers=True,
    labels={"year": "Tahun", "completion": "Kadar Penyiapan (%)", "stage": "Peringkat"},
    title=f"Purata Kadar Penyiapan Sekolah Mengikut Peringkat di {selected_state}"
)
fig.update_xaxes(dtick=1)
st.plotly_chart(fig, use_container_width=True)
