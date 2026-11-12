import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Psychometric Analysis", layout="wide")
st.title("3. Psychometric Attributes & Test Mark Correlation")

df_pilot = pd.read_excel("pilot_questionnaire_cleaned.xlsx", sheet_name="Cleaned_Data")
cols = ["TEST MARK", "Positive view", "Mindset"]
corr_matrix = df_pilot[cols].corr()

fig, ax = plt.subplots(figsize=(6, 4))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".3f", vmin=-1, vmax=1, ax=ax)
ax.set_title("Pearson Correlation Matrix")
st.pyplot(fig)
