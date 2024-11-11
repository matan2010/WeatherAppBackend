# Weather App Backend (Django)

## Introduction

This project focuses on building a robust and efficient Django backend for a weather application. The backend acts as an intermediary between the frontend (React) and third-party weather APIs, offering features such as data caching and optional user authentication for personalized experiences.

## Features

- **RESTful API**: Developed using Django REST Framework to handle weather data requests from the frontend.
- **Efficient Caching**: Caches responses from third-party APIs to minimize redundant calls and improve response times.
- **Weather Data Normalization**: Transforms incoming data from external APIs into a standardized format.
- **User Authentication**: Allows for user management and personalized experiences.

## Goals

- Create a functional and scalable **RESTful API** to handle weather data requests from the frontend.
- Implement **caching mechanisms** to optimize performance and reduce unnecessary third-party API calls.
- Build a service layer that efficiently interacts with external weather APIs.
- Ensure **data consistency** and **integrity** by normalizing API responses.
- Implement **user authentication** to enable personalized user features.

## Scope

### API Endpoints

- **POST /weather/**: Accepts location data (city name or coordinates) and returns current weather data.
- **GET /weather/{city}/**: Returns cached weather data for a specified city.
- **GET /weather/coordinates/{latitude}/{longitude}**: Fetches weather data for provided geographical coordinates.
- **POST /forecast/**: Retrieves 3-day or 7-day weather forecasts.
- **POST /signup/**: Registers a new user and returns a success message with a token.
- **POST /login/**: Authenticates a user and returns a session cookie and token for further requests.

### Caching

- **Caching Layer**: Uses Django's caching framework with a 5-minute expiration time to optimize repeated requests.
- **Cache Check**: Ensures that external API calls are only made if the cache is expired or unavailable.

### Weather API Integration

- Integrates with a reliable third-party weather API - OpenWeatherMap and Weatherbit.
- Normalizes weather data into a consistent format to serve to the frontend.

### User Authentication

- Implements **user authentication** using Django’s built-in authentication system and token-based authentication (via Django REST Framework).
- Supports user sessions for personalized weather features.
- **Data Security**: After a user signs up, their data is securely stored in an SQL database, ensuring that all sensitive information is safeguarded in compliance with industry standards.

## Technical Requirements

- **Framework**: Django
- **API Development**: Django REST Framework
- **Caching**: Django’s caching framework (with Redis as the backend)
- **External APIs**: OpenWeatherMap, Weatherbit
- **Celery** for background tasks such as cache refreshing.

## Deliverables

- A well-documented **Django project** with RESTful API endpoints to fetch and cache weather data.
- A **service layer** that abstracts and handles interactions with external weather APIs.
- Comprehensive **API documentation** (via tool Postman).
- **User Authentication** implementation for secure access and personalized features.

Here's a sample section you can add to your `README.md` file to explain how to run your project and start Celery:

---

### Running the Project

To run the weather app project, follow these steps:

1. **Start the Django Development Server**

   Run the following command to start the Django server:

   ```bash
   python manage.py runserver
   ```

   This will start the server on the default port (usually `http://127.0.0.1:8000`).

2. **Run Celery with the Beat Scheduler**

   To enable periodic tasks with Celery, run the following command in a separate terminal:

   ```bash
   celery -A weather_app_backend beat --loglevel=info
   ```

   This starts Celery with the beat scheduler, which handles scheduling tasks at regular intervals.
