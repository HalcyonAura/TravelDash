import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_trip(trip_id):
    conn = get_db_connection()
    trip = conn.execute('SELECT * FROM trips WHERE id = ?',
                        (trip_id,)).fetchone()
    conn.close()
    if trip is None:
        abort(404)
    return trip


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


@app.route('/')
def index():
    # make this empty page or sign in?
    return render_template('base.html')

@app.route('/trips')
def trips():
    conn = get_db_connection()
    trips = conn.execute('SELECT * FROM trips').fetchall()
    conn.close()
    return render_template('index.html', trips=trips)


@app.route('/<int:trip_id>')
def trip(trip_id):
    trip = get_trip(trip_id)
    return render_template('trip.html', trip=trip)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        record = request.form['record']
        #content = request.form['content']

        if not record:
            flash('record is required!')
        else:
            conn = get_db_connection()
            #conn.execute('INSERT INTO trips (record, content) VALUES (?, ?)',
            #             (record, content))
            conn.execute('INSERT INTO trips (record) VALUES (?,)',
                         (record,))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    trip = get_trip(id)

    if request.method == 'POST':
        record = request.form['record']
        #content = request.form['content']

        if not record:
            flash('record is required!')
        else:
            conn = get_db_connection()
            #conn.execute('UPDATE trips SET record = ?, content = ?'
            #             ' WHERE id = ?',
            #             (record, content, id))
            conn.execute('UPDATE trips SET record = ? WHERE id = ?',
                         (record, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', trip=trip)


@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    trip = get_trip(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM trips WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(trip['record']))
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()