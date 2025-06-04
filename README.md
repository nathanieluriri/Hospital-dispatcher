Dispatcher System Backend**:

---

# Hospital Dispatcher System Backend (Dockerized)

This guide explains how to build and run the Hospital Dispatcher System backend using Docker. The setup includes all dependencies and seeds the database automatically for quick, reproducible deployment.

---

## 📦 Prerequisites

* **Docker** must be installed:

  * [Docker Desktop (Windows/macOS)](https://www.docker.com/products/docker-desktop)
  * [Docker Engine (Linux)](https://docs.docker.com/engine/install/)

---

## 🚀 Build & Run with Docker

### 1. Build the Docker Image

In the project root (where `Dockerfile`, `requirements.txt`, `seed.py`, and app code are located), run:

```bash
docker build -t hospital-dispatcher-backend .
```

> 🔹 This creates an image named `hospital-dispatcher-backend` and installs dependencies.
> 🔹 `seed.py` is executed during the build to initialize the SQLite database. Ensure it's idempotent.

---

### 2. Run the Docker Container

```bash
docker run -p 8000:8000 hospital-dispatcher-backend
```

> 🔹 Maps internal port `8000` to your host.
> 🔹 Starts the FastAPI backend inside the container.

---

## 🌐 Access the Application
https://www.postman.com/orbital-module-geoscientist-92143211/workspace/my-workspace/collection/31971164-0ed4f5a5-94fd-4bff-93d4-4e327d798382?action=share&creator=31971164
* **Postman Public URL**: [https://www.postman.com/orbital-module-geoscientist-92143211/workspace/my-workspace/collection/31971164-0ed4f5a5-94fd-4bff-93d4-4e327d798382?action=share&creator=31971164](https://www.postman.com/orbital-module-geoscientist-92143211/workspace/my-workspace/collection/31971164-0ed4f5a5-94fd-4bff-93d4-4e327d798382?action=share&creator=31971164)
* **Base URL**: [http://localhost:8000](http://localhost:8000)
* **API Docs (Swagger)**: [http://localhost:8000/docs](http://localhost:8000/docs)
* **API Docs (ReDoc)**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

Let me know if you’d like to add environment variable support, volume mounts, or production deployment tips.
