import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Psychometric Analysis", layout="wide")

# 1. Main Title & Divider
st.title("Psychometric & Academic Performance Analysis 🧠")
st.divider()

# Load & Cache Dataset
@st.cache_data
def load_pilot_data():
    return pd.read_excel("pilot_questionnaire_cleaned.xlsx", sheet_name="Cleaned_Data")

df_pilot = load_pilot_data()

# Interactive Sidebar Filters
st.sidebar.header("Interactive Filters (Objective 3)")
min_mark, max_mark = int(df_pilot["TEST MARK"].min()), int(df_pilot["TEST MARK"].max())
selected_marks = st.sidebar.slider("Test Mark Range (TEST MARK):", min_mark, max_mark, (min_mark, max_mark))

corr_method = st.sidebar.selectbox("Correlation Method:", ["pearson", "spearman"])
x_variable = st.sidebar.selectbox("Psychometric Variable (X-Axis):", ["Positive view", "Mindset"])

# Filter Dataset
filtered_df = df_pilot[df_pilot["TEST MARK"].between(selected_marks[0], selected_marks[1])]

# 2. Dynamic KPI Metric Cards
col1, col2, col3, col4 = st.columns(4)
n_students = len(filtered_df)
mean_mark = filtered_df["TEST MARK"].mean() if n_students > 0 else 0
mean_pos = filtered_df["Positive view"].mean() if n_students > 0 else 0
corr_val = filtered_df["TEST MARK"].corr(filtered_df[x_variable], method=corr_method) if n_students > 1 else 0

col1.metric("Respondents (N)", f"{n_students}", border=True, help="Number of student respondents within the selected test mark range")
col2.metric("Mean Test Mark", f"{mean_mark:.1f}", border=True, help="Mean academic test score (scale 0–100)")
col3.metric("Mean Positive View", f"{mean_pos:.2f}", border=True, help="Mean positive self-efficacy score (scale 1–5)")
col4.metric(f"Correlation ({x_variable})", f"{corr_val:.3f}", border=True, help=f"{corr_method.capitalize()} correlation coefficient with TEST MARK")

# 3. Section Header & Status Banner
st.header("Psychometric Correlation Overview")
st.success("Data loaded successfully!")

if len(filtered_df) < 2:
    st.warning("Please widen the test mark range so that at least 2 respondents are included to compute correlations.")
else:
    # 4. Raw Data Preview
    st.subheader("Raw Data Preview")
    preview_cols = ["Respondent_ID", "TEST MARK", "Positive view", "Mindset", "Q1", "Q2", "Q3"]
    st.dataframe(filtered_df[preview_cols].head(5), use_container_width=True)

    # 5. Interactive Visualizations (Correlation Heatmap & Scatter Plot)
    st.subheader("Correlation Matrix & Psychometric Relationship")
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        cols = ["TEST MARK", "Positive view", "Mindset"]
        corr_matrix = filtered_df[cols].corr(method=corr_method)
        fig_heatmap = px.imshow(
            corr_matrix,
            text_auto=".3f",
            color_continuous_scale="RdBu_r",
            zmin=-1,
            zmax=1,
            title=f"{corr_method.capitalize()} Correlation Heatmap"
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)

    with chart_col2:
        fig_scatter = px.scatter(
            filtered_df,
            x=x_variable,
            y="TEST MARK",
            hover_data=["Respondent_ID", "Mindset", "Positive view"],
            color="TEST MARK",
            color_continuous_scale="Viridis",
            labels={x_variable: f"{x_variable} Score", "TEST MARK": "Academic Test Mark (TEST MARK)"},
            title=f"Relationship Between {x_variable} and Academic Test Mark"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
