from flask import Flask, request, render_template, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '7113'
app.config['MYSQL_DB'] = 'users'

mysql = MySQL(app)


@app.route('/hello')
def hello():
    return "Hello, World!"

@app.route('/')
def users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name, email, role FROM users")
    users = cur.fetchall()
    cur.close()
    return render_template('index.html', users=users)

@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        email = request.form['email']
        role = request.form['role']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (id, name, email, role) VALUES (%s, %s, %s, %s)", (id, name, email, role))
        mysql.connection.commit()
        cur.close()
        flash('User added successfully', 'success')
        return redirect(url_for('users'))
    return render_template('register.html')

@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
    mysql.connection.commit()
    cur.close()
    flash('User deleted successfully', 'success')
    return redirect(url_for('users'))

@app.route('/test_delete', methods=['DELETE'])
def test_delete():
    return 'DELETE method works!', 200
@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        email = request.form['email']
        role = request.form['role']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET name=%s, email=%s, role=%s WHERE id=%s", (name, email, role, id))
        mysql.connection.commit()
        cur.close()
        flash('User updated successfully', 'success')
        return redirect(url_for('users'))
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, name, email, role FROM users WHERE id = %s", (user_id,))
        user = cur.fetchone()
        cur.close()
        return render_template('edit.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)
