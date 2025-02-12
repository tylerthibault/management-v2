from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from cwmt.models.users import User

# Create a Blueprint instance
main_bp = Blueprint('main', __name__)

# Define routes using the blueprint
@main_bp.route('/')
def index():
    return render_template('pages/public/landing/index.html')

@main_bp.route('/about')
def about():
    return render_template('about.html')

# Example of a route with methods
@main_bp.route('/api/data', methods=['GET', 'POST'])
def handle_data():
    if request.method == 'POST':
        data = request.json
        # Process the data
        return jsonify({'status': 'success'})
    return jsonify({'message': 'GET request received'})

@main_bp.route('/login')
def login():
    return render_template('pages/public/login/index.html')

@main_bp.post('/login')
def check_login():
    # validate
    data = {**request.form}
    user = User.validate_login(data)

    if not user:
        return redirect(url_for('main.login'))

    # create session
    session['user'] = user.id

    # redirect to dashboard
    return redirect(url_for('main.dashboard'))

@main_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('main.index'))

@main_bp.route('/dashboard')
def dashboard():
    context = {
        'user': User.get(session.get('user'))
    }
    return render_template('pages/private/dashboard/index.html', **context)

@main_bp.route('/seed')
def seed():
    from cwmt.helpers.db.seed import seed_data
    seed_data()
    return 'Seed data inserted successfully'