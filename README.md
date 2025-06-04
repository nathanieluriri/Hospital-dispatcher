Hospital Dispatcher System Backend (Dockerized)
This README.md provides instructions on how to set up and run the Hospital Dispatcher System backend using Docker. This method containerizes the application, including its dependencies and database seeding process, for easy deployment and reproducibility.

Table of Contents
Prerequisites

Building and Running with Docker

Build the Docker Image

Run the Docker Container

Access the Application

Important Considerations

Prerequisites
To run this application using Docker, you need to have Docker installed on your system.

Docker Engine:

Install Docker Desktop (for Windows/macOS)

Install Docker Engine (for Linux)

Building and Running with Docker
Follow these steps to build the Docker image and run the application container.

Build the Docker Image
Navigate to the root directory of your project where the Dockerfile, requirements.txt, seed.py, and your application code reside. Then, execute the following command to build the Docker image:

docker build -t hospital-dispatcher-backend .

-t hospital-dispatcher-backend: This tags your image with the name hospital-dispatcher-backend. You can choose a different name if you prefer.

.: This indicates that the Docker build context is the current directory, meaning Docker will look for the Dockerfile and other necessary files in this location.

This process will install all Python dependencies from requirements.txt and run the seed.py script inside the Docker image during the build process. For SQLite, the seed.py script is expected to create the database file if it doesn't already exist. Ensure your seed.py is idempotent if you plan to rebuild the image frequently.

Run the Docker Container
Once the image is successfully built, you can run a container from it. This command will map the container's internal port 8000 to your host machine's port 8000, allowing you to access the application.

docker run -p 8000:8000 hospital-dispatcher-backend

-p 8000:8000: This publishes port 8000 from the container to port 8000 on your host.

hospital-dispatcher-backend: This is the name of the Docker image you built in the previous step.

Access the Application
After running the Docker container, your FastAPI application should be accessible at:

API Endpoints: http://localhost:8000/api/v1/...

Swagger UI (API Documentation): http://localhost:8000/docs

ReDoc (Alternative API Documentation): http://localhost:8000/redoc
