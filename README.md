# ChurnIQ — Customer Intelligence Platform

ChurnIQ is a Streamlit-based customer analytics platform designed to help teams
predict customer churn, understand customer value, quantify revenue exposure,
and turn risk signals into retention actions.

## Core Features

- Secure local authentication with hashed passwords
- Executive customer intelligence dashboard
- Churn prediction and risk classification
- RFM customer segmentation
- Cohort retention analytics
- Customer 360 profile
- Retention recommendation engine
- Revenue-at-risk intelligence
- AI Business Assistant
- CSV exports for analytics workflows
- Premium SaaS-style UI

## Tech Stack

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- Scikit-learn

## Project Structure

```text
ChurnIQ/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .streamlit/
│   └── config.toml
└── data/
    └── your_dataset.csv
```

> Keep real user databases, secrets, and private datasets out of GitHub.

## Local Setup

### 1. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Run ChurnIQ

```powershell
streamlit run app.py
```

## Deployment

The application can be deployed to a Streamlit-compatible hosting service.

Typical deployment settings:

- Main file: `app.py`
- Python dependencies: `requirements.txt`
- Python version: use a currently supported 3.x version
- Secrets: configure through the hosting platform, never commit secrets

## Portfolio Description

**ChurnIQ — AI-Powered Customer Churn & Revenue Intelligence Platform**

Built a professional customer analytics platform using Python, Streamlit,
Pandas and Plotly to analyze churn probability, customer segmentation,
cohort retention, customer value and revenue at risk. Implemented a
Customer 360 view, automated retention recommendations and an AI-style
business assistant to convert analytical signals into actionable decisions.

## Important Security Note

The included authentication is suitable for a local/demo portfolio application.
For production use, replace local SQLite authentication with a managed
authentication provider and a production-grade database, add authorization
roles, secure secrets, HTTPS, rate limiting, audit logging and proper data
protection controls.
