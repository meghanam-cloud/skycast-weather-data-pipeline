# SkyCast – Weather Data Pipeline (AWS)

SkyCast is a serverless weather data pipeline built on AWS.  
It fetches real-time weather data for a given location, processes it using AWS Lambda, and stores historical data in Amazon S3 for analysis.


##  Project Overview

This project demonstrates how to build an end-to-end, serverless data ingestion pipeline using AWS services.

Users can request weather data for any city by providing latitude and longitude.  
The system fetches live weather data from an external API, processes it, and appends the data to a CSV file stored in Amazon S3.


##  Architecture

**Flow:**

API Gateway → AWS Lambda → OpenWeather API → Amazon S3 (CSV)

**Components:**
- **API Gateway** – Exposes an HTTP endpoint for requesting weather data
- **AWS Lambda (Python)** – Fetches and processes live weather data
- **OpenWeather API** – External data source
- **Amazon S3** – Stores historical weather data as CSV


##  How the Pipeline Works

1. A user calls the API Gateway endpoint with latitude and longitude.
2. API Gateway triggers the Lambda function.
3. Lambda fetches real-time weather data from OpenWeather.
4. The response is cleaned and flattened into a structured format.
5. A new row is appended to a CSV file in Amazon S3.
6. The API returns a success response with the processed data.


##  Data Stored in S3

Each API call appends a new row with fields such as:

- Timestamp (IST)
- City
- Latitude & Longitude
- Temperature (current, min, max, feels like)
- Humidity & Pressure
- Weather condition
- Wind speed & direction

This creates a historical time-series dataset.


##  Analytics (Optional)

Dashboards were created in Amazon QuickSight during development to validate analytics and trends.  
QuickSight was later disabled to avoid recurring costs.  
Screenshots are included for reference.


##  Technologies Used

- AWS Lambda (Python)
- Amazon API Gateway
- Amazon S3
- OpenWeather API
- Amazon QuickSight (validation only)


## Security & Best Practices

- API keys and configuration values are managed using Lambda environment variables
- No secrets are committed to the repository
- Serverless architecture ensures scalability and cost efficiency


##  Screenshots

Screenshots showing:
- API response
- CSV data in S3
- Sample dashboard

are available in the `screenshots/` folder.
