# transformation_agent

A robust, containerized Python service for automated data transformation and processing, leveraging Google Cloud services.

## 1. Project Title and Badges

# `transformation_agent`

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.103.0-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![License: Unspecified](https://img.shields.io/badge/License-Unspecified-lightgrey)](https://choosealicense.com/no-license/)

A versatile and scalable Python application designed to perform automated data transformation tasks via a declarative API, integrating seamlessly with Google Cloud Storage and AI Platform for advanced data processing workflows.

## 2. Overview

The increasing complexity and volume of data necessitate efficient and reliable transformation mechanisms. Manual or ad-hoc data processing pipelines are prone to errors, lack scalability, and hinder rapid development. This project addresses these challenges by providing an API-driven solution for orchestrating and executing data transformation tasks.

`transformation_agent` is designed for data engineers, MLOps practitioners, and developers who require an automated, scalable, and auditable system for preparing data for analytical workloads or machine learning model consumption. It abstracts the underlying complexities of data manipulation, offering a straightforward interface to define and execute transformations.

Its key value proposition lies in its ability to:
- **Automate complex data transformation workflows** through a simple API interface.
- **Integrate seamlessly with Google Cloud services** for robust storage and AI-powered processing.
- **Provide a containerized, scalable, and maintainable solution** suitable for enterprise environments.

## 3. ✨ Features

- **API-Driven Data Transformation**: Exposes RESTful endpoints for initiating, monitoring, and managing data transformation jobs.
- **Google Cloud Storage Integration**: Directly reads input data from and writes transformed output data to Google Cloud Storage buckets.
- **Google Cloud AI Platform Integration**: Capable of leveraging Google Cloud AI Platform for advanced, ML-enhanced transformations or inferences as part of the data pipeline.
- **Efficient Data Processing with Pandas**: Utilizes the Pandas library for high-performance in-memory data manipulation and transformation.
- **Containerized Deployment**: Packaged as a Docker image for easy deployment, scalability, and environment consistency across various Google Cloud compute services (e.g., Cloud Run, GKE).
- **Extensible Transformation Logic**: Designed with a modular architecture to allow easy addition of new transformation types and custom logic within the `src` directory.

## 4. 🏗️ Architecture

The `transformation_agent` leverages a microservice architecture, orchestrating data flow between clients and Google Cloud services.

```
       User/Client
            |
            v
     FastAPI Service
   (transformation_agent)
            |
     +------+------+
     |             |
     v             v
    GCS         AI Platform
```

- **User/Client**: Initiates transformation requests, typically by sending data paths and transformation parameters to the FastAPI Service.
- **FastAPI Service (`transformation_agent`)**: The core application, handling API requests, orchestrating data movement, and applying transformations. It interacts with Google Cloud Storage for data I/O and Google Cloud AI Platform for specialized tasks.
- **GCS (Google Cloud Storage)**: Provides highly durable and scalable object storage for both input and output datasets.
- **AI Platform (Google Cloud AI Platform)**: Used for executing machine learning models or services, which may be part of complex transformation steps (e.g., data enrichment, feature engineering based on ML models).

## 5. 🛠️ Tech Stack

- **Backend**:
    - Python 3.9+
    - FastAPI: Web framework for building APIs
    - Uvicorn: ASGI server for FastAPI
    - Pandas: Data manipulation and analysis library
    - `python-multipart`: For handling form data, potentially for file uploads or complex API requests.
- **Cloud Services**:
    - Google Cloud Storage: Object storage for data persistence
    - Google Cloud AI Platform: Managed service for machine learning workloads (training, prediction, custom jobs)
- **Containerization**:
    - Docker: For packaging the application into a portable container
- **CI/CD & Deployment**:
    - Google Cloud Build: For automated build, test, and deployment pipelines
    - Google Cloud Run / Google Kubernetes Engine: Likely deployment targets for the containerized application

## 6. 📦 Installation

This section details how to set up and run the `transformation_agent` either locally or by building its Docker image.

### Prerequisites

- Python 3.9 or higher
- `pip` (Python package installer)
- `venv` (Python virtual environment manager)
- Docker Desktop (if building or running via Docker)
- Google Cloud SDK (for local authentication and interaction with GCP services)

### Setup Steps

1.  **Clone the Repository**:

    ```bash
    git clone https://github.com/your-org/transformation_agent.git
    cd transformation_agent
    ```

2.  **Option A: Local Setup with Virtual Environment**

    - Create and activate a Python virtual environment:
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate # On Linux/macOS
        # .venv\Scripts\activate # On Windows
        ```

    - Install the required dependencies:
        ```bash
        pip install -r requirements.txt
        ```

    - Set up Google Cloud authentication (if accessing GCP services locally):
        ```bash
        gcloud auth application-default login
        ```
        This command creates application default credentials that your Python code can use to authenticate with GCP services.

3.  **Option B: Docker Build**

    - Build the Docker image from the `Dockerfile`:
        ```bash
        docker build -t transformation_agent .
        ```
        This command creates a Docker image named `transformation_agent` from the current directory.

## 7. 🚀 Usage

This section provides instructions on how to run the `transformation_agent` and interact with its API.

### Running Locally (Virtual Environment)

1.  Ensure you have followed "Option A: Local Setup with Virtual Environment" from the Installation section and your virtual environment is active.
2.  Start the FastAPI application using Uvicorn:
    ```bash
    uvicorn app:app --host 0.0.0.0 --port 8000 --reload
    ```
    The `--reload` flag is useful for development as it automatically restarts the server on code changes. For production, remove this flag.
3.  The API will be accessible at `http://localhost:8000`.

### Running Locally (Docker Container)

1.  Ensure you have built the Docker image as per "Option B: Docker Build" from the Installation section.
2.  Run the Docker container, mapping port 8000:
    ```bash
    docker run -p 8000:8000 transformation_agent
    ```
3.  The API will be accessible at `http://localhost:8000`.

### Example API Interaction

The `transformation_agent` is designed to accept transformation requests via its API. A common endpoint would be for initiating a data transformation job.

- **Endpoint**: `POST /transform`
- **Description**: Initiates a data transformation process on specified input data and saves the result.
- **Request Body Example**:

    ```json
    {
      "input_gcs_path": "gs://your-bucket/input/data.csv",
      "output_gcs_path": "gs://your-bucket/output/transformed_data.parquet",
      "transformation_type": "standardize_columns",
      "parameters": {
        "columns_to_standardize": ["feature_1", "feature_2"],
        "output_format": "parquet"
      }
    }
    ```

- **Example `curl` Command**:

    ```bash
    curl -X POST \
         http://localhost:8000/transform \
         -H 'Content-Type: application/json' \
         -d '{
               "input_gcs_path": "gs://your-input-bucket/sales_data.csv",
               "output_gcs_path": "gs://your-output-bucket/processed_sales.csv",
               "transformation_type": "clean_and_aggregate",
               "parameters": {
                 "aggregation_column": "region",
                 "output_format": "csv"
               }
             }'
    ```

- **Expected Response**:

    ```json
    {
      "job_id": "TRANSFORMATION-JOB-12345",
      "status": "initiated",
      "message": "Transformation job successfully initiated. Monitor status via /jobs/{job_id}."
    }
    ```

## 8. ⚙️ Configuration

The `transformation_agent` relies on environment variables for configuration, particularly for interacting with Google Cloud services.

| Variable | Description | Example |
| :------------------------- | :-------------------------------------------------------------------------------------- | :------------------------ |
| `GCP_PROJECT_ID` | The Google Cloud Project ID where services like GCS and AI Platform are located. | `my-gcp-project-12345` |
| `GCS_DEFAULT_BUCKET` | Default Google Cloud Storage bucket for input/output if not specified in request. | `gs://my-data-bucket` |
| `AI_PLATFORM_PREDICTION_ENDPOINT` | The endpoint for a specific AI Platform custom prediction service or model. | `us-central1-aiplatform.googleapis.com/v1/projects/...` |
| `SERVICE_ACCOUNT_KEY_PATH` | Local path to a Google Service Account JSON key file (for local development/testing). | `/secrets/sa-key.json` |
| `FASTAPI_ENV` | Environment setting (e.g., `development`, `production`). Affects logging verbosity. | `development` |
| `LOG_LEVEL` | Logging level for the application (e.g., `INFO`, `DEBUG`, `WARNING`). | `INFO` |

**Note**: For production deployments on Google Cloud (e.g., Cloud Run, GKE), it's recommended to rely on Google Cloud's [Application Default Credentials (ADC)](https://cloud.google.com/docs/authentication/application-default-credentials) for authentication rather than explicit service account key files, enhancing security.

## 9. 📚 API Documentation

The `transformation_agent` provides a RESTful API for managing data transformations. The primary endpoint for initiating transformations is detailed below. Full interactive API documentation (Swagger UI) is available at `/docs` when the application is running, and ReDoc documentation at `/redoc`.

### **`POST /transform`**

- **Description**: Initiates an asynchronous data transformation task. The service reads data from the specified input GCS path, applies the requested transformation, and writes the results to the output GCS path.
- **Request Body**:
    | Parameter | Type | Description | Required | Example |
    | :----------------------- | :-------- | :------------------------------------------------------------------------------------- | :------- | :------------------------------------- |
    | `input_gcs_path` | `string` | Google Cloud Storage URI for the input data file(s). | Yes | `gs://my-bucket/raw/data.csv` |
    | `output_gcs_path` | `string` | Google Cloud Storage URI for where the transformed data will be saved. | Yes | `gs://my-bucket/processed/output.parquet` |
    | `transformation_type` | `string` | The identifier for the transformation logic to apply (e.g., `standardize_columns`, `aggregate_sales`). | Yes | `standardize_columns` |
    | `parameters` | `object` | A dictionary of key-value pairs specific to the `transformation_type`. | No | `{"columns": ["A", "B"], "method": "zscore"}` |
- **Responses**:
    - `200 OK`: Transformation job successfully initiated.
        ```json
        {
          "job_id": "TRANSFORMATION-JOB-UUID-1234",
          "status": "initiated",
          "message": "Transformation job accepted and started."
        }
        ```
    - `400 Bad Request`: Invalid request payload or missing required parameters.
        ```json
        {
          "detail": "Invalid input_gcs_path: gs://invalid-bucket/file.csv"
        }
        ```
    - `500 Internal Server Error`: An unexpected error occurred on the server.
- **Authentication**:
    - The service expects authentication via Google Cloud Application Default Credentials (ADC) when deployed on GCP.
    - For local development, ensure `gcloud auth application-default login` has been executed.
    - If deployed with specific service accounts, the underlying runtime environment must be configured with appropriate permissions to access GCS and AI Platform.

## 10. 🤝 Contributing

We welcome contributions to the `transformation_agent` project! Please follow these guidelines to ensure a smooth contribution process.

- **Fork the Repository**: Start by forking the `transformation_agent` repository to your GitHub account.
- **Create a Feature Branch**: Create a new branch for your feature or bug fix: `git checkout -b feature/your-feature-name` or `git checkout -b bugfix/issue-description`.
- **Code Style**: Adhere to [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code. We recommend using `black` for code formatting and `flake8` for linting.
- **Testing**:
    - Ensure your changes are covered by appropriate unit and integration tests.
    - Run existing tests to ensure no regressions are introduced: `pytest`.
- **Commit Messages**: Write clear, concise, and descriptive commit messages following the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification (e.g., `feat: Add new transformation type`, `fix: Resolve GCS connection issue`).
- **Pull Requests**:
    - Submit your changes via a Pull Request (PR) to the `main` branch of the original repository.
    - Provide a detailed description of your changes, including the problem it solves and how it was tested.
    - Ensure all checks (linters, tests) pass.
- **Review Process**: Your PR will be reviewed by maintainers. Be prepared to address feedback and make further adjustments.

## 11. 📄 License

No explicit license file was found within this repository. As such, the software's usage, distribution, and modification terms are currently unspecified. For licensing inquiries, please contact the repository owners.
