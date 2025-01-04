from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import pyodbc
from sqlalchemy import text  # Correct import for text()

# Initialize Flask app and SQLAlchemy
app = Flask(__name__)

# Configure the app for SQLAlchemy and your database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://MStefan:TszJ810+@DIST-6-505.uopnet.plymouth.ac.uk/COMP2001_MStefan?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Hardcoded JWT Secret Key for testing purposes
app.config['JWT_SECRET_KEY'] = 'test_secret_key_for_testing'  # Use a simple secret key for testing

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Test route to check database connection
@app.route('/test_connection', methods=['GET'])
def test_connection():
    try:
        # Wrap the query in the 'text()' function
        query = text("SELECT TOP 1 * FROM CW2G.Trail")  # This wraps the query in text()

        # Execute the query using SQLAlchemy's execute method
        result = db.session.execute(query)
        
        # Fetch the first row from the result set
        row = result.fetchone()

        # Check if any data was returned and respond accordingly
        if row:
            # Manually create a dictionary from row
            row_dict = {column: value for column, value in zip(result.keys(), row)}
            return jsonify({"message": "Connection successful", "data": row_dict})
        else:
            return jsonify({"message": "No data found in CW2G.Trail"}), 404
    except Exception as e:
        # Return the error message if an exception occurs
        return jsonify({"message": "Error", "error": str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)

