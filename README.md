# EcoCart Logistic 

Foundations of AI - TABA 

## Features
| Module |
| ** Route Optimizer **| DFS, BFS, A*, IDA*
| ** Inventory Forcast **| Random Forest Regressor - 200 Decision Trees
| ** Customer Segmentation **| K-means clustering and Bias Detection mitigation toggle

## Setup and Run

### Download the project
Create a folder (ex: taba) in any drive (created in D drive)

### 2. Create virtual environment
open cmd
D: 						| Move to the location C or D drive
pip install virtualenv
cd taba 				
virtualenv taba_env     | creating virtual environment named taba_env
cd taba_env
cd Scripts
Activate

### 2. Install Dependencies
pip install -r requirements.txt
pip install django
pip install numpy
pip install -U scikit-learn

### 3. Open the project in IDE


### 4. Apply migrations 
Folder --> Run in the folder that has manage.py ((taba_env) D:\taba\ecocart>)
python manage.py makemigrations
python manage.py migrate
 
### 5. Run Server
python manage.py runserver

### 6. Open in Browser
http://127.0.0.1:8000/


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

