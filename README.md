# Spotify Data Engineering ETL Pipeline (API → MySQL → Streamlit)

# Author: Thaadshaayani Rasanehru

This project implements a complete end-to-end data engineering pipeline using the Spotify Web API, Python ETL, MySQL for storage, and Streamlit dashboards for analytics.
It includes both a local MySQL-powered dashboard and a cloud-deployable CSV dashboard.

# 1. Project Overview
This system extracts music data such as tracks and artists from the Spotify API, processes it through a Python ETL workflow, stores it in a MySQL database, exports cleaned datasets to CSV, and visualizes insights using Streamlit.

Two deployment paths are supported:

# Local Workflow (Live MySQL Dashboard)
Spotify API → ETL (Python) → MySQL → Streamlit Dashboard (Local)

# Cloud Workflow (Streamlit Cloud Dashboard)
Spotify API → ETL (Python) → MySQL → CSV Export → Streamlit Dashboard (Cloud)

This dual approach allows both real-time database analytics and cloud-friendly deployment without a database server.

# 2. Architecture
High-Level Architecture Diagram

               Spotify API
                    ▼
                Python ETL          
        Extract • Transform • Load            
        └───────────────────────┘
                    ▼
               MySQL Database
        ┌───────────┴───────────────┐   
        ▼                           ▼
  CSV Export Layer           Streamlit Dashboard
  (tracks.csv,               (Local • uses MySQL)
   artists.csv)
        ▼
Streamlit Cloud Dashboard
(Cloud • uses CSV files)


# 3. Features
ETL Pipeline

- Extracts playlist, track, and artist data from Spotify API
- Cleans and normalizes track names
- Identifies BTS vs collaborator tracks
- Enriches artist records (followers, popularity, genres)
- Loads datasets into MySQL with UPSERT logic

Dashboards
- Track analytics
- Artist analytics
- Popularity distribution
- Song duration analysis
- Song version counts
- BTS vs collaborator breakdown
- Consistent UI for both Cloud and Local versions

Storage
- MySQL relational schema
- Optional CSV export for cloud deployment

# 4. Project Structure

project/
│
├── etl/
│   ├── spotify_client.py
│   ├── transform.py
│   ├── load.py
│   ├── run_etl.py
│   ├── test_extract.py
│   └── config.py
│
├── data/
│   ├── tracks.csv
│   ├── artists.csv
│
├── appmysql.py          # Local dashboard (MySQL)
├── appcsv.py            # Cloud dashboard (CSV)
├── export_to_csv.py
├── schema.sql
├── requirements.txt
└── README.md

# 5. Setup Instructions
 # 5.1 Install Dependencies

pip install -r requirements.txt

 # 5.2 Configure Environment Variables
Create a .env file:

SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret

MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=spotify
MYSQL_PORT=3306

# 5.3 Initialize MySQL Schema
Run the contents of schema.sql in your database.

python -m etl.run_etl

The script will:
- Authenticate with Spotify
- Fetch playlist data
- Transform and normalize fields
- Load results into MySQL tables

# 7. Exporting Data to CSV (Cloud Dashboard)

python export_to_csv.py

This generates:
data/tracks.csv
data/artists.csv

These files should be committed to GitHub for Streamlit Cloud deployment.

# 8. Running Streamlit Dashboards
  # 8.1 Local Dashboard (MySQL)

streamlit run appmysql.py

# 8.2 Cloud Dashboard (CSV files)
streamlit run appcsv.py

For Streamlit Cloud deployment:
- Upload project to GitHub
- Ensure data/*.csv files are included
- Point Streamlit Cloud to appcsv.py

# 9. Technical Stack
- Python
- Spotify Web API
- MySQL
- SQLAlchemy
- Pandas
- Streamlit
- dotenv
- CSV Export Layer

# 10. Future Improvements
- Add audio feature analysis
- Add time-series growth trends
- Add genre breakdown visualization
- Airflow or Prefect scheduling
- Deployment using Docker
- ML model for popularity prediction

# 11. Author

Thaadshaayani Rasanehru
Data Engineering | Data Science | Analytics

This project demonstrates practical experience with ETL pipelines, API integration, relational databases, and dashboard engineering.
