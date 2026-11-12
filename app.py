import streamlit as st

st.set_page_config(page_title="Educational Analytics Dashboard", layout="wide")

st.title("Educational Analytics Dashboard")
st.markdown("""
Welcome to the multi-page educational analytics dashboard. Use the **sidebar on the left** to navigate across the three core analytical objectives:

1. **Completion Trends:** District-level school completion rates across primary and secondary stages (2021–2025).
2. **School Density:** Institutional distribution and Public vs. Private sector reliance across areas and school levels.
3. **Psychometric Analysis:** Statistical correlation between student mindset, positive view, and academic test marks.
""")
