# Text Similarity API

This repository contains a Dockerized project that allows users to register, detect the similarity between two text strings, and refill tokens for more comparisons.

The project includes an API built using Flask and flask_restful. It uses MongoDB for data persistence and bcrypt for password hashing and verification.

The comparison is made by calculating the similarity score between two texts using Spacy's `similarity()` function.

## Files and Directories

- `app.py`: This is the main application file. It contains the Flask API endpoints and business logic.
- `requirements.txt`: This file lists all Python dependencies that are installed via pip.
- `docker-compose.yml`: This is a Docker Compose file that sets up and coordinates the web and database services.
- `Dockerfile`: This file contains instructions for building the Docker image for the application.

**Prerequisites**

You need to have Docker and Docker Compose installed on your machine.

**Steps**

1. Clone this repository.
    ```
    git clone <repository_url>
    ```

2. Navigate into the repository.
    ```
    cd <repository_directory>
    ```

3. Add your MongoDB URI to the `uri` variable in the `app.py` file. 
    ```python
    uri = "<your_mongodb_uri>"
    ```

4. Build and run the Docker image and container using Docker Compose.
    ```
    docker-compose up --build
    ```
   
## Usage

The application provides the following endpoints:

- `/register`: Register a new user. It takes a JSON object containing a "username" and "password".
- `/detect`: Detect similarity between two text strings. It takes a JSON object with a "username", "password", "text1", and "text2".
- `/refill`: Refill the tokens for a user. It takes a JSON object with a "username", "admin_pw", and "refill".

Use an HTTP client like curl or a tool like Postman to send HTTP POST requests to these endpoints.
