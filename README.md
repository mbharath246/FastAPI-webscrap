# Webscrap-using-FastAPI
  This project involves web scraping data from Hacker News, storing it in a PostgreSQL database, and using FastAPI to build a RESTful API for accessing the data. Docker is used to containerize the application, ensuring easy deployment and scalability. The web scraper fetches the latest news articles, and FastAPI endpoints allow users to query the stored data efficiently. This setup enables seamless integration and provides a robust solution for managing and accessing scraped data.

## Features

1. **Data Scraping API**: Provides an endpoint to scrape data from Hacker News and store it in a PostgreSQL relational database.
2. **Column-wise Data Retrieval**: Offers an API to get details for specific columns from the stored data.
3. **Generalized Data Description**: Implements an endpoint for generating a generalized description of the scraped data.
4. **Stop Words Count**: Includes an API to count stop words in the data, providing insights into common words used.
5. **Keyword Search**: Features a keyword search API to retrieve URLs from the database that match the search criteria.


### Prerequisites

- Python 3.10+
- Beautifulsoup
- FastApi
- Nltk
- SqlAlchemy
- psycopg2

### Steps

1. **Clone the repository:**

    ```bash
    git clone https://github.com/mbharath246/FastAPI-webscrap.git
    cd FastAPI-webscrap
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt

    install docker : https://docs.docker.com/engine/install/ubuntu/
    ```

4. **Set up for the project:**

    ```bash
    docker compose up
    ```


5. **Run the development server:**

    ```bash
    http://127.0.0.1:8000/docs
    ```
6. **Additional Steps**
    - Create User
    - User Login to get Token
    - Authorize Token
    - Now you can use all apis.

## Usage

### Start Scraping Job

Endpoint: `http://localhost:8000/blogs/5` 5 represents 5 pages scrapping change if you want  
Method: `POST`

#### Request Body

```json
{
  "message": "5 pages scrapped successfully"
}
```

### Check Scraping Status

Endpoint: `http://localhost:8000/blogs/heading`  
Method: `GET`

## Create User

![image](https://github.com/mbharath246/FastAPI-webscrap/assets/162307939/abffedd0-0625-48aa-80b8-98cdf0fa2c16)

## User Login for getting jwt token

![image](https://github.com/mbharath246/FastAPI-webscrap/assets/162307939/0cf7b124-3e5b-42fa-a2ee-03d0d3eb8531)

## Authorization

![image](https://github.com/mbharath246/FastAPI-webscrap/assets/162307939/48044c7e-c295-4895-b12c-8709d588fdb4)

## Scrapping the data

![image](https://github.com/mbharath246/FastAPI-webscrap/assets/162307939/e0dfa183-ffbb-41ce-a20c-6dca000c5b08)

## Keyword based Search urls

![image](https://github.com/mbharath246/FastAPI-webscrap/assets/162307939/4501a6c3-7d52-4d25-ab08-a5ebbeae3fe7)

## Stop words count

![image](https://github.com/mbharath246/FastAPI-webscrap/assets/162307939/d1ff1e59-b6e5-4dd0-b0cc-f20892c39ba8)
