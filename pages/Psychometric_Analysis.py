import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Psychometric Analysis", layout="wide")
st.title("3. Psychometric Attributes & Test Mark Correlation")

@st.cache_data
def load_pilot_data():
    return pd.read_excel("pilot_questionnaire_cleaned.xlsx", sheet_name="Cleaned_Data")

df_pilot = load_pilot_data()
cols = ["TEST MARK", "Positive view", "Mindset"]
corr_matrix = df_pilot[cols].corr()

col1, col2 = st.columns([1.2, 1])

with col1:
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".3f", vmin=-1, vmax=1, ax=ax)
    ax.set_title("Pearson Correlation Matrix (N = 133)")
    st.pyplot(fig)

with col2:
    st.subheader("Statistical Summary")
    st.dataframe(df_pilot[cols].describe().T[["mean", "std", "min", "50%", "max"]].round(2))
