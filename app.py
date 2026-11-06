import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & HEADER
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Educational Visualisation Dashboard",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Educational Analytics & Visualisation Dashboard")
st.markdown("""
This application addresses three primary educational objectives:
1. **District School Completion Trends** (Multi-Line Time-Series Chart)
2. **Spatial Density & Sector Reliance** (Grouped Bar Chart)
3. **Psychometric Correlations with Academic Performance** (Correlation Heatmap)
""")
st.divider()

# -----------------------------------------------------------------------------
# 2. DATA LOADING & CACHING
# -----------------------------------------------------------------------------
@st.cache_data
def load_datasets():
    # Dataset 1: School Completion Rates
    df_comp = pd.read_csv("completion_school_district_cleaned_final.csv")
    df_comp['date'] = pd.to_datetime(df_comp['date'])
    
    # Dataset 2: Institutional Infrastructure Demographics
    df_schools = pd.read_excel("dataset_schools_cleaned (1).xlsx", sheet_name="Sheet1")
    
    # Dataset 3: Psychometric Survey & Test Scores
    df_pilot = pd.read_excel("pilot_questionnaire_cleaned.xlsx", sheet_name="Cleaned_Data")
    
    return df_comp, df_schools, df_pilot

df_comp, df_schools, df_pilot = load_datasets()

# -----------------------------------------------------------------------------
# 3. OBJECTIVE 1: MULTI-LINE TIME-SERIES CHART
# -----------------------------------------------------------------------------
st.header("1. District School Completion Trends & Retention Drop-Offs")
st.markdown("""
**Objective:** Evaluate district-level school completion trends across Malaysia (2021–2025) 
and pinpoint retention drop-off points as students transition from primary to upper secondary education.
""")

col1, col2 = st.columns([1, 3])

with col1:
    selected_state = st.selectbox(
        "Select State:",
        options=sorted(df_comp['state'].unique()),
        index=0
    )
    
    available_districts = df_comp[
        (df_comp['state'] == selected_state) & 
        (df_comp['area_level'] == 'District')
    ]['district'].unique()
    
    selected_districts = st.multiselect(
        "Select Districts:",
        options=sorted(available_districts),
        default=sorted(available_districts)[:3] if len(available_districts) >= 3 else sorted(available_districts)
    )

with col2:
    if selected_districts:
        filtered_comp = df_comp[
            (df_comp['state'] == selected_state) &
            (df_comp['district'].isin(selected_districts)) &
            (df_comp['area_level'] == 'District')
        ]
        
        fig_line = px.line(
            filtered_comp,
            x="year",
            y="completion",
            color="district",
            line_dash="stage",
            markers=True,
            title=f"School Completion Trends across Stages in {selected_state} (2021–2025)",
            labels={
                "year": "Academic Year", 
                "completion": "Completion Rate (%)", 
                "stage": "Education Stage", 
                "district": "District"
            },
            range_y=[70, 105]
        )
        fig_line.update_layout(template="plotly_white", hovermode="x unified")
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.warning("Please select at least one district to display the multi-line chart.")

st.divider()

# -----------------------------------------------------------------------------
# 4. OBJECTIVE 2: GROUPED BAR CHART
# -----------------------------------------------------------------------------
st.header("2. Spatial Institutional Density & Public vs. Private Reliance")
st.markdown("""
**Objective:** Map the spatial density of educational institutions and evaluate public vs. private 
sector reliance across municipal areas and school levels.
""")

col_a, col_b = st.columns([1, 3])

with col_a:
    group_metric = st.radio("Group Institutional Density By:", ["School Level", "Top Municipal Areas"])
    
    if group_metric == "Top Municipal Areas":
        top_n = st.slider("Number of Top Municipal Areas:", min_value=3, max_value=10, value=5)

with col_b:
    if group_metric == "School Level":
        grouped_df = df_schools.groupby(['Level', 'Status']).size().reset_index(name='Count')
        fig_bar = px.bar(
            grouped_df,
            x='Level',
            y='Count',
            color='Status',
            barmode='group',
            title='Public vs. Private Sector Reliance across School Levels',
            labels={'Count': 'Number of Institutions', 'Level': 'School Level', 'Status': 'Sector Status'},
            color_discrete_map={'Public': '#1f77b4', 'Private': '#ff7f0e'},
            text_auto=True
        )
    else:
        top_areas = df_schools['Area'].value_counts().head(top_n).index
        filtered_area_df = df_schools[df_schools['Area'].isin(top_areas)]
        grouped_area = filtered_area_df.groupby(['Area', 'Status']).size().reset_index(name='Count')
        
        fig_bar = px.bar(
            grouped_area,
            x='Area',
            y='Count',
            color='Status',
            barmode='group',
            title=f'Public vs. Private Sector Reliance across Top {top_n} Municipal Areas',
            labels={'Count': 'Number of Institutions', 'Area': 'Municipal Area', 'Status': 'Sector Status'},
            color_discrete_map={'Public': '#1f77b4', 'Private': '#ff7f0e'},
            text_auto=True
        )
        
    fig_bar.update_layout(template="plotly_white")
    st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

# -----------------------------------------------------------------------------
# 5. OBJECTIVE 3: CORRELATION HEATMAP
# -----------------------------------------------------------------------------
st.header("3. Statistical Correlation: Psychological Attributes vs. Test Performance")
st.markdown("""
**Objective:** Determine the statistical correlation between psychological attributes (*Mindset*, *Positive view*) 
and individual student academic performance (*Test Mark*).
""")

col_h1, col_h2 = st.columns([1, 2])

psych_vars = ['TEST MARK', 'Positive view', 'Mindset']
corr_matrix = df_pilot[psych_vars].corr()

with col_h1:
    st.markdown("### Descriptive Statistics")
    st.dataframe(df_pilot[psych_vars].describe().T[['mean', 'std', 'min', '50%', 'max']].round(2))
    
    st.markdown("""
    **Key Correlation Summary (Pearson r):**
    * **Positive View vs. Test Mark:** $r = +0.309$ (Moderate Positive)
    * **Mindset vs. Test Mark:** $r = +0.018$ (Negligible Correlation)
    * **Positive View vs. Mindset:** $r = +0.297$ (Moderate Positive)
    """)

with col_h2:
    fig_heatmap, ax = plt.subplots(figsize=(6, 4))
    sns.heatmap(
        corr_matrix, 
        annot=True, 
        fmt=".3f", 
        cmap="coolwarm", 
        vmin=-1, 
        vmax=1, 
        linewidths=1,
        ax=ax,
        cbar_kws={'label': 'Pearson Correlation (r)'}
    )
    ax.set_title("Pearson Correlation Heatmap", fontsize=11, fontweight='bold', pad=10)
    plt.tight_layout()
    st.pyplot(fig_heatmap)