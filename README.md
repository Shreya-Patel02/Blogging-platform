# Blogging-platform
A blogging application that allows users to create, manage, and view blog posts. It is built using Django for the backend, PostgreSQL for the database, and integrates with OpenAI for advanced features like AI-powered content recommendations and analysis.

## Setup Instructions

### Clone the repository:
git clone https://github.com/yourusername/blogging_platform.git
cd blogging_platform

### Install the required dependencies:
pip install -r requirements.txt

### Set up the PostgreSQL database:
Install and start PostgreSQL if you haven't already.
Create a new database (you can use the psql command-line tool or a GUI like pgAdmin)
- CREATE DATABASE blogging_db;

### Configure the environment variables:
Copy the sample environment file and modify it with your own configuration.
- cp .env.example .env

Modify the .env file with your PostgreSQL credentials and OpenAI API key:
- POSTGRES_DB=blogging_db
- POSTGRES_USER=postgres
- POSTGRES_PASSWORD=yourpassword
- OPENAI_API_KEY=your-openai-api-key

### Apply database migrations: Run the following command to set up the database schema:
- python manage.py migrate

### Create a superuser to access the admin panel:
- python manage.py createsuperuser

### Run the development server: Start the Django development server by running
- python manage.py runserver

## LLM Integration
The blogging platform integrates with OpenAI's GPT model for advanced features like content recommendations and AI-powered analysis.

### Configure the API key in your environment file
 In the .env file of the project, set your OPENAI_API_KEY:
- OPENAI_API_KEY=your-openai-api-key

## Environment Variables
The following environment variables are required for the application to work properly:

POSTGRES_DB: The name of the PostgreSQL database (e.g., blogging_db).
POSTGRES_USER: The PostgreSQL user (e.g., postgres).
POSTGRES_PASSWORD: The password for the PostgreSQL user.
OPENAI_API_KEY: The API key for OpenAI integration (for AI-powered features).
DEBUG: Set to 1 to enable Django's debug mode.
SECRET_KEY: Django's secret key (should be a unique, secure value).
DJANGO_ALLOWED_HOSTS: Allowed hosts for your Django app.



 





