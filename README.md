# GitHub Analytics

![image](https://github.com/user-attachments/assets/40e84f27-dc2c-4124-9a91-4d7239bee432)
## A Comprehensive GitHub Repository Performance Analyzer

GitHub Analytics is an intuitive tool designed to provide in-depth insights into your GitHub repositories. This project simplifies repository analysis by visualizing key metrics such as commits, pull requests, issues, and code frequency, helping developers and teams track repository performance efficiently.

This project demonstrates:

- Automated fetching and processing of GitHub repository data using the GitHub API
- Visual representation of key metrics such as commits, pull requests, and issues
- Code frequency tracking to analyze development activity over time
- An interactive dashboard built with Streamlit to display repository analytics

## Key Features:

- **GitHub API Integration**: The application fetches data directly from GitHub using its API to provide real-time and accurate insights.
- **Repository Metrics Visualization**: Visualize essential repository metrics including commit frequency, pull requests, and open issues.
- **Code Frequency Analysis**: Track how code is added or modified over time with interactive charts.
- **Development Activity Insights**: Understand the contribution patterns and repository growth based on commit and issue data.
- **Interactive Dashboard**: A clean and user-friendly interface built with Streamlit for easy navigation and repository selection.

## Project Structure:

    data/
    ├── code_frequency.csv
    ├── commits.csv
    ├── issues.csv
    ├── pull_requests.csv
    ├── repo.csv
    └── reviews.csv
    dev_performance_dashboard/
        ├── data_collection/
        │   ├── github_api.py          # Handles data fetching from GitHub
        │   └── data_storage.py        # Manages data storage operations
        ├── metrics/
        │   └── calculator.py          # Performs calculations on the fetched data
        └── visualization/
            ├── charts.py              # Functions to generate visualizations (e.g., charts)
            └── dashboard.py           # Code for creating the dashboard interface
    ├── app.py                     # Main application entry point
    ├── requirements.txt           # Project dependencies
    └── README.md                  # Project documentation (this file)

## Installation and Setup:

Get started with the GitHub Analytics tool by following these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/GitHub-Analytics.git
    cd GitHub-Analytics
    ```

2. Install dependencies: Ensure you have Streamlit and other required packages installed.
    ```bash
    pip install -r requirements.txt
    ```

3. Set up environment variables:
    - You will need a GitHub personal access token to authenticate API requests.
    - Create a `.env` file in the root directory of the project and add the following content:
    ```bash
    GITHUB_TOKEN = your_github_personal_access_token
    ```

4. Launch the GitHub Analytics app:
    ```bash
    streamlit run app.py
    ```

## Usage Guide

1. **Enter GitHub Username and Repository**:
    - Provide your GitHub username and select the repository you wish to analyze.
      
![image](https://github.com/user-attachments/assets/d7a992db-1987-4e57-a6fa-89c4659abb16)


2. **View Repository Analytics**:
    - **Commits**: View the total number of commits made to the repository over time.
    - **Pull Requests**: Analyze the pull requests and their status (open/closed/merged).
    - **Issues**: Check the open issues and their progress.
    - **Code Frequency**: Visualize how frequently code is added to or modified in the repository over time.

3. **Explore Metrics**:
    - Use interactive charts to explore various repository metrics and gain insights into the development patterns.
  
4. **Data Refresh**:
    - The dashboard automatically updates the data based on your selected repository, ensuring real-time metrics.

## Find a Bug?

If you encounter any issues or would like to contribute to the project, please submit an issue using the issues tab above. If you wish to submit a pull request with a fix, make sure to reference the issue!

## Known Issues (Work in Progress)

- Some visualizations may be limited based on the data available in the repository (e.g., missing commits or pull request data).
- Future updates will include additional performance metrics and enhanced visualizations.

## Support This Project

If you find GitHub Analytics useful, here’s how to support it:

- **Share Your Experience**: Let us know how you are using the tool.
- **Contribute Ideas**: Check the issues section for suggestions or open a new one.
- **Provide Feedback**: Your feedback helps make this tool better.
