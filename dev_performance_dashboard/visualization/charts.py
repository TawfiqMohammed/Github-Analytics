import plotly.graph_objs as go
import streamlit as st
import pandas as pd
from plotly._subplots import make_subplots
import os
import sys 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def plot_gauge_pulls_issues(issues_df, pulls_df):
    total_issues = len(issues_df)
    open_issues = issues_df[issues_df['state'] == 'open'].shape[0]
    closed_issues_count = issues_df[issues_df['state'] == 'closed'].shape[0]

    total_pulls = len(pulls_df)
    closed_pulls_count = pulls_df[pulls_df['state'] == 'closed'].shape[0]
    merged_pulls = pulls_df[pulls_df['merged_at'].notna()].shape[0]

    percentage_open_issues = (open_issues / total_issues) * 100
    percentage_closed_issues = (closed_issues_count / total_issues) * 100
    percentage_closed_pulls = (closed_pulls_count / total_pulls) * 100
    percentage_merged_pulls = (merged_pulls / total_pulls) * 100

    fig = go.Figure()

    fig = make_subplots(rows=1, cols=4, specs=[[{"type": "indicator"}]*4])

    fig.add_trace(go.Indicator(
    mode="gauge+number",
        value=open_issues,
        title={'text': f"Open Issues - <span style='color:#569d4c;'><b>{percentage_open_issues:.1f}%</b></span>"},
        gauge=dict(
            axis={'range': [0, total_issues]},  
            bar=dict(
                color="#569d4c",  
                thickness=0.4 
            ),
            borderwidth=0.2,  
            steps=[{'range': [0, total_issues], 'color': '#4c4c4c'}] 
        )
    ), row=1, col=3)

    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=closed_issues_count,
        title={'text': f"Closed Issues - <span style='color:#569d4c;'><b>{percentage_closed_issues:.1f}%</b></span>"},
        gauge=dict(
            axis={'range': [0, total_issues]}, 
            bar=dict(
                color="#569d4c", 
                thickness=0.4  
            ),
            borderwidth=0.2, 
            steps=[{'range': [0, total_issues], 'color': '#4c4c4c'}]  
        ),
    ), row=1, col=4)

    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=closed_pulls_count,
        title={'text': f" Closed Pull Requests - <span style='color:#569d4c;'><b>{percentage_closed_pulls:.1f}%</b></span>"},
        gauge={'axis': {'range': [0, total_pulls]},
            'bar':dict(
                    color="#569d4c",  
                    thickness=0.4,  
                    
                ),
                'borderwidth': 0.2,
            'steps': [{'range': [0, total_pulls], 'color': '#4c4c4c'}]}
    ), row=1, col=1)

    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=merged_pulls,
        title={'text': f" Merged Pull Requests - <span style='color:#569d4c;'><b>{percentage_merged_pulls:.1f}%</b></span>"},
        gauge={'axis': {'range': [0, total_pulls]},
                'bar':dict(
                        color="#569d4c", 
                        thickness=0.4,  
                        
                    ),
                'borderwidth': 0.2,
            'steps': [{'range': [0, total_pulls], 'color': '#4c4c4c'}]}
    ), row=1, col=2)

    fig.update_layout(
        height=250, 
        margin=dict(l=0, r=0, t=0, b=0),  
        width=1200,  
    )
    
    st.plotly_chart(fig, use_container_width=True)

def plot_combined_charts(commits_df, pulls_df, issues_df, cf_df, rows=2, cols=2):
    fig = make_subplots(
        rows=rows, cols=cols, 
        subplot_titles=(
            "Commits per Developer", 
            "Count of PR Merges Over Time", 
            "Count of Issue Resolutions Over Time", 
            "Code Lines Changes Over Time"
        )
    )

    commit_frequency = commits_df[commits_df['author'] != 'Unknown'].groupby('author').size().reset_index(name='commit_count')
    top_commit_freq = commit_frequency.sort_values(by='commit_count', ascending=False).head(10)
    fig.add_trace(go.Bar(
        x=top_commit_freq['author'], 
        y=top_commit_freq['commit_count'], 
        marker_color='#569d4c', 
        name="Commits per Developer",
        width=0.1
    ), row=1, col=1)

    closed_pulls = pulls_df[pulls_df['merged_at'].notna()]
    merge_count = closed_pulls['merged_at'].dt.date.value_counts().reset_index()
    merge_count.columns = ['merge_date', 'merge_count']
    merge_count = merge_count.sort_values('merge_date')
    fig.add_trace(go.Scatter(
        x=merge_count['merge_date'], 
        y=merge_count['merge_count'], 
        mode='lines+markers', 
        name="PR Merges", 
        line=dict(color='#569d4c', width=2)
    ), row=1, col=2)

    closed_issues = issues_df[issues_df['closed_at'].notna()]
    resolution_count = closed_issues['closed_at'].dt.date.value_counts().reset_index()
    resolution_count.columns = ['resolution_date', 'resolution_count']
    resolution_count = resolution_count.sort_values('resolution_date')
    fig.add_trace(go.Scatter(
        x=resolution_count['resolution_date'], 
        y=resolution_count['resolution_count'], 
        mode='lines+markers', 
        name="Issue Resolutions", 
        line=dict(color='#569d4c', width=2)
    ), row=2, col=1)

    cf_df['date'] = pd.to_datetime(cf_df['date'])

    fig.add_trace(go.Scatter(
        x=cf_df['date'],
        y=cf_df['lines_added'],
        mode='lines',
        fill='tozeroy',  
        line=dict(color='#569d4c', width=2),  
    ), row=2, col=2)

    fig.add_trace(go.Scatter(
        x=cf_df['date'],
        y=-cf_df['lines_deleted'], 
        mode='lines',
        fill='tozeroy', 
        line=dict(color='#dd6051', width=2, dash='dash'),  
    ), row=2, col=2)

    fig.update_layout(
        template="plotly_dark",  
        height=700,
        plot_bgcolor='rgba(0, 0, 0, 0)',  
        paper_bgcolor='rgba(0, 0, 0, 0)',  
        showlegend=False,

    )

    st.plotly_chart(fig, use_container_width=True)

