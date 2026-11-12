import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Completion Trends", layout="wide")

# 1. Main Title & Divider
st.title("District School Completion Trends 📈")
st.divider()

# Load & Cache Dataset
@st.cache_data
def load_completion_data():
    df = pd.read_csv("completion_school_district_cleaned_final.csv")
    df = df[df["area_level"] == "District"].copy()
    stage_labels = {
        "primary": "Primary School",
        "secondary_lower": "Secondary Lower",
        "secondary_upper": "Secondary Upper"
    }
    df["Stage_Label"] = df["stage"].map(stage_labels).fillna(df["stage"])
    return df

df_comp = load_completion_data()

# Interactive Sidebar Filters
st.sidebar.header("Interactive Filters (Objective 1)")
state_list = ["All States"] + sorted(df_comp["state"].dropna().unique().tolist())
selected_state = st.sidebar.selectbox("Select State:", state_list)

if selected_state != "All States":
    df_state = df_comp[df_comp["state"] == selected_state]
else:
    df_state = df_comp

district_list = sorted(df_state["district"].dropna().unique().tolist())
selected_districts = st.sidebar.multiselect(
    "Select Districts:",
    options=district_list,
    default=district_list
)

stage_list = sorted(df_comp["Stage_Label"].dropna().unique().tolist())
selected_stages = st.sidebar.multiselect(
    "Select Education Stages:",
    options=stage_list,
    default=stage_list
)

min_yr, max_yr = int(df_comp["year"].min()), int(df_comp["year"].max())
selected_years = st.sidebar.slider("Select Year Range:", min_yr, max_yr, (min_yr, max_yr))

# Filter Dataset
filtered_df = df_state[
    (df_state["district"].isin(selected_districts)) &
    (df_state["Stage_Label"].isin(selected_stages)) &
    (df_state["year"].between(selected_years[0], selected_years[1]))
]

# 2. Dynamic KPI Metric Cards
col1, col2, col3, col4 = st.columns(4)
overall_mean = filtered_df["completion"].mean() if not filtered_df.empty else 0
primary_mean = filtered_df[filtered_df["stage"] == "primary"]["completion"].mean() if not filtered_df.empty else 0
lower_mean = filtered_df[filtered_df["stage"] == "secondary_lower"]["completion"].mean() if not filtered_df.empty else 0
upper_mean = filtered_df[filtered_df["stage"] == "secondary_upper"]["completion"].mean() if not filtered_df.empty else 0

col1.metric("Overall Completion", f"{overall_mean:.1f}%", border=True, help="Overall mean school completion rate for the selected filters")
col2.metric("Primary Stage", f"{primary_mean:.1f}%", border=True, help="Mean completion rate at the Primary School stage")
col3.metric("Lower Secondary", f"{lower_mean:.1f}%", border=True, help="Mean completion rate at the Lower Secondary stage")
col4.metric("Upper Secondary", f"{upper_mean:.1f}%", border=True, help="Mean completion rate at the Upper Secondary stage")

# 3. Section Header & Status Banner
st.header("Completion Rate Overview")
st.success("Data loaded successfully!")

if filtered_df.empty:
    st.warning("No data available for the selected filters. Please select at least one district and education stage.")
else:
    # 4. Raw Data Preview
    st.subheader("Raw Data Preview")
    preview_cols = ["state", "district", "Stage_Label", "year", "completion", "quality_flag"]
    st.dataframe(filtered_df[preview_cols].head(5), use_container_width=True)

    # 5. Interactive Visualization
    st.subheader("School Completion Rate Trends by Stage")
    trend_df = filtered_df.groupby(["year", "Stage_Label"], as_index=False)["completion"].mean()

    fig = px.line(
        trend_df,
        x="year",
        y="completion",
        color="Stage_Label",
        markers=True,
        labels={"year": "Year", "completion": "Average Completion Rate (%)", "Stage_Label": "Education Stage"},
        title=f"School Completion Rate Trends ({selected_state}: {selected_years[0]}–{selected_years[1]})"
    )
    fig.update_xaxes(dtick=1)
    fig.update_traces(line=dict(width=3), marker=dict(size=8))
    st.plotly_chart(fig, use_container_width=True)
