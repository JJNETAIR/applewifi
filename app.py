from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from datetime import datetime, timedelta
import csv
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

voucher_db = 'vouchers.csv'

def load_vouchers():
    if not os.path.exists(voucher_db):
        return {}
    with open(voucher_db, newline='') as f:
        reader = csv.DictReader(f)
        return {row['code']: row for row in reader}

def save_voucher(code, start_date, duration):
    vouchers = load_vouchers()
    vouchers[code] = {
        'code': code,
        'start_date': start_date,
        'duration': duration
    }
    with open(voucher_db, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['code', 'start_date', 'duration'])
        writer.writeheader()
        for v in vouchers.values():
            writer.writerow(v)

@app.route('/', methods=['GET', 'POST'])
def check():
    result = None
    if request.method == 'POST':
        code = request.form['code'].strip()
        vouchers = load_vouchers()
        if code in vouchers:
            start_date = datetime.strptime(vouchers[code]['start_date'], "%Y-%m-%d")
            duration = int(vouchers[code]['duration'])
            end_date = start_date + timedelta(days=duration)
            remaining = (end_date - datetime.now()).days
            result = {
                'valid': remaining >= 0,
                'code': code,
                'start_date': start_date.strftime("%Y-%m-%d"),
                'end_date': end_date.strftime("%Y-%m-%d"),
                'remaining': remaining
            }
        else:
            result = {'valid': False, 'code': code}
    return render_template('index.html', result=result)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        code = request.form['code'].strip()
        start_date = request.form['start_date']
        duration = request.form['duration']
        save_voucher(code, start_date, duration)
        flash('Voucher saved successfully!')
    return render_template('admin.html')

@app.route('/export')
def export():
    return send_file(voucher_db, as_attachment=True)

@app.route('/analytics')
def analytics():
    vouchers = load_vouchers()
    total = len(vouchers)
    active = sum((datetime.strptime(v['start_date'], "%Y-%m-%d") + timedelta(days=int(v['duration']))) > datetime.now() for v in vouchers.values())
    expired = total - active
    return render_template('analytics.html', total=total, active=active, expired=expired)