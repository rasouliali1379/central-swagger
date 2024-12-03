# Central Swagger

### Introduction

This project is a **Full Stack Application** designed to aggregate Swagger files from multiple projects and display them in a unified **Swagger UI** interface. 

The project is structured into two main directories:

1. **Frontend**: A simple React application to serve the user interface for displaying aggregated Swagger files.
2. **Backend**: A FastAPI application that handles the retrieval, aggregation, and serving of Swagger specifications to the frontend.


### Project Structure

```plaintext
.
├── frontend/    # React project for the user interface
├── backend/     # FastAPI project for API handling
├── Makefile     # Automation commands
└── README.md    # Project documentation
```

### Prerequisites

Ensure you have the following installed on your system:
- Node.js (v14+)
- Python (v3.8+)
- Make (for running the Makefile commands)

### Getting Started

Follow these steps to set up and run the project:

1. Install Dependencies

Run the following command to install dependencies for both the backend and frontend:

```bash
make install
```

2. Run the Application

Start both the backend and frontend servers with:

```bash
make start
```

The backend will run at: http://localhost:8000

The frontend will run at: http://localhost:3000

3. Stop the Application

Stop both servers with:

```bash
make stop
```

## API Endpoints

The backend provides the following key API endpoints:
- `GET /docs`: Access FastAPI’s built-in Swagger UI for backend APIs.
- `GET /central-swagger/collections/`: Endpoint to retrieve all collection with their sepcs.
- `POST /central-swagger/collections/`: Endpoint to create a new collection.
- `POST /central-swagger/collections/{key}/specs`: Endpoint to add or update specs of a collection.
- `GET /central-swagger/collections/all`: Endpoint to retrieve all collection names without specs.
- `GET /central-swagger/collections/aggregated`: Endpoint to retrieve all specs in a single collection.

## Usage

1.	Run the application as described above.
2.  Open the frontend application in your browser (http://localhost:3000).
3.  Interact with the interface to view the aggregated Swagger files.
4.  Go to http://localhost:3000/admin page to create new collection.