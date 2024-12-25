from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import os
from database import Database
import base64
from enum import Enum
from routes import user_bp, init_user_routes, equipments_bp, init_equipments_routes, bookings_bp, init_bookings_routes

class Unit(Enum):
    MINUTE = "Minute"
    HOUR = "Hour"
    DAY = "Day"

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'RANDOM$#NJFD32KEY')
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, 'sql/upkaranmitra.db')
db = Database(db_path)

init_user_routes(db)
init_equipments_routes(db)
init_bookings_routes(db)

app.register_blueprint(user_bp)
app.register_blueprint(equipments_bp)
app.register_blueprint(bookings_bp)

@app.route('/')
def index():
    query = "SELECT * FROM equipment_category"
    result = db.execute_select_all_query(query)
    return render_template('index.html', categories=result)

def b64encode(value):
    if value is None:
        return ''
    return base64.b64encode(value).decode('utf-8')

app.jinja_env.filters['b64encode'] = b64encode

if __name__ == '__main__':
    app.run(debug=True)