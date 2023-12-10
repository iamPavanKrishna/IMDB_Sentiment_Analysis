# Sentiment Analysis Flask App

## Overview

This Flask app performs sentiment analysis on user-provided movie reviews. It uses a machine learning model to predict sentiment and stores the results in a MySQL database.

## Live Demo
http://34.93.227.66

## Prerequisites

- Docker: Ensure Docker is installed on your machine. [Install Docker](https://docs.docker.com/get-docker/)
- Docker Compose: Ensure Docker Compose is installed. [Install Docker Compose](https://docs.docker.com/compose/install/)

## How to Run

1. Clone the repository:

   ```bash
   git clone https://github.com/iamPavanKrishna/IMDB_Sentiment_Analysis.git
    ```
2. Navigate to the project directory:

   ```bash
   cd IMDB_Sentiment_Analysis
   ```  
3. Build the Docker image:

   ```bash
    docker-compose up --build
    ```
This command will download the necessary images, build the Docker containers, and start the Flask app and MySQL services.

4. Access the app:

    Open your web browser and go to http://localhost:5000 to access the Sentiment Analysis app.

5. Perform Sentiment Analysis:

    Enter a movie review in the provided form and click "Predict" to see the sentiment prediction.
    The results are stored in the MySQL database and displayed on the homepage.

### Additional Information
The MySQL database is running in a Docker container, and the Flask app is accessible at http://localhost:5000.

To stop the application, press Ctrl+C in the terminal where Docker Compose is running, and then run:

```bash
docker-compose down
```
Customize the Flask app by modifying the code in the app directory.
