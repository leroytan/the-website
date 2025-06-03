# Project Setup Guide

This guide outlines the steps to set up and run the backend and frontend components of the project.

## Backend Setup

1.  **Install Poetry:**
    ```bash
    pip install poetry
    ```

2.  **Navigate to Backend Directory:**
    ```bash
    cd backend
    ```

3.  **Install Dependencies:**
    ```bash
    poetry install
    ```

4.  **Run Backend Server:**
    ```bash
    poetry run python -m uvicorn api.index:app --reload
    ```

## Frontend Setup

1.  **Navigate to Frontend Directory:**
    ```bash
    cd frontend
    ```

2.  **Install Dependencies:**
    ```bash
    npm install
    ```

3.  **Run Frontend (Development):**
    ```bash
    npm run next-dev
    ```

4.  **Run Frontend (Production Testing):**
    ```bash
    npm run build
    npm start
    ```

## Requirements

Please search online for instructions on how to install and set up the following:

* **Database:**
    * PostgreSQL server (for local testing)
    * Supabase (for remote testing)
* **Python & Pip**
* **npm & Node.js**
* **ngrok** (for exposing local backend for Stripe webhooks)
* **Stripe Account/Setup**
* **R2 Object Storage Account/Setup**