import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="School Density", layout="wide")

# 1. Main Title & Divider
st.title("School Infrastructure & Sector Density 🏫")
st.divider()

# Load & Cache Dataset
@st.cache_data
def load_schools_data():
    return pd.read_excel("dataset_schools_cleaned (1).xlsx")

df_schools = load_schools_data()

# Interactive Sidebar Filters
st.sidebar.header("Interactive Filters (Objective 2)")
all_areas = sorted(df_schools["Area"].dropna().unique().tolist())
select_all_areas = st.sidebar.checkbox("Select All Areas", value=True)

if select_all_areas:
    selected_areas = all_areas
else:
    selected_areas = st.sidebar.multiselect("Select Areas:", options=all_areas, default=all_areas[:5])

all_levels = sorted(df_schools["Level"].dropna().unique().tolist())
selected_levels = st.sidebar.multiselect("Select School Levels:", options=all_levels, default=all_levels)

all_status = sorted(df_schools["Status"].dropna().unique().tolist())
selected_status = st.sidebar.multiselect("Select School Sector (Status):", options=all_status, default=all_status)

# Filter Dataset
filtered_df = df_schools[
    (df_schools["Area"].isin(selected_areas)) &
    (df_schools["Level"].isin(selected_levels)) &
    (df_schools["Status"].isin(selected_status))
]

# 2. Dynamic KPI Metric Cards
col1, col2, col3, col4 = st.columns(4)
total_schools = len(filtered_df)
public_count = len(filtered_df[filtered_df["Status"] == "Public"])
private_count = len(filtered_df[filtered_df["Status"] == "Private"])
private_share = (private_count / total_schools * 100) if total_schools > 0 else 0

col1.metric("Total Schools", f"{total_schools:,}", border=True, help="Total number of school institutions matching the current filters")
col2.metric("Public Schools", f"{public_count:,}", border=True, help="Total number of Public sector schools")
col3.metric("Private Schools", f"{private_count:,}", border=True, help="Total number of Private sector schools")
col4.metric("Private Reliance", f"{private_share:.1f}%", border=True, help="Percentage share of Private sector institutions")

# 3. Section Header & Status Banner
st.header("Institutional Distribution Overview")
st.success("Data loaded successfully!")

if filtered_df.empty:
    st.warning("No data available for the selected filters. Please select at least one area, level, and status.")
else:
    # 4. Raw Data Preview
    st.subheader("Raw Data Preview")
    st.dataframe(filtered_df.head(10), use_container_width=True)

    # 5. Interactive Visualization
    st.subheader("Public vs. Private School Distribution by Education Level")
    grouped_df = filtered_df.groupby(["Level", "Status"], as_index=False).size().rename(columns={"size": "School Count"})

    fig = px.bar(
        grouped_df,
        x="Level",
        y="School Count",
        color="Status",
        barmode="group",
        text_auto=True,
        color_discrete_map={"Public": "#3b82f6", "Private": "#8b5cf6"},
        labels={"Level": "Education Level", "School Count": "Number of Schools", "Status": "Sector"},
        title="Public vs. Private School Distribution by Education Level"
    )
    st.plotly_chart(fig, use_container_width=True)
