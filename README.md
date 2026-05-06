# RetailPulse -- AI-Powered Customer Analytics & Demand Forecasting Platform

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-red.svg)](https://streamlit.io)
[![MLflow](https://img.shields.io/badge/MLOps-MLflow-blue.svg)](https://mlflow.org)

> **End-to-End Data Science & Analytics Solution for Retail Demand Prediction & Customer Insights**

Retailers lose billions due to poor demand forecasting and stock mismanagement. RetailPulse uses advanced analytics and machine learning to predict demand, segment customers, detect churn, and optimize inventory -- helping retailers reduce stockouts by 30-50% and increase revenue by 15-25%.

---

## Business Objectives

| Metric | Target |
|--------|--------|
| Reduce stockouts | 30-50% through accurate demand forecasting |
| Increase revenue | 15-25% through better inventory decisions |
| Forecast accuracy | MAPE <= 12% |
| Churn detection | AUC-ROC >= 0.88 |
| Processing speed | < 5 min for daily batch jobs on 10M+ transactions |

## Core Features

| ID | Feature | Description | Acceptance Criteria |
|----|---------|-------------|---------------------|
| F-01 | Data Ingestion & Cleaning | Automated ETL pipeline with data quality checks | Validated pipeline, reproducible |
| F-02 | Customer Segmentation | RFM + K-Means / DBSCAN clustering | 6-8 meaningful business segments |
| F-03 | Demand Forecasting | Prophet + LSTM hybrid ensemble | MAPE <= 12%, 30-day predictions |
| F-04 | Churn Prediction | XGBoost with SHAP explainability | AUC-ROC >= 0.88 |
| F-05 | Inventory Optimization | Reorder recommendations from forecasted demand | 25-40% reduction in over/understock |
| F-06 | Interactive Dashboard | Streamlit with what-if analysis | Real-time insights, exportable reports |

## Technology Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Language | Python 3.11 | Data science ecosystem |
| Data Processing | Pandas, NumPy, Scikit-learn | Core data manipulation & ML |
| Forecasting | Prophet + LSTM (PyTorch) | Hybrid time-series forecasting |
| Classification | XGBoost + SHAP | Interpretable churn prediction |
| Dashboard | Streamlit | Fast interactive analytics |
| Experiment Tracking | MLflow | Model versioning & reproducibility |
| Data Validation | Great Expectations | Automated data quality checks |
| Drift Detection | Evidently AI | Model & data drift monitoring |
| Containerization | Docker + Kubernetes | Scalable deployment |
| Monitoring | Prometheus + Grafana | Performance monitoring |

## Project Structure

```
RetailPulse/
├── data/
│   ├── raw/            # Original dataset files
│   ├── processed/      # Cleaned, feature-engineered data
│   └── interim/        # Intermediate transformations
├── notebooks/          # EDA, modeling, evaluation notebooks
├── src/
│   ├── ingestion/      # ETL and data download scripts
│   ├── segmentation/   # RFM analysis + clustering
│   ├── forecasting/    # Prophet + LSTM models
│   ├── churn/          # XGBoost + SHAP pipeline
│   └── inventory/      # Optimization logic
├── dashboard/          # Streamlit application
├── mlflow/             # Experiment tracking config
├── docker/             # Dockerfile, docker-compose
├── reports/figures/    # Generated EDA plots & visualizations
├── models/             # Saved model artifacts
├── .github/workflows/  # CI/CD pipeline
├── requirements.txt
└── README.md
```

## Quick Start

```bash
# Clone the repository
git clone https://github.com/A-P-S-Bhaidav/retailpulse-analytics.git
cd retailpulse-analytics

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download the dataset
python src/ingestion/download_data.py

# Run notebooks in order
jupyter notebook notebooks/
```

## Dataset

**Online Retail II** -- UCI Machine Learning Repository
- 525,461 transactions across 28,816 invoices
- 4,632 unique products, 4,383 customers
- 40 countries, date range: Dec 2009 - Dec 2010

Source: [UCI ML Repository](https://archive.ics.uci.edu/dataset/502/online+retail+ii)

## Development Timeline

| Week | Focus | Key Deliverables |
|------|-------|-----------------|
| Week 1 | Data Foundation | EDA, cleaning, baseline models |
| Week 2 | Advanced Modeling | Hybrid forecasting, churn, optimization |
| Week 3 | Dashboard | Interactive Streamlit application |
| Week 4 | Deployment | Docker, K8s, CI/CD, monitoring |

---
