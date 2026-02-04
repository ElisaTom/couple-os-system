# Lifestyle & Relationship Management System

**Status:** Active Development
**Stack:** Python, Streamlit, Scikit-Learn, Google Sheets API

## Project Overview

This repository contains the source code for a centralized, serverless web application designed to optimize shared decision-making and experience logging. The system functions as a data-driven operating system for couple management, utilizing statistical analysis and machine learning to reduce decision fatigue and track satisfaction metrics over time.

## Technical Architecture

The application is built on a serverless architecture using Streamlit for the frontend and application logic, while leveraging Google Sheets as a lightweight, cloud-based NoSQL database for persistence.

* **Frontend & Logic:** Streamlit (Python 3.x)
* **Data Processing:** Pandas, NumPy
* **Machine Learning:** Scikit-Learn (TF-IDF Vectorization, Cosine Similarity)
* **Visualization:** Plotly Express (Interactive Radar Charts and Time Series)
* **Database:** Google Sheets API (via `streamlit-gsheets`)

## Installation and Setup

### Prerequisites
* Python 3.9+
* Google Cloud Platform Service Account (for Sheets API access)

### Local Development

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/elisatom/activity-management.git](https://github.com/elisatom/activity-management.git)
    cd activity-management
    ```

2.  **Initialize Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run Application**
    ```bash
    streamlit run app.py
    ```

## License

Private Repository. All rights reserved.