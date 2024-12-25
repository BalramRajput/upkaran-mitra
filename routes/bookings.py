from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify

bookings_bp = Blueprint('bookings_bp', __name__)
db = None

@bookings_bp.route('/myBookings', methods=['GET'])
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


@bookings_bp.route('/updateBooking/<int:booking_id>', methods=['POST'])
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

def init_bookings_routes(database):
    global db
    db = database