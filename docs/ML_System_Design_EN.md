# Machine Learning System Design Document - Demand Forecasting

## 1. Goals and Premises
### 1.1. Business Goals
Supermegaretaillite is a marketplace encompassing thousands of consumer and office electronics products. These categories have unique characteristics, demand, and supply cycles, which category managers need to consider when planning purchases. Before selling any product, Supermegaretaillite must procure it in the necessary volumes from suppliers. Due to limited warehouse space, the category manager must consider several key aspects when purchasing products:
- **Out-of-stock**: When the required product is not in stock, and the next shipment will arrive only after several days. As a result, the customer turns to competitors, leading to lost profits.
- **Overstock**: When a product "stagnates" and does not sell, requiring liquidation by significantly lowering the price and selling below cost to free up warehouse space.
- **Lost profit**: The revenue lost due to out-of-stock situations.
- **Inventory turnover**: The time from when a product arrives at the warehouse until it is shipped to the customer.

The goal of this ML service development project is to increase Supermegaretaillite's profits and optimize the work of category managers. Currently, their approach involves calculating the average sales of a product over the past n days and multiplying it by the number of days for which the purchase is made. This method does not account for seasonality, demand, and supply history. Therefore, the management of Supermegaretaillite decided to invest in developing an automated supplier purchasing management system, including the development of an ML service for demand forecasting.

### 1.2. Current Process Analysis
Currently, product ordering is done manually by the category manager based on intuition. This method does not scale well and has several drawbacks, such as the manager's illness or resignation.

### 1.3. Advantages of Using ML
Our ML solution automates the purchasing process, considering sales history, seasonality, and other factors affecting demand. In theory, this will increase profits and optimize the work of category managers, as well as eliminate human factors like illness or resignation.

### 1.4. Cost Evaluation
Our development budget consists of:
1. ML engineer salary: 100,000 rubles per month
2. Cloud computing resources rental (servers, PostgreSQL, S3): 5,000 rubles per month

### 1.5. Business Requirements and Constraints
#### 1.5.1 Business Requirements
- **Accuracy**: The model should reduce Out-of-stock and Overstock rates by 10%. Currently, Out-of-stock is 15-20%, and Overstock is 20-30%, which will increase inventory turnover and raise profits by 10%.
- **Response Time**: The service should respond to requests within 3-5 seconds.
- **Operational Reliability**: The service should be available 24/7, with daily backups of all databases sent to two independent storage locations.

#### 1.5.2 Business Constraints
- **Timeframe**: The first version of the service should be ready within one month.

#### 1.5.3 MVP Integration Steps
- **Optimal ML Model Search**: Conduct research and determine the optimal ML model for demand forecasting.
- **Data Collection and Storage Organization**: Create a PostgreSQL and S3 database for storing data for model training and testing.
- **Model Training**: Train the model on the collected data.
- **Testing**: Write integration, unit, and functional tests for the service to prevent production issues.
- **Streamlit Interface Development**: Develop a Streamlit interface for category managers to interact with the service.
- **MVP Launch**: Launch the MVP for a limited store and a limited number of products.

#### 1.5.4 MVP Success Criteria
- **Response Time**: The service should respond to requests within 3-5 seconds.
- **Operational Reliability**: The service should be available 24/7, with daily backups of all databases sent to two independent storage locations.
- **Service Accuracy**: The service should reduce Out-of-stock and Overstock rates by 10%. Currently, Out-of-stock is 15-20%, and Overstock is 20-30%, which will increase inventory turnover and raise profits by 10%.

### 1.6. Project Scope and Exclusions
#### 1.6.1 Scope
- Development and interpretation of a robust demand forecasting model.
- Integration of the service with the PostgreSQL database and S3 storage.
- Development of an ML service for demand forecasting for Supermegaretaillite as a Streamlit application.
- Testing and monitoring.

#### 1.6.2 Exclusions
- Does not include optimizing the model's and service's speed.
- Does not include developing a supply and order management system.
- Does not include experiments with CatBoost, Prophet, ETNA, feature engineering, and other model improvements.

## 2. Methodology

### 2.1. Problem Definition
The main business problems are out-of-stock and overstock situations, leading to low turnover and lost profits. To solve this problem, a demand forecasting model needs to be developed, considering all these factors.

In this MVP version, we will use quantile regression for demand forecasting because the business is interested not only in demand forecasting but also in specific issues: out-of-stock, overstock, and lost profit. We also need to manage the confidence level in forecasts so that category managers can make decisions based on risk, which can be achieved with quantile regression.

Forecasting inevitably involves errors. For different products, these errors can vary. Therefore, it is essential to consider different aspects of the "demand distribution" for each product. In some cases, overestimation is critical, in others — underestimation.

To solve these problems, we will forecast not only average sales for the next N days but also quantile forecasts. Each quantile represents a forecast with a different confidence level:

