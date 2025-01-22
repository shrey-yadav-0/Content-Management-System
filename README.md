# Content-Management-System

## Project Setup Guide

Follow these steps to set up the project locally.

### 1. Install Python (preferably Python 3.12)

Make sure Python 3.12 is installed on your system. You can check your Python version by running:

```bash
python --version
```

### 2. Create a Virtual Environment for the Project

It’s recommended to create a virtual environment for managing dependencies. Run the following commands to create and activate the virtual environment:

For Windows:
```bash
python -m venv venv
.\venv\Scripts\activate
```

For macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

Once your virtual environment is activated, install the project dependencies by running:
```bash
pip install -r requirements.txt
```

### 4. Set Up the Database and Admin Roles

Run the following commands to set up the database and create the necessary roles:
```bash
python manage.py migrate
python manage.py create_roles
python manage.py create_admin
```

### 5. Start the Server

To start the development server, use the following command:
```bash
python manage.py runserver
```
The server will start at http://127.0.0.1:8000/ by default.

### 6. Access the API Endpoints

You can now access the following API endpoints:

    Register: POST /app/register

    Login: POST /app/login

    Manage Content:
        GET /app/contents
        POST /app/contents

        GET /app/contents/<integer:content_id>
        PUT /app/contents/<integer:content_id>
        DELETE /app/contents/<integer:content_id>

    Search Content
        GET /app/content-search
