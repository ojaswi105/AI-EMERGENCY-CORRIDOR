import sqlite3
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.secret_key = "nagpur_emergency_secret_2026"

# 1. DATABASE INITIALIZE
def init_db():
    conn = sqlite3.connect('patients.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            blood_group TEXT,
            condition TEXT,
            bp TEXT,
            pulse TEXT,
            spo2 TEXT,
            severity TEXT,
            abha_id TEXT,
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# NAGPUR 8 MAJOR HOSPITALS DATASET
NAGPUR_HOSPITALS = [
    {"id": "aiims_ngp", "name": "AIIMS Hospital, MIHAN", "area": "MIHAN", "beds": "12 BEDS OPEN", "status": "open", "phone": "+91 712 298 5555"},
    {"id": "gmc_ngp", "name": "GMC Hospital, Medical Chowk", "area": "Ajni / Medical", "beds": "FULL - 0 BEDS", "status": "full", "phone": "+91 712 274 4441"},
    {"id": "mayo_ngp", "name": "IGGMC (Mayo Hospital)", "area": "Central Avenue", "beds": "5 BEDS OPEN", "status": "open", "phone": "+91 712 272 5423"},
    {"id": "kingsway_ngp", "name": "Kingsway Hospital", "area": "Railway Station", "beds": "4 BEDS OPEN", "status": "open", "phone": "+91 712 667 8999"},
    {"id": "orange_city_ngp", "name": "Orange City Hospital (OCHRI)", "area": "Khamla / Ring Road", "beds": "6 BEDS OPEN", "status": "open", "phone": "+91 712 222 3456"},
    {"id": "alexis_ngp", "name": "Max Alexis Hospital", "area": "Mankapur, Koradi Rd", "beds": "8 BEDS OPEN", "status": "open", "phone": "+91 712 712 0000"},
    {"id": "care_ngp", "name": "CARE Hospital", "area": "Panchsheel / Ramdaspeth", "beds": "2 BEDS OPEN", "status": "open", "phone": "+91 712 398 2222"},
    {"id": "wockhardt_ngp", "name": "Wockhardt Hospital", "area": "Shankar Nagar", "beds": "FULL - 0 BEDS", "status": "full", "phone": "+91 712 662 4444"}
]

# ROUTE 1: Login Gateway
@app.route('/')
def home():
    return render_template('login.html')

# ROUTE 2: Main Dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    role = request.args.get('role') or request.form.get('role', 'driver')
    name = request.args.get('name') or request.form.get('name', 'Rajesh Kumar Verma' if role == 'driver' else 'Amit S. Sharma')
    phone = request.args.get('phone') or request.form.get('phone', '+91 98231 44550' if role == 'driver' else '+91 94220 11223')
    vehicle = request.args.get('vehicle') or request.form.get('vehicle', 'MH 31 EQ 4002')
    service = request.args.get('service') or request.form.get('service', 'ambulance')
    address = request.args.get('address') or request.form.get('address', 'Plot 24, Near Garden, Trimurti Nagar')
    city = request.args.get('city') or request.form.get('city', 'Nagpur')
    pincode = request.args.get('pincode') or request.form.get('pincode', '440022')
    severity = request.args.get('severity') or request.form.get('severity', 'critical')
    abha_id = request.args.get('abha_id') or request.form.get('abha_id', '91-4402-9912-3301')
    insurance = request.args.get('insurance_provider') or request.form.get('insurance_provider', 'Star Health (Cashless Pre-Auth)')
    condition = request.args.get('condition') or ("Acute Myocardial Infarction (Severe Chest Pain & Unconscious)" if severity == 'critical' else "Accidental Trauma & Fracture Stabilization")

    return render_template(
        'index.html',
        role=role,
        name=name,
        phone=phone,
        vehicle=vehicle,
        service=service,
        address=address,
        city=city,
        pincode=pincode,
        severity=severity,
        abha_id=abha_id,
        insurance=insurance,
        condition=condition,
        hospitals=NAGPUR_HOSPITALS
    )

# ROUTE 3: Hospital ER Dashboard
@app.route('/er-dashboard')
def er_dashboard():
    return render_template('er_dashboard.html')

# ROUTE 4: Family Live Tracking
@app.route('/family-track')
def family_track():
    return render_template('family_tracking.html')

# ROUTE 5: API TO SAVE PATIENT IN DATABASE
@app.route('/api/save-patient', methods=['POST'])
def save_patient():
    data = request.json or {}
    conn = sqlite3.connect('patients.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO patients (name, phone, blood_group, condition, bp, pulse, spo2, severity, abha_id, address)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('name'),
        data.get('phone'),
        data.get('blood_group'),
        data.get('condition'),
        data.get('bp'),
        data.get('pulse'),
        data.get('spo2'),
        data.get('severity'),
        data.get('abha_id'),
        data.get('address')
    ))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "Saved to database"})

# ROUTE 6: API TO VIEW SAVED PATIENTS
@app.route('/api/get-patients', methods=['GET'])
def get_patients():
    conn = sqlite3.connect('patients.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM patients ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)

if __name__ == '__main__':
    app.run(debug=True, port=5000)