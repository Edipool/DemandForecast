Demand Forecast
==============================
## What is the project about
Products such as electronics, household appliances, clothing, and books have varying characteristics and demand cycles. Category managers, responsible for overseeing these items throughout their lifecycle, face challenges in planning purchases, especially when the assortment spans tens of thousands of items. As data volume increases and platform complexity grows, traditional methods of inventory management and demand forecasting become less effective. In response to these challenges, X6 is investing in the development of an automated system, including an ML-based demand forecasting service.

Project Organization
------------

    ├── LICENSE
    ├── .dvc              <- DVC files
    ├── .github           <- Github actions
    |    └── workflows
    |        └── python-package-conda
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    |   |   └── features_targets.csv
    |   |   └── predictions.csv
    |   |   └── sku_demand_day.csv
    │   └── raw            <- The original, immutable data dump.
    |       └── sales.csv
    |       └── features.csv
    |       └── demand_orders_status_2023_09_22.csv
    |       └── demand_orders_2023_09_22.csv
    |
    ├── grafana_data
    │
    |── config             <- Configuration files for the project
    |
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │   └── model.pkl
    │   └── losses.json
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    |
    ├── prometheus_data
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to split data on train and test sets
    │   │   └── split_dataset.py
    |   ├── entities       <- Scripts to create entities for modeling
    │   │   └── feature_params.py
    │   │   └── model_params.py
    │   │   └── split_params.py
    │   │   └── train_pipeline_params.py
    |   |   └── validation_params.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── AddFeatures.py
    │   |   └── AddTargets.py
    │   |   └── build_sku_by_day.py
    │   |   └── build_transformer.py
    │   ├── inference      <- Scripts to make predictions and requests to te app service
    │   │   └── make_request.py
    │   │
    │   ├── models         <- Scripts to train models and make experiments
    │   │   │
    │   │   ├── repro_experiments.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │   │    └── visualize.py
    │   │
    │   └── tests          <- Scripts to test the project
    │      └── conftest.py
    │      └── features_targets.csv
    │      └── features.csv
    │      └── sales.csv
    │      └── data
    │      │   └── test_data.py
    │      └── features
    │      │   └── test_features_targets.py
    │      └── models
    │
    ├── .dockerignore      <- Files to be ignored by docker
    ├── .dvcsconfig        <- Configuration file for dvc
    ├── .gitignore         <- Files to be ignored by git
    ├── app.py             <- FastAPI app
    ├── data.dvc           <- DVC file for data
    ├── Dockerfile         <- Dockerfile for building the app
    ├── dvc.lock           <- DVC lock file
    ├── dvc.yaml           <- DVC yaml file
    ├── test_environment.py <- Script to test the environment
    ├── train_pipeline.py  <- Script to train the model
    ├── docker-compose.yml <- Docker compose file
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
