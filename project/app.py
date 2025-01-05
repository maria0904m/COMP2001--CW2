from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text

# Initialize Flask app and SQLAlchemy
app = Flask(__name__)

# Configure for SQLAlchemy and database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://MStefan:TszJ810+@DIST-6-505.uopnet.plymouth.ac.uk/COMP2001_MStefan?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Hardcoded JWT Secret Key for testing purposes
app.config['JWT_SECRET_KEY'] = 'C0mP2001' 

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Define database models for Country and Trail
class Country(db.Model):
    __tablename__ = 'CW2G.Country'
    CountryID = db.Column(db.Integer, primary_key=True)
    CountryName = db.Column(db.String(255))

class Trail(db.Model):
    __tablename__ = 'CW2G.Trail'
    TrailID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255))
    Length = db.Column(db.Numeric(5, 2))
    Elevation = db.Column(db.Integer)
    Type = db.Column(db.String(50))
    Difficulty = db.Column(db.String(50))
    Description = db.Column(db.Text)
    CountryID = db.Column(db.Integer, db.ForeignKey('CW2G.Country.CountryID'))
    country = db.relationship('Country', backref=db.backref('trails', lazy=True))

# Define database models for users
class User(db.Model):
    __tablename__ = 'CW2G.Users'
    UserID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(255), unique=True, nullable=False)
    Email = db.Column(db.String(255), unique=True, nullable=False)
    Password = db.Column(db.String(255), nullable=False)  
    Role = db.Column(db.String(50), nullable=False)  

    def __repr__(self):
        return f'<User {self.Username}>'

# Route to handle user login and return JWT token

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    try:
       
        query = text("""
            SELECT * FROM CW2G.Users WHERE Username = :username
        """)
        result = db.session.execute(query, {'username': username})
        user = result.fetchone()  

        if user:
            
            stored_password = user[3]  # Password is in the 4th column 
            role = user[4]  # Role is in the 5th column 

            # Check if the provided password matches the stored password hash
            if check_password_hash(stored_password, password):  
                access_token = create_access_token(identity=username, additional_claims={"role": role})
                return jsonify({'access_token': access_token}), 200
            else:
                return jsonify({'message': 'Invalid credentials'}), 401
        else:
            return jsonify({'message': 'User not found'}), 404

    except Exception as e:
        return jsonify({'message': 'Error', 'error': str(e)}), 500


# Route to create a new trail using raw SQL for insertion
@app.route('/trails', methods=['POST'])
@jwt_required()  
def create_trail():
    data = request.get_json()

   
    if 'Name' not in data or 'Length' not in data or 'CountryID' not in data:
        return jsonify({'message': 'Missing required fields (Name, Length, CountryID)'}), 400

    # Check the user's role
    role = get_jwt_identity().get('role', 'user')  
    if role != 'admin':
        return jsonify({'message': 'Permission denied'}), 403  # Admin only can create trails

    try:
        query = text(""" 
            INSERT INTO CW2G.Trail (Name, Length, Elevation, Type, Difficulty, Description, CountryID)
            OUTPUT inserted.TrailID
            VALUES (:Name, :Length, :Elevation, :Type, :Difficulty, :Description, :CountryID)
        """)
        result = db.session.execute(query, {
            'Name': data['Name'],
            'Length': data['Length'],
            'Elevation': data.get('Elevation', None),
            'Type': data.get('Type', None),
            'Difficulty': data.get('Difficulty', None),
            'Description': data.get('Description', None),
            'CountryID': data['CountryID']
        })
        db.session.commit()
        return jsonify({'message': 'Trail created successfully!'}), 201
    except Exception as e:
        return jsonify({'message': 'Error', 'error': str(e)}), 500


# Route to get a trail by ID using raw SQL execution
@app.route('/trails/<int:trail_id>', methods=['GET'])
def get_trail(trail_id):
    try:
        query = text(""" 
            SELECT TrailID, Name, Length, Elevation, Type, Difficulty, Description, CountryID
            FROM CW2G.Trail
            WHERE TrailID = :trail_id
        """)
        
        result = db.session.execute(query, {'trail_id': trail_id})
        row = result.fetchone()

        if row:
            row_dict = {
                'TrailID': row[0],
                'Name': row[1],
                'Length': row[2],
                'Elevation': row[3],
                'Type': row[4],
                'Difficulty': row[5],
                'Description': row[6],
                'CountryID': row[7]
            }
            return jsonify(row_dict), 200
        else:
            return jsonify({'message': 'Trail not found!'}), 404
    except Exception as e:
        return jsonify({'message': 'Error', 'error': str(e)}), 500


# Route to update a trail
@app.route('/trails/<int:trail_id>', methods=['PUT'])
@jwt_required() 
def update_trail(trail_id):
    data = request.get_json()
    
    #check users role
    role = get_jwt_identity().get('role', 'user')  
    if role != 'admin':
        return jsonify({'message': 'Permission denied'}), 403  # Admin only can update trails

    # Validate required fields
    if 'Name' not in data or 'Length' not in data or 'CountryID' not in data:
        return jsonify({'message': 'Missing required fields (Name, Length, CountryID)'}), 400

    try:
        query = text(""" 
            UPDATE CW2G.Trail
            SET Name = :Name,
                Length = :Length,
                Elevation = :Elevation,
                Type = :Type,
                Difficulty = :Difficulty,
                Description = :Description,
                CountryID = :CountryID
            WHERE TrailID = :trail_id
        """)
        db.session.execute(query, {
            'Name': data['Name'],
            'Length': data['Length'],
            'Elevation': data.get('Elevation', None),
            'Type': data.get('Type', None),
            'Difficulty': data.get('Difficulty', None),
            'Description': data.get('Description', None),
            'CountryID': data['CountryID'],
            'trail_id': trail_id
        })
        db.session.commit()
        return jsonify({'message': 'Trail updated successfully!'}), 200
    except Exception as e:
        return jsonify({'message': 'Error', 'error': str(e)}), 500


# Route to delete a trail
@app.route('/trails/<int:trail_id>', methods=['DELETE'])
@jwt_required()  
def delete_trail(trail_id):

    #check users role
    role = get_jwt_identity().get('role', 'user')  
    if role != 'admin':
        return jsonify({'message': 'Permission denied'}), 403  # Admin only can update trails
    
    try:
        query = text("DELETE FROM CW2G.Trail WHERE TrailID = :trail_id")
        db.session.execute(query, {'trail_id': trail_id})
        db.session.commit()
        return jsonify({'message': 'Trail deleted successfully!'}), 200
    except Exception as e:
        return jsonify({'message': 'Error', 'error': str(e)}), 500


# Test route to check database connection
@app.route('/test_connection', methods=['GET'])
def test_connection():
    try:
        query = text("SELECT TOP 1 * FROM CW2G.Trail")
        result = db.session.execute(query)
        row = result.fetchone()
        if row:
            row_dict = {column: value for column, value in zip(result.keys(), row)}
            return jsonify({"message": "Connection successful", "data": row_dict})
        else:
            return jsonify({"message": "No data found in CW2G.Trail"}), 404
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 500


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
