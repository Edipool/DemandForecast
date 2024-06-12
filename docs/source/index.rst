.. Eduard Poliakov documentation master file, created by
   sphinx-quickstart on Fri May 17 11:15:33 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Eduard Poliakov's documentation!
===========================================

.. toctree::
   :maxdepth: 4
   :caption: Contents:

   modules

Demand Forecast
===============

What is the project about?
--------------------------
Products such as electronics, household appliances have varying characteristics and demand cycles. Category managers, responsible for overseeing these items throughout their lifecycle, face challenges in planning purchases, especially when the assortment spans thousands of items. As data volume increases and platform complexity grows, traditional methods of inventory management and demand forecasting become less effective. In response to these challenges, Supermegaretaillite is investing in the development of an automated system, including an ML-based demand forecasting service.

To preserve the primacy of the source code, the SRC module is loaded in `PyPi <https://pypi.org/project/demand-forecast-source>`_ for further use in repositories `training-pipeline <https://github.com/Edipool/Demand_Forecast_Airflow>`_ and inference-pipeline.

How to use this project?
------------------------
This project is deployed on the server and is fully ready to work 24/7.
If you want to use this service, you need to:
1. Open `this <http://45.91.8.168:8501>`_ web address.
2. For example, you would like to know the demand for the product with SKU ID 20 for the next 7 days. You should fill in the fields in web service: SKU_ID = 20, Stock = 10, Horizon Days = 7, Confidence Level = 0.90.
3. Click the buttons:
    - "Get how much to order" to find out how much inventory you need to order from the supplier.
    - "Get stock level" to find out how much stock you will have in 7 days.
    - "Get low stock SKU ID" to find out which products will be out of stock in 7 days.

Project Pipeline
----------------
.. image:: ../images/Demand_Forencast_Pipeline.jpg

Main tools used
---------------
.. image:: https://img.shields.io/badge/-MLOps-090909?style=for-the-badge&logo=MLOps
.. image:: https://img.shields.io/badge/-ML_System_Design-090909?style=for-the-badge&logo=ML_System_Design
.. image:: https://img.shields.io/badge/-Streamlit-090909?style=for-the-badge&logo=Streamlit
.. image:: https://img.shields.io/badge/-Fastapi-090909?style=for-the-badge&logo=Fastapi
.. image:: https://img.shields.io/badge/-DVC-090909?style=for-the-badge&logo=DVC
.. image:: https://img.shields.io/badge/-Amazon_S3-090909?style=for-the-badge&logo=Amazon_S3
.. image:: https://img.shields.io/badge/-mlflow-090909?style=for-the-badge&logo=mlflow
.. image:: https://img.shields.io/badge/-Docker-090909?style=for-the-badge&logo=Docker
.. image:: https://img.shields.io/badge/-docker_compose-090909?style=for-the-badge&logo=docker_compose
.. image:: https://img.shields.io/badge/-Scikit_learn-090909?style=for-the-badge&logo=Scikit_learn
.. image:: https://img.shields.io/badge/-Grafana_data-090909?style=for-the-badge&logo=Grafana
.. image:: https://img.shields.io/badge/-CI/CD-090909?style=for-the-badge&logo=CI/CD

