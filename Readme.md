# Traffic Sensor Dashboard

Deployed to Heroku. See live at: [https://traffic-sensors-6fa380496f26.herokuapp.com/](https://traffic-sensors-6fa380496f26.herokuapp.com/)

# Real-Time Sensor Data Monitoring and Visualization Web Application

## Key Features and Technologies Used

- **Django Backend**:

  - Implemented Django models to store sensor data including fields such as sensor location (latitude and longitude), timestamp, vehicle speed, and speed limit at the sensor location.
  - Leveraged Django Channels to handle real-time updates, enabling a seamless flow of sensor data to the front-end.
  - Utilized Daphne as an HTTP, HTTP2, and WebSocket protocol server for Django, facilitating real-time updates without requiring a separate server setup.
  - Created RESTful APIs using Django Rest Framework to retrieve and filter traffic data based on user inputs (e.g., date range, location).
  - Implemented proper error handling and validation for API requests to ensure data integrity and system stability.

- **Real-Time Data Emulation**:

  - Mock sensor data emulator simulating real-time data transmission, updating every 5 seconds.

- **Interactive Frontend using Chart.js**:

  - Dynamic, real-time updating charts for sensor data visualization.
  - Interactive features for data exploration.

- **Asynchronous Data Handling**:

  - Efficient data loading and manipulation ensuring responsive real-time updates.

- **Proper Error Handling and Validation**:

  - Graceful error handling with clear error messages.
  - Comprehensive data validation for data integrity.

- **User Interaction and Engagement**:
  - Interactive elements for enhanced data understanding and analysis.

## Overview

This project is built using Django. Further utilized Django's Channels for handling real-time updates which is essential for our Traffic Sensor Dashboard to display live data. Data is stored in a PostgreSQL database. The application is hosted and ran using Danphe. The real-time communication in our app is facilitated by WebSockets, Django Channels, and Danphe which provide a seamless experience for real-time updates on the dashboard.

## Getting Started

Here's how to set up the project locally for development.

### 1. Clone the Repository

```bash
$ git clone https://github.com/your-username/traffic-sensors.git
$ cd traffic-sensors
```

### 2. Install Python and create a virtual env

python -m venv venv

```bash
$ py -m venv myworld
```

### 3. Activate the virtual Environment

```bash
$ venv\Scripts\activate
```

### 4. Install dependencies

```bash
$ pip install -r requirements.txt
```

### 5. Setup the Database

We are using PostgreSQL here.

### 6. SAMPLE-ENV Below

```bash
DEBUG=
SECRET_KEY=
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
ALLOWED_HOSTS=
SESSION_COOKIE_SECURE=
CSRF_COOKIE_SECURE=
DJANGO_SETTINGS_MODULE=
WS_URL=
ICON_URL=
```

### 7. Apply Database Migrations

```bash
$ python manage.py migrate
```

### 8. Run the server using Daphne

```bash
$ daphne traffic_dashboard.asgi:application
```

Now, the application should be running at http://localhost:8000
