# 🚀 ChurnIQ — Customer Intelligence Platform

> Predict churn. Protect revenue. Retain customers.

ChurnIQ is an AI-powered customer analytics platform built with Python and
Streamlit to help businesses identify customers at risk of churn, understand
customer segments, analyze retention trends, and estimate revenue at risk.

## 🌐 Live Demo

🔗 **Live Application:** https://churniq-customer-intelligence-crj4ivixlpg77nsa5q272t.streamlit.app/

## 📌 Overview

ChurnIQ transforms customer data into actionable business intelligence.

The platform provides:

- 🧠 Customer churn prediction
- 👥 RFM customer segmentation
- 📅 Cohort retention analysis
- 💰 Revenue-at-risk analysis
- 🔎 Customer 360 exploration
- 🎯 Retention recommendations
- 🤖 AI-style business insights
- 📊 Interactive analytics dashboards

## ✨ Key Features

### 🧠 Churn Prediction

Classifies customers into:

- High Risk
- Medium Risk
- Low Risk

and provides churn probability to help prioritize retention activities.

### 👥 RFM Segmentation

Analyzes customers using:

- Recency
- Frequency
- Monetary value

to identify high-value and at-risk customer groups.

### 📅 Cohort Analysis

Tracks customer retention across signup cohorts and helps identify
retention patterns over time.

### 💰 Revenue Intelligence

Estimates potential revenue exposure from customers with high churn risk.

### 🔎 Customer 360

Provides customer-level insights including:

- Customer profile
- Purchase activity
- Churn probability
- Risk level
- Revenue contribution
- Retention signals

### 🤖 AI Business Assistant

Provides business-oriented insights from customer analytics to support
data-driven retention decisions.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming |
| Streamlit | Web application |
| Pandas | Data processing |
| NumPy | Numerical analysis |
| Plotly | Interactive visualization |
| Scikit-learn | Machine learning |
| SQLite | Local authentication |
| Git & GitHub | Version control |

---

## 📊 Application Architecture

```text
                ┌─────────────────────┐
                │       User          │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │    Streamlit UI     │
                └──────────┬──────────┘
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
 Authentication      Analytics Engine    AI Insights
        │                  │                  │
        ▼                  ▼                  ▼
   SQLite DB       Pandas / Scikit-learn   Business Logic
                           │
                           ▼
                 Customer Dataset
                           │
                           ▼
                    Visualizations