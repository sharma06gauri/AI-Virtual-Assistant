from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import os

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Database connection configuration (replace with your MySQL credentials)
db_config = {
    'host': 'localhost',
    'user': 'your_mysql_username',
    'password': 'your_mysql_password',
    'database': 'finance_assistant_db'
}

def get_db_connection():
    """Establishes a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

# Routes
@app.route('/')
def home():
    """Home page route."""
    return "<h1>Welcome to the AI Personal Virtual Assistant for Finance!</h1>" # Placeholder

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User signup route."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Add logic to securely hash the password
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            query = "INSERT INTO users (username, password) VALUES (%s, %s)"
            try:
                cursor.execute(query, (username, password))
                conn.commit()
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('login'))
            except mysql.connector.Error as err:
                flash(f'Registration failed: {err}', 'danger')
            finally:
                cursor.close()
                conn.close()
    return render_template('signup.html') # You will need to create this HTML template

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login route."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM users WHERE username = %s AND password = %s" # In a real app, use hashed passwords
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            
            if user:
                session['user_id'] = user['id']
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password.', 'danger')
            
            cursor.close()
            conn.close()
    return render_template('login.html') # You will need to create this HTML template

@app.route('/dashboard')
def dashboard():
    """Dashboard route (requires login)."""
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    # Example: fetch user data or expenses
    # user_id = session['user_id']
    # conn = get_db_connection()
    # ... your code to fetch data ...
    
    return render_template('dashboard.html') # You will need to create this HTML template

@app.route('/logout')
def logout():
    """User logout route."""
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
