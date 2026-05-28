<div align="center">
  <h1>RetailPulse Analytics</h1>
  <p>An end-to-end data science and machine learning platform for retail intelligence.</p>
  
  [![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://python.org)
  [![Streamlit](https://img.shields.io/badge/Streamlit-1.34-FF4B4B.svg)](https://streamlit.io)
  [![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-EE4C2C.svg)](https://pytorch.org)
  [![XGBoost](https://img.shields.io/badge/XGBoost-3.2-blue.svg)](https://xgboost.readthedocs.io)
  [![MLflow](https://img.shields.io/badge/MLflow-Tracking-0194E2.svg)](https://mlflow.org)
</div>

## 📌 Overview

RetailPulse is a comprehensive machine learning pipeline and interactive dashboard designed to solve core business problems for retail companies. It ingests raw transactional data and applies advanced modeling to provide actionable insights into customer behavior, demand forecasting, and inventory optimization.

### Key Features
- **Customer Segmentation:** Groups customers using K-Means and DBSCAN based on Recency, Frequency, and Monetary (RFM) value.
- **Demand Forecasting:** Predicts daily revenue 30 days into the future using a Hybrid Ensemble of **Meta Prophet** and **LSTM (PyTorch)** neural networks.
- **Churn Prediction:** Identifies at-risk customers using an **XGBoost** classifier, fully optimized via **Optuna** and explained using **SHAP** values.
- **Inventory Optimization:** Simulates stock levels and calculates optimal Economic Order Quantity (EOQ), Safety Stock, and Reorder Points to minimize stockouts.
- **Experiment Tracking:** All models and parameters are versioned and logged using **MLflow**.
- **Data Drift Detection:** Monitors input feature distributions using Population Stability Index (PSI) and Kolmogorov-Smirnov (KS) tests via **Evidently AI**.

---

## 🏗 Project Architecture

The project is structured into sequential Jupyter Notebooks representing a chronological data science workflow, culminating in a production-ready Streamlit dashboard.

```text
RetailPulse/
├── data/
│   ├── raw/                 # Raw transactional data
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

## 🚀 Getting Started

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
To launch the interactive intelligence platform:

```bash
cd dashboard
streamlit run app.py
```
The application will be accessible at `http://localhost:8501`.

### Docker Deployment
To run the dashboard in an isolated container:
```bash
docker build -t retailpulse .
docker run -p 8501:8501 retailpulse
```

---

## 🧠 Modeling Details

- **Time-Series Forecasting:** We employ a walk-forward cross-validation strategy, combining Prophet's strong grasp of seasonal trends with an LSTM's ability to capture non-linear sequences. The predictions are ensembled via an optimal blending search grid to minimize Mean Absolute Percentage Error (MAPE).
- **Churn Classification:** Because churn is an imbalanced problem (most customers don't churn at once), the XGBoost classifier utilizes `scale_pos_weight`. Hyperparameters are tuned over 50 Bayesian optimization trials using Optuna to maximize ROC AUC.

---

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
