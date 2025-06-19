import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Player Prop Tool", layout="wide")

uploaded_file = st.sidebar.file_uploader("Upload prop CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    def to_decimal(odds):
        return 1 + odds / 100 if odds > 0 else 1 + 100 / abs(odds)

    def calculate_ev(row):
        prob = row['%_hit'] / 100
        payout = to_decimal(row['best_odds'])
        return round((prob * (payout - 1)) - (1 - prob), 4)

    df['best_odds'] = df[['odds_dk', 'odds_fd', 'odds_pinnacle']].max(axis=1)
    df['EV'] = df.apply(calculate_ev, axis=1)

    st.title("Multi-Book Prop EV Tool")
    st.dataframe(df)

    st.download_button("Download Filtered CSV", df.to_csv(index=False), file_name="filtered_props.csv")
else:
    st.warning("Upload a CSV file to get started.")