- 0.1 quantile — "pessimistic" forecast (90% of the time, the forecast is below actual sales);
- 0.5 quantile — "conservative" forecast (50% of the time, actual sales are higher, 50% — lower);
- 0.9 quantile — "optimistic" forecast (90% of the time, the forecast is above actual sales).

For example, for product 1, the quantile sales forecasts for the next two weeks may be as follows:

- 0.1 quantile (pessimistic forecast) — 3 units (90% probability that sales will be 3 units or more);
- 0.5 quantile (conservative forecast) — 5 units;
- 0.9 quantile (optimistic forecast) — 8 units (90% probability that sales will be 8 units or less).

This allows category managers to make purchasing decisions based on needs and risk levels.

Additionally, we use statistical methods such as bootstrapping to estimate the error magnitude and confidence in forecasts. Bootstrapping allows creating confidence intervals, providing information about the range of values. This is significantly more useful than a point estimate of the average value, which does not account for the error magnitude.

### 2.2. Metrics Selection

#### 2.2.1. Offline Metrics
Offline metrics allow assessing the model's quality on historical data before its real-time deployment.

- **Quantile Loss**: The primary loss function we will optimize. This metric assesses the quality of forecasts for various quantiles (0.1, 0.5, 0.9) and penalizes underestimation and overestimation depending on the chosen quantile. The formula for quantile loss:
  \[
  L(y, p; q) = q \cdot \max(y - p, 0) + (1 - q) \cdot \max(p - y, 0)
  \]
  where:
  - \( y \) — actual value,
  - \( p \) — predicted value,
  - \( q \) — quantile (0.1, 0.5, 0.9).

- **RMSE**: Root Mean Squared Error. This metric allows assessing the overall accuracy of the model. RMSE shows how much the predicted values deviate from the actual values. We will also use this metric as a proxy for comparing our initial model (quantile regression) with other models.

- **Coverage Probability**: The proportion of actual sales values that fall within the interval between predicted 0.1 and 0.9 quantiles. This is important for assessing the reliability of forecast intervals.

#### 2.2.2. Online Metrics
- **Prediction Interval Coverage Probability (PICP)**: The proportion of actual values that fall within the predicted interval between quantiles 0.1 and 0.9. This is similar to the coverage probability metric but measured in real-time.

- **Real-time Quantile Loss**: Similar to offline quantile loss but measured in real-time. This metric allows assessing the model's accuracy in current sales conditions.

- **Uptime**: The time during which the service was available. This is an important metric as we need to track whether the service is available and take measures to restore it if not.

#### 2.2.3. Business Metrics
Business metrics evaluate the model's impact on key business performance indicators.

- **Out-of-stock Rate**: The proportion of time when a product is out of stock. Reducing this metric indicates improved demand forecasts and, consequently, better inventory management.

- **Overstock Rate**: The proportion of time when a product is overstocked. Reducing this metric indicates more accurate demand forecasts and lower storage costs.

- **Lost Profit**: The amount of lost revenue due to out-of-stock situations. This metric allows assessing the direct impact of forecast accuracy on

 company revenue.

- **Inventory Turnover**: Higher turnover indicates effective inventory management, leading to lower costs and improved cash flow.

### 2.3. Object and Target Definition
For each row in the dataset (a row represents a product-day), we will calculate the following features:
- Average sales for the last N days.
- X-th quantile of sales for the last N days.

For the target, we will calculate:
- Total sales for the next N days.

### 2.4. Data Collection
Table demand_orders_status (order statuses):
- order_id – unique order number.
- status_id – status identifier.
- status – status name.

Table demand_orders (orders table):
- order_id – unique order number.
- timestamp – date and time when the order was placed.
- sku_id – unique product identifier.
- sku – product name.
- price – product price, which remains unchanged throughout the day.
- qty – quantity of product in the order.
- status_id – status identifier of the order.

### 2.5. Data Preparation
The atomic unit of the dataset will be product-day (sku, day). Accordingly, each forecast will be made for each point in time (each day) and each product for a certain period in the future (1-2-3-4 weeks).

To calculate both future sales aggregates (targets) and past sales aggregates (features), we need daily sales aggregates.

For each product-day, we will calculate the total sales quantity (qty) and obtain the following table:
- day – day.
- sku_id – unique product identifier.
- sku – product name.
- price – product price on the current day.
- qty – total sales quantity of the product on the current day.

However, the simple qty value is not enough, so we will calculate the necessary features and target variables using window functions: a sliding window into the past to calculate features and a sliding window into the future to calculate the target.

## 3. Pilot Version Training

### 3.1. ML Solution Architecture
#### 3.1.1. Basic Solution
The basic solution will be a quantile regression model, as mentioned earlier. We will use the quantile loss function to optimize the model for various quantiles (0.1, 0.5, 0.9). The model will forecast quantile sales values for the next N days.

Our training pipeline is as follows:

![pipeline](../images/Demand_Forencast_Pipeline.jpg)

