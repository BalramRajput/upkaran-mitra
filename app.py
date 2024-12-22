from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import os
from database import Database
import base64
from enum import Enum

class Unit(Enum):
    MINUTE = "Minute"
    HOUR = "Hour"
    DAY = "Day"

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'RANDOM$#NJFD32KEY')
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, 'sql/upkaranmitra.db')
db = Database(db_path)

@app.route('/')
def index():
    query = "SELECT * FROM equipment_category"
    result = db.execute_select_all_query(query)
    return render_template('index.html', categories=result)

@app.route('/register', methods= ['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        phone_number = request.form['phone_number']
        email = request.form['email']
        password = request.form['password']
        address_line1 = request.form['address_line1']
        address_line2 = request.form['address_line2']
        village = request.form['village']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        zipcode = request.form['zipcode']

        query = "INSERT INTO address (address_line1, address_line2, village, city, state, country, zipcode) VALUES (?, ?, ?, ?, ?, ?, ?)"
        result = db.execute_write_query(query, (address_line1, address_line2, village, city, state, country, zipcode))
        if result:
            address_id = result
            
            query = "INSERT INTO user (name, phone_number, email, password, address_id) VALUES (?, ?, ?, ?, ?)"
            id = db.execute_write_query(query, (name, phone_number, email, password, address_id))

            if id:
                flash(f"Registration successful with id: {id}", "success")
                return redirect(url_for('login'))
            else:
                flash("Error during user registration.", "danger")
        else:
            flash("Error during address registration.", "danger")
       
    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        password = request.form['password']

        query = "SELECT * FROM user WHERE phone_number = ? AND password = ?"
        result = db.execute_select_one_query(query, (phone_number, password))

        if result:
            session['id'] = result[0]
            flash("Login successful!", "success")
            return redirect(url_for('index'))
        else:
            flash("Invalid credentials.", "danger")

    return render_template('login.html')

# My Equipments
@app.route('/myEquipments', methods=['GET'])
def my_equipments():
    user_id = session['id']
    query = """
    SELECT ue.*, ec.name as category_name
    FROM user_equipments ue
    JOIN equipment_category ec ON ue.equipment_category_id = ec.id
    WHERE ue.user_id = ?
    """
    result = db.execute_select_all_query(query, (user_id,))
    if result:
        return render_template('my_equipment.html', equipments=result)
    else:
        flash("You don't own any equipment at the moment", "success")
        return render_template('my_equipment.html', equipments=result)

@app.route('/addEquipment', methods=['GET', 'POST'])
def add_equipment():
    if request.method == 'POST':
        print("request received to add equipment",request.form)
        user_id = session['id']
        name = request.form['name']
        equipment_category_id = request.form['equipment_category_id']
        used_for = request.form['used_for']
        image = request.files['image'].read() if 'image' in request.files else None
        rate = request.form['rate']
        unit = request.form['unit']
        specification = request.form['specification']
        
        query = """
        INSERT INTO user_equipments (user_id, name, equipment_category_id, used_for, image, rate, unit, specification)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        result = db.execute_write_query(query, (user_id, name, equipment_category_id, used_for, image, rate, unit, specification))
        
        if result:
            flash("Equipment added successfully!", "success")
            return redirect(url_for('my_equipments'))
        else:
            flash("Error adding equipment.", "danger")
    else:
        query = """
        SELECT * FROM equipment_category
        """
        result = db.execute_select_all_query(query)
        units = [unit.value for unit in Unit]
        return render_template('add_equipment.html', units=units, equipment_categories=result)

@app.route('/equipments/<int:category_id>', methods=['GET'])
def equipments(category_id):
    user_id = session['id']
    query = """
    SELECT ue.*, a.village, u.name as owner_name, u.phone_number as owner_contact
    FROM user_equipments ue
    JOIN user u ON ue.user_id = u.id
    JOIN address a ON u.address_id = a.id
    WHERE ue.equipment_category_id = ? AND ue.is_available = 1 AND ue.user_id != ?
    """
    result = db.execute_select_all_query(query, (category_id, user_id))
    if result:
        for item in result:
            if 'image' in item:
                item['image'] = base64.b64encode(item['image']).decode('utf-8')
        return jsonify(result)
    else:
        return jsonify([])

@app.route('/bookEquipment', methods=['POST'])
def book_equipment():
    if 'id' not in session:
        flash("You need to be logged in to book equipment.", "danger")
        return redirect(url_for('login'))

    user_id = session['id']
    equipment_id = request.form['equipment_id']
    amount = request.form['amount']

    query = """
    INSERT INTO booking (user_id, user_equipment_id, amount, booked_at, is_payment_done)
    VALUES (?, ?, ?, datetime('now'), 0)
    """
    result = db.execute_write_query(query, (user_id, equipment_id, amount))

    if result:
        query = """
        UPDATE user_equipments SET is_available = 0 WHERE id = ?
        """
        db.execute_write_query(query, (equipment_id,))
        flash("Equipment booked successfully!", "success")
        return redirect(url_for('my_bookings'))
    else:
        flash("Error booking equipment.", "danger")
        return redirect(url_for('index'))

@app.route('/myBookings', methods=['GET'])
def my_bookings():
    user_id = session['id']
    query = """
    SELECT b.id, b.booked_at, b.started_at, b.completed_at, b.amount, b.is_payment_done, 
    ue.name as equipment_name, ue.user_id as borrowed_from_id, u.name as borrowed_from_name 
    FROM booking b
    JOIN user_equipments ue ON b.user_equipment_id = ue.id
    JOIN user u ON ue.user_id = u.id
    WHERE b.user_id = ?
    """
    equipments_borrowed = db.execute_select_all_query(query, (user_id,))

    query = """
    SELECT b.id, b.booked_at, b.started_at, b.completed_at, b.amount, b.is_payment_done,
    ue.name as equipment_name, b.user_id as lent_to_id, u.name as lent_to_name
    FROM booking b
    JOIN user_equipments ue ON b.user_equipment_id = ue.id
    JOIN user u ON b.user_id = u.id
    WHERE ue.user_id = ?
    """
    equipments_lent = db.execute_select_all_query(query, (user_id,))

    if equipments_borrowed or equipments_lent:
        return render_template('my_booking.html', equipments_borrowed=equipments_borrowed, equipments_lent=equipments_lent)

    else:
        flash("You don't have any bookings at the moment", "success")
        return render_template('my_booking.html', equipments_borrowed=equipments_borrowed, equipments_lent=equipments_lent)
    
# Logout
@app.route('/logout')
def logout():
    session.pop('id', None)
    flash("Logged out successfully.", "info")
    return redirect(url_for('login'))

@app.route('/updateBooking/<int:booking_id>', methods=['POST'])
def update_booking(booking_id):
    action = request.args.get('action')
    if action == 'start':
        query = """
        UPDATE booking
        SET started_at = datetime('now')
        WHERE id = ? AND started_at IS NULL
        """
        result = db.execute_write_query(query, (booking_id,))
        return "Booking started successfully!", 200
    elif action == 'complete':
        query = """
        UPDATE booking
        SET completed_at = datetime('now'), is_payment_done = 1
        WHERE id = ? AND completed_at IS NULL
        """
        result = db.execute_write_query(query, (booking_id,))
        query = """
        UPDATE user_equipments
        SET is_available = 1
        WHERE id = (SELECT user_equipment_id FROM booking WHERE id = ?)
        """
        db.execute_write_query(query, (booking_id,))
        return "Booking completed successfully!", 200
    else:
        return "Invalid action.", 400

def b64encode(value):
    if value is None:
        return ''
    return base64.b64encode(value).decode('utf-8')

app.jinja_env.filters['b64encode'] = b64encode

if __name__ == '__main__':
    app.run(debug=True)