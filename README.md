# COMP2001--CW2
This is a Flask-based microservice for managing trails with JWT-based authentication. It allows users to create, view, and manage trails in a database. The app uses SQLAlchemy for database interaction and FastCGI for deployment on IIS.

Features:

JWT Authentication for secure access

Role-based access control (Admin role)

CRUD operations for trail management (Create, Retrieve, Update)

Easy deployment on IIS with FastCGI support

Installation

Clone the repository:


git clone <repository-url>

cd <repository-folder>

Install dependencies:


pip install -r requirements.txt

Set up the environment variables:

Configure your database URI in the SQLALCHEMY_DATABASE_URI.
Set your Flask app secret key for JWT in the .env file or as an environment variable.
Running the Application
Run the Flask app locally:


python app.py

Access the app:

The app will be available at: http://127.0.0.1:5000
Deployment
To deploy the Flask application on IIS:

Install IIS and enable FastCGI.
Set up a new IIS site with the correct directory and port.
Configure FastCGI to run Python for your Flask app.
Ensure web.config is properly configured with the correct paths for Python and the application file.
Testing
The core functionalities of the application, including JWT token generation, CRUD operations for trails, and basic validation, have been tested. However, role-based access was not fully tested due to issues with reading credentials from the user table. This is an area to revisit for future development.
