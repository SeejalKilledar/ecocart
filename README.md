# EcoCart Logistic 

## Features
| Module |
| ** Route Optimizer **| DFS, BFS, A*, IDA*
| ** Inventory Forcast **| Random Forest Regressor - 200 Decision Trees
| ** Customer Segmentation **| K-means clustering and Bias Detection mitigation toggle

## Project Structure

```
ecocart/
├── manage.py
├── requirements.txt
├── ecocart/               # Django project config
│   ├── settings.py
│   └── urls.py
├── dashboard/             # Home page & AI Agents overview
├── route_optimizer/       # DFS, BFS, A*, IDA* algorithms
│   └── algorithms.py
├── inventory/             # ML demand forecasting (Random Forest)
│   └── ml_model.py
├── customer_segment/      # K-Means + bias analysis
│   └── segmentation.py
├── templates/             # HTML templates (Bootstrap 5)
└── static/                # CSS / JS assets

