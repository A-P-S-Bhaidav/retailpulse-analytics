<div align="center">
  <h1>RetailPulse Analytics</h1>
  <p>An end-to-end data science and machine learning platform for retail intelligence.</p>
  
  [![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://python.org)
  [![Streamlit](https://img.shields.io/badge/Streamlit-1.34-FF4B4B.svg)](https://streamlit.io)
  [![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-EE4C2C.svg)](https://pytorch.org)
  [![XGBoost](https://img.shields.io/badge/XGBoost-3.2-blue.svg)](https://xgboost.readthedocs.io)
  [![MLflow](https://img.shields.io/badge/MLflow-Tracking-0194E2.svg)](https://mlflow.org)
</div>

## Overview

RetailPulse is a comprehensive machine learning pipeline and interactive dashboard designed to solve core business problems for retail companies. It ingests raw transactional data and applies advanced modeling to provide actionable insights into customer behavior, demand forecasting, and inventory optimization.

### Key Features
- **Customer Segmentation:** Groups 5,878 customers using K-Means and DBSCAN based on Recency, Frequency, and Monetary (RFM) value.
- **Demand Forecasting:** Predicts daily revenue 30 days into the future using a Hybrid Ensemble of **Meta Prophet** and **LSTM (PyTorch)** neural networks.
- **Churn Prediction:** Identifies at-risk customers using an **XGBoost** classifier, fully optimized via **Optuna** and explained using **SHAP** values.
- **Inventory Optimization:** Simulates stock levels and calculates optimal Economic Order Quantity (EOQ), Safety Stock, and Reorder Points to minimize stockouts.
- **Experiment Tracking:** All models and parameters are versioned and logged using **MLflow**.
- **Data Drift Detection:** Monitors input feature distributions using Population Stability Index (PSI) and Kolmogorov-Smirnov (KS) tests.

---

## Dataset

| Property | Detail |
|---|---|
| Name | Online Retail II |
| Source | UCI Machine Learning Repository |
| Total records | 1,067,371 (raw), 1,033,034 (after deduplication) |
| Period | 01 December 2009 – 09 December 2011 |
| Format | Two Excel sheets (Year 2009-2010 and Year 2010-2011), merged and deduplicated |

---

## Project Architecture

The project is structured into 14 sequential Jupyter Notebooks representing a chronological data science workflow, culminating in a production-ready Streamlit dashboard.

```text
RetailPulse/
├── data/
│   ├── raw/                 # Raw transactional data (1,033,034 rows)
│   └── processed/           # Engineered features and model outputs
├── notebooks/               # Chronological pipeline (01 to 14)
├── models/                  # Saved weights (LSTM, XGBoost)
├── mlflow/                  # MLflow tracking registry
├── reports/                 # Generated figures and analysis plots
├── dashboard/               # Streamlit application
│   ├── app.py               # Main entry point
│   └── views/               # Dashboard module pages
├── Dockerfile               # Containerization config
└── README.md
```

---

## Getting Started

### Prerequisites
- Python 3.11+
- Git

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/A-P-S-Bhaidav/retailpulse-analytics.git
   cd retailpulse-analytics
   ```

2. **Set up the virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r dashboard/requirements.txt
   ```

### Running the Dashboard Locally
```bash
cd dashboard
streamlit run app.py
```
The application will be accessible at `http://localhost:8501`.

### Docker Deployment
```bash
docker build -t retailpulse .
docker run -p 8501:8501 retailpulse
```

---

## Pipeline Summary

| Day | Notebook | What It Does |
|---|---|---|
| 1 | `01_eda_exploration` | Exploratory data analysis on 1,033,034 transactions |
| 2 | `02_data_cleaning_feature_engineering` | Cleaning, RFM scoring, daily aggregation (739 trading days, 5,878 customers) |
| 3 | `03_customer_segmentation` | K-Means (k=4) and DBSCAN clustering on RFM features |
| 4 | `04_timeseries_preparation` | Stationarity tests (ADF, KPSS), seasonal decomposition |
| 5 | `05_prophet_forecasting` | Prophet with weekly + monthly seasonality tuning (MAPE: 23.06%) |
| 6 | `06_lstm_forecasting` | 2-layer LSTM with 30-day lookback (MAPE: 21.43%) |
| 7 | `07_mlflow_experiment_tracking` | MLflow logging for Week 1 models |
| 8 | `08_hybrid_ensemble` | Prophet + LSTM ensemble — 4 blending strategies (Best MAPE: 20.97%) |
| 9 | `09_churn_prediction` | XGBoost binary classifier with SHAP explainability |
| 10 | `10_inventory_optimization` | EOQ, Safety Stock, Reorder Point, 739-day simulation (Fill Rate: 98.9%) |
| 11 | `11_optuna_tuning` | 50-trial Bayesian hyperparameter optimization for XGBoost |
| 12 | `12_drift_detection` | PSI and KS tests for data drift monitoring |
| 13 | `13_model_refinement` | Walk-forward cross-validation for Prophet |
| 14 | `14_mlflow_week2` | MLflow logging for Week 2 models |

---

## Modeling Details

- **Time-Series Forecasting:** Walk-forward cross-validation strategy, combining Prophet's strong grasp of seasonal trends with an LSTM's ability to capture non-linear sequences. The predictions are ensembled via blending search to minimize MAPE.
- **Churn Classification:** XGBoost classifier with `scale_pos_weight` for class imbalance, tuned over 50 Bayesian optimization trials using Optuna to maximize ROC AUC.
- **Inventory Optimization:** EOQ formula with 95% service level safety stock and 7-day lead time. Monte Carlo simulation over 739 historical days achieves 98.9% fill rate.

---

## License
This project is licensed under the MIT License.
