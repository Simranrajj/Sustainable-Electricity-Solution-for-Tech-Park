# Sustainable Energy Forecasting for Commercial Tech Parks

## 1. Project Overview

This project is an end-to-end data science solution designed to help a Real Estate Investment Trust (REIT) forecast monthly electricity consumption for tenants in a commercial tech park. The goal is to enable proactive energy management, identify efficiency opportunities, and provide tenants with data-driven insights into their usage, ultimately promoting sustainability and reducing operational costs.

## 2. Technology Stack

* **Data Engineering & Analysis:** Python (Pandas, NumPy)
* **Machine Learning:** Scikit-learn, LightGBM
* **Data Visualization:** Power BI, Matplotlib, Seaborn

## 3. Methodology

#### Data Engineering
A realistic, 10-year synthetic dataset was custom-built for this project as real-world data was unavailable. The process involved:
* Researching the tenant profiles and building characteristics of Manyata Tech Park in Bengaluru.
* Integrating historical weather data for the region to model its impact on energy usage (e.g., higher AC use on hotter days).
* Simulating realistic data patterns, including daily, weekly, and seasonal consumption cycles, and introducing controlled missing values and errors to replicate real-world data quality challenges.

#### Predictive Modeling
A LightGBM regression model was trained to predict the "Electricity Reading (kWh)" for each tenant.
* Features included tenant industry type, number of employees, day of the week, month, and weather conditions.
* The model provides accurate forecasts that can be used for resource planning and billing estimations.

## 4. Final Dashboard Showcase

An interactive Power BI dashboard was designed as the frontend to present the model's predictions and provide analytical insights.

*(Note: The original `.pbix` file was unfortunately lost due to a local file system error. The following screenshots are from the completed project and demonstrate the final user interface and functionality.)*

### Summary Page
*This page provides a high-level overview with key performance indicators (KPIs) and the main prediction module.*
!(YOUR_IMAGE_LINK_HERE_FOR_MTP1.JPG)

### Electricity Analysis Page
*This page allows for a deeper dive into historical electricity consumption trends by industry, day of the week, and year.*
!(YOUR_IMAGE_LINK_HERE_FOR_MTP2.JPG)

### Tenant Analysis Page
*This page focuses on tenant-specific metrics like energy efficiency and energy usage per employee.*
!(YOUR_IMAGE_LINK_HERE_FOR_MTP3.JPG)
