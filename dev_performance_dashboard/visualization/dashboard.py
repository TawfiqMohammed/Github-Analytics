import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from metrics.calculator import (
    calculate_kpis
)

from visualization.charts import (
    plot_gauge_pulls_issues,
    plot_combined_charts
)

def display_metric(label, value):
    if pd.isna(value):
        value = "0"
    else:
        value = str(round(value))
    formatted_text = f"""
    <h5 style='text-align: center; margin: 0;'>{label}</h5>
    <h1 style='text-align: center; margin: 0; padding: 0;color: #569d4c;'>{value}</h1>
    """
    # Display the formatted text in Streamlit
    st.markdown(formatted_text, unsafe_allow_html=True)

def build_dashboard(repo_df, commits_df, issues_df, pulls_df, code_freq_df):
    kpi_data = calculate_kpis(repo_df, issues_df, pulls_df, commits_df)

    st.divider()
    formatted_text1 = f"""
    <h1 style='text-align: center; margin: 0; padding: 0;'><b>Developer Activity Overview</b></h1>
    """
    reponame = repo_df['repo_name'].iloc[0]
    formatted_text2 = f"""
    <h4 style='text-align: center; margin: 0; padding: 0;'><b>Insights for Repo: {reponame}</b></h4>
    """
    st.markdown(formatted_text1, unsafe_allow_html=True)
    st.markdown("")
    st.markdown(formatted_text2, unsafe_allow_html=True)
    st.markdown("")
    st.divider()
    # Create columns for layout
    col1, col2, col3, col4 = st.columns(4)

    # Display metrics using the generalized function
    with col1:
        display_metric("Number of Forks ↗️", int(repo_df['repo_forks']))

    with col2:
        display_metric("Number of Stars ⭐", int(kpi_data['total_stars']))

    with col3:
        display_metric("PR Merge Time 🔀", kpi_data['avg_merge_time'])

    with col4:
        display_metric("Resolve Time ✅", kpi_data['avg_issue_resolution_time'])
    st.divider()
    
    plot_combined_charts(commits_df, pulls_df, issues_df, code_freq_df, rows=2, cols=2)
    st.divider()

    plot_gauge_pulls_issues(issues_df, pulls_df)
 

# Main entry point for the Streamlit app
if __name__ == "__main__":
    build_dashboard()

