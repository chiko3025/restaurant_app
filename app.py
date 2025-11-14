from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime, timedelta


app = Flask(__name__)
app.secret_key = "change_this_to_a_random_secret"  # change this in production
app.permanent_session_lifetime = timedelta(hours=5)

@app.context_processor
def inject_current_year():
    return {'current_year': datetime.now().year}

# In-memory store for demo (not persistent)
users = {}


@app.route('/')
def index():
    # sample 9 dish entries (image seeds produce unique placeholder images)
    dishes = [
        {"name": "Spicy Paneer Tikka", "desc": "Charred paneer with spices",
         "img": "https://th.bing.com/th/id/OIP.yesJV2fXeJm88QwUWl__SQHaE7?w=284&h=189"},

        {"name": "Veg Manchurian", "desc": "Crispy vegetable balls in spicy sauce",
         "img": "https://th.bing.com/th/id/OIP.UadataUgn2-230iTlucJ1gHaEK?w=277&h=180&c=7&r=0&o=7&cb=ucfimg2&dpr=1.5&pid=1.7&rm=3&ucfimg=1"},

        {"name": "Masala Dosa", "desc": "Crispy dosa stuffed with spiced potatoes",
         "img": "https://th.bing.com/th/id/OIP.yuas1mk_PucOQaOYEvzmuAHaD4?w=291&h=180&c=7&r=0&o=7&cb=ucfimg2&dpr=1.5&pid=1.7&rm=3&ucfimg=1"},

        {"name": "Veg Biryani", "desc": "Fragrant basmati rice with mixed vegetables",
         "img": "https://th.bing.com/th/id/OIP.EtDhYnU2n4qbTYt9OXvzdQHaE8?w=278&h=185&c=7&r=0&o=7&cb=ucfimg2&dpr=1.5&pid=1.7&rm=3&ucfimg=1"},

        {"name": "Chole Bhature", "desc": "Punjabi-style spicy chickpeas with fried bread",
         "img": "https://th.bing.com/th/id/OIP.Y484f7AzHY0b45zV4uPMawHaEK?w=316&h=180&c=7&r=0&o=7&cb=ucfimg2&dpr=1.5&pid=1.7&rm=3&ucfimg=1"},

        {"name": "Aloo Paratha", "desc": "Stuffed flatbread with spiced potato filling",
         "img": "https://th.bing.com/th/id/OIP.Sokc_0rSAieTE1RU4qnoIgHaFE?w=299&h=203&c=7&r=0&o=7&cb=ucfimg2&dpr=1.5&pid=1.7&rm=3&ucfimg=1"},

        {"name": "Veg Pulao", "desc": "Light aromatic rice loaded with veggies",
         "img": "https://th.bing.com/th/id/OIP.9HPyWxkrVTyFiESuJpfh8AHaEK?w=323&h=182&c=7&r=0&o=7&cb=ucfimg2&dpr=1.5&pid=1.7&rm=3&ucfimg=1"},

        {"name": "Palak Paneer", "desc": "Cottage cheese cooked in creamy spinach gravy",
         "img": "https://th.bing.com/th/id/OIP.WAJxMXY3_CxCtZEcp3AZWwHaEJ?w=333&h=187&c=7&r=0&o=7&cb=ucfimg2&dpr=1.5&pid=1.7&rm=3&ucfimg=1"},

        {"name": "Veg Spring Rolls", "desc": "Crispy rolls stuffed with seasoned vegetables",
         "img": "https://th.bing.com/th/id/OIP.JRKHY2kME0j7QDjuClCxqAHaE8?w=283&h=189&c=7&r=0&o=7&cb=ucfimg2&dpr=1.5&pid=1.7&rm=3&ucfimg=1"}

           ]
    return render_template('index.html', dishes=dishes)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        if not username or not email or not password:
            flash('Please fill all fields', 'error')
            return redirect(url_for('login'))
        # For this flow: after login details are provided, go to registration page
        session['pending_user'] = {'username': username, 'email': email, 'password': password}
        return redirect(url_for('register'))
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    pending = session.get('pending_user')
    if not pending:
        flash('Please login first', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        date = request.form.get('date')
        time = request.form.get('time')
        guests = request.form.get('guests')
        notes = request.form.get('notes')
        # create user record and store reservation
        user = pending['username']
        users[user] = {
            'username': pending['username'],
            'email': pending['email'],
            'password': pending['password'],
            'reservation': {
                'date': date,
                'time': time,
                'guests': guests,
                'notes': notes
            }
        }
        # set logged in
        session.pop('pending_user', None)
        session['user'] = user
        flash('Reservation confirmed! Welcome to your dashboard.', 'success')
        return redirect(url_for('dashboard'))

    return render_template('register.html', pending=pending)


@app.route('/dashboard')
def dashboard():
    user_key = session.get('user')
    if not user_key or user_key not in users:
        flash('You must complete registration to view dashboard', 'error')
        return redirect(url_for('login'))
    user = users[user_key]
    return render_template('dashboard.html', user=user)


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out', 'info')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
