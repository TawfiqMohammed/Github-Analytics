import streamlit as st
import pandas as pd
import os
import sys

# Ensure the correct path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

st.set_page_config(layout="wide")

# Import custom functions
from dev_performance_dashboard.data_collection.github_api import get_repo_list, fetch_and_save_github_data
from dev_performance_dashboard.visualization.dashboard import build_dashboard

def home_page():
    # Add a brief introduction to what the app does
    st.markdown("####")
    st.markdown("""
    <p style='text-align: left; font-size: 1.3em; color: #FFFFFF ;'>
    This app provides an interactive dashboard to help you analyze and visualize key metrics from your GitHub repositories. 
    Whether you are an individual developer or part of a team, you can track repository performance with ease.
    </p>
    """, unsafe_allow_html=True)
    st.markdown("######")
    # Highlight what the user can do with the app
    st.markdown("""
    <p style='text-align: left; font-size: 1.3em; color: #FFFFFF ;'>Simply input your GitHub username and select a repository to:</p>
    <ul style='font-size: 1.3em; color: #FFFFFF ;'>
        <li style='font-size: 0.9em; color: #FFFFFF ;'>Visualize key repository metrics like commits, pull requests, and issues.</li>
        <li style='font-size: 0.9em; color: #FFFFFF ;'>Track code frequency and development activity over time.</li>
        <li style='font-size: 0.9em; color: #FFFFFF ;'>Gain insights into your repository’s performance and contributions.</li>
    </ul>
    <br>
    <p style='text-align: center; font-size: 1.3em; color: #569d4c;'>Start by selecting a repository from the list to see detailed analytics.</p>
    """, unsafe_allow_html=True)

    # Layout for GitHub username and repository selection
    username = st.text_input("Enter GitHub Username")
    if username:
        repos = get_repo_list(username)
        if repos:
                selected_repo = st.selectbox("Select Repository", repos)
        else:
            st.write("No repositories found for this user.")
    else:
        st.write("Please enter a GitHub username.")
    
    # Check if both username and repository are selected
    if username and selected_repo:
        continue_button = st.button("Continue")
        if continue_button:
            # Store the selected repo in session state to persist across pages
            st.session_state.username = username.replace(" ", "")
            st.session_state.selected_repo = selected_repo.replace(" ", "")
            fetch_and_save_github_data(st.session_state.username, st.session_state.selected_repo)
            st.session_state.repo_selected = True
            st.success("Data Fetched and Saved. Go to Analytics to view the dashboard.")

def analytics_page():
       # Check if repository data has been selected
    if 'repo_selected' in st.session_state and st.session_state.repo_selected:
        try:
            # Load the data files
            commits_df = pd.read_csv('data/commits.csv')
            pulls_df = pd.read_csv('data/pull_requests.csv')
            issues_df = pd.read_csv('data/issues.csv')
            code_freq_df = pd.read_csv('data/code_frequency.csv')
            repo_df = pd.read_csv('data/repo.csv')

            # Show the dashboard
            build_dashboard(repo_df, commits_df, issues_df, pulls_df, code_freq_df)
        except FileNotFoundError as e:
            st.error(f"Error loading data files: {e}")
    else:
        st.warning("Please select a repository on the Home page to analyze the data.")

def main():
    # Navigation panel
    st.sidebar.markdown("##")
    st.sidebar.markdown("##")
    st.sidebar.title("GitHub Repository Analyzer")
    st.sidebar.title("🧭 Navigation:")
    page = st.sidebar.radio("", ["Repository Selection", "Analytics"])

    # Handle page navigation
    if page == "Repository Selection":
        home_page()
    elif page == "Analytics":
        analytics_page()

if __name__ == "__main__":
    main()