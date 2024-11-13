import sys
import os
from github import Github
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data_collection.data_storage import (
    save_to_csv
)

def get_repo_list(username):
    access_token = "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"
    g = Github(access_token)
    user = g.get_user(username)
    repos = user.get_repos()
    repo_list = [repo.name for repo in repos]
    return repo_list

def fetch_and_save_github_data(username, repo_name):
    directory='data'
    access_token = "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" 
    g = Github(access_token)
    repo_link = username+"/"+repo_name
    repos = g.get_repo(repo_link)

    # Fetch general repository data
    repo_data = {
        "repo_name": [repos.name],
        "repo_description": [repos.description],
        "repo_stars": [repos.stargazers_count],
        "repo_forks": [repos.forks_count],
    }
    repo_df = pd.DataFrame(repo_data)

    # st.write(username, selected_repo)


    # Fetch and process code lines 
    code_lines = repos.get_commits()
    code_freq_data = []
    for event in code_lines:
        event_info = {
            "date": event.commit.author.date.date(),
            "lines_added": event.stats.additions if event.stats else 0,
            "lines_deleted": event.stats.deletions if event.stats else 0,
        }
        code_freq_data.append(event_info)
    code_freq_df = pd.DataFrame(code_freq_data)

    # Fetch and process commits
    commits = repos.get_commits()
    commit_data = []
    for commit in commits:
        commit_info = {
            "sha": commit.sha,
            "author": commit.author.login if commit.author else "Unknown",
            "date": commit.commit.author.date.date(),
            "message": commit.commit.message,
        }
        commit_data.append(commit_info)
    commits_df = pd.DataFrame(commit_data)

    # Fetch and process pull requests
    pulls = repos.get_pulls(state='all')
    pr_data = []
    for pr in pulls:
        pr_info = {
            "id": pr.id,
            "title": pr.title,
            "user": pr.user.login,
            "state": pr.state,
            "created_at": pr.created_at.date() if pr.created_at else None,
            "closed_at": pr.closed_at.date() if pr.closed_at else None,
            "merged_at": pr.merged_at.date() if pr.merged_at else None
        }
        pr_data.append(pr_info)
    prs_df = pd.DataFrame(pr_data)

    # Fetch and process issues
    issues = repos.get_issues(state='all')
    issue_data = []
    for issue in issues:
        issue_info = {
            "id": issue.id,
            "title": issue.title,
            "user": issue.user.login,
            "state": issue.state,
            "created_at": issue.created_at.date() if issue.created_at else None,
            "closed_at": issue.closed_at.date() if issue.closed_at else None
        }
        issue_data.append(issue_info)
    issues_df = pd.DataFrame(issue_data)

    # Fetch and process reviews
    reviews_data = []
    for pr in pulls:
        reviews = pr.get_reviews()
        for review in reviews:
            review_info = {
                "pull_request_id": pr.id,
                "review_id": review.id,
                "state": review.state,
                "submitted_at": review.submitted_at.date() if review.submitted_at else None
            }
            reviews_data.append(review_info)
    reviews_df = pd.DataFrame(reviews_data)

    # Create the data directory if it does not exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    else:
        # Clear existing data if it exists
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

    # Save DataFrames to CSV files
    save_to_csv(repo_df, os.path.join(directory, "repo.csv"))
    save_to_csv(commits_df, os.path.join(directory, "commits.csv"))
    save_to_csv(prs_df, os.path.join(directory, "pull_requests.csv"))
    save_to_csv(issues_df, os.path.join(directory, "issues.csv"))
    save_to_csv(reviews_df, os.path.join(directory, "reviews.csv"))
    save_to_csv(code_freq_df, os.path.join(directory, "code_frequency.csv"))
