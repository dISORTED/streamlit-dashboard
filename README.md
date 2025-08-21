# Streamlit Data Dashboard

**Repository:** [https://github.com/](https:/dISORTED/github.com/)<usuario>/streamlit-dashboard

## Description

The Streamlit Data Dashboard is an interactive web application for exploratory data analysis of tabular datasets. It provides users with the ability to:

* Upload a CSV file and visualize its contents.
* Connect to a SQLite database file and retrieve data from a specified table.
* Display descriptive statistics and generate interactive charts.

The application is built with Streamlit and deployed on Streamlit Community Cloud. Continuous integration is managed via GitHub Actions.

## Features

* CSV file upload for ad hoc data analysis
* SQLite database connection with automatic table creation if needed
* Key metrics display: number of rows, columns, and missing values
* Data table view and descriptive statistics (count, mean, std, min, max)
* Interactive bar chart of column means
* Optional scatter plot for selected numeric columns
* Themed interface with sidebar configuration

## Technologies

* Python 3.12
* Streamlit
* Pandas
* Plotly Express
* SQLAlchemy
* SQLite
* GitHub Actions
* Streamlit Community Cloud

## Repository Structure

```
streamlit-dashboard/
├── .github/workflows/ci.yml    GitHub Actions workflow for linting and tests
├── .streamlit/
│   ├── config.toml             Streamlit theme configuration
│   └── secrets.toml            Database URL secret
├── data/
│   ├── sample.csv              Example CSV dataset
│   └── sample.db               Example SQLite database
├── tests/
│   └── test_data_loading.py    Pytest test for CSV loading
├── streamlit_app.py            Main Streamlit application
├── requirements.txt            Python dependencies
└── README.md                   Project documentation
```

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/<usuario>/streamlit-dashboard.git
   cd streamlit-dashboard
   ```
2. Create and activate a virtual environment (optional):

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:

   ```bash
   streamlit run streamlit_app.py
   ```
5. Open `http://localhost:8501` in your browser.

## Deployment

The application can be deployed on Streamlit Community Cloud:

1. Log in to [https://share.streamlit.io](https://share.streamlit.io) and connect your GitHub account.
2. Select the `streamlit-dashboard` repository and the `main` branch.
3. Set the entry point to `streamlit_app.py` and deploy.

## Contributing

Contributions are welcome. To contribute:

1. Open an issue to discuss your proposal.
2. Create a pull request with your changes.
3. Ensure that all tests pass (`pytest`) and code meets style requirements (`flake8`).

## License

This project is licensed under the MIT License. See the LICENSE file for details.

