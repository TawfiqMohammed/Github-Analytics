import pandas as pd

# Function to calculate KPIs
def calculate_kpis(repo_df, issues_df, pulls_df, commits_df):
    pulls_df['merged_at'] = pd.to_datetime(pulls_df['merged_at'], errors='coerce')
    pulls_df['created_at'] = pd.to_datetime(pulls_df['created_at'], errors='coerce')

    closed_pulls = pulls_df
    closed_pulls['merge_time'] = (closed_pulls['merged_at'] - closed_pulls['created_at']).dt.days
    avg_merge_time = closed_pulls['merge_time'].mean()

    issues_df['closed_at'] = pd.to_datetime(issues_df['closed_at'], errors='coerce')
    issues_df['created_at'] = pd.to_datetime(issues_df['created_at'], errors='coerce')

    closed_issues = issues_df
    closed_issues['resolution_time'] = (closed_issues['closed_at'] - closed_issues['created_at']).dt.days
    avg_issue_resolution_time = closed_issues['resolution_time'].mean()

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

    total_stars = repo_df['repo_stars']
    
    commit_frequency = commits_df[commits_df['author'] != 'Unknown'].groupby('author').size().reset_index(name='commit_count')
    return {
        'avg_merge_time': avg_merge_time,
        'avg_issue_resolution_time': avg_issue_resolution_time,
        'percentage_open_issues': percentage_open_issues,
        'percentage_closed_issues': percentage_closed_issues,
        'percentage_closed_pulls': percentage_closed_pulls,
        'percentage_merged_pulls': percentage_merged_pulls, 
        'total_stars': total_stars, 
        'commit_frequency': commit_frequency
    }