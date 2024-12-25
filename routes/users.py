from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify

user_bp = Blueprint('user_bp', __name__)
db = None

@user_bp.route('/login', methods=['GET', 'POST'])
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

@user_bp.route('/register', methods= ['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        phone_number = request.form['phone_number']
        email = request.form['email']
        password = request.form['password']
        address_line1 = request.form['address_line1']
        address_line2 = request.form['address_line2']
        village_id = request.form['village']
        zipcode = request.form['zipcode']

        query = "INSERT INTO address (address_line1, address_line2, village_id, zipcode) VALUES (?, ?, ?, ?)"
        result = db.execute_write_query(query, (address_line1, address_line2, village_id, zipcode))
        if result:
            address_id = result
            
            query = "INSERT INTO user (name, phone_number, email, password, address_id) VALUES (?, ?, ?, ?, ?)"
            id = db.execute_write_query(query, (name, phone_number, email, password, address_id))

            if id:
                flash(f"Registration successful with id: {id}", "success")
                return redirect(url_for('user_bp.login'))
            else:
                flash("Error during user registration.", "danger")
        else:
            flash("Error during address registration.", "danger")
    else:
        query_country = "SELECT * FROM country"
        query_state = "SELECT * FROM state"
        query_district = "SELECT * FROM district"
        query_sub_district = "SELECT * FROM sub_district"

        countries = db.execute_select_all_query(query_country)
        states = db.execute_select_all_query(query_state)
        districts = db.execute_select_all_query(query_district)
        sub_districts = db.execute_select_all_query(query_sub_district)
        return render_template('register.html', countries=countries, states=states, districts=districts, sub_districts=sub_districts)

@user_bp.route('/logout')
def logout():
    session.pop('id', None)
    flash("Logged out successfully.", "info")
    return redirect(url_for('user_bp.login'))

@user_bp.route('/villages/<int:sub_district_id>', methods=['GET'])
def get_villages(sub_district_id):
    query = "SELECT * FROM village WHERE sub_district_id = ?"
    result = db.execute_select_all_query(query, (sub_district_id,))
    if result:
        return jsonify(result)
    else:
        return jsonify([])

def init_user_routes(database):
    global db
    db = database