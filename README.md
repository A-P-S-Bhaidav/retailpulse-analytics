# RetailPulse: Executive Analytics & Forecasting Platform

## 1. Executive Summary
RetailPulse is an end-to-end data analytics and machine learning platform built to transform raw retail transactional data into actionable business intelligence. The platform solves three core retail challenges:
1.  **Customer Retention & Segmentation:** Understanding who the most valuable customers are and predicting which high-value customers are at risk of churning.
2.  **Demand Forecasting:** Accurately predicting future revenue using hybrid time-series modeling.
3.  **Inventory Optimization:** Translating demand forecasts into mathematical inventory parameters (Economic Order Quantity, Safety Stock, Reorder Points) to minimize holding costs and prevent stockouts.

The final deliverable is an interactive Streamlit dashboard providing executive summaries, customer intelligence, forecasting comparisons, and inventory timelines.

---

## 2. Technical Architecture & Data Flow

The project is structured as a chronological, reproducible pipeline.

*   **Data Ingestion:** Raw transactional data (525K rows) representing 2 years of online retail sales.
*   **Data Processing:** Feature engineering, outlier removal, and aggregation at the daily and customer level.
*   **Modeling Layer:**
    *   *Unsupervised:* K-Means and DBSCAN for customer segmentation.
    *   *Supervised (Time-Series):* Prophet, LSTM (PyTorch), and Hybrid Ensembling for demand forecasting.
    *   *Supervised (Classification):* XGBoost for churn prediction.
*   **Evaluation & Tracking:** Optuna for Bayesian hyperparameter tuning, Evidently for Data Drift detection, and MLflow for experiment tracking and model registry.
*   **Presentation Layer:** Streamlit web application.

---

## 3. Detailed Step-by-Step Implementation

### Phase 1: Data Foundation (Days 1-2)
*   **Objective:** Clean raw transactions and create foundational features.
*   **Actions Taken:**
    *   Removed canceled orders (quantities < 0) and missing customer IDs.
    *   Filtered out unrealistic unit prices.
    *   Engineered **RFM metrics** (Recency: days since last purchase, Frequency: total orders, Monetary: total spend).
    *   Aggregated data into `daily_sales_features.csv` (for forecasting) and `customer_rfm.csv` (for customer modeling).
*   **Business Rationale:** High-quality foundational data is required for accurate forecasting and modeling.

### Phase 2: Customer Intelligence (Day 3)
*   **Objective:** Group customers based on purchasing behavior to enable targeted marketing.
*   **Actions Taken:**
    *   Applied **K-Means clustering** to normalized RFM scores.
    *   Evaluated clusters using the Silhouette Score to determine the optimal number of segments (k=4).
    *   Used **DBSCAN** to identify extreme outliers (e.g., bulk wholesale buyers versus regular retail customers).
*   **Business Rationale:** Allows the business to treat highly-valued segments differently than at-risk segments, optimizing marketing spend.

### Phase 3: Demand Forecasting Models (Days 4-6)
*   **Objective:** Predict daily revenue 30 days into the future.
*   **Actions Taken:**
    *   **Time-Series Prep:** Conducted Augmented Dickey-Fuller (ADF) tests to confirm stationarity and decomposed the series into trend and seasonality.
    *   **Prophet Model:** Implemented Meta's Prophet model to capture strong weekly and monthly seasonality.
    *   **LSTM Model:** Built a Long Short-Term Memory neural network in PyTorch using a 30-day lookback window to capture non-linear, sequential patterns.
*   **Business Rationale:** Accurate demand forecasting is the prerequisite for supply chain optimization and cash flow planning.

### Phase 4: Hybrid Ensemble & Experiment Tracking (Days 7-8)
*   **Objective:** Maximize forecasting accuracy and ensure reproducibility.
*   **Actions Taken:**
    *   **MLflow:** Integrated MLflow to log all hyperparameters (e.g., LSTM layers, Prophet seasonality) and metrics (MAPE, RMSE).
    *   **Ensemble Modeling:** Combined Prophet and LSTM predictions. Tested simple averaging, inverse-error weighting, grid-search blending, and linear stacking. The optimal blend minimized the Mean Absolute Percentage Error (MAPE).
*   **Business Rationale:** Neural networks and statistical models have different strengths; combining them yields a more robust, stable forecast that is less susceptible to individual model errors.

### Phase 5: Churn Prediction & Explainability (Day 9)
*   **Objective:** Identify customers who are likely to stop purchasing.
*   **Actions Taken:**
    *   Defined churn as 90+ days without a purchase.
    *   Trained an **XGBoost Classifier** on historical RFM data. Handled class imbalance using `scale_pos_weight`.
    *   Implemented **SHAP (SHapley Additive exPlanations)** to interpret the model, outputting exactly *why* a specific customer was flagged as high risk.
*   **Business Rationale:** Acquiring a new customer is significantly more expensive than retaining an existing one. Predicting churn allows for proactive retention campaigns.

### Phase 6: Inventory Optimization (Day 10)
*   **Objective:** Mathematically determine stock levels.
*   **Actions Taken:**
    *   Calculated **Safety Stock** for 90%, 95%, and 99% service levels using the standard deviation of historical demand.
    *   Calculated the **Reorder Point** incorporating lead times.
    *   Calculated the **Economic Order Quantity (EOQ)** using standard holding and ordering cost assumptions.
    *   Built a historical simulation to test if these parameters would have prevented stockouts.
*   **Business Rationale:** Minimizes capital tied up in excess inventory while mathematically guaranteeing a specific service level (fill rate) for customers.

### Phase 7: Model Refinement & Drift Detection (Days 11-14)
*   **Objective:** Ensure models are robust, tuned, and not degrading over time.
*   **Actions Taken:**
    *   **Optuna Tuning:** Ran 50 trials of Bayesian optimization to find the absolute best hyperparameters for the XGBoost churn model, using 5-fold stratified cross-validation.
    *   **Data Drift:** Calculated Population Stability Index (PSI) and Kolmogorov-Smirnov (KS) tests comparing the first 18 months of data to the last 6 months to detect distribution shifts in purchasing behavior.
    *   **Walk-Forward CV:** Implemented expanding-window cross-validation for the time-series models to prove the model's accuracy holds up across different historical periods, not just a single train/test split.
*   **Business Rationale:** Proves to stakeholders that the models are mathematically rigorous, fully optimized, and monitored for real-world degradation.

---

## 4. How to Run the Application

The final deliverable is containerized and accessible via a Streamlit web interface.

### Running Locally (Python)
1. Install requirements:
   ```bash
   pip install -r dashboard/requirements.txt
   ```
2. Run the application:
   ```bash
   streamlit run dashboard/app.py
   ```
3. Open `http://localhost:8501` in your browser.

### Running via Docker
1. Build the image:
   ```bash
   docker build -t retailpulse .
   ```
2. Run the container:
   ```bash
   docker run -p 8501:8501 retailpulse
   ```

---

*This project was developed as a comprehensive demonstration of full-stack data science: moving from raw unstructured data to engineered features, complex modeling, robust evaluation, and finally, executive-level business intelligence delivery.*
