# Game Analytics & Player Engagement Platform

An end-to-end analytics and machine learning project for analyzing player behavior, engagement, monetization, and risk.

## Features

- Player and genre analytics using SQL
- Engagement and monetization KPIs
- Statistical analysis and hypothesis testing
- Player purchase prediction using machine learning
- Player segmentation
- Anomaly detection
- Interactive Streamlit dashboard
- FastAPI prediction service
- Automated API testing with Pytest
- GitHub Actions CI
- Dockerized API deployment

## Tech Stack

- Python
- Pandas
- NumPy
- Scikit-learn
- SQL
- SQLite
- FastAPI
- Streamlit
- Pytest
- Docker
- GitHub Actions
- Matplotlib

## Project Structure

```text
game-analytics-platform/
├── api/
│   └── app.py
├── dashboard/
│   └── app.py
├── data/
│   ├── raw/
│   └── processed/
├── models/
├── notebooks/
├── sql/
├── src/
├── tests/
├── Dockerfile
├── requirements.txt
└── README.md
```
## Analytics

The project calculates player-level and business KPIs including:

Total players
Average sessions per week
Average weekly playtime
Average session duration
Total revenue
Purchase rate
At-risk player rate
Genre-level performance
Engagement-level performance
Player revenue rankings

SQL analysis uses aggregations, CTEs, and window functions.

## Machine Learning

A classification pipeline predicts whether a player is likely to make an in-game purchase.

Models evaluated:

Logistic Regression
Random Forest

The pipeline includes:

Numerical preprocessing
Categorical encoding
Feature scaling
Stratified train/test split
Precision
Recall
F1-score
ROC-AUC

The best-performing model is saved and served through the FastAPI application.

## Statistical Analysis

The project includes:

Welch's t-test for comparing player groups
Chi-square testing for categorical relationships
Correlation analysis

An A/B testing workflow is also included as a simulated educational experiment for demonstrating randomized conversion analysis and hypothesis testing.

## Anomaly Detection

Isolation Forest is used to identify unusual player behavior based on activity, progression, and monetization features.

## Dashboard

The Streamlit dashboard provides:

Overall player KPIs
Engagement analysis
Revenue by genre
Player segmentation
Anomaly analysis
Top revenue players
Genre and engagement filters

Run the dashboard with:

python -m streamlit run dashboard/app.py
API

The FastAPI service provides a prediction endpoint.

Start the API:

python -m uvicorn api.app:app --reload

API documentation is available at:

http://127.0.0.1:8000/docs
Docker

Build the image:

docker build -t game-analytics-api .

Run the container:

docker run -p 8000:8000 game-analytics-api

The API will be available at:

http://localhost:8000
Testing

Run the API tests:

python -m pytest tests/test_api.py -v

GitHub Actions is configured to automatically run the tests on pushes and pull requests to main.

## Dataset

The project uses a synthetic player-engagement dataset containing player activity, progression, game preferences, and monetization information.

Because the dataset is synthetic, the results should be interpreted as a demonstration of an analytics and machine learning workflow rather than real-world game or EA data.

## Limitations

The dataset does not contain detailed event-level timestamps, so true D7/D30 retention analysis cannot be performed.

The A/B testing component is simulated and is included to demonstrate the analytical methodology.

## Future Improvements
Event-level retention analysis
Real-time player activity ingestion
More advanced forecasting
Experimentation on real product data
Production-scale data warehouse integration