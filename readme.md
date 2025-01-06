# Ad Platform Project Structure
my-project/
├── backend/                         # FastAPI backend
│   ├── app/                         # FastAPI app folder
│   │   ├── __init__.py
│   │   ├── main.py                  # FastAPI main entry file
│   │   ├── api/                     # API routes
│   │   ├── models/                  # Database models
│   │   └── services/                # Business logic and services
│   ├── Dockerfile                   # Dockerfile for FastAPI backend
│   ├── requirements.txt             # Python dependencies
│   └── .env                         # Environment variables (optional)
├── frontend/                        # React frontend
│   ├── public/                      # Public assets
│   ├── src/                         # Source code
│   │   ├── components/              # React components
│   │   ├── pages/                   # Pages for routing
│   │   ├── services/                # API requests (e.g., for Kafka, FastAPI)
│   │   └── App.js                   # Main React app file
│   ├── Dockerfile                   # Dockerfile for React frontend
│   └── package.json                 # React dependencies
├── kafka/                           # Kafka setup (Optional: Kafka can be managed via Docker Compose)
│   └── Dockerfile                   # Kafka setup if custom
├── postgres/                        # Postgres setup (Optional: Postgres managed via Docker Compose)
│   └── init.sql                     # SQL initialization scripts for Postgres (optional)
├── redis/                           # Redis setup (Optional: Redis managed via Docker Compose)
│   └── Dockerfile                   # Dockerfile for Redis (optional)
├── prometheus/                      # Monitoring setup with Prometheus (optional)
│   └── prometheus.yml               # Prometheus config (optional)
├── scripts/                         # Useful scripts (e.g., setup, migrations)
│   ├── setup.sh                     # Bash setup script
├── .env                              # Global environment variables (optional)
├── docker-compose.yml               # Unified docker-compose file (includes all services)
└── README.md                        # Project documentation


# Ad Platform Project

**Ad Platform Project** is a full-stack platform designed to integrate with Google Ads for managing campaigns, performance analysis, and other advertising services. This platform features a backend built with **FastAPI**, a frontend with **React**, and supports services such as **PostgreSQL**, **Redis**, **Kafka**, and **Docker** for containerized environments.

## Project Overview

The project is structured with separate services for backend and frontend, allowing for flexible management and scaling. The backend handles business logic and integrates with Google Ads API, while the frontend provides an interactive user interface. The backend is also responsible for authentication, token management, and handling requests to the Google Ads API.

### Key Features

- **Backend:** FastAPI with SQLAlchemy for database interactions and Pydantic for data validation.
- **Frontend:** React-based UI for managing Google Ads campaigns.
- **Google Ads API Integration:** Fetch and manage campaigns, including Performance Max and other campaign types.
- **Authentication:** Token-based session authentication.
- **Dockerized Environment:** All services are containerized for easy deployment on **Google Cloud Run**.

### Technologies Used

- **Frontend:** React.js
- **Backend:** FastAPI, SQLAlchemy, Alembic
- **Database:** PostgreSQL
- **Caching:** Redis
- **Messaging:** Kafka (optional)
- **Authentication:** JWT Token-based Authentication
- **Containerization:** Docker
- **Deployment:** Google Cloud Run

### Services

- **Frontend:** React application serving the user interface.
- **Backend:** FastAPI service handling API requests, including Google Ads management.
- **PostgreSQL:** Database for storing user and campaign data.
- **Redis:** Used for caching and session management.
- **Kafka (Optional):** Messaging queue for scalable communication.

## Getting Started

### Prerequisites

- Docker
- Docker Compose
- Python 3.9+
- Node.js (for frontend development)

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/ad-platform-project.git
    cd ad-platform-project
    ```

2. **Backend Setup:**
    - Navigate to the backend directory:
    ```bash
    cd backend
    ```
    - Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
    - Create the `.env` file and set your environment variables (e.g., database URL, Redis URL).

3. **Frontend Setup:**
    - Navigate to the frontend directory:
    ```bash
    cd frontend
    ```
    - Install the dependencies:
    ```bash
    npm install
    ```

4. **Run the Application:**
    - Build and start the application using Docker Compose:
    ```bash
    docker-compose up --build
    ```

    This will start all the services including backend, frontend, PostgreSQL, Redis, and Kafka (if configured).

---

## TODO List

- **Google Ads Integration:**
  - Complete integration with Google Ads API for campaign management.
  - Implement performance tracking and analysis for different campaign types (including Performance Max).
  - Add additional features for managing campaigns such as creating, pausing, and editing ads.

- **Authentication & Authorization:**
  - Enhance session management with JWT tokens for secure user authentication.
  - Implement OAuth-based authentication for Google sign-in (done).
  - Implement role-based access control for different user roles.

- **Frontend:**
  - Complete the UI for managing Google Ads campaigns.
  - Add forms for creating and editing campaigns.
  - Implement a dashboard for viewing campaign performance.

- **Backend:**
  - Refine token-based authentication with session validation.
  - Add logging and error handling throughout the backend services.
  - Implement background tasks for periodic data syncing with Google Ads API.

- **Deployment:**
  - Set up continuous deployment on **Google Cloud Run**.
  - Configure environment variables for production deployment.
  - Finalize Docker configuration for optimized production deployment.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