#### 3.1.2. Improvements After the Basic Solution
After training the basic model, we will evaluate its performance and make improvements based on the results. We will experiment with various models, such as CatBoost, Prophet, and ETNA, to find the best model for demand forecasting. We will also experiment with different features, such as price, discounts, and promotions, to improve the model's performance. But not in this MVP version.

### 3.2. Preliminary Quality Assurance
Before launching the service, we will conduct a series of tests to ensure the model's and service's quality. We will test the model's performance on historical data and evaluate its accuracy, coverage probability, and quantile loss. We will also test the service's response time and reliability to ensure it meets business requirements. We will also ask category managers to evaluate the service and provide feedback on its accuracy, stability, and usefulness.

### 3.3. Pilot Project Evaluation Method
- **Functional Requirements**: The service must be available 24/7 and respond to requests within 3-5 seconds in Streamlit.
- **Non-functional Requirements**: The service must be reliable and minimize failures and errors in forecasts according to the metrics described above on historical data (for one past year).

### 3.4. Pilot Project Success Criteria
If we can confirm the points from section 1.5.4 on historical data, the pilot project is considered successful.

### 3.5. Infrastructure and Scalability
We will use the following infrastructure for the pilot project:
- **Service**: We will need two servers for our task: one will contain the ML service, databases, and web interface, and the other will be used for monitoring and storing backups. Both servers will have 2 CPU cores, 4 GB of RAM, and 16 GB of storage.

### 3.6. Monitoring
We will monitor the service's performance using Grafana, Prometheus, and Uptime Kuma tools to track the metrics from section 2.2.

### 3.7. System Operation Requirements
The system must be available 24/7 and respond to requests within 3-5 seconds. The service must be reliable and minimize failures and errors in forecasts according to the metrics discussed above on historical data (for one past year). A backup of all databases will be created daily and sent to another independent server. The service must also automatically restart containers upon reboot.

### 3.8. System Security

#### 3.8.1. Data Encryption
We will use HTTPS for secure data transmission and encrypt stored data to prevent unauthorized access, limiting server access to whitelisted IPs. We can also protect databases from SQL injections using ORM (Object-Relational Mapping) and prepared statements.

#### 3.8.2. Authentication and Access Management
Access to the service should be restricted: we control the issuance of the root password for the server (it should be known only to the architect and ML engineer), and in all other cases, we issue an SSH key, which can be deleted at any time, thereby restricting access. We can also use HashiCorp Vault to manage access to credentials and secrets.

#### 3.8.3. Credential Security
Sensitive credentials will not be stored openly in code repositories. We will use environment variables and secure secret management tools to handle credentials securely. In the future, we may also use HashiCorp Vault for secret management.

### 3.9. Risks
- **Data Quality**: Poor data quality can lead to inaccurate forecasts. We will address this issue by cleaning and preprocessing data before training the model and writing tests to check data quality.
- **Model Performance**: The model may provide inaccurate forecasts, leading to out-of-stock or overstock situations. We will address this issue by monitoring the model's performance and not releasing the model to production unless it exceeds the metrics established in the metrics section on historical data.
- **Service Reliability**: A critical error can lead to the loss of all data on the server. We will address this issue by creating backups of all databases and sending them to two independent storage locations daily.
- **Forecast Errors**: Inaccurate forecasts can lead to lost profits and overstock situations. We will address this issue by monitoring the model's performance and not releasing the model to production unless it exceeds the metrics established in the metrics section on historical data. We will also use the service for one store and a limited number of products to evaluate the model's accuracy and performance before a full-scale launch for all stores and products.

## 4. Pilot Project Implementation

### 4.1. MVP Implementation Stages
The pilot project will include a limited store and a limited number of products. This will allow evaluating the service's accuracy and performance in real conditions before a full-scale launch.

#### 4.1.1. Prototyping and Preliminary Experiment
We will start by collecting and processing data from PostgreSQL and S3 for training the model on historical data. Then we will develop a Streamlit interface for category managers to interact with the service.

#### 4.1.2. Testing
We will test the service on historical data and evaluate its performance based on the discussed metrics. We will also ask category managers to evaluate the service and provide feedback on its accuracy, stability, and usefulness. Additionally, we will write integration (checking the interaction between components), unit (checking individual components), and functional (checking functionality) tests for the service to prevent production issues.

#### 4.1.3. MVP Launch
After testing the service on historical data and receiving feedback from category managers, we will launch the service for a limited store and a limited number of products. We will monitor the service's performance and evaluate its accuracy, coverage probability, and quantile loss. We will also track response time and service reliability to ensure it meets business requirements.

#### 4.1.4. Feedback Analysis
After the MVP launch, we will analyze feedback from category managers and evaluate the service's performance based on the discussed metrics. We will also monitor the service's performance and evaluate its accuracy, coverage probability, and quantile loss. We will also track response time and service reliability to ensure it meets business requirements.