Project Organization
--------------------
.. code-block:: text

    .
    ├── app.py                <--- FastAPI app
    ├── configs               <--- Configs for this project
    │   └── train_config.yaml     <--- Training configuration file
    ├── data                  <--- Data for this project
    │   ├── external              <--- External data sources
    │   ├── interim               <--- Intermediate data
    │   ├── processed             <--- Processed data ready for analysis
    │   │   ├── features_targets.csv  <--- Features and targets for training
    │   │   ├── predictions.csv     <--- Model predictions
    │   │   └── sku_demand_day.csv  <--- Demand forecast for each SKU
    │   └── raw                   <--- Raw data before processing
    │       ├── demand_orders.csv  <--- Demand orders data
    │       ├── demand_orders_status.csv  <--- Demand orders status data
    │       ├── features.csv     <--- Features data
    │       └── sales.csv       <--- Sales data
    ├── data.dvc               <--- DVC data tracking file
    ├── docker-compose.yml     <--- Docker Compose configuration
    ├── Dockerfile             <--- Dockerfile for building the project container
    ├── docs                   <--- Documentation for this project
    │   ├── Makefile               <--- Makefile for building docs
    │   └── ML_System_Design.md    <--- ML System Design document
    ├── dvc.lock               <--- DVC lock file
    ├── dvc.yaml               <--- DVC pipeline definition
    ├── images                 <--- Images used in documentation
    │   └── Demand_Forencast_Pipeline.jpg
    ├── __init__.py            <--- Package initializer
    ├── LICENSE                <--- License for this project
    ├── logs                   <--- Logs generated by the application
    │   ├── app.log
    ├── Makefile               <--- Makefile for various build tasks
    ├── MANIFEST.in            <--- Manifest for package distribution
    ├── models                 <--- ML models and associated files
    │   ├── losses.json            <--- Model training losses
    │   └── model.pkl              <--- Serialized model
    ├── notebooks              <--- Jupyter notebooks for exploration and analysis
    │   └── EDA.ipynb              <--- Exploratory Data Analysis notebook
    ├── project_structure.txt  <--- Project structure description
    ├── prometheus_data        <--- Prometheus monitoring configuration
    │   ├── app_metrics.py         <--- Application metrics for Prometheus
    │   └── prometheus.yml         <--- Prometheus configuration file
    ├── README.md              <--- Readme file with project overview
    ├── requirements.txt       <--- Python dependencies
    ├── setup.cfg              <--- Setup configuration
    ├── setup.py               <--- Setup script for installing the package
    ├── src_demand_forecast    <--- Source code for demand forecast
    │   ├── data                   <--- Data processing scripts
    │   │   ├── __init__.py
    │   │   └── split_dataset.py   <--- Script for splitting the dataset
    │   ├── download               <--- Data download scripts
    │   │   ├── download_from_s3.py<--- Script to download data from S3
    │   │   └── __init__.py
    │   ├── entities               <--- Entity definitions
    │   │   ├── feature_params.py
    │   │   ├── __init__.py
    │   │   ├── model_params.py  <--- Model parameters
    │   │   ├── split_params.py  <--- Split parameters
    │   │   ├── train_pipeline_params.py  <--- Training pipeline parameters
    │   │   └── validation_params.py  <--- Validation parameters
    │   ├── features               <--- Feature engineering scripts
    │   │   ├── AddFeatures.py  <--- Script for adding features
    │   │   ├── AddTargets.py  <--- Script for adding targets
    │   │   ├── build_sku_by_day.py  <--- Script for building SKU demand by day
    │   │   ├── build_transformer.py  <--- Script for building a transformer
    │   │   └── __init__.py
    │   ├── inference              <--- Inference scripts
    │   │   ├── __init__.py
    │   │   └── make_request.py    <--- Script for making inference requests
    │   ├── __init__.py
    │   ├── models                 <--- Model training and evaluation scripts
    │   │   ├── __init__.py
    │   │   ├── repro_experiments.py <--- Reproducibility experiments
    │   │   └── train_model.py     <--- Model training script
    │   ├── upload                 <--- Data upload scripts
    │   │   ├── __init__.py
    │   │   └── s3_storage.py      <--- Script to upload data to S3
    │   └── visualization          <--- Data visualization scripts
    │       ├── __init__.py
    │       └── visualize.py       <--- Script for visualizing data
    ├── tests                  <--- Unit tests for the project
    │   ├── app                    <--- Tests for the FastAPI app
    │   │   └── test_streamlit_app.py  <--- Tests for the Streamlit app
    │   ├── conftest.py          <--- Pytest configuration
    │   ├── data                   <--- Tests for data processing
    │   │   └── test_data.py     <--- Tests for data processing
    │   └── models                 <--- Tests for models
    ├── tox.ini                <--- Tox configuration for testing
    ├── train_pipeline.py      <--- Script for running the training pipeline
    └── web_app                <--- Web application scripts
        ├── Dockerfile         <--- Dockerfile for the web application
        ├── __init__.py
        ├── requirements.txt  <--- Python dependencies for the web application
        └── streamlit_app.py    <--- Streamlit web application
