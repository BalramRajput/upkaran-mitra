from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
import base64
from enum import Enum

class Unit(Enum):
    MINUTE = "Minute"
    HOUR = "Hour"
    DAY = "Day"

equipments_bp = Blueprint('equipments_bp', __name__)
db = None

@equipments_bp.route('/myEquipments', methods=['GET'])
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

@equipments_bp.route('/addEquipment', methods=['GET', 'POST'])
def add_equipment():
    if request.method == 'POST':
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
            return redirect(url_for('equipments_bp.my_equipments'))
        else:
            flash("Error adding equipment.", "danger")
    else:
        query = """
        SELECT * FROM equipment_category
        """
        result = db.execute_select_all_query(query)
        units = [unit.value for unit in Unit]
        return render_template('add_equipment.html', units=units, equipment_categories=result)

@equipments_bp.route('/equipments/<int:category_id>', methods=['GET'])
def equipments(category_id):
    user_id = session['id']
    query = """
    SELECT ue.*, v.village_name as village, u.name as owner_name, u.phone_number as owner_contact
    FROM user_equipments ue
    JOIN user u ON ue.user_id = u.id
    JOIN address a ON u.address_id = a.id
    JOIN village v ON a.village_id = v.village_id
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

@equipments_bp.route('/bookEquipment', methods=['POST'])
def book_equipment():
    if 'id' not in session:
        flash("You need to be logged in to book equipment.", "danger")
        return redirect(url_for('user_bp.login'))

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
        return redirect(url_for('bookings_bp.my_bookings'))
    else:
        flash("Error booking equipment.", "danger")
        return redirect(url_for('index'))

def init_equipments_routes(database):
    global db
    db = database