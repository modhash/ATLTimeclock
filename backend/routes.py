from flask import request, jsonify, session, redirect, url_for, render_template, flash
from models import db, User, TimeLog

def setup_routes(app):
    @app.route('/profile')
    def profile():
        if 'user_email' not in session:
            return redirect(url_for('index'))
        user = User.query.filter_by(email=session['user_email']).first()
        if not user:
            return redirect(url_for('index'))
        logs = TimeLog.query.filter_by(user_id=user.id).all()
        return render_template('profile.html', user=user, logs=logs)

    @app.route('/admin')
    def admin():
        if 'user_email' not in session:
            return redirect(url_for('index'))
        user = User.query.filter_by(email=session['user_email']).first()
        if not user or not user.is_admin:
            return redirect(url_for('profile'))
        users = User.query.all()
        return render_template('admin.html', users=users)

    @app.route('/api/log', methods=['POST'])
    def log_time():
        data = request.json
        user = User.query.filter_by(email=data['email']).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404

        log = TimeLog(user_id=user.id, log_type=data['log_type'])
        db.session.add(log)
        db.session.commit()

        return jsonify({'message': 'Time log created successfully'}), 201

    @app.route('/api/logs', methods=['GET'])
    def get_logs():
        email = request.args.get('email')
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404

        logs = TimeLog.query.filter_by(user_id=user.id).all()
        return jsonify([{
            'id': log.id,
            'log_type': log.log_type,
            'timestamp': log.timestamp
        } for log in logs]), 200

    @app.route('/register', methods=['POST'])
    def register():
        data = request.form
        user = User.query.filter_by(email=data['email']).first()
        if user:
            flash('Email already registered')
            return redirect(url_for('admin'))

        new_user = User(email=data['email'], username=data['username'])
        new_user.set_password(data['password'])
        db.session.add(new_user)
        db.session.commit()
        flash('User created successfully')
        return redirect(url_for('admin'))

    @app.route('/login', methods=['POST'])
    def login():
        data = request.form
        user = User.query.filter_by(username=data['username']).first()
        if user and user.check_password(data['password']):
            session['user_email'] = user.email
            return redirect(url_for('profile'))
        flash('Invalid username or password')
        return redirect(url_for('index'))

    @app.route('/logout')
    def logout():
        session.pop('user_email')
        return redirect(url_for('index'))
